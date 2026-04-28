# 160sp Grader Dashboard — Claude Integration Handoff

**Date**: 2026-04-27
**From**: AG (Antigravity session)
**To**: Claude (any session with repo access)
**Repo**: `/Users/davidusa/REPOS/Knowledge_Atlas/`

---

## Your Mission

You are picking up a partially-built grading system for COGS 160sp — a 10-week course with 3 student tracks, 3 tasks per track, and 675 total points. The automated autograder suite (9 Python scripts) and a Grader's Page web dashboard (HTML + Python server) have been built and committed. **Your job is to integrate this into the existing grading infrastructure** so DK can use a single, polished Grader's Page to grade, review, and manage student submissions.

---

## What Exists Right Now

### 1. Autograder Suite (BUILT, TESTED, COMMITTED)

Location: `160sp/autograders/`

```
160sp/autograders/
├── shared/
│   ├── __init__.py
│   ├── validators.py     # 237 lines — JSON, file, HTML DOM, provenance, data quality checks
│   ├── report.py         # 179 lines — GradeReport dataclass → JSON + Markdown
│   ├── ruthless.py       # 163 lines — Subprocess execution with timeout + error collection
│   └── roster.py         # 149 lines — Student roster model, CSV export
├── t1_task1_grader.py    # 239 lines — Image Collection (75 pts)
├── t1_task2_grader.py    #  62 lines — Latent Tag Detectors (75 pts, ruthless import test)
├── t1_task3_grader.py    #  76 lines — Image Viewer (75 pts)
├── t2_task1_grader.py    #  58 lines — Fix Contribute Page (75 pts)
├── t2_task2_grader.py    #  74 lines — Gap Targeting (60 pts, ruthless subprocess test)
├── t2_task3_grader.py    #  90 lines — Search Execution (75 pts, ruthless subprocess test)
├── t3_task1_grader.py    #  90 lines — Model Collection (75 pts)
├── t3_task2_grader.py    #  68 lines — VR Testing (75 pts)
├── t3_task3_grader.py    #  79 lines — AI Front-End (75 pts)
├── run_all.py            #  88 lines — CLI entry point (--track, --task, --student, --self-test)
└── roster.json           # Sample roster (4 students, 3 tracks)
```

**Self-test status**: All 9 graders pass on empty submissions (verified 2026-04-27).

**How each grader works**:
- Every grader has a `grade(submission_dir, student_id) → GradeReport` function
- The GradeReport contains: checks (criterion, points, PASS/FAIL/WARN/SKIP, detail), repo_items (flagged for integration), ruthless_comments, summary, strengths, weaknesses, missing
- The GradeReport can serialize to `.to_json()` and `.to_markdown()`
- The first check in every grader is the **CONTRACT GATE** (`is_gate=True`) — if the student didn't write contracts/success conditions, the gate fails
- 4 graders run **ruthless subprocess tests**: T1.2 (detector import), T2.2 (gap_extractor.py), T2.3 (abstract_collector.py), T3.3 (AI front-end DOM grep)

### 2. Grader's Page (BUILT, TESTED, COMMITTED)

Location: `160sp/grader_page/`

```
160sp/grader_page/
├── index.html     # 295 lines — Dark-themed dashboard (vanilla HTML/CSS/JS)
├── server.py      # 226 lines — Zero-dependency stdlib http.server backend
└── results/       # Directory for saved grade reports
```

**Current dashboard features**:
- Track selector (radio: T1/T2/T3), Task selector (radio: 1/2/3), Student dropdown
- "Grade This" button → POSTs to `/api/grade` → renders results
- Results panel: Task Question, What They Did, Critique (✅ Strong / ⚠️ Weak / ❌ Missing), Check Details table, Repo-Worthy Items (Approve/Reject/Changes buttons), Ruthless Test Output
- Class Roster table: Name, Track, Task 1/2/3 grades with status icons, Total, Email
- Export Grades CSV / Export Roster CSV buttons
- Fallback offline rendering when server isn't running

**Server endpoints**:
- `GET /` → serves index.html
- `POST /api/grade` → runs grader, saves JSON+MD reports, updates roster
- `GET /api/roster` → returns roster with grades
- `POST /api/review` → approve/reject/request-changes on repo items
- `GET /api/export/grades` → CSV download
- `GET /api/results/<student_id>` → stored reports
- `GET /api/task-info/<track>/<task>` → task title + description

**Launch**: `cd 160sp/grader_page && python3 server.py` → http://localhost:5050

### 3. Existing AI Grading Design (APPROVED, NOT YET IMPLEMENTED)

Location: `160sp/rubrics/AI_GRADING_DESIGN_2026-04-17.md` (395 lines)

This is DK's approved design for AI-assisted grading. Key points you need to know:

- **Three-criterion frame**: Completeness (counts), Quality (exemplar-anchored pairwise comparison), Reflection (specificity + cross-artefact consistency + provenance check)
- **Grade dossier**: every grading pass produces a structured markdown file at `160sp/grading/{student_id}/{deliverable_id}_{date}.md`
- **Human audit**: TA audits 20% stratified sample; divergence > 0.5 pts pauses AI grading
- **Subscription-LLM orchestration**: grader runs on DK's Claude subscription via master session dispatching subagents
- **The design references `scripts/ai_grader.py` and `ka_admin.html Grading tab`** — these do NOT exist yet. The autograder suite we built is the automated-check layer that feeds INTO this system.

### 4. TA Audit Procedures (EXISTS)

Location: `160sp/rubrics/verification/README.md` (141 lines)

Defines per-track audit procedures for the human TA. The Grader's Page roster should eventually surface the audit-sample selection.

### 5. Assignment Rubrics (EXISTS)

The master handoff with all 9 assignments:
- `160sp/rubrics/ALL_TRACKS_COMPLETE_HANDOFF.md` (3,171 lines)

Per-track rubric files:
- `160sp/rubrics/t1/T1_TASK1_IMAGE_COLLECTION_PIPELINE.md`
- `160sp/rubrics/t1/T1_TASK2_LATENT_TAG_DETECTORS.md`
- `160sp/rubrics/t1/T1_TASK3_IMAGE_VIEWER_EFFECT_BROWSER.md`
- `160sp/rubrics/t2/T2_TASK1_FIX_CONTRIBUTE_PAGE.md`
- `160sp/rubrics/t2/T2_TASK2_GAP_TARGETING.md`
- `160sp/rubrics/t2/T2_TASK3_SEARCH_EXECUTION.md`
- `160sp/rubrics/t3_new/T3_TASK1_MODEL_COLLECTION.md`
- `160sp/rubrics/t3_new/T3_ALL_TASKS_FOR_HTML_CONVERSION.md`

---

## What You Need to Do

### Priority 1: Merge the Grader's Page into the Course Dashboard

The course already has HTML pages in the Knowledge Atlas site structure. The Grader's Page needs to be integrated with:

1. **The navbar** — `ka_canonical_navbar.js` defines the site-wide navigation. Add a "Grading" link that opens the Grader's Page. This should only be visible to instructors (the page is instructor-facing, not student-facing).

2. **The existing `ka_admin.html` Grading tab concept** from the AI Grading Design. The design document (§ 12, item 6) calls for: "shows per-student per-deliverable AI scores + dossier links + appeal status." The existing Grader's Page dashboard *is* this — it just needs to be connected.

3. **Style consistency** — the Grader's Page uses a dark theme with Inter font and purple accent. Adapt this to match or complement the existing KA site style if needed, OR keep it as a standalone tool (DK's preference may vary).

### Priority 2: Connect to Real Student Data

The roster.json currently has 4 sample students. You need to:

1. **Get the real class roster** — DK should provide student names, emails, tracks, and submission directories. Update `160sp/autograders/roster.json` with real data.

2. **Set submission directories** — each student's `submission_dir` field should point to where their deliverables live (Git checkout, shared drive folder, etc.).

3. **Handle the file manifest** — students submit `git diff --name-only HEAD` and `git status --short` outputs with each assignment. The autograders check for this.

### Priority 3: Bridge to the AI Grading Design

The autograder suite handles **automated checks** (file existence, JSON schema, code compilation, DOM patterns). The AI Grading Design handles **qualitative grading** (is the reflection substantive? Is the code well-written? Are the tag judgements correct?).

These are two layers that should work together:

```
Layer 1: Autograder (automated)
  → Checks file existence, schema, counts, compilation
  → Produces GradeReport with points + pass/fail
  → Runs ruthless subprocess tests
  → Flags repo-worthy items

Layer 2: AI Qualitative Grader (the dossier system)
  → Reads the student's actual content
  → Scores Quality (exemplar-anchored) and Reflection (specificity + consistency)
  → Produces grade dossier markdown file
  → Cross-references the Layer 1 GradeReport

Grader's Page shows both layers:
  → Autograder results (what's there now)
  → Dossier content (to be added)
  → Combined score
```

To implement this bridge:

1. Add a "Dossier" section to the results panel that shows the AI-written qualitative assessment
2. The server should look for dossier files at `160sp/grading/{student_id}/` and serve them alongside the autograder report
3. The combined score should weight: autograder checks (Completeness) + AI Quality score + AI Reflection score

### Priority 4: Populate with Real Rubric Content

Each grader has `TASK_TITLE` and `TASK_DESC` constants that show in the results panel. These should be expanded to include the full rubric criteria from the assignment handoff, so the instructor sees the rubric alongside the results without needing to open a separate file.

---

## GradeReport Schema (what the Grader's Page consumes)

```json
{
  "track": "t1",
  "task": 1,
  "student_id": "smith_jane",
  "task_title": "Track 1 · Task 1: Build an Image Collection",
  "task_description": "75 points. Build a 500-image collection...",
  "max_points": 75,
  "total_earned": 58,
  "gate_passed": true,
  "graded_at": "2026-04-27T20:52:16Z",
  "summary": "Student submitted 487 images across 14 room types...",
  "strengths": ["Provenance tracking is thorough", "Rate limiting implemented"],
  "weaknesses": ["Only 487/500 images", "Missing upload zone"],
  "missing": ["No contract for Phase 3"],
  "checks": [
    {
      "criterion": "Contracts + tests",
      "earned": 20, "possible": 20,
      "result": "PASS",
      "detail": "Contract/success conditions found",
      "is_gate": true
    }
  ],
  "repo_items": [
    {
      "filename": "collection.json",
      "target_repo": "Knowledge_Atlas",
      "target_path": "160sp/data/",
      "status": "needs_review",
      "reason": "487 images, 480 with full provenance"
    }
  ],
  "ruthless_comments": ["✅ Script runs without errors", "✅ Output is valid JSON"]
}
```

---

## Repo-Worthiness Destinations

When the instructor clicks "Approve" on a repo-worthy item, the file should be copied to the target repo. Here's the mapping:

| Deliverable | Target Repo | Target Path |
|---|---|---|
| T1 image collection | `Knowledge_Atlas` | `160sp/data/` |
| T1 annotations | `Knowledge_Atlas` | `160sp/data/annotations/` |
| T1 detectors | `image-tagger` | `extractors/` |
| T1/T3 viewer apps | `Knowledge_Atlas` | `160sp/apps/` |
| T2 contribute page | `Knowledge_Atlas` | Root (PR) |
| T2 gap/query scripts | `Article_Finder` | `scripts/` |
| T2 PRISMA dashboard | `Knowledge_Atlas` | `160sp/apps/` |
| T2 accepted papers | `Article_Eater` | Waiting room |
| T3 mesh annotations | `Knowledge_Atlas` | `160sp/data/vr_models/` |
| T3 VR viewer + AI modifier | `Knowledge_Atlas` | `160sp/apps/` |
| T3 material library | `Knowledge_Atlas` | `160sp/data/materials/` |

All repos exist at `/Users/davidusa/REPOS/`:
- `Knowledge_Atlas/`
- `Article_Eater_PostQuinean_v1/`
- `Article_Finder_v3_2_3/`
- `image-tagger/`
- `Tagging_Contractor/`
- `Outcome_Contractor/`
- `atlas_shared/`

---

## How to Test

```bash
# Self-test (all 9 graders, zero deps):
cd /Users/davidusa/REPOS/Knowledge_Atlas/160sp/autograders
python3 run_all.py --self-test

# Grade one student CLI:
python3 run_all.py --track t1 --task 1 --student smith_jane --dir /path/to/submission

# Start the Grader's Page (zero deps, stdlib only):
cd /Users/davidusa/REPOS/Knowledge_Atlas/160sp/grader_page
python3 server.py
# Open http://localhost:5050

# The server uses only Python stdlib — no Flask, no pip install needed.
```

---

## Key Design Constraints

1. **Zero external dependencies** for the autograders and server. Everything runs on Python stdlib. Do not add Flask, Django, or any pip-installable dependency.

2. **Contract gate is a hard blocker**. Every assignment requires students to write contracts with Inputs/Processing/Outputs/Success Conditions BEFORE building. If the contract gate fails, the grader's report should prominently flag this.

3. **Both JSON + Markdown output**. Every grading run produces both formats. The JSON feeds the Grader's Page; the Markdown is human-readable and gets stored at `grader_page/results/{student_id}/`.

4. **Review-request flow**. The instructor can approve, reject, or request changes on each repo-worthy item. This action should be persisted in the report JSON (the current server does this via the `/api/review` endpoint).

5. **The "ruthless" subprocess tests** run student Python code with a 30-second timeout. They should NEVER execute untrusted code with elevated privileges. The ruthless runner captures stdout/stderr and checks for output file creation — it does not grant filesystem access beyond the submission directory.

---

## Files to Read (in order of importance)

1. `160sp/grader_page/index.html` — the dashboard UI (295 lines)
2. `160sp/grader_page/server.py` — the backend (226 lines)
3. `160sp/autograders/shared/report.py` — the GradeReport schema (179 lines)
4. `160sp/autograders/shared/validators.py` — all validation functions (237 lines)
5. `160sp/autograders/t1_task1_grader.py` — longest grader, good reference (239 lines)
6. `160sp/autograders/roster.json` — current roster data
7. `160sp/rubrics/AI_GRADING_DESIGN_2026-04-17.md` — the approved AI grading architecture (395 lines)
8. `160sp/rubrics/ALL_TRACKS_COMPLETE_HANDOFF.md` — all 9 assignments (3,171 lines)

Total codebase for the autograder system: **2,174 lines across 18 files**.
