# Grader Integration Reconnaissance

**Date**: 2026-04-27
**Author**: Recon agent (CW orchestration)
**Subject**: Integrating AG's `160sp/grader_page/` + `160sp/autograders/` suite into the Knowledge Atlas instructor surface, plus designing Track 4 graders against the rubrics CW just shipped.
**Source handoff**: `160sp/CLAUDE_GRADER_PAGE_HANDOFF.md`

---

## §1. Existing grader system — endpoints, schema, theme

### 1.1 HTTP endpoints (`160sp/grader_page/server.py`, stdlib `http.server`, port 5050)

| Method | Path | Purpose |
|---|---|---|
| GET  | `/` (and `/index.html`) | Serves the dashboard HTML |
| GET  | `/api/roster` | Returns `{students:[…]}` from `roster.json` (per-task status + grade + total) |
| GET  | `/api/results/<student_id>` | Returns all stored `*_report.json` files for that student |
| GET  | `/api/task-info/<track>/<task>` | Returns `{title, description, max_points}` introspected from the grader module |
| GET  | `/api/export/grades` | CSV download of the roster |
| POST | `/api/grade` | Body `{track, task, student_id, submission_dir?}` → runs grader, persists JSON+MD under `results/<student_id>/`, updates roster, returns the report |
| POST | `/api/review` | Body `{student_id, track, task, filename, action}` → mutates `repo_items[].status` to `ready` / `blocked` / `needs_review` |

The grader registry is a static dict `GRADERS = {"t1_1": "t1_task1_grader", …}` covering the existing nine modules. Adding Track 4 is a one-line-per-task change.

### 1.2 GradeReport schema (`160sp/autograders/shared/report.py`)

`GradeReport` is a `@dataclass` with fields: `track, task, student_id, max_points, task_title, task_description, checks[], repo_items[], ruthless_comments[], summary, strengths[], weaknesses[], missing[], graded_at`. Two derived properties: `total_earned` (sum over `checks`) and `gate_passed` (no `is_gate=True` check is `FAIL`). Builders: `add_check(criterion, pts_possible, result, detail, *, pts_earned=None, is_gate=False)` (defaults: PASS = full, WARN = half, FAIL = 0) and `add_repo_item(filename, target_repo, target_path, status, reason)`. `to_dict()` / `to_json()` produce the JSON the dashboard consumes; `to_markdown()` produces an H1 task title + score header, Critique list (✅/⚠️/❌), Check Details table, Repo-Worthy Items, Ruthless Test Output. The handoff document’s schema example is faithful to the dataclass.

### 1.3 Theme

`grader_page/index.html` is a self-contained dark dashboard. Palette (CSS vars): `--bg:#0f1117`, `--surface:#1a1d27`, `--surface2:#252833`, `--border:#2e3240`, `--text:#e4e6ed`, `--text2:#9ca3b4`, `--accent:#6c63ff` (purple), `--accent2:#8b83ff`, plus traffic-light `--green/--yellow/--red`. Typography: Inter 400/500/600/700 from Google Fonts. Header is a navy-violet linear gradient (`#1e1b4b → #312e81`). Score badge tints (high/mid/low) keyed off percentage. Pure vanilla HTML/CSS/JS, no framework. This contrasts deliberately with the rest of KA (paper/ink palette — see §6).

---

## §2. Navbar wiring — where to add a "Grading" link, instructor-mode status

### 2.1 The navbar already understands instructor / admin

`ka_canonical_navbar.js` already has the role plumbing (no new mode-pill needed):

- `USER_TYPES_GATED = [{id:'160-student'}, {id:'instructor'}]` (line 65–68).
- `syncCompatSessionFromLocalAuth()` at line 123 promotes a user with `role === 'instructor' || 'admin'` to `ka.admin = 'yes'` and `ka.userType = 'instructor'`. So the existing distinction is **admin** (any instructor-or-admin) vs. **student** vs. **anonymous**.
- `detectSession()` returns `{isAdmin, studentAuthed, impersonating, userType, email, authState}` where `authState ∈ {admin, student, authenticated, anonymous}`.
- `buildRight()` already renders an admin-only `★ Admin` pill linking to `ka_admin.html` (line 415–421).

The legacy KA pages also still carry an inline `<span class="mode-pill">STUDENT</span>` (e.g. `t1_submissions.html` line 23, `t4_task1.html` line 23) — that is a **static** label on the legacy `top-nav`, unrelated to the canonical navbar. It is not driven by auth state and is being retired by `retireLegacyTopNavs()` whenever `ka_canonical_navbar.js` mounts on a page.

### 2.2 Where to add the "Grading" item

The two natural insertion points, both in `REGIME_ITEMS` (lines 36–57):

1. **Inside the `'160sp'` array** — but make rendering conditional on `session.isAdmin`. Cleanest UX, since Grading lives under the 160sp regime alongside Track 1–4.

   Insertion line: between current `track4` (line 55) and the closing `]` (line 56):

   ```js
   { id:'grading', label:'Grading', href:'ka_admin.html#grading', instructorOnly:true },
   ```

   Then, in `buildLinks()` (lines 390–408), filter the items array:

   ```js
   const items = (REGIME_ITEMS[regime] || [])
     .filter(it => !it.instructorOnly || session.isAdmin);
   ```

   `buildLinks(regime, activeId)` will need to accept `session` (currently it doesn’t — it’s called from `buildNavbar` at line 466 which has `session` in scope, so threading it in is one signature change).

2. Alternatively, **leave the `★ Admin` pill as the sole instructor entrypoint** and just deep-link it to `ka_admin.html#grading`. This requires no array change but hides the Grading affordance behind the small admin pill — less discoverable for a heavy grading day.

**Recommendation**: option 1. The instructor will use this link weekly; it deserves a top-level item, gated on `session.isAdmin`. The `instructorOnly` flag is forward-compatible with future instructor-only items (e.g. Audit, Calibration).

---

## §3. `ka_admin.html` — the Grading tab already exists

**Status: file exists** at `160sp/ka_admin.html` (~1,200 lines). It is a polished tabbed admin console with Dashboard / Roster / Logins & Keys / Tracks & Deliverables / Progress / **Grading** / Announcements / Site Health / Content / Settings / Access & Roles / Archive / Audit Log tabs (lines 419–432).

The **Grading tab** (`<section id="tab-grading">`, lines 710–825) already contains:

- **Class grading summary** card with KPIs (class avg, median, high, low, dossiers on file, open appeals) and a `Run grading pass` button wired to a no-op `runGradingPass()` JS stub (line 722).
- **Per-student totals** table (`#gradingTable`, columns: Student, Track, A0/5, A1/5, Track/75, F160/15, Total/100, Last AI pass, Audit, Conf., action) — currently filled from a `DEMO_GRADING` constant via `kaApiGet('/grading', DEMO_GRADING)`.
- **Calibration health** table (κ Comp / κ Qual / κ Refl per deliverable).
- **Audit queue** table (stratified 20% sample).
- **Open appeals** table (two-stage resolution).

So the Grading-tab concept is already **fully scaffolded** (UI + endpoints stubbed at lines 1287–1298). What is missing is the wiring to AG’s real backend.

### 3.1 Recommended integration shape

Do **not** create a new file. Augment the existing `tab-grading` panel with a new sub-card titled "Live grader" that hosts the AG dashboard. Two options:

- **Option A (lowest friction): iframe embed.** Add `<iframe src="http://localhost:5050/" style="width:100%; height:1400px; border:0; border-radius:8px;"></iframe>` inside `tab-grading` after the existing cards. Works the moment `python3 server.py` is running. The dark theme inside the iframe will visually contrast with the surrounding KA admin chrome — see §6.
- **Option B (deeper integration): replace stubs with real fetches.** Point `kaApiGet('/grading', …)` etc. at the AG endpoints (`/api/roster`, `/api/grade`, `/api/review`). This avoids the iframe but requires reskinning AG’s result-rendering (currently only inside its own `index.html`) for embedding into the KA card layout.

Given the handoff’s explicit ask ("a single, polished Grader’s Page to grade, review, and manage student submissions") and AG’s page already being polished, **Option A is the right first move** — ship in one commit, then later promote selected widgets (per-student totals, calibration table) into native KA cards if DK wants tighter integration.

A new `ka_admin.html` is **not** needed and would duplicate the Grading-tab work that already exists. Do not create one.

---

## §4. Submissions page link plan — converting `Comments & critique` cells to live links

### 4.1 Current pattern (verified in t1/t2/t3/t4 submissions)

Every `t{N}_submissions.html` uses the same table structure:

```html
<table class="data-table" data-submission-table="track1">
  …
  <tr>
    <td><strong>Task 1:</strong> <a href="t1_task1.html">…</a> <div class="row-meta">75 points</div></td>
    <td class="cell-empty" data-field="submitted_at">&mdash;</td>
    <td class="cell-empty" data-field="grade">&mdash;</td>
    <td class="cell-empty" data-field="critique_link">&mdash;</td>
  </tr>
  …
</table>
```

The `data-submission-table="trackN"` attribute and the `data-field="critique_link"` cell are stable hooks — there is no JS file populating them today (verified by Grep — they only exist as static markup), so a single new script can own them.

### 4.2 Recommended pattern

Two cells need to become live: the **grade** cell (number with color-coded score badge) and the **critique_link** cell (link to the grader page filtered for this student × track × task).

Static-HTML version of the link cell, keyed off the canonical KA login (the page already knows the student via `ka.studentEmail` in sessionStorage):

```html
<td data-field="critique_link">
  <a class="btn-link"
     href="ka_admin.html#grading?student={{student_id}}&track=t1&task=1">
    View critique
  </a>
</td>
```

…where `{{student_id}}` resolves at page load via a small inline `_track_submissions.js` that:

1. Reads `sessionStorage.getItem('ka.studentEmail')`, derives `student_id` (lookup against roster).
2. `fetch('/api/results/' + student_id)` against the AG server (or a JSON mirror at `160sp/grader_page/results/<sid>/`).
3. For each task row in the table: populates `submitted_at`, color-codes `grade`, and rewrites `critique_link` to the `ka_admin.html#grading?student=…&track=…&task=…` URL above.

`ka_admin.html`’s Grading tab JS then needs a single `URLSearchParams` reader at tab-open time that auto-selects the right student/track/task and POSTs to `/api/grade`, mirroring the dashboard’s `runGrade()` (`grader_page/index.html` line 176). When the iframe is in use (Option A in §3), the same query string can be passed straight through: `<iframe src="http://localhost:5050/?student=…&track=…&task=…">` and `index.html`'s init code reads them.

This makes the cell a true round-trip: student sees a "View critique" link → clicks → the grader opens, runs (or shows the cached report), and the instructor (or student, if we ever expose read-only) sees the full critique. For students, only the read-only summary needs to surface — the Approve/Reject repo-item buttons should be hidden when `session.userType !== 'instructor'`.

---

## §5. Track 4 grader design — three new Python modules

Track 4 differs from Tracks 1–3 in being **mostly paper artefacts** (spreadsheet, markdown methods file, fitting catalog, two-page reflection) plus one HTML prototype in T4.3. The autograders will therefore be heavier on file-shape + field-presence checks and ruthless content-grep checks, lighter on subprocess execution.

All three follow `t1_task1_grader.py`’s pattern: module-level `TASK_TITLE`, `TASK_DESC`, `MAX_POINTS = 75`; a single `grade(submission_dir, student_id) → GradeReport` function; first check is the **CONTRACT GATE** (`is_gate=True`); CLI entrypoint at the bottom prints `report.to_markdown()`. Repo-worthy items flagged via `r.add_repo_item(filename, target_repo, target_path, status, reason)` — Track 4 destinations are all `Knowledge_Atlas` under `160sp/track4_corpora/` (corpora) and `160sp/apps/` (prototype HTML).

### 5.1 `t4_task1_grader.py` — Persona Question Corpus (75 pts)

- **TASK_TITLE**: `"Track 4 · Task 1: Build a Persona Question Corpus"`
- **TASK_DESC**: `"75 points. 40–60 questions for one persona, with adequacy_condition, cognitive_purpose, answer_shape, evidential_demand, persona_fit, theoretical_commitment, source, provenance fields. Three sources: LLM panels, literature mining (PNU templates), cross-product synthesis. Plus a methods file documenting panel configurations and known limitations."`
- **Contract gate (20 pts)**: same walk-the-tree text-grep for `success condition` / `contract` as T1.1, plus require a `methods.md` (or equivalent) with the substring `panel configuration`. Without it, gate FAILS.
- **Substantive checks** (per the rubric on `t4_task1.html` lines 264–276):
  1. **Coverage (20 pts)** — load corpus (`questions.csv`/`.json`/`.xlsx`), count rows; PASS if 40–60 with ≥5 per declared sub-flavour and ≥3 questions in each of the four cross-product corners (low/low, low/high, high/low, high/high). WARN if 30–39 rows or one sub-flavour < 5. FAIL < 30.
  2. **Tagging quality (20 pts)** — every row must have all five required tag axes populated and use the rubric’s controlled vocabulary (`{information-seeking, inquiry, deliberation, persuasion, discovery}` for `cognitive_purpose`; `{Toulmin, field-map, procedure, contrast-pair, ranked-brief}` for `answer_shape`; `{suggestive, converging, mechanistic, causal-with-mechanism, measurement-grade}` for `evidential_demand`). Reject free-text in those columns.
  3. **Adequacy conditions (15 pts)** — every row has a non-empty `adequacy_condition`; flag rows whose adequacy condition is shorter than 40 chars (likely "I'll know it when I see it") as WARN.
  4. **Provenance (10 pts)** — every row has non-empty `source` ∈ `{panel, mining, cross-product}` and non-empty `provenance` (panel run ID, template ID, or hierarchy coords).
  5. **Honest documentation (10 pts)** — `methods.md` (or `methods.txt`) exists and contains substrings: `panel`, `mining`, `limitation` (case-insensitive). PASS only if all three. WARN if methods file exists but missing one term.
- **Repo item**: if the corpus passes Coverage + Tagging + Adequacy, flag `questions.json` as `needs_review` → `Knowledge_Atlas` / `160sp/track4_corpora/<student_id>/`.

### 5.2 `t4_task2_grader.py` — Winnow & Fit Answer Shapes (75 pts)

- **TASK_TITLE**: `"Track 4 · Task 2: Winnow and Fit Answer Shapes"`
- **TASK_DESC**: `"75 points. Three-stage extension to the Task-1 corpus: (A) winnowing log with per-stage attrition counts and a backlog file; (B) every surviving question fitted to one of five canonical answer shapes with a one-paragraph shape sketch; (C) every surviving question carries at least one strong (citable) defeater per the four-question heuristic."`
- **Contract gate (15 pts)**: file `winnowing_log.md` (or `.json`) exists AND contains the substrings `Deduplicate`, `Adequacy gate`, `Persona-fit gate`, `Coverage balance` AND has at least one numeric attrition count (regex `\d+\s*%` or `\d+\s*→\s*\d+`). Without the log, gate FAILS — the rubric makes the log itself a deliverable ("a Codebook Custodian who hides the dropped items hides the team's quality control").
- **Substantive checks** (rubric on `t4_task2.html` lines 244–256):
  1. **Winnowing rigour (15 pts)** — counts at all four stages, backlog file present, gaps acknowledged. FAIL if log lacks counts; WARN if backlog file missing.
  2. **Shape fitting (25 pts)** — load fitted corpus; every surviving row has `chosen_shape` ∈ the five canonical shapes (composites flagged with `+`, e.g. `field-map+Toulmin`, are PASS); `shape_sketch` field is non-empty and ≥120 chars; rows where `shape_sketch` ≤ 60 chars are WARN ("label not sketch").
  3. **Defeater quality (25 pts)** — every row has a `defeaters` field with ≥1 entry; each entry has at least one of `{citation, doi, author_year}` populated (citable = strong); rows with only invented defeaters (no citation field) trigger WARN. FAIL if any row has zero defeaters.
  4. **Honesty about uncertainty (10 pts)** — corpus contains a `confidence` or `under_supported` flag column AND at least 5% of rows carry a low-confidence flag (a corpus that admits no uncertainty is suspicious; mirrors the rubric’s "honest about uncertainty" criterion).
- **Repo item**: `fitted_corpus.json` → `Knowledge_Atlas` / `160sp/track4_corpora/<student_id>/`, status `needs_review` if all four checks pass.

### 5.3 `t4_task3_grader.py` — Prototype an Evidential Journey (75 pts)

- **TASK_TITLE**: `"Track 4 · Task 3: Prototype an Evidential Journey"`
- **TASK_DESC**: `"75 points. Three artefacts: (a) one working journey prototype (HTML, no back-end) with landing page, populated answer-shape diagram, exposed Chinn-Brewer rebuttal panel, reader-response stage; (b) LLM-panel reader-test transcripts (3–5 readers); (c) a two-page academic-prose reflection."`
- **Contract gate (10 pts)**: at least one HTML file present in submission AND one `reader_test*.{md,json,txt}` file AND `reflection.md` (or `.docx`) AND that reflection is ≥1500 chars. Missing any → gate FAILS.
- **Substantive checks** (rubric on `t4_task3.html` lines 187–199):
  1. **Working prototype (30 pts)** — primary HTML file (named per a small list: `journey*.html`, `prototype*.html`, `index.html` under a `prototype/` dir) loads with BeautifulSoup-free DOM keyword grep using `validators.check_html_has_keyword`. PASS requires ≥4 of: a `<form>` or input on landing page; a `<svg>` or grid container (the answer-shape diagram); a `<details>` / `.rebuttal` / `chinn` substring (the rebuttal panel exposed by default — check it is NOT inside `<details closed>` or behind `display:none`); a `response` form/select; a footer linking back into the Atlas. WARN if 2–3, FAIL if ≤1.
  2. **Rebuttal economy (15 pts)** — HTML must contain at least one of `chinn-brewer`, `chinn_brewer`, `rebuttal-panel` substring AND the prototype's defeater text matches one of the defeaters from this student's Task-2 `fitted_corpus.json` (cross-reference). PASS if matched defeater present, WARN if rebuttal panel present but no Task-2 defeater echo, FAIL if no rebuttal markup at all.
  3. **LLM-panel reader test (15 pts)** — reader-test file exists, has 3–5 distinct reader sections (count separators or JSON entries), every reader section mentions: where the reader stopped, which Chinn-Brewer response was taken, what would have improved adequacy. WARN if 1–2 readers; FAIL if file missing.
  4. **Reflection (10 pts)** — `reflection.md` length 1500–6000 chars (two-page guideline ≈ 4000); regex check for at least one uncertainty hedge (`uncertain|ambiguous|don't know|would change|in retrospect`). WARN if uncertainty hedge absent (rubric: "a reflection that admits no uncertainty is read as either dishonest or insufficiently reflective").
  5. **Site integration (5 pts)** — HTML contains references to `_track_pages_shared.css` OR includes a `top-nav` / `breadcrumb` / `side-nav` / `site-footer` substring. PASS if 2+, WARN if 1.
- **Ruthless test**: optional — open prototype HTML files with Python's `http.server` in a subprocess for ≤10s and `urllib.request` GET each file; report HTTP status and any crash. Mirrors T2.2 / T2.3 / T3.3 ruthless pattern.
- **Repo item**: if checks 1 + 2 pass, flag the prototype directory as `needs_review` → `Knowledge_Atlas` / `160sp/apps/track4_<student_id>/`.

### 5.4 Wiring into server

Three lines in `server.py` `GRADERS` dict (line 33–37):

```python
"t4_1": "t4_task1_grader",
"t4_2": "t4_task2_grader",
"t4_3": "t4_task3_grader",
```

Plus add a Track 4 radio in `index.html` `#trackSelect` (line 73–77) and update the `MAX_POINTS = 4 × 225 = 900` in any handoff documentation. Roster `students[].track` must support `"t4"`. Verify with `python3 run_all.py --self-test`.

---

## §6. Style consistency — keep grader theme standalone

**Recommendation: keep AG’s dark/Inter/purple grader page as a standalone tool, embed via iframe into `ka_admin.html`’s Grading tab; do not restyle.**

Reasons:

1. **Audience and use mode are different.** KA pages (`--ka-cream:#F7F4EF`, navy nav, paper-and-ink aesthetic — see `ka_canonical_navbar.js` lines 217–221) are for browsing knowledge slowly, with calm contrast. The grader is a high-throughput tool used in 30-minute grading bursts. A dark, dense, color-coded dashboard is the right ergonomics for that mode — the same reason developer tools, log viewers, and CI dashboards all run dark.

2. **Visual signal of role.** The dark surface inside the KA admin frame instantly tells the instructor "you are now in tooling, not in the public site." A full restyle to the cream KA palette would lose that signal and risk an instructor confusing a grading view with a student-facing page during screen-shares or office hours.

3. **Cost of restyling.** AG already shipped a working, polished page in 295 lines. A cream/serif restyle would not just swap CSS variables — score badges, gate-pass/fail color semantics, and the surface2/border layering all rest on the dark palette. Restyling would be a 2–3 hour rewrite for a result that would clash with the rest of the admin tooling philosophy.

4. **Compromise — minimal chrome touches.** Two small adjustments would reconcile the embedded look without a full restyle: (a) replace the Inter font import with `system-ui, -apple-system, "Segoe UI"` to match the navbar font stack and avoid the network round-trip; (b) replace the purple-violet header gradient with the KA navy `#1C3D3A → #2A7868` gradient so the header band feels related to the parent page even when the body stays dark. These are six lines of CSS in `index.html` and preserve all the dashboard ergonomics.

If DK later wants a fully native KA look (e.g. for student read-only critique views), the right move is a separate slim component — not a wholesale restyle of the grader.

---

**Word count**: ~2,400.

**Files referenced** (all absolute paths under `/Users/davidusa/REPOS/Knowledge_Atlas/`):

- `160sp/CLAUDE_GRADER_PAGE_HANDOFF.md`
- `160sp/grader_page/index.html`, `160sp/grader_page/server.py`
- `160sp/autograders/shared/report.py`, `160sp/autograders/t1_task1_grader.py`
- `ka_canonical_navbar.js`
- `160sp/ka_admin.html` (Grading tab at lines 710–825)
- `160sp/t1_submissions.html`, `t2_submissions.html`, `t3_submissions.html`, `t4_submissions.html`
- `160sp/t4_task1.html`, `t4_task2.html`, `t4_task3.html`
