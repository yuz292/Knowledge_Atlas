#!/usr/bin/env python3
"""
T2 Task 1 — Grading & Comment Tool
====================================
Run against a student's Knowledge_Atlas clone to assign grades and comments
for the "Fix the Contribute Page" assignment.

Usage
-----
    python3 t2_task1_grader.py /path/to/student/Knowledge_Atlas

The grader:
  1. Runs the 10 instructor-side tests automatically where possible
  2. Prompts the TA for manual rubric scores (diagrams, spec, verification log)
  3. Computes a weighted total
  4. Writes a grade report to  <student_repo>/160sp/rubrics/t2/GRADE_REPORT.md
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ════════════════════════════════════════════════
# DATA MODEL
# ════════════════════════════════════════════════

@dataclass
class TestResult:
    name: str
    passed: bool
    weight: str  # "critical", "important", "minor"
    details: str = ""
    auto: bool = True  # True = automated, False = manual

@dataclass
class RubricScore:
    criterion: str
    max_points: int
    points: int = 0
    comment: str = ""

@dataclass
class GradeReport:
    student_name: str = ""
    student_email: str = ""
    grader: str = ""
    timestamp: str = ""
    rubric_scores: list = field(default_factory=list)
    auto_tests: list = field(default_factory=list)
    total_points: int = 0
    max_points: int = 0
    overall_comment: str = ""
    file_manifest: list = field(default_factory=list)


# ════════════════════════════════════════════════
# AUTOMATED TESTS
# ════════════════════════════════════════════════

def find_db_path(repo: Path) -> Optional[Path]:
    """Find the article database in the student's repo."""
    candidates = [
        repo / "data" / "ka_auth.db",
        repo / "data" / "storage" / "ka_auth.db",
        repo / "ka_auth.db",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def find_lifecycle_db(repo: Path) -> Optional[Path]:
    """Find the lifecycle database."""
    candidates = [
        repo / "160sp" / "pipeline_lifecycle_full.db",
        repo / "data" / "pipeline_lifecycle_full.db",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def get_db(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(path), timeout=5.0)
    db.row_factory = sqlite3.Row
    return db


def test_corrupt_pdf(repo: Path) -> TestResult:
    """Test 4: Submit a non-PDF file. Expect rejection, not crash."""
    name = "Corrupt PDF handling"
    # Check if the endpoint file exists and has validation logic
    endpoint_file = repo / "ka_article_endpoints.py"
    if not endpoint_file.exists():
        return TestResult(name, False, "critical",
                          "ka_article_endpoints.py not found — no endpoint to test")

    source = endpoint_file.read_text()
    has_magic_check = "PDF-" in source or "%PDF" in source or "magic" in source.lower()
    has_validation = "_validate_pdf" in source or "validate" in source.lower()

    if has_magic_check or has_validation:
        return TestResult(name, True, "critical",
                          "PDF validation function found in endpoint code")
    else:
        return TestResult(name, False, "critical",
                          "No PDF magic-byte or validation check found in endpoint code")


def test_db_field_completeness(db_path: Path) -> TestResult:
    """Test 6: No required fields are NULL."""
    name = "DB field completeness"
    try:
        db = get_db(db_path)
        rows = db.execute("""
            SELECT article_id, article_type, status, created_at
            FROM articles
            WHERE status IS NULL OR created_at IS NULL
        """).fetchall()
        db.close()
        if len(rows) == 0:
            return TestResult(name, True, "important",
                              "All articles have status and created_at populated")
        else:
            ids = [r["article_id"] for r in rows[:5]]
            return TestResult(name, False, "important",
                              f"{len(rows)} articles with NULL required fields: {ids}")
    except Exception as e:
        return TestResult(name, False, "important", f"DB query failed: {e}")


def test_audit_log_presence(db_path: Path) -> TestResult:
    """Test 7: Every article has at least one audit log entry."""
    name = "Audit log presence"
    try:
        db = get_db(db_path)
        # Check if audit_log table exists
        tables = [r[0] for r in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        if "audit_log" not in tables:
            db.close()
            return TestResult(name, False, "minor",
                              "audit_log table does not exist")

        orphans = db.execute("""
            SELECT a.article_id, a.status
            FROM articles a
            LEFT JOIN audit_log al ON a.article_id = al.article_id
            WHERE al.log_id IS NULL
        """).fetchall()
        db.close()
        if len(orphans) == 0:
            return TestResult(name, True, "minor",
                              "All articles have audit log entries")
        else:
            return TestResult(name, False, "minor",
                              f"{len(orphans)} articles without audit log entries")
    except Exception as e:
        return TestResult(name, False, "minor", f"Audit log check failed: {e}")


def test_storage_path_correctness(db_path: Path) -> TestResult:
    """Test 8: Rejected papers have no stored path; accepted papers do."""
    name = "Storage path correctness"
    try:
        db = get_db(db_path)
        # Rejected papers should NOT have quarantine_path
        bad_rejects = db.execute("""
            SELECT article_id, status, quarantine_path
            FROM articles
            WHERE status LIKE 'reject%' AND quarantine_path IS NOT NULL
        """).fetchall()

        # Accepted/staged papers SHOULD have quarantine_path
        bad_accepts = db.execute("""
            SELECT article_id, status, quarantine_path
            FROM articles
            WHERE status IN ('received', 'staged', 'validated')
              AND quarantine_path IS NULL
        """).fetchall()
        db.close()

        issues = []
        if bad_rejects:
            issues.append(f"{len(bad_rejects)} rejected papers with stored paths")
        if bad_accepts:
            issues.append(f"{len(bad_accepts)} accepted papers without stored paths")

        if not issues:
            return TestResult(name, True, "critical",
                              "Storage paths are consistent with paper status")
        else:
            return TestResult(name, False, "critical", "; ".join(issues))
    except Exception as e:
        return TestResult(name, False, "critical", f"Storage check failed: {e}")


def test_edge_case_distinguishability(db_path: Path) -> TestResult:
    """Test 9: Accepted and edge-case papers are distinguishable in the DB."""
    name = "Accepted vs edge case distinguishability"
    try:
        db = get_db(db_path)
        # Get non-rejected articles
        articles = db.execute("""
            SELECT article_id, status, article_type, relevance_score,
                   validation_notes
            FROM articles
            WHERE status NOT IN ('rejected_bad_file', 'duplicate_existing',
                                 'rejected_off_topic')
            ORDER BY created_at DESC LIMIT 20
        """).fetchall()
        db.close()

        if len(articles) < 2:
            return TestResult(name, False, "important",
                              f"Only {len(articles)} non-rejected articles — "
                              "need at least 2 to check distinguishability")

        # Check if there's any variation in status or score
        statuses = set(r["status"] for r in articles)
        scores = set(str(r["relevance_score"]) for r in articles)

        if len(statuses) > 1 or len(scores) > 1:
            return TestResult(name, True, "important",
                              f"Found {len(statuses)} distinct statuses: {statuses}")
        else:
            return TestResult(name, False, "important",
                              "All non-rejected papers have identical status and score — "
                              "edge cases are not distinguished from accepted papers")
    except Exception as e:
        return TestResult(name, False, "important", f"Distinguishability check failed: {e}")


def test_duplicate_detection_exists(repo: Path) -> TestResult:
    """Test 2: Check if duplicate detection logic exists in the code."""
    name = "Duplicate detection logic"
    endpoint_file = repo / "ka_article_endpoints.py"
    if not endpoint_file.exists():
        return TestResult(name, False, "important",
                          "ka_article_endpoints.py not found")
    source = endpoint_file.read_text()
    has_dedup = ("duplicate" in source.lower() or
                 "check_duplicate" in source or
                 "pdf_hash" in source)
    if has_dedup:
        return TestResult(name, True, "important",
                          "Duplicate detection logic found in endpoint code")
    else:
        return TestResult(name, False, "important",
                          "No duplicate detection logic found")


def test_classifier_integration(repo: Path) -> TestResult:
    """Test 1: Check that the classifier is actually imported and called."""
    name = "Classifier integration (round-trip)"
    endpoint_file = repo / "ka_article_endpoints.py"
    if not endpoint_file.exists():
        # Check for any new Python files
        py_files = list(repo.glob("*.py")) + list((repo / "160sp").glob("*.py"))
        for pf in py_files:
            src = pf.read_text()
            if "AdaptiveClassifierSubsystem" in src or "classifier_system" in src:
                return TestResult(name, True, "critical",
                                  f"Classifier imported in {pf.name}")
        return TestResult(name, False, "critical",
                          "No file imports AdaptiveClassifierSubsystem")

    source = endpoint_file.read_text()
    has_import = ("AdaptiveClassifierSubsystem" in source or
                  "classifier_system" in source or
                  "atlas_shared" in source)
    has_call = ".classify(" in source

    if has_import and has_call:
        return TestResult(name, True, "critical",
                          "Classifier is imported and .classify() is called")
    elif has_import:
        return TestResult(name, False, "critical",
                          "Classifier is imported but .classify() is never called")
    else:
        return TestResult(name, False, "critical",
                          "Classifier is not imported from atlas_shared")


def test_contribute_page_modified(repo: Path) -> TestResult:
    """Check that the contribute page was actually changed."""
    name = "Contribute page modified"
    page = repo / "ka_contribute_public.html"
    if not page.exists():
        return TestResult(name, False, "critical", "ka_contribute_public.html not found")

    source = page.read_text()
    has_results = ("result" in source.lower() and
                   ("accept" in source.lower() or "reject" in source.lower() or
                    "edge" in source.lower()))
    has_fetch = ("fetch(" in source or "XMLHttpRequest" in source or
                 "axios" in source or "/api/articles" in source)

    if has_results and has_fetch:
        return TestResult(name, True, "critical",
                          "Contribute page has results section and API call")
    elif has_fetch:
        return TestResult(name, False, "critical",
                          "Contribute page calls API but has no visible results section")
    elif has_results:
        return TestResult(name, False, "critical",
                          "Contribute page has results markup but no API call")
    else:
        return TestResult(name, False, "critical",
                          "Contribute page appears unmodified — "
                          "no results section or API call found")


def collect_file_manifest(repo: Path) -> list[str]:
    """Get list of changed/new files via git."""
    manifest = []
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(repo), capture_output=True, text=True, timeout=10)
        if diff.stdout.strip():
            manifest.extend(diff.stdout.strip().split("\n"))

        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(repo), capture_output=True, text=True, timeout=10)
        for line in status.stdout.strip().split("\n"):
            if line.strip():
                # git status --short: "?? file" or " M file"
                parts = line.strip().split(None, 1)
                if len(parts) == 2 and parts[1] not in manifest:
                    manifest.append(f"[{parts[0]}] {parts[1]}")
    except Exception:
        manifest.append("(git not available — could not generate manifest)")
    return manifest


# ════════════════════════════════════════════════
# MANUAL RUBRIC PROMPTS
# ════════════════════════════════════════════════

RUBRIC_CRITERIA = [
    RubricScore("Diagnosis: Boxology diagrams accurate, gap statement correct", 15),
    RubricScore("Spec quality: Contract is complete, specific, and testable", 15),
    RubricScore("Verification questions: Probing questions caught real problems", 15),
    RubricScore("Validation: At least 3/4 test papers produce correct results", 20),
    RubricScore("Diagnosis of failures: Correctly identified spec vs implementation bugs", 15),
    RubricScore("File manifest: Complete and matches actual changes", 5),
    RubricScore("Automated tests: Instructor-side tests pass (auto-scored)", 15),
]


def prompt_manual_score(criterion: RubricScore) -> RubricScore:
    """Prompt the TA for a score and comment on one criterion."""
    print(f"\n{'─' * 60}")
    print(f"  {criterion.criterion}")
    print(f"  Max points: {criterion.max_points}")
    print(f"{'─' * 60}")

    while True:
        try:
            raw = input(f"  Score (0–{criterion.max_points}): ").strip()
            if raw == "":
                print("  (skipped — 0 points)")
                score = 0
                break
            score = int(raw)
            if 0 <= score <= criterion.max_points:
                break
            print(f"  Must be between 0 and {criterion.max_points}")
        except ValueError:
            print("  Enter a number")
        except (EOFError, KeyboardInterrupt):
            print("\n  (aborted — 0 points)")
            score = 0
            break

    comment = input("  Comment (optional): ").strip()
    criterion.points = score
    criterion.comment = comment
    return criterion


# ════════════════════════════════════════════════
# REPORT GENERATION
# ════════════════════════════════════════════════

def compute_auto_score(results: list[TestResult]) -> tuple[int, int]:
    """Compute points from automated tests. Max 15 points."""
    max_pts = 15
    weights = {"critical": 3, "important": 2, "minor": 1}
    total_weight = sum(weights[r.weight] for r in results)
    earned_weight = sum(weights[r.weight] for r in results if r.passed)

    if total_weight == 0:
        return 0, max_pts
    return round(max_pts * earned_weight / total_weight), max_pts


def render_report(report: GradeReport) -> str:
    """Render the grade report as markdown."""
    lines = []
    lines.append("# T2 Task 1 — Grade Report")
    lines.append("")
    lines.append(f"**Student:** {report.student_name or '(not set)'}")
    lines.append(f"**Email:** {report.student_email or '(not set)'}")
    lines.append(f"**Grader:** {report.grader or '(not set)'}")
    lines.append(f"**Date:** {report.timestamp}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary
    lines.append(f"## Total: {report.total_points} / {report.max_points}")
    lines.append("")

    # Rubric scores
    lines.append("## Rubric Scores")
    lines.append("")
    lines.append("| Criterion | Score | Comment |")
    lines.append("|-----------|-------|---------|")
    for s in report.rubric_scores:
        comment = s.comment.replace("|", "\\|") if s.comment else "—"
        lines.append(f"| {s.criterion} | {s.points}/{s.max_points} | {comment} |")
    lines.append("")

    # Automated tests
    lines.append("## Automated Test Results")
    lines.append("")
    lines.append("| Test | Status | Weight | Details |")
    lines.append("|------|--------|--------|---------|")
    for t in report.auto_tests:
        icon = "✅" if t.passed else "❌"
        details = t.details.replace("|", "\\|")[:100]
        lines.append(f"| {t.name} | {icon} | {t.weight} | {details} |")
    lines.append("")

    # File manifest
    if report.file_manifest:
        lines.append("## File Manifest (from student's repo)")
        lines.append("")
        lines.append("```")
        for f in report.file_manifest:
            lines.append(f)
        lines.append("```")
        lines.append("")

    # Overall comment
    if report.overall_comment:
        lines.append("## Overall Comments")
        lines.append("")
        lines.append(report.overall_comment)
        lines.append("")

    return "\n".join(lines)


# ════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Grade a student's T2 Task 1 submission")
    parser.add_argument("repo", type=Path,
                        help="Path to the student's Knowledge_Atlas clone")
    parser.add_argument("--student-name", default="",
                        help="Student name (or will prompt)")
    parser.add_argument("--student-email", default="",
                        help="Student email")
    parser.add_argument("--grader", default="",
                        help="Grader name (or will prompt)")
    parser.add_argument("--auto-only", action="store_true",
                        help="Run automated tests only, skip manual rubric")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output path for grade report (default: <repo>/160sp/rubrics/t2/GRADE_REPORT.md)")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.exists():
        print(f"Error: {repo} does not exist")
        sys.exit(1)

    print("=" * 60)
    print("  T2 Task 1 Grader — Fix the Contribute Page")
    print("=" * 60)
    print(f"  Repo: {repo}")
    print()

    # ── Student info
    student_name = args.student_name or input("Student name: ").strip()
    student_email = args.student_email or input("Student email: ").strip()
    grader = args.grader or input("Grader name: ").strip()

    # ── Run automated tests
    print("\n" + "=" * 60)
    print("  Running automated tests...")
    print("=" * 60)

    auto_results = []

    # Test 1: Classifier integration
    auto_results.append(test_classifier_integration(repo))

    # Test 2: Duplicate detection
    auto_results.append(test_duplicate_detection_exists(repo))

    # Test 3: Contribute page modified
    auto_results.append(test_contribute_page_modified(repo))

    # Test 4: Corrupt PDF handling
    auto_results.append(test_corrupt_pdf(repo))

    # Tests 6-9: Database tests (only if DB exists)
    db_path = find_db_path(repo)
    if db_path:
        print(f"  Found article DB: {db_path}")
        auto_results.append(test_db_field_completeness(db_path))
        auto_results.append(test_audit_log_presence(db_path))
        auto_results.append(test_storage_path_correctness(db_path))
        auto_results.append(test_edge_case_distinguishability(db_path))
    else:
        print("  ⚠ Article database not found — skipping DB tests")
        for name in ["DB field completeness", "Audit log presence",
                      "Storage path correctness",
                      "Accepted vs edge case distinguishability"]:
            auto_results.append(TestResult(name, False, "important",
                                           "Article database not found"))

    # Print results
    for r in auto_results:
        icon = "✅" if r.passed else "❌"
        print(f"  {icon} [{r.weight:>9s}] {r.name}: {r.details}")

    auto_score, auto_max = compute_auto_score(auto_results)
    print(f"\n  Automated score: {auto_score}/{auto_max}")

    # ── File manifest
    print("\n" + "=" * 60)
    print("  Collecting file manifest...")
    print("=" * 60)
    manifest = collect_file_manifest(repo)
    for f in manifest:
        print(f"    {f}")

    # ── Manual rubric
    rubric_scores = []
    if not args.auto_only:
        print("\n" + "=" * 60)
        print("  Manual rubric scoring")
        print("  (Review the student's submission documents, then score)")
        print("=" * 60)

        for criterion in RUBRIC_CRITERIA:
            if "Automated tests" in criterion.criterion:
                # Auto-scored
                criterion.points = auto_score
                criterion.comment = f"Auto: {sum(1 for r in auto_results if r.passed)}/{len(auto_results)} tests passed"
                rubric_scores.append(criterion)
            else:
                rubric_scores.append(prompt_manual_score(criterion))
    else:
        # Auto-only mode: zero out manual scores
        for criterion in RUBRIC_CRITERIA:
            if "Automated tests" in criterion.criterion:
                criterion.points = auto_score
                criterion.comment = f"Auto: {sum(1 for r in auto_results if r.passed)}/{len(auto_results)} tests passed"
            else:
                criterion.comment = "(auto-only mode — not scored)"
            rubric_scores.append(criterion)

    # ── Overall comment
    overall_comment = ""
    if not args.auto_only:
        print(f"\n{'─' * 60}")
        print("  Overall comment (multi-line, end with empty line):")
        comment_lines = []
        while True:
            try:
                line = input("  > ")
                if line == "":
                    break
                comment_lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        overall_comment = "\n".join(comment_lines)

    # ── Compute total
    total = sum(s.points for s in rubric_scores)
    max_total = sum(s.max_points for s in rubric_scores)

    # ── Build report
    report = GradeReport(
        student_name=student_name,
        student_email=student_email,
        grader=grader,
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        rubric_scores=rubric_scores,
        auto_tests=auto_results,
        total_points=total,
        max_points=max_total,
        overall_comment=overall_comment,
        file_manifest=manifest,
    )

    report_md = render_report(report)

    # ── Write report
    output_path = args.output
    if output_path is None:
        output_dir = repo / "160sp" / "rubrics" / "t2"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "GRADE_REPORT.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_md)

    print("\n" + "=" * 60)
    print(f"  TOTAL: {total} / {max_total}")
    print(f"  Report written to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
