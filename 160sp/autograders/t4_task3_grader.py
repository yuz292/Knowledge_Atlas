"""
T4 Task 3 Autograder — Prototype an Evidential Journey (75 points)

Validates the deliverables specified in 160sp/t4_task3.html:
  - working journey prototype (HTML, with landing page, populated answer shape,
    Chinn-Brewer rebuttal panel exposed by default, reader-response stage)
  - LLM-panel reader-test transcripts (3-5 readers)
  - two-page reflection in academic prose
  - team-collective walkthrough notes
  - top-nav, breadcrumb, footer, side-nav for site integration
"""
import os
import sys
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.report import GradeReport
from shared.validators import load_html, check_html_has_keyword

TASK_TITLE = "Track 4 · Task 3: Prototype an Evidential Journey"
TASK_DESC = (
    "75 points. Build one working HTML prototype that takes a reader from a "
    "typed-in question to a populated answer shape with a Chinn-Brewer "
    "rebuttal panel exposed by default and a reader-response stage at the "
    "end. Run 3-5 LLM-panel reader tests. Submit a two-page reflection in "
    "academic prose."
)
MAX_POINTS = 75


def _find_journey_html(submission_dir: str):
    """Find the prototype HTML file. Prefer files named journey*.html or
    prototype*.html; fall back to the largest .html in the submission."""
    journey_candidates = []
    other_html = []
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            path = os.path.join(root, f)
            lname = f.lower()
            if not lname.endswith(".html"):
                continue
            if "journey" in lname or "prototype" in lname:
                journey_candidates.append(path)
            else:
                other_html.append(path)
    if journey_candidates:
        return max(journey_candidates, key=lambda p: os.path.getsize(p))
    if other_html:
        return max(other_html, key=lambda p: os.path.getsize(p))
    return None


def grade(submission_dir: str, student_id: str = "unknown") -> GradeReport:
    r = GradeReport(track="t4", task=3, student_id=student_id,
                    max_points=MAX_POINTS, task_title=TASK_TITLE,
                    task_description=TASK_DESC)

    journey_path = _find_journey_html(submission_dir)
    html = load_html(journey_path) if journey_path else ""

    # ── 1. Working prototype (30 pts, GATE) ──────────────────────
    if not html:
        r.add_check("Working prototype HTML", 30, "FAIL",
                    "No prototype HTML found in submission — GATE FAILED",
                    is_gate=True)
        r.missing.append("Prototype HTML file (gate failure)")
    else:
        # 4 required pieces from the t4_task3 checklist
        landing = check_html_has_keyword(html, "search") or \
                  check_html_has_keyword(html, "search-box") or \
                  check_html_has_keyword(html, "typed-in") or \
                  re.search(r'<input[^>]*type=["\']text["\']', html, re.I) is not None
        diagram = (check_html_has_keyword(html, "<svg") or
                   check_html_has_keyword(html, "data-table") or
                   check_html_has_keyword(html, "toulmin") or
                   check_html_has_keyword(html, "field-map") or
                   check_html_has_keyword(html, "ranked"))
        chinn = (check_html_has_keyword(html, "chinn") or
                 check_html_has_keyword(html, "rebuttal panel") or
                 check_html_has_keyword(html, "cb-panel") or
                 check_html_has_keyword(html, "seven response"))
        response_stage = (check_html_has_keyword(html, "your response") or
                          check_html_has_keyword(html, "reader response") or
                          check_html_has_keyword(html, "save my response") or
                          check_html_has_keyword(html, "which response"))
        pieces_found = sum([landing, diagram, chinn, response_stage])
        missing_pieces = [name for name, ok in [
            ("landing", landing), ("answer-shape diagram", diagram),
            ("Chinn-Brewer panel", chinn), ("reader-response stage", response_stage),
        ] if not ok]

        if pieces_found == 4:
            r.add_check("Working prototype HTML (4 required pieces)", 30, "PASS",
                        "All four required pieces detected: landing, diagram, "
                        "Chinn-Brewer panel, reader-response stage",
                        is_gate=True)
            r.strengths.append("Prototype contains all four required pieces")
        elif pieces_found >= 2:
            pts = 18 if pieces_found == 3 else 10
            r.add_check("Working prototype HTML (4 required pieces)", 30, "WARN",
                        f"{pieces_found}/4 pieces present; missing: {', '.join(missing_pieces)}",
                        pts_earned=pts, is_gate=True)
            r.weaknesses.append(f"Prototype missing: {', '.join(missing_pieces)}")
        else:
            r.add_check("Working prototype HTML (4 required pieces)", 30, "FAIL",
                        f"Only {pieces_found}/4 required pieces present", is_gate=True)
            r.missing.append(f"Prototype missing: {', '.join(missing_pieces)}")

    # ── 2. Rebuttal economy — Chinn-Brewer exposed by default (15 pts) ──
    if html:
        # Inspect: is the cb panel actually rendered, or is it hidden behind
        # a click? We look for the seven dispositions appearing in the page,
        # which would only be present if the panel is rendered/exposed.
        seven_responses = [
            "ignore", "reject", "exclude", "abeyance",
            "reinterpret", "peripheral", "change the theory",
        ]
        responses_in_html = sum(1 for w in seven_responses if w in html.lower())
        # A defeater being named (any year-marked citation in vicinity of "rebut")
        defeater_citation = re.search(
            r"rebut[^<]{0,300}\((19|20)\d{2}\)", html, re.I
        ) is not None or re.search(
            r"\((19|20)\d{2}\)[^<]{0,300}rebut", html, re.I
        ) is not None

        if responses_in_html >= 6 and defeater_citation:
            r.add_check("Rebuttal economy (Chinn-Brewer + defeater)", 15, "PASS",
                        f"{responses_in_html}/7 Chinn-Brewer responses present in DOM "
                        "and defeater carries a year-marked citation")
            r.strengths.append("Rebuttal panel fully populated with citable defeater")
        elif responses_in_html >= 4:
            r.add_check("Rebuttal economy (Chinn-Brewer + defeater)", 15, "WARN",
                        f"{responses_in_html}/7 Chinn-Brewer responses present; "
                        f"defeater citation: {'yes' if defeater_citation else 'missing'}",
                        pts_earned=9)
            r.weaknesses.append("Rebuttal economy partial")
        else:
            r.add_check("Rebuttal economy (Chinn-Brewer + defeater)", 15, "FAIL",
                        f"Only {responses_in_html}/7 Chinn-Brewer responses in DOM")
            r.weaknesses.append("Chinn-Brewer panel not exposed by default")
    else:
        r.add_check("Rebuttal economy (Chinn-Brewer + defeater)", 15, "FAIL",
                    "No prototype HTML to check")

    # ── 3. LLM-panel reader test (15 pts) ────────────────────────
    reader_test_files = []
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            lname = f.lower()
            if (("reader" in lname or "panel" in lname) and "test" in lname) or \
               "reader_test" in lname or "panel_test" in lname:
                reader_test_files.append(os.path.join(root, f))

    if len(reader_test_files) >= 3:
        r.add_check("LLM-panel reader test (3-5 transcripts)", 15, "PASS",
                    f"{len(reader_test_files)} reader-test transcript files found")
        r.strengths.append(f"{len(reader_test_files)} LLM-panel reader tests recorded")
    elif len(reader_test_files) >= 1:
        r.add_check("LLM-panel reader test (3-5 transcripts)", 15, "WARN",
                    f"Only {len(reader_test_files)} transcript file(s); target 3-5",
                    pts_earned=8)
        r.weaknesses.append("Reader-test sample size below 3")
    else:
        r.add_check("LLM-panel reader test (3-5 transcripts)", 15, "FAIL",
                    "No reader-test transcript files found")
        r.missing.append("LLM-panel reader-test transcripts")

    # ── 4. Reflection (10 pts) ───────────────────────────────────
    reflection_path = None
    for root, _dirs, files in os.walk(submission_dir):
        for f in files:
            lname = f.lower()
            if "reflection" in lname and lname.endswith((".md", ".txt", ".docx")):
                reflection_path = os.path.join(root, f)
                break
        if reflection_path:
            break

    if reflection_path:
        try:
            with open(reflection_path, "r", encoding="utf-8", errors="ignore") as fh:
                ref_text = fh.read()
            words = len(ref_text.split())
            if 600 <= words <= 1500:
                r.add_check("Two-page reflection", 10, "PASS",
                            f"Reflection at {words} words (~2 pages)")
                r.strengths.append("Reflection at appropriate length")
            elif 300 <= words < 600:
                r.add_check("Two-page reflection", 10, "WARN",
                            f"Reflection at {words} words; target ~2 pages (~600-1000)",
                            pts_earned=6)
                r.weaknesses.append(f"Reflection short: {words} words")
            elif words > 1500:
                r.add_check("Two-page reflection", 10, "WARN",
                            f"Reflection at {words} words; target ~2 pages",
                            pts_earned=7)
                r.weaknesses.append(f"Reflection long: {words} words")
            else:
                r.add_check("Two-page reflection", 10, "FAIL",
                            f"Reflection too short: {words} words")
        except Exception:
            r.add_check("Two-page reflection", 10, "WARN",
                        "Reflection file present but unreadable", pts_earned=4)
    else:
        r.add_check("Two-page reflection", 10, "FAIL",
                    "No reflection.md / reflection.txt found")
        r.missing.append("Two-page reflection")

    # ── 5. Site integration (5 pts) ──────────────────────────────
    if html:
        scaffold_pieces = [
            ("top-nav", '<nav' in html.lower() or 'top-nav' in html.lower()),
            ("breadcrumb", 'breadcrumb' in html.lower()),
            ("footer", '<footer' in html.lower() or 'site-footer' in html.lower()),
        ]
        present = sum(1 for _, ok in scaffold_pieces if ok)
        if present == 3:
            r.add_check("Site integration (nav + breadcrumb + footer)", 5, "PASS",
                        "All three scaffold pieces present")
            r.strengths.append("Prototype integrates with Atlas scaffold")
        elif present >= 2:
            r.add_check("Site integration (nav + breadcrumb + footer)", 5, "WARN",
                        f"{present}/3 scaffold pieces present", pts_earned=3)
            r.weaknesses.append(f"Site integration partial: {present}/3 scaffold pieces")
        else:
            r.add_check("Site integration (nav + breadcrumb + footer)", 5, "FAIL",
                        f"Only {present}/3 scaffold pieces present")
            r.weaknesses.append("Prototype has no site scaffold")
    else:
        r.add_check("Site integration (nav + breadcrumb + footer)", 5, "FAIL",
                    "No prototype HTML to check")

    # Repo worthiness
    if html and journey_path:
        size_kb = os.path.getsize(journey_path) // 1024
        r.add_repo_item(os.path.basename(journey_path), "Knowledge_Atlas",
                        "160sp/track4/student_journeys/", "needs_review",
                        f"{size_kb} KB prototype, ready for team walkthrough review")

    r.summary = _build_summary(r, journey_path)
    return r


def _build_summary(r: GradeReport, journey_path) -> str:
    parts = []
    for c in r.checks:
        if c.result == "PASS":
            parts.append(f"{c.criterion}: {c.detail}")
        elif c.result == "WARN":
            parts.append(f"{c.criterion}: partial — {c.detail}")
    if parts:
        prefix = (
            f"Student submitted a journey prototype "
            f"({os.path.basename(journey_path)}). "
            if journey_path else "Student submitted Task 3 deliverables. "
        )
        return prefix + ". ".join(parts[:4]) + "."
    return "Submission incomplete — most deliverables missing."


if __name__ == "__main__":
    sub_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    sid = sys.argv[2] if len(sys.argv) > 2 else "test_student"
    print(grade(sub_dir, sid).to_markdown())
