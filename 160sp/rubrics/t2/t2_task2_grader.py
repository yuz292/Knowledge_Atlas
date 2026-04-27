#!/usr/bin/env python3
"""
T2 Task 2 — Grading & Comment Tool (Gap Targeting & Query Generation)
======================================================================
Usage:  python3 t2_task2_grader.py /path/to/student/Knowledge_Atlas
        python3 t2_task2_grader.py --auto-only /path/to/student/Knowledge_Atlas
"""

import argparse, json, os, re, subprocess, sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class TestResult:
    name: str; passed: bool; weight: str; details: str = ""

@dataclass
class RubricScore:
    criterion: str; max_points: int; points: int = 0; comment: str = ""

@dataclass
class GradeReport:
    student_name: str = ""; student_email: str = ""; grader: str = ""
    timestamp: str = ""; rubric_scores: list = field(default_factory=list)
    auto_tests: list = field(default_factory=list); total_points: int = 0
    max_points: int = 0; overall_comment: str = ""
    file_manifest: list = field(default_factory=list)


def _all_py(repo: Path) -> list[tuple[Path, str]]:
    results = []
    for pat in ["*.py", "scripts/*.py", "pipeline/*.py"]:
        for p in repo.glob(pat):
            try: results.append((p, p.read_text(errors="replace")))
            except: pass
    return results


# ── Tests ──

def test_gap_extractor(repo):
    name = "Gap extractor script exists"
    for pat in ["gap_extractor.py", "topic_proposer.py", "gap_analyzer.py"]:
        if (repo / pat).exists():
            return TestResult(name, True, "critical", f"Found: {pat}")
    for p, src in _all_py(repo):
        if "mechanism_chain" in src and "confidence" in src:
            return TestResult(name, True, "critical", f"Found in {p.name}")
    return TestResult(name, False, "critical", "No gap extractor found")


def test_reads_templates(repo):
    name = "Reads PNU templates + confidence"
    for p, src in _all_py(repo):
        if "json.load" in src and "mechanism_chain" in src:
            has_threshold = "< 0.5" in src or "<0.5" in src or "threshold" in src
            detail = "Reads JSON + mechanism_chain"
            if has_threshold: detail += " + confidence threshold"
            return TestResult(name, True, "critical", f"{detail} ({p.name})")
    return TestResult(name, False, "critical", "No template reading found")


def test_voi_scoring(repo):
    name = "VOI scoring integration"
    markers = ["VOICalculator", "calculate_voi", "voi_score", "voi_search"]
    for p, src in _all_py(repo):
        hits = [m for m in markers if m in src]
        if hits:
            return TestResult(name, True, "important", f"Uses: {hits} ({p.name})")
    return TestResult(name, False, "important", "No VOI scoring found")


def test_gap_results_json(repo):
    name = "Gap results JSON exists"
    for pat in ["gap_results.json", "data/gap*.json", "gaps.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                count = len(data) if isinstance(data, list) else len(data.get("gaps", []))
                return TestResult(name, True, "critical", f"{f.name}: {count} gaps")
            except: pass
    return TestResult(name, False, "critical", "No gap results JSON found")


def test_query_results_json(repo):
    name = "Query results JSON exists"
    for pat in ["query_results.json", "data/quer*.json", "queries.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("queries", [])
                has_both = False
                for item in items[:5]:
                    if isinstance(item, dict):
                        has_ai = any(k in item for k in ["ai_citation", "ai_scholar", "ai_query"])
                        has_bool = any(k in item for k in ["boolean", "boolean_query", "keyword"])
                        if has_ai and has_bool: has_both = True
                detail = f"{f.name}: {len(items)} queries"
                if has_both: detail += " (both formats)"
                return TestResult(name, True, "critical", detail)
            except: pass
    return TestResult(name, False, "critical", "No query results JSON found")


def test_ai_citation_quality(repo):
    name = "AI Citation queries are full sentences"
    for pat in ["query_results.json", "queries.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("queries", [])
                sentence_count = 0
                for item in items:
                    if not isinstance(item, dict): continue
                    q = item.get("ai_citation", item.get("ai_scholar", item.get("ai_query", "")))
                    if isinstance(q, str) and len(q) > 50 and "?" in q:
                        sentence_count += 1
                if sentence_count >= 3:
                    return TestResult(name, True, "important",
                                      f"{sentence_count} queries are proper research questions")
                elif sentence_count > 0:
                    return TestResult(name, True, "important",
                                      f"Only {sentence_count} queries are full sentences")
            except: pass
    return TestResult(name, False, "important", "Cannot verify AI Citation query quality")


def test_boolean_quality(repo):
    name = "Boolean queries use proper operators"
    for pat in ["query_results.json", "queries.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("queries", [])
                proper = 0
                for item in items:
                    if not isinstance(item, dict): continue
                    q = item.get("boolean", item.get("boolean_query", item.get("keyword", "")))
                    if isinstance(q, str):
                        has_quotes = '"' in q
                        has_ops = " AND " in q or " OR " in q
                        if has_quotes and has_ops: proper += 1
                if proper >= 3:
                    return TestResult(name, True, "important",
                                      f"{proper} queries use quotes + AND/OR")
                elif proper > 0:
                    return TestResult(name, True, "important",
                                      f"Only {proper} queries use proper Boolean syntax")
            except: pass
    return TestResult(name, False, "important", "Cannot verify Boolean query quality")


RUBRIC = [
    RubricScore("Gap extraction: Identified low-confidence steps from templates", 15),
    RubricScore("VOI scoring: Gaps ranked; can explain why one scores higher", 10),
    RubricScore("AI Citation queries: Follow 5-component pattern, specific", 10),
    RubricScore("Boolean queries: Proper AND/OR/quotes, not comma-separated", 10),
    RubricScore("Spot-check: Tested 3 queries in Google, reported results", 5),
    RubricScore("Verification questions: Caught problems in AI implementation", 10),
]


def prompt_manual(c: RubricScore):
    print(f"\n{'─'*60}\n  {c.criterion}\n  Max: {c.max_points}\n{'─'*60}")
    while True:
        try:
            raw = input(f"  Score (0–{c.max_points}): ").strip()
            s = int(raw) if raw else 0
            if 0 <= s <= c.max_points: break
            print(f"  0–{c.max_points}")
        except ValueError: print("  Number please")
        except (EOFError, KeyboardInterrupt): s = 0; break
    c.points = s
    c.comment = input("  Comment: ").strip()
    return c


def compute_auto(results):
    w = {"critical": 3, "important": 2, "minor": 1}
    total = sum(w[r.weight] for r in results)
    earned = sum(w[r.weight] for r in results if r.passed)
    return round(15 * earned / total) if total else 0


def render(report):
    lines = [
        "# T2 Task 2 — Grade Report (Gap Targeting & Query Generation)", "",
        f"**Student:** {report.student_name or '(not set)'}",
        f"**Email:** {report.student_email or '(not set)'}",
        f"**Grader:** {report.grader or '(not set)'}",
        f"**Date:** {report.timestamp}", "", "---", "",
        f"## Total: {report.total_points} / {report.max_points}", "",
        "## Rubric Scores", "", "| Criterion | Score | Comment |",
        "|-----------|-------|---------|",
    ]
    for s in report.rubric_scores:
        lines.append(f"| {s.criterion} | {s.points}/{s.max_points} | {(s.comment or '—').replace('|','\\|')} |")
    lines += ["", "## Automated Tests", "", "| Test | Status | Details |",
              "|------|--------|---------|"]
    for t in report.auto_tests:
        lines.append(f"| {t.name} | {'✅' if t.passed else '❌'} | {t.details[:100].replace('|','\\|')} |")
    if report.file_manifest:
        lines += ["", "## File Manifest", "", "```"] + report.file_manifest + ["```"]
    if report.overall_comment:
        lines += ["", "## Overall Comments", "", report.overall_comment]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Grade T2 Task 2")
    ap.add_argument("repo", type=Path)
    ap.add_argument("--student-name", default="")
    ap.add_argument("--student-email", default="")
    ap.add_argument("--grader", default="")
    ap.add_argument("--auto-only", action="store_true")
    ap.add_argument("--output", type=Path, default=None)
    args = ap.parse_args()

    repo = args.repo.resolve()
    if not repo.exists(): print(f"Error: {repo} not found"); sys.exit(1)

    print(f"{'='*60}\n  T2 Task 2 Grader — Gap Targeting & Query Generation\n{'='*60}\n  Repo: {repo}\n")

    sn = args.student_name or input("Student name: ").strip()
    se = args.student_email or input("Student email: ").strip()
    gr = args.grader or input("Grader name: ").strip()

    auto = [test_gap_extractor(repo), test_reads_templates(repo),
            test_voi_scoring(repo), test_gap_results_json(repo),
            test_query_results_json(repo), test_ai_citation_quality(repo),
            test_boolean_quality(repo)]

    print(f"\n{'='*60}\n  Automated tests\n{'='*60}")
    for r in auto: print(f"  {'✅' if r.passed else '❌'} [{r.weight:>9s}] {r.name}: {r.details}")
    auto_score = compute_auto(auto)
    print(f"\n  Auto: {auto_score}/15")

    # manifest
    manifest = []
    try:
        d = subprocess.run(["git","diff","--name-only","HEAD"], cwd=str(repo),
                          capture_output=True, text=True, timeout=10)
        if d.stdout.strip(): manifest.extend(d.stdout.strip().split("\n"))
        s = subprocess.run(["git","status","--short"], cwd=str(repo),
                          capture_output=True, text=True, timeout=10)
        for l in s.stdout.strip().split("\n"):
            if l.strip():
                p = l.strip().split(None,1)
                if len(p)==2 and p[1] not in manifest: manifest.append(f"[{p[0]}] {p[1]}")
    except: manifest.append("(git not available)")

    rubric = []
    if not args.auto_only:
        print(f"\n{'='*60}\n  Manual rubric\n{'='*60}")
        for c in RUBRIC: rubric.append(prompt_manual(c))
    else:
        for c in RUBRIC: c.comment = "(auto-only)"; rubric.append(c)

    total = sum(s.points for s in rubric) + auto_score
    max_t = sum(s.max_points for s in rubric) + 15

    rpt = GradeReport(sn, se, gr,
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        rubric, auto, total, max_t, "", manifest)

    out = args.output or (repo/"160sp"/"rubrics"/"t2"/"GRADE_REPORT_T2_TASK2.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rpt))
    print(f"\n{'='*60}\n  TOTAL: {total}/{max_t}\n  Report: {out}\n{'='*60}")


if __name__ == "__main__": main()
