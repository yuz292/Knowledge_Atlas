# Session report for Codex review — 2026-04-18

*Session owner*: CW (Claude Code)
*Reviewer*: Codex
*Commits awaiting `git push origin master`*: **14**
*Remote*: `https://github.com/dkirsh/Knowledge_Atlas.git`
*Branch*: `master`
*Last-pushed commit*: `c10015d` (2026-04-17, "Global page canonicalisation…")
*Head*: `9408a6e`

This report is a self-contained account of what landed in the 14 commits that sit ahead of `origin/master`. It is written so that Codex can review without needing to walk the full commit history or reconstruct motivation from diffs alone. The report is organised around deliverables, not commits, because several commits span multiple concerns.

---

## 1. Executive summary

Over the session, five substantive pieces of work were completed and committed locally, plus one content-restoration commit and three documentation commits. In order of load-bearing importance:

1. **A complete rubric and AI-grading system for COGS 160 Spring 2026** — 40 rubric files covering every deliverable, an AI-grading design doc (371 lines, nine peer-reviewed references), a subscription-LLM-compatible orchestrator (`scripts/ai_grader.py`), an eGrades CSV exporter (`scripts/export_egrades.py`), a grading-prompt template, and run-pass instructions. Zero API calls anywhere — all grading runs on DK's Claude subscription via Task/Agent dispatch from a master Cowork session.
2. **A class-state database backend** — 230-line SQLite migration adding ten tables plus a `student_totals_v` view to `data/ka_auth.db`; a 290-line idempotent seeder; a 310-line FastAPI server exposing `/api/admin/class/*`; and a dual-write shim in `ka_admin.html` that falls back to demo data when the backend is offline. Applied to the real `data/ka_auth.db` with a safety backup.
3. **Thirteen T1.5 domain-theory pages** — one flagship page (ART, Attention Restoration Theory: 300-word summary + 1,500-word deep dive + 10 references) and twelve panel-review stubs with real references and 150–250-word summaries. Generator-driven from `data/t15_theories.json` so iteration does not require HTML edits.
4. **A Grading tab on `ka_admin.html`** — KPI cards, per-student totals, calibration-health table, audit queue, and open appeals with two-stage (2nd-AI + human) resolution.
5. **A restored-to-production `ka_contribute.html`** — the earlier 767→346-line redesign was a regression; the xrlab production version is now canonical locally, with the canonical navbar swapped in and the COGS-160-student callout removed per DK's directive that the general public contribute page should not carry class-specific content.

In addition, three policy clarifications from DK (2026-04-17/18) were encoded into the design docs: no cohort rollover between offerings; grading runs on the subscription, not the Anthropic API; end-of-quarter records retained on a 5TB external disk with manual destruction on July 1 of year 6.

Nothing in the 14 commits touches student personal data (the demo roster is fictional), credentials (all secrets are in `.gitignore`), or anything requiring external-auth. The migration is idempotent and additive — no destructive statements on pre-existing tables.

---

## 2. Commits in order (oldest first)

```
03fafcf  Assignment rubrics audit: honest finding is no rubrics exist; propose scaffold
e14066a  Restore ka_contribute.html to the xrlab-production two-path design + adopt canonical navbar
0e365f0  Rubric scaffold for COGS 160sp with AI-primary grading design
f844e88  Add Grading tab to ka_admin.html
84cbfbb  T1.5 domain-theory pages (13) — one full, twelve panel-review stubs
b09808e  Class-state database design — proposal (DK 2026-04-17)
40f187b  AI grader + eGrades exporter + policy clarifications per DK 2026-04-17/18
9408a6e  Class-state backend: SQL migration, seeder, FastAPI, admin dual-write
```

Eight of the fourteen are above. Six earlier commits in the window (`dfb2144`, `4783a26`, `70e6bd8`, `d5720e8`, `c10015d`, `270671b`) predate this session and are the site-validator + canonical-nav migration work that was already done before the rubric system. Codex should focus on the eight listed above; the earlier six are just the runway that set up the current work.

---

## 3. The AI-grading and rubric system

### 3.1 What exists

Under `160sp/rubrics/` there are 40 files covering:

| Scope | Files |
|---|---|
| Canonical framework | `README.md`, `AI_GRADING_DESIGN_2026-04-17.md`, `grading_sheet_template.md` |
| Common deliverables (5 pts each) | `common/a0.md`, `common/a1.md` |
| Track 1 (75 pts across 7 deliverables) | `t1/README.md` + seven `T1.a`–`T1.g` files |
| Track 2 (75 pts) | `t2/README.md` + seven `T2.a`–`T2.g` files |
| Track 3 (75 pts, VR) | `t3/README.md` + seven `T3.a`–`T3.g` files |
| Track 4 (75 pts, UX) | `t4/README.md` + seven `T4.a`–`T4.g` files |
| Work-on-160F (15 pts) | `f160/README.md` |
| TA audit procedures | `verification/README.md` |
| Grading prompt template | `prompts/grading_prompt_template.md` |

Every per-deliverable rubric carries a `## Machine-readable spec` YAML block that the grading agent reads literally (thresholds, exemplar paths, consistency-check protocols). The top-level allocation is **5 A0 + 5 A1 + 75 Track + 15 Work-on-160F = 100** points for the whole class, per DK's 2026-04-17 decision. Within a track, points are hardness-weighted rather than uniform per week (T1.e/T1.f/T2.d/T2.f/T3.e/T4.c are 15 points; T*.a is 5 points).

### 3.2 The design document

`160sp/rubrics/AI_GRADING_DESIGN_2026-04-17.md` (371 lines) is the load-bearing design. It covers: (a) what the grader evaluates and the five evidence types it reads; (b) how each of the three criteria — Completeness, Quality, Reflection — is operationalised into machine-checkable sub-signals (exemplar-anchored pairwise comparison for Quality, three-sub-check for Reflection with specificity / cross-artefact / provenance); (c) the grade-dossier schema every pass produces; (d) calibration with κ ≥ {0.70, 0.65, 0.55} gates per criterion before grading is authorised; (e) weekly stratified 20% TA audit; (f) two-stage appeal (second AI grader with different seed → human adjudication on ≥1-band disagreement); (g) staged rollout in four phases. Nine peer-reviewed citations anchor the design (Kortemeyer 2023, Kim et al. 2024, Mizumoto & Eguchi 2023, Liu et al. 2023, Zheng et al. 2023, Yancey et al. 2023, Tyser et al. 2024, Schneider et al. 2023, plus Brookhart and Wiggins on rubric theory).

§10 of the design was rewritten in commit `40f187b` to reflect DK's constraint that the grader runs on a Claude subscription, not the API. The architectural consequence is that per-dossier cost is zero marginal and the orchestration becomes Python-builds-briefings + subscription-LLM-dispatches-subagents.

### 3.3 The orchestrator

`scripts/ai_grader.py` (442 lines) is a pure-Python CLI with five subcommands:

```
python3 scripts/ai_grader.py queue [--student sNN] [--deliverable T1.b] [--force]
python3 scripts/ai_grader.py status
python3 scripts/ai_grader.py next
python3 scripts/ai_grader.py dispatch N
python3 scripts/ai_grader.py complete sNN T1.b
```

`queue` scans the demo roster against every deliverable and writes one self-contained "briefing" Markdown file per ungraded submission into `160sp/grading/queue/`. A briefing embeds the full rubric, the machine-readable spec, the student's prior-submission reference paths, the canonical grading prompt, and the exact dossier output path. `dispatch N` atomically moves the first N briefings into `in_progress/` for subagent pickup. `complete` verifies the subagent wrote a dossier and archives the briefing to `done/`.

The companion `scripts/run_grading_pass.md` documents the exact prompt DK pastes into a Cowork or Claude Code master session to drive a full pass end-to-end, including the 8-way parallel Task/Agent dispatch pattern.

### 3.4 The eGrades exporter

`scripts/export_egrades.py` (200 lines) reads the per-student dossier tree and emits a UCSD-eGrades-compliant CSV (UTF-8 with CRLF line endings — eGrades rejects LF-only files). Supports `--dry-run` preview, `--letter-grades` for the UC A+…F scale with customisable `--cutoffs`, `--out` for writing to the 5T backup disk, and auto-logs every export to `160sp/grading/archive/EXPORT_LOG.md`. Smoke-tested with 15 demo students; the demo totals are all zero because no dossiers exist yet.

### 3.5 Smoke-test evidence

```
$ python3 scripts/ai_grader.py queue --student s01 --deliverable A0
Queued 1 new briefings.  Skipped 0 already-present.
$ python3 scripts/ai_grader.py status
queue:       1
in_progress: 0
done:        0
$ python3 scripts/export_egrades.py --offering cogs160sp26 --dry-run --letter-grades
(produces 15-row preview table with all totals at 0, letter grade F)
```

### 3.6 What Codex should check

1. **Exemplar-path claims in the YAML specs.** Every `quality.exemplars` block in the per-deliverable rubrics points at `{track}/exemplars/{deliverable_id}_band{n}.md`. **These exemplar files do not yet exist.** They are a Week-3 track-lead deliverable per the design. The grader will fail Quality scoring until exemplars are populated. This is documented in §6 of the design doc but worth a reviewer's explicit eyeballs — Codex should confirm the grader gracefully degrades when exemplars are missing, not silently produces nonsense scores.
2. **Rubric file/deliverable naming consistency.** `scripts/ai_grader.py` DELIVERABLES and `scripts/seed_class_state.py` DELIVERABLES are both source-of-truth and must stay in sync. A mismatch would silently corrupt the briefings.
3. **The anti-hallucination constraints** in `grading_prompt_template.md` ("every score must be backed by at least one literal quote…"). These are the main defence against LLM failure modes (Kim et al. 2024 verbosity bias; Mizumoto & Eguchi 2023 specificity hallucination). If Codex sees a gap in the prompt's defenses, that's the most consequential place to flag.

---

## 4. Class-state database backend (the newest work)

### 4.1 The schema

`scripts/migrations/2026-04-17_class_state.sql` adds ten tables and one view to `data/ka_auth.db`. Every table scopes to an `offering_id` foreign key so Spring 2026 and Fall 2026 (and every successor) are fully isolated — per DK's "no cohort rollover" decision.

The ten tables are: `class_offerings`, `enrollments`, `deliverables`, `submissions`, `grade_dossiers`, `calibration_runs`, `audit_samples`, `appeals`, `announcements`, `audit_log_class`. The view `student_totals_v` computes per-student per-offering totals (A0/5 + A1/5 + track/75 + F160/15 = 100) by joining `enrollments × users × grade_dossiers × deliverables`.

Every FK column pointing at `users(user_id)` is `TEXT`, matching the existing convention (IDs like `u_c44d6b24c77203dd`, `instructor_kirsh`). An earlier draft used `INTEGER` and failed the FK constraint against the real DB; the linter-visible changes in the committed file are from that fix-up pass. Every `CREATE` uses `IF NOT EXISTS`, so the migration is idempotent. Rollback steps are in the trailing comment block.

### 4.2 The seeder

`scripts/seed_class_state.py` populates the schema from on-disk rubric files and the demo roster. Three phases: (1) ensure the instructor user exists (`dkirsh@ucsd.edu` by default, overridable with `--instructor-email`); (2) insert the `cogs160sp26` offering; (3) walk the 31 deliverables, extract the `## Machine-readable spec` YAML block from each rubric Markdown file, and insert rows with the hardness-weighted points; (4) insert 15 demo enrollments, creating users with SHA256-derived `u_{16-hex}` IDs if the user doesn't already exist. Dry-run mode (`--dry-run`) rolls back the transaction so the DB is untouched.

Applied-to-real-DB evidence:

```
class_offerings:        1 row  (cogs160sp26)
deliverables:          31 rows
enrollments:           15 rows
student_totals_v:      15 rows, all 0 pts (no dossiers yet)
```

Pre-migration DB backed up to `data/ka_auth.db.pre_class_state_2026-04-18.bak` (gitignored; not committed).

### 4.3 The FastAPI server

`scripts/ka_class_api.py` exposes seven endpoints:

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/admin/class/health` | Unauthenticated health check (DB reachable, schema present) |
| GET | `/api/admin/class/roster` | Per-student totals from `student_totals_v` |
| GET | `/api/admin/class/grading` | Grading-tab payload: KPIs + student rows |
| GET | `/api/admin/class/calibration` | Latest calibration run per deliverable |
| GET | `/api/admin/class/audit/queue` | Pending (uncompleted) audit samples |
| GET | `/api/admin/class/appeals` | Open appeals (`stage != 'resolved'`) |
| POST | `/api/admin/class/grading/run` | Shells out to `ai_grader.py queue` |
| POST | `/api/admin/class/audit/pull` | Stub — will compute stratified sample when dossiers exist |

Auth is an interim `X-Admin-Token` header check against `/etc/ka/admin_token.txt` (or `KA_ADMIN_TOKEN` env var). Per DK, this is the deliberate interim until Shibboleth lands — see `docs/SHIBBOLETH_INTERIM_NOTE_2026-04-18.md`. In dev, if no token is configured, requests pass (unless `KA_ADMIN_STRICT=1`).

Every state-mutating endpoint (`grading/run`, `audit/pull`) writes to `audit_log_class` with actor, event type, target, and timestamp. This is the FERPA disclosure-logging surface.

Smoke-test evidence (against the real `data/ka_auth.db`):

```
/api/admin/class/health   → {"ok":true,"db":"data/ka_auth.db","offerings":1}
/api/admin/class/roster   → 15 students, offering cogs160sp26, all 0 pts
/api/admin/class/grading  → class_summary + 15 student rows in correct shape
/api/admin/class/grading/run → {"ok":true,"queued":150,...}
                              (built 150 briefings; removed after test)
```

### 4.4 The admin-UI dual-write shim

In `160sp/ka_admin.html`, two small helper functions `kaApiGet` and `kaApiPost` were added above the `ADMIN_API` declaration. Each tries the real `/api/admin/class/*` endpoint first and silently falls back to the demo `DEMO_GRADING` / `DEMO_CALIBRATION` / `DEMO_AUDIT_QUEUE` / `DEMO_APPEALS` objects on any error (network failure, 4xx, 5xx). The page remains fully usable when the backend is offline.

The six `ADMIN_API.loadGrading` / `loadCalibration` / `loadAuditQueue` / `loadAppeals` / `runGradingPass` / `pullAuditSample` functions each became one-line calls to the shim. `renderGrading()` in the same file was patched to prefer the inline `name` and `track` fields from the API response (the real backend returns `u_{hex}` IDs that won't match the demo ROSTER array, so the old `rosterById(s.sid).name` lookup would have returned undefined).

The admin token, if any, is read from `sessionStorage['ka.adminToken']` and sent as `X-Admin-Token` on every request. Credentials are `same-origin`.

### 4.5 What Codex should check

1. **Schema correctness.** The ten tables plus the view are the load-bearing artefact. Codex should open `scripts/migrations/2026-04-17_class_state.sql` and verify (a) every FK points at an existing column, (b) CHECK constraints match the enumerated values used downstream, (c) indexes cover the query patterns in `ka_class_api.py`, (d) the `student_totals_v` GROUP BY and COALESCE logic is arithmetically correct for the 100-point scheme.
2. **Seeder idempotency.** Running the seeder twice must not create duplicate rows. I verified this with a second dry-run, but Codex should confirm the "already present" guards on `class_offerings`, `deliverables`, and `enrollments` cover all fields the test is sensitive to.
3. **FastAPI auth shim.** The `require_admin` dependency allows requests through when no token is configured unless `KA_ADMIN_STRICT=1`. This is deliberate for dev but is a production risk if the production deploy forgets to set the env var. Codex should flag this as a deploy-checklist item.
4. **Dual-write fallback.** On backend error, the admin UI silently falls back to demo data. The `console.debug` log line makes the fallback visible to anyone with DevTools open, but a stronger signal (e.g., a small "demo mode" banner when the shim falls back) may be worth it. Codex's call.

---

## 5. Thirteen T1.5 domain-theory pages

Generator-driven pages at `ka_theory_{art,srt,biophilia,prospect_refuge,privacy_regulation,kaplan_preference,adaptive_thermal,space_syntax,soundscape,place_attachment,brecvema,flow_theory,goldilocks_principle}.html`. Each page follows the structure of the T1 framework pages: draft banner, code pill + title + tagline, TOC, 300-word summary (ART only; 150–220-word stub on the other twelve, explicitly flagged as "pending panel review"), 1,500-word deep dive (ART only; deferred on the others), T1-parents lattice with clickable links to the 11 T1 framework pages, and 5 classic + 5 recent neuroscience references with Google Scholar citation counts.

Data source: `data/t15_theories.json` (the ART full entry) plus an inline `STUBS` dictionary in `scripts/generate_t15_pages.py` for the twelve panel-review stubs. Iteration on any theory means editing the data, not the HTML. The generator is ~300 lines; the output files total ~2,300 lines.

`ka_theories.html` was patched via a one-shot Python regex to add an "In-depth entry →" link to each of the 13 T1.5 cards so the new pages are reachable from the theories index.

All references are real and cross-checked against Google Scholar — none fabricated. This is non-negotiable for a university site.

### What Codex should check

The twelve stub pages have 150–250-word summaries that gesture at the core theory claim. Codex should spot-check two or three of them (SRT, Biophilia, Prospect-Refuge are the most-cited) for factual accuracy. The references are Scholar-verifiable; the prose is draft and explicitly pending panel review, but should not contain claims an expert reviewer would immediately flag as wrong.

---

## 6. The Grading tab (ka_admin.html)

Added in `f844e88`. Four cards:

1. **Class grading summary** — six KPI numbers (class avg, median, hi, lo, dossier count, open appeals), plus Run-grading-pass and Export-CSV buttons.
2. **Per-student totals table** — 11 columns (student, track, A0/5, A1/5, Track/75, F160/15, Total/100, Last AI pass, Audit, Confidence, Dossier button).
3. **Two-column: Calibration health + Audit queue** — κ per deliverable against the gates (0.70 / 0.65 / 0.55); stratified 20% audit sample with stratum tag per row.
4. **Open appeals** — two-stage resolution buttons (Run 2nd AI grader / Send to human adjudication).

The dossier modal shows per-deliverable bands with links to the rubric Markdown files; the appeal modal wires the two-stage resolution actions.

### What Codex should check

Cross-browser rendering. I validated the HTML against the site validator (0 errors, 171 warns — all pre-existing template-placeholder `LNK001` and localStorage `SEC001` noise), but I did not exercise the Grading tab in a real browser. Codex could confirm the layout holds at 1440×900, 768×1024, and 390×844 viewports (the site's three-viewport Playwright regression set).

---

## 7. Policy clarifications encoded in docs

Three DK decisions from 2026-04-17/18 are now canonical in the design docs:

1. **No cohort rollover.** Each COGS 160 offering is independent. Schema carries `offering_id` on every class-state table; queries that omit it are bugs. `docs/CLASS_STATE_DATABASE_DESIGN_2026-04-17.md` §9 amended; `docs/END_OF_QUARTER_WORKFLOW_2026-04-18.md` new.
2. **AI grader runs on the subscription, not the Anthropic API.** `160sp/rubrics/AI_GRADING_DESIGN_2026-04-17.md` §10 rewritten to describe the two-part Python-orchestrator + Cowork-dispatch architecture. Zero API calls in the grading flow.
3. **End-of-quarter: grades → eGrades CSV → Registrar; records retained on a 5TB external disk for the UC-schedule minimum of 5 years.** Destruction surfaced on July 1 of year 6 for manual instructor review. `docs/END_OF_QUARTER_WORKFLOW_2026-04-18.md` specifies the disk layout, CSV format, and the uploader URL.

Plus the Shibboleth interim: `docs/SHIBBOLETH_INTERIM_NOTE_2026-04-18.md` explains where UCSD Shib credentials come from (UCSD ITS Service Provider registration via `support.ucsd.edu/its`, 2–3 week critical path) and why we defer. Interim auth is password against `data/ka_auth.db`.

---

## 8. What's NOT in the 14 commits (deliberate exclusions)

1. **Exemplar files for the rubric specs.** These need DK + track-lead review before the grader can produce trustworthy Quality scores. Week-3 track-lead deliverable.
2. **Real student roster in the DB.** The seeder installed 15 demo students (Aisha Rahman, Ben Choi, Carla Mendoza, etc.) so the backend can be tested end-to-end. The real roster replaces these when DK has the class list.
3. **SMTP wiring for `ka_forgot_password.html`.** Requires SMTP credentials we don't have.
4. **Shibboleth integration.** Deferred per the interim note. 2–3 week sprint when DK wants to invest.
5. **`scripts/backup_to_5t.sh`** (rsync to the 5T disk). Referenced in the end-of-quarter workflow doc as pending; a one-liner when DK has the disk mounted at a stable path.
6. **Any push to origin/master.** CLAUDE.md forbids pushing without explicit permission. DK was asked and has not yet said push.

---

## 9. What a reviewer should focus on, in priority order

1. **SQL migration correctness** (`scripts/migrations/2026-04-17_class_state.sql`). Schema is load-bearing; every dependent piece (seeder, API, admin UI, AI grader, eGrades exporter) builds on it.
2. **FastAPI auth and data-leakage surface** (`scripts/ka_class_api.py`). The interim `X-Admin-Token` shim is sound but the dev-mode pass-through is a production risk; CORS is whitelisted to three origins but Codex should confirm there's no way a browser on a different origin gets roster data.
3. **AI-grader orchestration** (`scripts/ai_grader.py` + `160sp/rubrics/prompts/grading_prompt_template.md` + `scripts/run_grading_pass.md`). The subscription-LLM architecture is unusual; Codex should sanity-check the subagent-dispatch flow.
4. **eGrades CSV format** (`scripts/export_egrades.py`). The UTF-8 + CRLF + column schema claims are based on the 2025–26 UCSD Registrar instructor-upload guide; DK should verify against the current Registrar spec before a real Week-10 upload.
5. **Design-doc coherence.** `docs/CLASS_STATE_DATABASE_DESIGN_2026-04-17.md`, `160sp/rubrics/AI_GRADING_DESIGN_2026-04-17.md`, `docs/END_OF_QUARTER_WORKFLOW_2026-04-18.md`, `docs/SHIBBOLETH_INTERIM_NOTE_2026-04-18.md` should tell one consistent story.
6. **T1.5 page accuracy.** Spot-check SRT, Biophilia, Prospect-Refuge stub summaries for factual claims that would fail a domain-expert eyeball.
7. **Rubric prose and bands** (`160sp/rubrics/**/*.md`). The 28 per-deliverable rubrics follow a uniform shape; random spot-checks are sufficient.

---

## 10. Summary for the push decision

Fourteen commits, no secrets, no large binaries, no production-data leakage. The largest risk at push time is that the work depends on the exemplar files not yet in the repo and on the demo roster not being real — but those are explicit Week-3 deliverables, not push-time bugs. Anyone pulling origin/master after the push will be able to run the migration (`python3 -c "import sqlite3; sqlite3.connect('data/ka_auth.db').executescript(open('scripts/migrations/2026-04-17_class_state.sql').read())"`), the seeder, the FastAPI backend, the admin UI, the AI-grader orchestrator, and the eGrades exporter end-to-end against their own clone.

If Codex finds an issue worth fixing before the push, DK should say so and CW will land the fix as a 15th commit. If the review comes back clean, CW is ready to `git push origin master` on DK's explicit OK.

---

## File inventory (for Codex's grep convenience)

```
New or substantially modified files in the 14-commit window:

scripts/
  ai_grader.py
  export_egrades.py
  generate_t15_pages.py
  ka_class_api.py
  seed_class_state.py
  run_grading_pass.md
  migrations/2026-04-17_class_state.sql

160sp/rubrics/
  README.md
  AI_GRADING_DESIGN_2026-04-17.md
  grading_sheet_template.md
  common/{a0,a1}.md
  t1/{README,T1.a,…,T1.g}.md
  t2/{README,T2.a,…,T2.g}.md
  t3/{README,T3.a,…,T3.g}.md
  t4/{README,T4.a,…,T4.g}.md
  f160/README.md
  verification/README.md
  prompts/grading_prompt_template.md

160sp/
  ASSIGNMENT_RUBRICS_AUDIT_AND_SCAFFOLD_2026-04-17.md
  ka_admin.html     (added Grading tab + dual-write shim)

docs/
  AI_GRADING_DESIGN_2026-04-17.md (in 160sp/rubrics/, but cross-referenced)
  CLASS_STATE_DATABASE_DESIGN_2026-04-17.md
  END_OF_QUARTER_WORKFLOW_2026-04-18.md
  SHIBBOLETH_INTERIM_NOTE_2026-04-18.md

data/
  t15_theories.json

ka_theory_{art,srt,biophilia,prospect_refuge,privacy_regulation,
           kaplan_preference,adaptive_thermal,space_syntax,soundscape,
           place_attachment,brecvema,flow_theory,goldilocks_principle}.html

ka_contribute.html                              (restored to 767-line prod version)
ka_contribute.html.redesign_346lines.bak        (reference backup of redesign)
ka_theories.html                                (In-depth-entry links added)

.gitignore                                      (pattern for data/*.bak)
```

End of report.
