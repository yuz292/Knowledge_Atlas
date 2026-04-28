"""
T4 Task 1 Autograder — Build a Persona Question Corpus (75 points)

Validates the deliverables specified in 160sp/t4_task1.html:
  - tagged corpus (40-60 questions, all 5 axis tags + adequacy_condition + provenance)
  - methods file documenting LLM-panel configurations and mining samples
  - persona-presentation-round notes (team milestone)

Looks for the corpus as either:
  - corpus.csv with the canonical column schema
  - corpus.json (a list of dicts) with the same fields
  - questions.csv / questions.json under any subdirectory of submission_dir

The grader is structurally similar to t1_task1_grader.py (AG's reference grader);
follows the same GradeReport schema and the same contract-gate convention.
"""
import os
import sys
import csv
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.report import GradeReport
from shared.validators import (
    check_json_loadable, check_file_exists,
)

TASK_TITLE = "Track 4 · Task 1: Build a Persona Question Corpus"
TASK_DESC = (
    "75 points. Generate 40 to 60 persona-specific questions for the persona "
    "you chose, tagged on the five axes (cognitive_purpose, answer_shape, "
    "evidential_demand, persona_fit, theoretical_commitment) with an "
    "adequacy_condition and provenance per row. Submit a methods file and "
    "the team's persona-presentation-round notes."
)
MAX_POINTS = 75

REQUIRED_AXES = [
    "cognitive_purpose", "answer_shape", "evidential_demand",
    "persona_fit", "theoretical_commitment",
]
REQUIRED_FIELDS = REQUIRED_AXES + ["question", "adequacy_condition", "source"]


def _load_corpus(submission_dir: str):
    """Return (rows, source_path, error). Rows is a list of dicts."""
    candidates = []
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            if f.lower() in ("corpus.csv", "corpus.json", "questions.csv", "questions.json"):
                candidates.append(os.path.join(root, f))
    if not candidates:
        return [], None, "no corpus.csv / corpus.json / questions.csv / questions.json found"

    path = candidates[0]
    try:
        if path.endswith(".csv"):
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                rows = list(csv.DictReader(fh))
            return rows, path, None
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                data = json.load(fh)
            if isinstance(data, dict) and "questions" in data:
                data = data["questions"]
            if not isinstance(data, list):
                return [], path, f"{os.path.basename(path)} is not a list of question rows"
            return data, path, None
    except Exception as e:
        return [], path, f"could not parse {os.path.basename(path)}: {e}"


def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t4", task=1, student_id=student_id,
                    max_points=MAX_POINTS, task_title=TASK_TITLE,
                    task_description=TASK_DESC)

    # ── 1. Contract gate (15 pts, GATE) ──────────────────────────
    contract_found = False
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            if f.endswith((".md", ".txt", ".json")):
                try:
                    with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fh:
                        text = fh.read().lower()
                    if "success condition" in text or "contract" in text or "adequacy condition" in text:
                        contract_found = True
                        break
                except Exception:
                    pass
        if contract_found:
            break

    if contract_found:
        r.add_check("Contract / adequacy-condition discipline", 15, "PASS",
                    "Contract or adequacy-condition language found in submission",
                    is_gate=True)
        r.strengths.append("Contract / adequacy-condition discipline present")
    else:
        r.add_check("Contract / adequacy-condition discipline", 15, "FAIL",
                    "No contract or adequacy-condition language found — GATE FAILED",
                    is_gate=True)
        r.missing.append("Contract / adequacy-condition file (gate failure)")

    # ── 2. Corpus size (20 pts) ──────────────────────────────────
    rows, corpus_path, err = _load_corpus(submission_dir)
    n = len(rows)

    if err:
        r.add_check("Corpus size (40-60 rows)", 20, "FAIL", err)
        r.missing.append("Corpus file")
    elif 40 <= n <= 60:
        r.add_check("Corpus size (40-60 rows)", 20, "PASS",
                    f"{n} questions in {os.path.basename(corpus_path)}")
        r.strengths.append(f"{n} questions submitted (target window 40-60)")
    elif 30 <= n < 40 or 60 < n <= 75:
        r.add_check("Corpus size (40-60 rows)", 20, "WARN",
                    f"{n} questions; target window is 40-60", pts_earned=12)
        r.weaknesses.append(f"Corpus size {n} sits outside the 40-60 target window")
    else:
        r.add_check("Corpus size (40-60 rows)", 20, "FAIL",
                    f"{n} questions; target window is 40-60")
        r.weaknesses.append(f"Corpus size {n} is far outside the 40-60 window")

    # ── 3. Five-axis tagging completeness (15 pts) ───────────────
    if rows:
        with_all_axes = sum(
            1 for row in rows
            if all(str(row.get(ax, "")).strip() for ax in REQUIRED_AXES)
        )
        ratio = with_all_axes / max(1, n)
        if ratio >= 0.95:
            r.add_check("Five-axis tagging", 15, "PASS",
                        f"{with_all_axes}/{n} rows carry all 5 axis tags")
            r.strengths.append(f"All 5 axis tags present on {with_all_axes}/{n} rows")
        elif ratio >= 0.75:
            r.add_check("Five-axis tagging", 15, "WARN",
                        f"{with_all_axes}/{n} rows carry all 5 axis tags",
                        pts_earned=10)
            r.weaknesses.append(f"Only {with_all_axes}/{n} rows carry all 5 axis tags")
        else:
            r.add_check("Five-axis tagging", 15, "FAIL",
                        f"Only {with_all_axes}/{n} rows have all 5 axis tags")
            r.weaknesses.append(f"Tagging incomplete: only {with_all_axes}/{n} rows fully tagged")
    else:
        r.add_check("Five-axis tagging", 15, "FAIL", "No corpus rows to check")

    # ── 4. Adequacy conditions present (10 pts) ──────────────────
    if rows:
        with_adequacy = sum(1 for row in rows if str(row.get("adequacy_condition", "")).strip())
        ratio = with_adequacy / max(1, n)
        if ratio >= 0.95:
            r.add_check("Adequacy conditions", 10, "PASS",
                        f"{with_adequacy}/{n} rows have a non-empty adequacy_condition")
            r.strengths.append(f"Adequacy conditions on {with_adequacy}/{n} rows")
        elif ratio >= 0.70:
            r.add_check("Adequacy conditions", 10, "WARN",
                        f"{with_adequacy}/{n} rows have adequacy_condition", pts_earned=6)
            r.weaknesses.append(f"Only {with_adequacy}/{n} rows have an adequacy_condition")
        else:
            r.add_check("Adequacy conditions", 10, "FAIL",
                        f"Only {with_adequacy}/{n} rows have adequacy_condition")
            r.weaknesses.append(f"Most rows missing adequacy_condition: {with_adequacy}/{n}")
    else:
        r.add_check("Adequacy conditions", 10, "FAIL", "No corpus rows to check")

    # ── 5. Provenance (10 pts) ───────────────────────────────────
    if rows:
        with_provenance = sum(
            1 for row in rows
            if str(row.get("source", "")).strip() and str(row.get("provenance", "")).strip()
        )
        ratio = with_provenance / max(1, n)
        if ratio >= 0.90:
            r.add_check("Provenance (source + provenance)", 10, "PASS",
                        f"{with_provenance}/{n} rows traceable")
            r.strengths.append(f"Provenance on {with_provenance}/{n} rows")
        elif ratio >= 0.60:
            r.add_check("Provenance (source + provenance)", 10, "WARN",
                        f"{with_provenance}/{n} rows traceable", pts_earned=6)
            r.weaknesses.append(f"Only {with_provenance}/{n} rows carry provenance")
        else:
            r.add_check("Provenance (source + provenance)", 10, "FAIL",
                        f"Only {with_provenance}/{n} rows traceable")
            r.weaknesses.append(f"Provenance missing on most rows ({with_provenance}/{n})")
    else:
        r.add_check("Provenance (source + provenance)", 10, "FAIL", "No corpus rows to check")

    # ── 6. Methods file (5 pts) ──────────────────────────────────
    methods_found = False
    methods_path = None
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            if "method" in f.lower() and f.endswith((".md", ".txt")):
                methods_found = True
                methods_path = os.path.join(root, f)
                break
        if methods_found:
            break

    if methods_found:
        try:
            with open(methods_path, "r", encoding="utf-8", errors="ignore") as fh:
                methods_text = fh.read().lower()
            if "panel" in methods_text and ("mining" in methods_text or "template" in methods_text):
                r.add_check("Methods file", 5, "PASS",
                            f"Methods file documents panels and mining: {os.path.basename(methods_path)}")
                r.strengths.append("Methods file documents panel and mining configurations")
            else:
                r.add_check("Methods file", 5, "WARN",
                            "Methods file present but does not document panels and mining clearly",
                            pts_earned=3)
                r.weaknesses.append("Methods file thin on panel / mining detail")
        except Exception:
            r.add_check("Methods file", 5, "WARN", "Methods file unreadable", pts_earned=2)
    else:
        r.add_check("Methods file", 5, "FAIL", "No methods.md / methods.txt found")
        r.missing.append("Methods file documenting panels and mining")

    # Repo worthiness — a clean corpus is worth shipping into the team's
    # shared corpora directory so others can study it as an exemplar.
    if rows and n >= 40 and corpus_path:
        r.add_repo_item(os.path.basename(corpus_path), "Knowledge_Atlas",
                        "160sp/track4/student_corpora/", "needs_review",
                        f"{n} tagged questions, ready for team peer review")

    # ── Summary ──────────────────────────────────────────────
    r.summary = _build_summary(r, n)
    return r


def _build_summary(r: GradeReport, n: int) -> str:
    parts = []
    for c in r.checks:
        if c.result == "PASS":
            parts.append(f"{c.criterion}: {c.detail}")
        elif c.result == "WARN":
            parts.append(f"{c.criterion}: partial — {c.detail}")
    if parts:
        return f"Student submitted a {n}-question corpus. " + ". ".join(parts[:4]) + "."
    return "Submission incomplete — most deliverables missing."


if __name__ == "__main__":
    sub_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    sid = sys.argv[2] if len(sys.argv) > 2 else "test_student"
    print(grade(sub_dir, sid).to_markdown())
