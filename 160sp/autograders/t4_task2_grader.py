"""
T4 Task 2 Autograder — Winnow & Fit Answer Shapes (75 points)

Validates the deliverables specified in 160sp/t4_task2.html:
  - working corpus (Task-1 corpus extended with chosen_shape, shape_sketch,
    named_defeaters per surviving row)
  - winnowing log (counts at each sieve stage, backlog populated)
  - team-collective fitting-critique notes
"""
import os
import sys
import csv
import json
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.report import GradeReport

TASK_TITLE = "Track 4 · Task 2: Winnow & Fit Answer Shapes"
TASK_DESC = (
    "75 points. Run the four-stage winnowing protocol on your Task-1 corpus, "
    "fit each surviving question to one of five canonical answer shapes "
    "(Toulmin, field-map, procedure, contrast-pair, ranked-brief) with a "
    "shape_sketch and at least one named_defeater per row. Submit a winnowing "
    "log and the team's fitting-critique notes."
)
MAX_POINTS = 75

VALID_SHAPES = {"toulmin", "field-map", "fieldmap", "field_map",
                "procedure", "contrast-pair", "contrastpair",
                "contrast_pair", "ranked-brief", "rankedbrief", "ranked_brief"}


def _load_working_corpus(submission_dir: str):
    candidates = []
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            if f.lower() in ("working_corpus.csv", "working_corpus.json",
                             "fitting_catalog.csv", "fitting_catalog.json"):
                candidates.append(os.path.join(root, f))
    if not candidates:
        return [], None, "no working_corpus / fitting_catalog file found"
    path = candidates[0]
    try:
        if path.endswith(".csv"):
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                rows = list(csv.DictReader(fh))
            return rows, path, None
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                data = json.load(fh)
            if isinstance(data, dict) and "rows" in data:
                data = data["rows"]
            return (data if isinstance(data, list) else []), path, None
    except Exception as e:
        return [], path, str(e)


def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t4", task=2, student_id=student_id,
                    max_points=MAX_POINTS, task_title=TASK_TITLE,
                    task_description=TASK_DESC)

    rows, corpus_path, err = _load_working_corpus(submission_dir)
    n = len(rows)

    # ── 1. Winnowing log (15 pts, GATE) ──────────────────────────
    log_text = None
    log_path = None
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            lname = f.lower()
            if lname in ("winnowing_log.md", "winnowing_log.txt", "winnow_log.md"):
                log_path = os.path.join(root, f)
                break
        if log_path:
            break

    if log_path:
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as fh:
                log_text = fh.read()
        except Exception:
            log_text = ""

    if log_text and re.search(r"stage\s*1", log_text.lower()) and re.search(r"stage\s*4", log_text.lower()):
        r.add_check("Winnowing log (4-stage sieve)", 15, "PASS",
                    f"Winnowing log present with stage-1 and stage-4 entries: {os.path.basename(log_path)}",
                    is_gate=True)
        r.strengths.append("Winnowing log present with all four sieve stages")
    elif log_text:
        r.add_check("Winnowing log (4-stage sieve)", 15, "WARN",
                    "Log present but does not clearly document all four sieve stages",
                    pts_earned=8, is_gate=True)
        r.weaknesses.append("Winnowing log missing stage entries")
    else:
        r.add_check("Winnowing log (4-stage sieve)", 15, "FAIL",
                    "No winnowing_log.md / winnowing_log.txt found — GATE FAILED",
                    is_gate=True)
        r.missing.append("Winnowing log (gate failure)")

    # ── 2. Working corpus exists (10 pts) ────────────────────────
    if err:
        r.add_check("Working corpus file", 10, "FAIL", err)
        r.missing.append("Working corpus file")
    elif n == 0:
        r.add_check("Working corpus file", 10, "FAIL",
                    f"{os.path.basename(corpus_path)} has zero rows")
    else:
        r.add_check("Working corpus file", 10, "PASS",
                    f"{n} working-corpus rows in {os.path.basename(corpus_path)}")
        r.strengths.append(f"Working corpus carries {n} winnowed rows")

    # ── 3. Shape fitting (25 pts) ────────────────────────────────
    if rows:
        with_shape = sum(
            1 for row in rows
            if str(row.get("chosen_shape", "")).lower().replace(" ", "-") in VALID_SHAPES
        )
        with_sketch = sum(
            1 for row in rows
            if len(str(row.get("shape_sketch", "")).strip()) >= 80
        )
        ratio_shape = with_shape / max(1, n)
        ratio_sketch = with_sketch / max(1, n)
        if ratio_shape >= 0.95 and ratio_sketch >= 0.85:
            r.add_check("Shape fitting (chosen_shape + sketch)", 25, "PASS",
                        f"{with_shape}/{n} rows carry a valid chosen_shape; "
                        f"{with_sketch}/{n} carry a substantive sketch (≥80 chars)")
            r.strengths.append(f"Shape fitting complete on {with_shape}/{n} rows with substantive sketches")
        elif ratio_shape >= 0.75:
            r.add_check("Shape fitting (chosen_shape + sketch)", 25, "WARN",
                        f"{with_shape}/{n} have valid chosen_shape; {with_sketch}/{n} substantive sketches",
                        pts_earned=15)
            r.weaknesses.append(
                f"Shape fitting partial: {with_shape}/{n} valid shapes, "
                f"{with_sketch}/{n} substantive sketches"
            )
        else:
            r.add_check("Shape fitting (chosen_shape + sketch)", 25, "FAIL",
                        f"Only {with_shape}/{n} rows have a valid chosen_shape")
            r.weaknesses.append(f"Most rows lack a fitted shape: {with_shape}/{n}")
    else:
        r.add_check("Shape fitting (chosen_shape + sketch)", 25, "FAIL", "No rows to check")

    # ── 4. Defeater quality (15 pts) ─────────────────────────────
    if rows:
        with_defeater = sum(
            1 for row in rows
            if len(str(row.get("named_defeaters", "")).strip()) >= 60
        )
        # crude proxy for "citable" — does the defeater field mention
        # a year-style citation pattern (e.g. "(2011)")?
        with_citation = sum(
            1 for row in rows
            if re.search(r"\(\s*(19|20)\d{2}\s*\)", str(row.get("named_defeaters", "")))
        )
        ratio_def = with_defeater / max(1, n)
        ratio_cite = with_citation / max(1, n)
        if ratio_def >= 0.90 and ratio_cite >= 0.50:
            r.add_check("Defeater catalog (substantive + citable)", 15, "PASS",
                        f"{with_defeater}/{n} rows have substantive defeaters; "
                        f"{with_citation}/{n} cite a year-marked source")
            r.strengths.append(
                f"Defeater catalog substantive ({with_defeater}/{n}) "
                f"with year-marked citations on {with_citation}/{n}"
            )
        elif ratio_def >= 0.70:
            r.add_check("Defeater catalog (substantive + citable)", 15, "WARN",
                        f"{with_defeater}/{n} substantive; {with_citation}/{n} cite a year",
                        pts_earned=9)
            r.weaknesses.append("Defeater catalog thin on citations")
        else:
            r.add_check("Defeater catalog (substantive + citable)", 15, "FAIL",
                        f"Only {with_defeater}/{n} rows have substantive defeaters")
            r.weaknesses.append(f"Defeater catalog incomplete: {with_defeater}/{n}")
    else:
        r.add_check("Defeater catalog (substantive + citable)", 15, "FAIL", "No rows to check")

    # ── 5. Team fitting-critique notes (10 pts) ──────────────────
    critique_found = False
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            lname = f.lower()
            if "critique" in lname and lname.endswith((".md", ".txt")):
                critique_found = True
                break
        if critique_found:
            break

    if critique_found:
        r.add_check("Team fitting-critique notes", 10, "PASS",
                    "Team critique file present")
        r.strengths.append("Team fitting-critique milestone documented")
    else:
        r.add_check("Team fitting-critique notes", 10, "WARN",
                    "No critique file found", pts_earned=4)
        r.weaknesses.append("Team fitting-critique notes missing")

    # Repo worthiness
    if rows and n >= 25 and corpus_path:
        r.add_repo_item(os.path.basename(corpus_path), "Knowledge_Atlas",
                        "160sp/track4/student_fitting_catalogs/", "needs_review",
                        f"{n} fitted rows ready for team peer review")

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
        return f"Student submitted a working corpus of {n} rows. " + ". ".join(parts[:4]) + "."
    return "Submission incomplete — most deliverables missing."


if __name__ == "__main__":
    sub_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    sid = sys.argv[2] if len(sys.argv) > 2 else "test_student"
    print(grade(sub_dir, sid).to_markdown())
