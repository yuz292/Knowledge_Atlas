#!/usr/bin/env python3
"""
T2 Task 3 — Grading & Comment Tool (Search Execution & Abstract-First Triage)
==============================================================================
Usage:  python3 t2_task3_grader.py /path/to/student/Knowledge_Atlas
        python3 t2_task3_grader.py --auto-only /path/to/student/Knowledge_Atlas
"""

import argparse, json, os, re, sqlite3, subprocess, sys
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


def _all_py(repo):
    r = []
    for pat in ["*.py", "scripts/*.py", "pipeline/*.py"]:
        for p in repo.glob(pat):
            try: r.append((p, p.read_text(errors="replace")))
            except: pass
    return r


# ── Tests ──

def test_serpapi_integration(repo):
    name = "SerpAPI integration"
    markers = ["serpapi", "SERPAPI_KEY", "google_scholar", "engine.*scholar"]
    for p, src in _all_py(repo):
        if any(m in src for m in markers[:3]) or re.search(markers[3], src):
            return TestResult(name, True, "critical", f"SerpAPI in {p.name}")
    return TestResult(name, False, "critical", "No SerpAPI integration found")


def test_search_results(repo):
    name = "Search results JSON exists"
    for pat in ["search_results*.json", "data/search*.json", "serpapi_results*.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("results", data.get("searches", []))
                return TestResult(name, True, "critical", f"{f.name}: {len(items)} entries")
            except: pass
    return TestResult(name, False, "critical", "No search results found")


def test_abstract_collector(repo):
    name = "Abstract collector exists"
    markers = ["abstract_collector", "fetch_by_doi", "SemanticScholarClient",
               "CrossRefClient", "PubMedClient", "paper_fetcher", "fallback"]
    for p, src in _all_py(repo):
        hits = [m for m in markers if m in src]
        if len(hits) >= 2:
            return TestResult(name, True, "critical", f"Collector in {p.name}: {hits}")
    return TestResult(name, False, "critical", "No abstract collection logic found")


def test_fallback_chain(repo):
    name = "Abstract fallback chain (multi-source)"
    sources_found = set()
    source_markers = {
        "semantic_scholar": ["SemanticScholarClient", "semantic_scholar", "api.semanticscholar"],
        "crossref": ["CrossRefClient", "crossref", "api.crossref"],
        "pubmed": ["PubMedClient", "pubmed", "eutils"],
        "openalex": ["openalex", "api.openalex"],
    }
    for p, src in _all_py(repo):
        for source, markers in source_markers.items():
            if any(m in src for m in markers):
                sources_found.add(source)
    if len(sources_found) >= 3:
        return TestResult(name, True, "important",
                          f"Uses {len(sources_found)} sources: {sorted(sources_found)}")
    elif len(sources_found) >= 2:
        return TestResult(name, True, "important",
                          f"Uses {len(sources_found)} sources: {sorted(sources_found)} (ideally 3+)")
    elif sources_found:
        return TestResult(name, False, "important", f"Only 1 source: {sources_found}")
    return TestResult(name, False, "important", "No fallback chain found")


def test_triage_logic(repo):
    name = "Abstract triage (ACCEPT/EDGE_CASE/REJECT)"
    for p, src in _all_py(repo):
        has_accept = "ACCEPT" in src
        has_reject = "REJECT" in src
        has_edge = "EDGE" in src or "edge_case" in src.lower()
        has_missing = "MISSING_ABSTRACT" in src or "missing_abstract" in src
        if has_accept and has_reject:
            detail = "ACCEPT + REJECT"
            if has_edge: detail += " + EDGE_CASE"
            if has_missing: detail += " + MISSING_ABSTRACT"
            return TestResult(name, True, "critical", f"Triage in {p.name}: {detail}")
    return TestResult(name, False, "critical", "No triage logic found")


def test_classifier_integration(repo):
    name = "Classifier integration (atlas_shared)"
    for p, src in _all_py(repo):
        if any(m in src for m in ["atlas_shared", "AdaptiveClassifier", "classifier_system"]):
            return TestResult(name, True, "important", f"Classifier in {p.name}")
    return TestResult(name, False, "important", "No classifier integration")


def test_voi_scoring(repo):
    name = "VOI scoring on abstracts"
    for p, src in _all_py(repo):
        if any(m in src for m in ["score_voi", "voi_scoring", "aggregate_paper_voi"]):
            return TestResult(name, True, "important", f"VOI scoring in {p.name}")
    return TestResult(name, False, "important", "No VOI scoring on abstracts")


def test_triage_results(repo):
    name = "Triage results JSON exists"
    for pat in ["triage_results*.json", "data/triage*.json", "abstract_triage*.json"]:
        for f in repo.glob(pat):
            try:
                data = json.loads(f.read_text())
                items = data if isinstance(data, list) else data.get("results", [])
                counts = {}
                for item in items:
                    if isinstance(item, dict):
                        d = item.get("triage_decision", item.get("decision", "unknown"))
                        counts[d] = counts.get(d, 0) + 1
                return TestResult(name, True, "critical",
                                  f"{f.name}: {len(items)} papers, decisions: {counts}")
            except: pass
    return TestResult(name, False, "critical", "No triage results found")


def test_dashboard(repo):
    name = "PRISMA dashboard exists"
    for c in ["ka_topic_proposer.html", "ka_search_dashboard.html",
              "prisma_dashboard.html", "search_pipeline.html"]:
        p = repo / c
        if p.exists():
            src = p.read_text(errors="replace").lower()
            features = []
            if any(w in src for w in ["funnel", "prisma", "screened"]): features.append("PRISMA")
            if any(w in src for w in ["accept", "reject", "triage"]): features.append("triage")
            if any(w in src for w in ["gap", "voi"]): features.append("gaps")
            return TestResult(name, True, "important", f"{c}: {features}")
    return TestResult(name, False, "important", "No dashboard found")


def test_null_results(repo):
    name = "Null result / MISSING_ABSTRACT handling"
    for p, src in _all_py(repo):
        if any(m in src.lower() for m in ["missing_abstract", "null result", "no results",
                                            "zero results", "no papers"]):
            return TestResult(name, True, "minor", f"Handled in {p.name}")
    return TestResult(name, False, "minor", "No null/missing handling found")


def test_db_entries(repo):
    name = "Accepted papers in database"
    for db_path in [repo/"data"/"ka_auth.db", repo/"ka_auth.db"]:
        if db_path.exists():
            try:
                db = sqlite3.connect(str(db_path), timeout=5.0)
                n = db.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
                db.close()
                if n > 0: return TestResult(name, True, "important", f"{n} articles")
                return TestResult(name, False, "important", "Table empty")
            except Exception as e:
                return TestResult(name, False, "important", f"DB error: {e}")
    return TestResult(name, False, "important", "DB not found")


RUBRIC = [
    RubricScore("SerpAPI integration: Queried Google Scholar, got results", 10),
    RubricScore("Abstract collection: Fallback chain works, ≥70% hit rate", 15),
    RubricScore("Abstract triage: Classifier + VOI → ACCEPT/EDGE/REJECT", 15),
    RubricScore("PRISMA funnel: Dashboard shows real numbers at each stage", 10),
    RubricScore("End-to-end trace: One paper from gap → search → triage → store", 10),
    RubricScore("Null results + MISSING_ABSTRACT: Documented, not dropped", 5),
    RubricScore("Verification questions: Caught real problems", 10),
]


def prompt_manual(c):
    print(f"\n{'─'*60}\n  {c.criterion}\n  Max: {c.max_points}\n{'─'*60}")
    while True:
        try:
            raw = input(f"  Score (0–{c.max_points}): ").strip()
            s = int(raw) if raw else 0
            if 0 <= s <= c.max_points: break
            print(f"  0–{c.max_points}")
        except ValueError: print("  Number please")
        except (EOFError, KeyboardInterrupt): s = 0; break
    c.points = s; c.comment = input("  Comment: ").strip()
    return c


def compute_auto(results):
    w = {"critical": 3, "important": 2, "minor": 1}
    total = sum(w[r.weight] for r in results)
    earned = sum(w[r.weight] for r in results if r.passed)
    return round(15 * earned / total) if total else 0


def render(report):
    lines = [
        "# T2 Task 3 — Grade Report (Search Execution & Abstract-First Triage)", "",
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
    ap = argparse.ArgumentParser(description="Grade T2 Task 3")
    ap.add_argument("repo", type=Path)
    ap.add_argument("--student-name", default="")
    ap.add_argument("--student-email", default="")
    ap.add_argument("--grader", default="")
    ap.add_argument("--auto-only", action="store_true")
    ap.add_argument("--output", type=Path, default=None)
    args = ap.parse_args()

    repo = args.repo.resolve()
    if not repo.exists(): print(f"Error: {repo} not found"); sys.exit(1)

    print(f"{'='*60}\n  T2 Task 3 Grader — Search Execution & Triage\n{'='*60}\n  Repo: {repo}\n")

    sn = args.student_name or input("Student name: ").strip()
    se = args.student_email or input("Student email: ").strip()
    gr = args.grader or input("Grader name: ").strip()

    auto = [
        test_serpapi_integration(repo), test_search_results(repo),
        test_abstract_collector(repo), test_fallback_chain(repo),
        test_triage_logic(repo), test_classifier_integration(repo),
        test_voi_scoring(repo), test_triage_results(repo),
        test_dashboard(repo), test_null_results(repo), test_db_entries(repo),
    ]

    print(f"\n{'='*60}\n  Automated tests\n{'='*60}")
    for r in auto: print(f"  {'✅' if r.passed else '❌'} [{r.weight:>9s}] {r.name}: {r.details}")
    auto_score = compute_auto(auto)
    print(f"\n  Auto: {auto_score}/15")

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

    out = args.output or (repo/"160sp"/"rubrics"/"t2"/"GRADE_REPORT_T2_TASK3.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rpt))
    print(f"\n{'='*60}\n  TOTAL: {total}/{max_t}\n  Report: {out}\n{'='*60}")


if __name__ == "__main__": main()
