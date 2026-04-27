#!/usr/bin/env python3
"""
T2 Task 2 — Grading & Comment Tool
====================================
Run against a student's Knowledge_Atlas clone to assign grades and comments
for the "Topic Proposer & Search Pipeline" assignment.

Usage
-----
    python3 t2_task2_grader.py /path/to/student/Knowledge_Atlas

    # Auto-only mode (no manual prompts)
    python3 t2_task2_grader.py --auto-only /path/to/student/Knowledge_Atlas

The grader:
  1. Runs automated tests checking pipeline artifacts exist and are well-formed
  2. Prompts the TA for manual rubric scores (spec quality, search quality, etc.)
  3. Computes a weighted total
  4. Writes a grade report to  <student_repo>/160sp/rubrics/t2/GRADE_REPORT_T2.md
"""

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
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

def find_topic_proposer(repo: Path) -> Optional[Path]:
    """Find the topic proposer script."""
    candidates = [
        "topic_proposer.py",
        "search_pipeline.py",
        "gap_analyzer.py",
        "proposer.py",
        "160sp/topic_proposer.py",
        "scripts/topic_proposer.py",
    ]
    for c in candidates:
        p = repo / c
        if p.exists():
            return p
    # Search for any python file mentioning "mechanism_chain" or "gap"
    for py in repo.glob("*.py"):
        try:
            source = py.read_text(errors="replace")
            if "mechanism_chain" in source or "gap_type" in source:
                return py
        except Exception:
            pass
    return None


def find_dashboard(repo: Path) -> Optional[Path]:
    """Find the dashboard HTML page."""
    candidates = [
        "ka_topic_proposer.html",
        "ka_search_dashboard.html",
        "ka_pipeline_dashboard.html",
        "topic_proposer.html",
        "search_pipeline.html",
        "160sp/ka_topic_proposer.html",
    ]
    for c in candidates:
        p = repo / c
        if p.exists():
            return p
    return None


def find_search_results(repo: Path) -> list[Path]:
    """Find search result JSON files."""
    results = []
    for pattern in ["search_results*.json", "data/search*.json",
                     "data/storage/search*.json", "**/search_results*.json"]:
        results.extend(repo.glob(pattern))
    return results


def test_topic_proposer_exists(repo: Path) -> TestResult:
    """Check that a topic proposer script exists."""
    name = "Topic proposer script exists"
    script = find_topic_proposer(repo)
    if script:
        return TestResult(name, True, "critical",
                          f"Found: {script.relative_to(repo)}")
    return TestResult(name, False, "critical",
                      "No topic proposer script found")


def test_topic_proposer_reads_templates(repo: Path) -> TestResult:
    """Check that the proposer reads PNU template JSON files."""
    name = "Proposer reads template data"
    script = find_topic_proposer(repo)
    if not script:
        return TestResult(name, False, "critical", "No proposer script found")

    source = script.read_text(errors="replace")
    reads_json = "json.load" in source or "json.loads" in source
    reads_chain = "mechanism_chain" in source
    reads_conf = "confidence" in source

    if reads_json and reads_chain and reads_conf:
        return TestResult(name, True, "critical",
                          "Reads JSON, accesses mechanism_chain, checks confidence")
    elif reads_json and (reads_chain or reads_conf):
        return TestResult(name, True, "critical",
                          "Reads JSON and partially accesses template structure")
    elif reads_json:
        return TestResult(name, False, "critical",
                          "Reads JSON but doesn't access mechanism_chain or confidence")
    else:
        return TestResult(name, False, "critical",
                          "Does not appear to read template JSON files")


def test_generates_search_queries(repo: Path) -> TestResult:
    """Check that the proposer generates search queries."""
    name = "Generates search queries"
    script = find_topic_proposer(repo)
    if not script:
        return TestResult(name, False, "important", "No proposer script found")

    source = script.read_text(errors="replace")
    has_query = ("search_quer" in source.lower() or
                 "query" in source.lower() or
                 "keyword" in source.lower())
    has_multiple_formats = (
        ("ai_scholar" in source or "natural_language" in source or
         "scholar" in source.lower()) and
        ("keyword" in source.lower() or "boolean" in source.lower())
    )

    if has_multiple_formats:
        return TestResult(name, True, "important",
                          "Generates multiple search query formats")
    elif has_query:
        return TestResult(name, True, "important",
                          "Generates search queries (single format)")
    else:
        return TestResult(name, False, "important",
                          "No search query generation found")


def test_gap_type_awareness(repo: Path) -> TestResult:
    """Check if the proposer is aware of gap types."""
    name = "Gap type classification"
    script = find_topic_proposer(repo)
    if not script:
        return TestResult(name, False, "important", "No proposer script found")

    source = script.read_text(errors="replace")
    gap_types = ["MISSING_NODE", "MISSING_EDGE", "AMBIGUOUS_DIRECTION",
                 "UNKNOWN_INTERACTION", "gap_type"]
    found = [g for g in gap_types if g in source]

    if len(found) >= 2:
        return TestResult(name, True, "important",
                          f"Found gap type awareness: {found}")
    elif found:
        return TestResult(name, True, "important",
                          f"Partial gap type awareness: {found}")
    else:
        return TestResult(name, False, "important",
                          "No gap type classification found — "
                          "proposer doesn't distinguish gap types")


def test_search_results_exist(repo: Path) -> TestResult:
    """Check that search results were actually produced."""
    name = "Search results exist"
    results = find_search_results(repo)
    if results:
        total_results = 0
        for r in results:
            try:
                data = json.loads(r.read_text())
                if isinstance(data, list):
                    total_results += len(data)
                elif isinstance(data, dict) and "results" in data:
                    total_results += len(data["results"])
            except Exception:
                pass
        return TestResult(name, True, "critical",
                          f"Found {len(results)} result file(s) "
                          f"with {total_results} total results")
    return TestResult(name, False, "critical",
                      "No search result JSON files found")


def test_dashboard_exists(repo: Path) -> TestResult:
    """Check that a dashboard page exists."""
    name = "Dashboard page exists"
    dashboard = find_dashboard(repo)
    if dashboard:
        source = dashboard.read_text(errors="replace")
        has_gap_display = ("gap" in source.lower() and
                           ("template" in source.lower() or
                            "confidence" in source.lower()))
        has_results_display = ("result" in source.lower() or
                               "search" in source.lower())
        features = []
        if has_gap_display:
            features.append("gaps")
        if has_results_display:
            features.append("results")
        return TestResult(name, True, "important",
                          f"Found: {dashboard.name} — displays: {features}")
    return TestResult(name, False, "important", "No dashboard page found")


def test_dashboard_persistence(repo: Path) -> TestResult:
    """Check that dashboard reads from persistent storage, not memory."""
    name = "Dashboard data persistence"
    dashboard = find_dashboard(repo)
    if not dashboard:
        return TestResult(name, False, "minor", "No dashboard found")

    source = dashboard.read_text(errors="replace")
    persistent = ("fetch(" in source or "XMLHttpRequest" in source or
                   "localStorage" in source or
                   ".json" in source or "sqlite" in source.lower())
    if persistent:
        return TestResult(name, True, "minor",
                          "Dashboard reads from persistent source (API/file/localStorage)")
    return TestResult(name, False, "minor",
                      "Dashboard may not persist data — no fetch/file/storage calls found")


def test_vetting_integration(repo: Path) -> TestResult:
    """Check if the pipeline integrates with the Task 1 vetting endpoint."""
    name = "Vetting integration (Task 1 endpoint)"
    # Check all Python files for endpoint calls
    for py in list(repo.glob("*.py")) + list(repo.glob("scripts/*.py")):
        try:
            source = py.read_text(errors="replace")
            has_submit = ("/api/articles/submit" in source or
                          "submit" in source.lower() and
                          "requests.post" in source)
            has_classify = ("classify" in source.lower() or
                            "classifier" in source.lower() or
                            "AdaptiveClassifier" in source)
            if has_submit or has_classify:
                return TestResult(name, True, "important",
                                  f"Found vetting integration in {py.name}")
        except Exception:
            pass
    return TestResult(name, False, "important",
                      "No integration with Task 1 contribute/submit endpoint found")


def test_q01_q30_mapping(repo: Path) -> TestResult:
    """Check if the proposer maps gaps to research questions Q01–Q30."""
    name = "Research question mapping (Q01–Q30)"
    script = find_topic_proposer(repo)
    if not script:
        return TestResult(name, False, "minor", "No proposer script found")

    source = script.read_text(errors="replace")
    has_question_mapping = (
        "question_id" in source or "Q01" in source or
        "research_question" in source.lower() or
        "atlas_topic" in source
    )
    if has_question_mapping:
        return TestResult(name, True, "minor",
                          "Maps gaps to research questions")
    return TestResult(name, False, "minor",
                      "No research question mapping found")


def find_db_path(repo: Path) -> Optional[Path]:
    """Find the article database."""
    for candidate in [repo / "data" / "ka_auth.db", repo / "ka_auth.db"]:
        if candidate.exists():
            return candidate
    return None


def test_vetted_papers_in_db(repo: Path) -> TestResult:
    """Check if any vetted papers from the search pipeline appear in the DB."""
    name = "Vetted papers stored in database"
    db_path = find_db_path(repo)
    if not db_path:
        return TestResult(name, False, "important", "Article database not found")
    try:
        db = sqlite3.connect(str(db_path), timeout=5.0)
        db.row_factory = sqlite3.Row
        count = db.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        db.close()
        if count > 0:
            return TestResult(name, True, "important",
                              f"{count} articles in database")
        return TestResult(name, False, "important",
                          "articles table exists but is empty")
    except Exception as e:
        return TestResult(name, False, "important", f"DB check failed: {e}")


# ════════════════════════════════════════════════
# MANUAL RUBRIC
# ════════════════════════════════════════════════

RUBRIC_CRITERIA = [
    RubricScore("Gap analysis: Correctly identified low-confidence steps and gap types", 15),
    RubricScore("Spec quality: Contract covers Topic Proposer, Search Runner, Vetting, Dashboard", 15),
    RubricScore("Search quality: Queries are specific and produce relevant results", 15),
    RubricScore("End-to-end pipeline: At least one paper traced gap → search → vet → store", 20),
    RubricScore("Dashboard: Shows gaps, searches, results; data persists", 10),
    RubricScore("Verification questions: Caught problems in AI's implementation", 10),
    RubricScore("Automated tests: Pipeline artifacts exist and are well-formed (auto-scored)", 15),
]


def prompt_manual_score(criterion: RubricScore) -> RubricScore:
    """Prompt the TA for a score and comment."""
    print(f"\n{'─' * 60}")
    print(f"  {criterion.criterion}")
    print(f"  Max points: {criterion.max_points}")
    print(f"{'─' * 60}")

    while True:
        try:
            raw = input(f"  Score (0–{criterion.max_points}): ").strip()
            if raw == "":
                score = 0
                break
            score = int(raw)
            if 0 <= score <= criterion.max_points:
                break
            print(f"  Must be between 0 and {criterion.max_points}")
        except ValueError:
            print("  Enter a number")
        except (EOFError, KeyboardInterrupt):
            score = 0
            break

    comment = input("  Comment (optional): ").strip()
    criterion.points = score
    criterion.comment = comment
    return criterion


# ════════════════════════════════════════════════
# SCORING & REPORT
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
    lines.append("# T2 Task 2 — Grade Report")
    lines.append("")
    lines.append(f"**Student:** {report.student_name or '(not set)'}")
    lines.append(f"**Email:** {report.student_email or '(not set)'}")
    lines.append(f"**Grader:** {report.grader or '(not set)'}")
    lines.append(f"**Date:** {report.timestamp}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"## Total: {report.total_points} / {report.max_points}")
    lines.append("")

    lines.append("## Rubric Scores")
    lines.append("")
    lines.append("| Criterion | Score | Comment |")
    lines.append("|-----------|-------|---------|")
    for s in report.rubric_scores:
        comment = s.comment.replace("|", "\\|") if s.comment else "—"
        lines.append(f"| {s.criterion} | {s.points}/{s.max_points} | {comment} |")
    lines.append("")

    lines.append("## Automated Test Results")
    lines.append("")
    lines.append("| Test | Status | Weight | Details |")
    lines.append("|------|--------|--------|---------|")
    for t in report.auto_tests:
        icon = "✅" if t.passed else "❌"
        details = t.details.replace("|", "\\|")[:100]
        lines.append(f"| {t.name} | {icon} | {t.weight} | {details} |")
    lines.append("")

    if report.file_manifest:
        lines.append("## File Manifest")
        lines.append("")
        lines.append("```")
        for f in report.file_manifest:
            lines.append(f)
        lines.append("```")
        lines.append("")

    if report.overall_comment:
        lines.append("## Overall Comments")
        lines.append("")
        lines.append(report.overall_comment)
        lines.append("")

    return "\n".join(lines)


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
                parts = line.strip().split(None, 1)
                if len(parts) == 2 and parts[1] not in manifest:
                    manifest.append(f"[{parts[0]}] {parts[1]}")
    except Exception:
        manifest.append("(git not available)")
    return manifest


# ════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Grade a student's T2 Task 2 submission")
    parser.add_argument("repo", type=Path,
                        help="Path to the student's Knowledge_Atlas clone")
    parser.add_argument("--student-name", default="")
    parser.add_argument("--student-email", default="")
    parser.add_argument("--grader", default="")
    parser.add_argument("--auto-only", action="store_true",
                        help="Run automated tests only, skip manual rubric")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.exists():
        print(f"Error: {repo} does not exist")
        sys.exit(1)

    print("=" * 60)
    print("  T2 Task 2 Grader — Topic Proposer & Search Pipeline")
    print("=" * 60)
    print(f"  Repo: {repo}")
    print()

    student_name = args.student_name or input("Student name: ").strip()
    student_email = args.student_email or input("Student email: ").strip()
    grader = args.grader or input("Grader name: ").strip()

    # ── Automated tests
    print("\n" + "=" * 60)
    print("  Running automated tests...")
    print("=" * 60)

    auto_results = []
    auto_results.append(test_topic_proposer_exists(repo))
    auto_results.append(test_topic_proposer_reads_templates(repo))
    auto_results.append(test_generates_search_queries(repo))
    auto_results.append(test_gap_type_awareness(repo))
    auto_results.append(test_search_results_exist(repo))
    auto_results.append(test_dashboard_exists(repo))
    auto_results.append(test_dashboard_persistence(repo))
    auto_results.append(test_vetting_integration(repo))
    auto_results.append(test_q01_q30_mapping(repo))
    auto_results.append(test_vetted_papers_in_db(repo))

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
        print("=" * 60)

        for criterion in RUBRIC_CRITERIA:
            if "auto-scored" in criterion.criterion.lower():
                criterion.points = auto_score
                criterion.comment = (
                    f"Auto: {sum(1 for r in auto_results if r.passed)}"
                    f"/{len(auto_results)} tests passed"
                )
                rubric_scores.append(criterion)
            else:
                rubric_scores.append(prompt_manual_score(criterion))
    else:
        for criterion in RUBRIC_CRITERIA:
            if "auto-scored" in criterion.criterion.lower():
                criterion.points = auto_score
                criterion.comment = (
                    f"Auto: {sum(1 for r in auto_results if r.passed)}"
                    f"/{len(auto_results)} tests passed"
                )
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

    # ── Build and write report
    total = sum(s.points for s in rubric_scores)
    max_total = sum(s.max_points for s in rubric_scores)

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

    output_path = args.output
    if output_path is None:
        output_dir = repo / "160sp" / "rubrics" / "t2"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "GRADE_REPORT_T2.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(report))

    print("\n" + "=" * 60)
    print(f"  TOTAL: {total} / {max_total}")
    print(f"  Report written to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
