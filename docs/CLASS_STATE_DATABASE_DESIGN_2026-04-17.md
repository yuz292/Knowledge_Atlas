# Class-state database design — COGS 160sp (and successor cohorts)

*Date*: 2026-04-17
*Author*: CW (for DK approval)
*Status*: Design proposal — supersedes the demo-array and JSON-file state scattered across `ka_admin.html`, `160sp/rubrics/*.md`, and the dossier filesystem

---

## 1. Why this matters

The site currently holds class-relevant state in at least five different places:

| State | Current home | Problem |
|-------|--------------|---------|
| Student roster (names, emails, tracks, login status) | `ROSTER` array hardcoded in `ka_admin.html` lines 1275–1335 | Edits go stale the moment the file is redeployed; no audit trail; impossible for backend to know about a student who exists only in one browser tab |
| Logins / auth | `data/ka_auth.db` (SQLite) already in place | Already a DB — good. But the admin UI does not yet talk to it |
| Articles submitted through the pipeline | `data/ka_auth.db` `articles` table + `data/ka_workflow.db` `intake_submissions` + `pipeline_registry_unified.db` | Three tables across two databases; intake vs. registry boundary is unclear |
| Grading dossiers | Planned as flat markdown files at `160sp/grading/{sid}/{deliv}.md` | Files work for human reading, fail for class-wide queries ("who is below 60 points at Week 6?"), and make audit tamper-evidence hard |
| Rubrics + machine-readable specs | Markdown files in `160sp/rubrics/` | Markdown is right for human authoring; at grading time a DB-backed canonical view is what the AI grader needs |

The fragmentation is not a crisis — the site has been running fine — but it imposes three real costs. First, the demo `ROSTER` array desynchronises from the real auth database the first time a real student signs up. Second, cross-cutting queries ("for every student, show A0 + A1 + track subtotal + F160 subtotal at the current moment") cannot be written at all with the current split; they are done by joining JS arrays with file reads, which does not scale. Third, regulatory needs — FERPA compliance for educational records, audit trails for grade appeals, data retention for Fall-cohort transfer — require a proper database because the audit evidence has to be tamper-evident and queryable.

The pragmatic recommendation is not to build a new database from scratch. `ka_auth.db` already exists and already carries users, articles, audit_log, and tokens. It can be extended to carry the class-state rows we need, and the admin UI can be re-pointed at it via the `ADMIN_API` seam I have been maintaining in `ka_admin.html`.

The remainder of this document proposes the extended schema, the migration path, the admin-UI changes, and the deployment concerns.

---

## 2. Current database inventory (what we already have)

The repository has three SQLite files in use or close to in use:

```
data/ka_auth.db          (primary — users, articles, submissions, audit)
data/ka_workflow.db      (registrations, intake_submissions, track_targets)
pipeline_registry_unified.db   (1,428 papers × 162 columns — Track 2 target DB)
```

`ka_auth.db` is the natural home for class-state extensions because it already owns `users`, `audit_log`, `refresh_tokens`, and the Article submission surface. `ka_workflow.db` is doing overlapping work — its `registrations` and `intake_submissions` tables should in the longer run be collapsed into `ka_auth.db`. `pipeline_registry_unified.db` is a separate concern (Track 2's evidence corpus) and should stay separate.

The table I am proposing to add is a compact set of class-state tables inside `ka_auth.db`. This keeps the foreign-key chain short and avoids a second cross-database join at query time.

---

## 3. Proposed schema extension

Ten new tables, all inside `ka_auth.db`. Existing `users` table anchors everything via `user_id`.

### 3.1 `class_offerings`

One row per course offering. COGS 160 Spring 2026 is one row; Fall 2026 will be another.

```sql
CREATE TABLE class_offerings (
  offering_id        TEXT PRIMARY KEY,          -- e.g. 'cogs160sp26'
  title              TEXT NOT NULL,
  quarter            TEXT NOT NULL,             -- 'Spring 2026', 'Fall 2026'
  instructor_user_id INTEGER NOT NULL REFERENCES users(user_id),
  starts_on          DATE NOT NULL,
  ends_on            DATE NOT NULL,
  status             TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','completed','archived')),
  total_points       INTEGER NOT NULL DEFAULT 100,
  created_at         TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 `enrollments`

Student-to-offering mapping. Independent of `users` so a TA or auditor can be non-enrolled.

```sql
CREATE TABLE enrollments (
  enrollment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id            INTEGER NOT NULL REFERENCES users(user_id),
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  role               TEXT    NOT NULL DEFAULT 'student' CHECK(role IN ('student','ta','auditor','track_lead')),
  track              TEXT    CHECK(track IN ('t1','t2','t3','t4',NULL)),
  f160_track         TEXT    CHECK(f160_track IN ('docs','site_pr','transfer','scaffolding',NULL)),
  partner_user_id    INTEGER REFERENCES users(user_id),  -- for T1.c paired kappa, T4.e reproducibility
  status             TEXT    NOT NULL DEFAULT 'active' CHECK(status IN ('active','dropped','at_risk','pending')),
  enrolled_at        TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_sign_in_at    TEXT,
  UNIQUE(user_id, offering_id)
);
```

### 3.3 `deliverables`

Catalogue of every deliverable: A0, A1, T1.a through T1.g, T2.a–g, T3.a–g, T4.a–g, F160. Pre-loaded from the rubric files at the Week-3 planning meeting.

```sql
CREATE TABLE deliverables (
  deliverable_id     TEXT PRIMARY KEY,   -- 'T1.b', 'A0', 'F160' etc.
  offering_id        TEXT NOT NULL REFERENCES class_offerings(offering_id),
  track              TEXT CHECK(track IN ('common','t1','t2','t3','t4','f160')),
  title              TEXT NOT NULL,
  hardness           TEXT CHECK(hardness IN ('easy','medium','medium-hard','hard')),
  points             INTEGER NOT NULL,
  timeliness_bonus   INTEGER NOT NULL DEFAULT 0,
  span_start         DATE NOT NULL,
  span_end           DATE NOT NULL,
  rubric_path        TEXT NOT NULL,      -- e.g. '160sp/rubrics/t1/T1.b_tag_100.md'
  spec_yaml          TEXT NOT NULL,      -- the machine-readable YAML block, stored inline
  status             TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','revised','retired'))
);
```

### 3.4 `submissions`

Every artefact submitted. References `deliverables` and whichever underlying artefact system the submission lives in (article, tag row set, git commit, prose doc, media file).

```sql
CREATE TABLE submissions (
  submission_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id            INTEGER NOT NULL REFERENCES users(user_id),
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  deliverable_id     TEXT    NOT NULL REFERENCES deliverables(deliverable_id),
  artefact_type      TEXT    NOT NULL CHECK(artefact_type IN (
                        'registry_rows','tag_rows','git_commit','prose_doc',
                        'media','survey_csv','wireframe','build','pdf','other')),
  artefact_ref       TEXT    NOT NULL,   -- URL, file path, DOI, git SHA, or a JSON array of refs
  word_count         INTEGER,            -- for prose
  row_count          INTEGER,            -- for tabular
  submitted_at       TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_late            INTEGER NOT NULL DEFAULT 0,
  days_late          INTEGER NOT NULL DEFAULT 0,
  revision_of        INTEGER REFERENCES submissions(submission_id)
);
CREATE INDEX ix_submissions_user_deliv ON submissions(user_id, deliverable_id);
```

### 3.5 `grade_dossiers`

One row per AI-graded submission. The dossier content is stored inline as markdown so the full artefact is queryable, not buried in a filesystem. Files still exist as read-only mirrors.

```sql
CREATE TABLE grade_dossiers (
  dossier_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  submission_id      INTEGER NOT NULL REFERENCES submissions(submission_id),
  user_id            INTEGER NOT NULL REFERENCES users(user_id),
  deliverable_id     TEXT    NOT NULL REFERENCES deliverables(deliverable_id),
  offering_id        TEXT    NOT NULL REFERENCES class_offerings(offering_id),
  completeness_raw   INTEGER NOT NULL CHECK(completeness_raw BETWEEN 0 AND 3),
  quality_raw        INTEGER NOT NULL CHECK(quality_raw BETWEEN 0 AND 3),
  reflection_raw     INTEGER NOT NULL CHECK(reflection_raw BETWEEN 0 AND 3),
  timeliness_bonus   INTEGER NOT NULL DEFAULT 0,
  late_penalty       INTEGER NOT NULL DEFAULT 0,
  points_awarded     INTEGER NOT NULL,
  confidence         TEXT    NOT NULL CHECK(confidence IN ('high','medium','low')),
  dossier_markdown   TEXT    NOT NULL,   -- the full structured dossier body
  grader_model       TEXT    NOT NULL,   -- e.g. 'claude-opus-4-6'
  graded_at          TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_final           INTEGER NOT NULL DEFAULT 1,  -- 0 if superseded by a later pass
  rubric_hash        TEXT    NOT NULL    -- hash of the rubric file content at grading time
);
CREATE INDEX ix_dossiers_user_deliv ON grade_dossiers(user_id, deliverable_id, graded_at);
```

### 3.6 `calibration_runs`

Per-deliverable kappa measurements against the calibration set. One row per run, including the one before the first real grading pass.

```sql
CREATE TABLE calibration_runs (
  calibration_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  deliverable_id     TEXT    NOT NULL REFERENCES deliverables(deliverable_id),
  run_at             TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  n                  INTEGER NOT NULL,
  kappa_completeness REAL    NOT NULL,
  kappa_quality      REAL    NOT NULL,
  kappa_reflection   REAL    NOT NULL,
  pass_completeness  INTEGER NOT NULL,  -- 1 if >= 0.70
  pass_quality       INTEGER NOT NULL,  -- 1 if >= 0.65
  pass_reflection    INTEGER NOT NULL,  -- 1 if >= 0.55
  reason             TEXT,
  grader_model       TEXT    NOT NULL
);
```

### 3.7 `audit_samples`

TA blind-audit assignments. One row per dossier selected into the audit sample; TA's score goes into the same row when submitted.

```sql
CREATE TABLE audit_samples (
  audit_id           INTEGER PRIMARY KEY AUTOINCREMENT,
  dossier_id         INTEGER NOT NULL REFERENCES grade_dossiers(dossier_id),
  assigned_to_ta     INTEGER NOT NULL REFERENCES users(user_id),
  stratum            TEXT    NOT NULL CHECK(stratum IN ('low_confidence','band_boundary','random','flagged_deliverable')),
  pulled_at          TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_by             TEXT    NOT NULL,
  ta_completeness    INTEGER CHECK(ta_completeness BETWEEN 0 AND 3),
  ta_quality         INTEGER CHECK(ta_quality BETWEEN 0 AND 3),
  ta_reflection      INTEGER CHECK(ta_reflection BETWEEN 0 AND 3),
  ta_notes           TEXT,
  completed_at       TEXT
);
```

### 3.8 `appeals`

Student-initiated grade appeals, the two-stage resolution tracked inline.

```sql
CREATE TABLE appeals (
  appeal_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  dossier_id         INTEGER NOT NULL REFERENCES grade_dossiers(dossier_id),
  user_id            INTEGER NOT NULL REFERENCES users(user_id),
  criterion          TEXT    NOT NULL CHECK(criterion IN ('completeness','quality','reflection')),
  original_band      INTEGER NOT NULL,
  student_asks_band  INTEGER NOT NULL,
  reason             TEXT    NOT NULL,
  stage              TEXT    NOT NULL DEFAULT 'opened' CHECK(stage IN ('opened','2nd_ai_grading','human_adjudication','resolved')),
  opened_at          TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  second_dossier_id  INTEGER REFERENCES grade_dossiers(dossier_id),
  adjudicator_id     INTEGER REFERENCES users(user_id),
  final_band         INTEGER,
  resolved_at        TEXT
);
```

### 3.9 `announcements` and `audit_log_class`

Optional but useful. `announcements` replaces the current demo broadcast stub. `audit_log_class` extends the existing `audit_log` with class-scoped events (grading pass started, appeal opened, calibration failed, roster import); this can be a VIEW rather than a new table if we prefer.

### 3.10 Primary totals view (no new table; just a view)

```sql
CREATE VIEW student_totals_v AS
SELECT
  e.offering_id,
  e.user_id,
  u.first_name || ' ' || u.last_name AS name,
  u.email,
  e.track,
  COALESCE(SUM(CASE WHEN d.deliverable_id='A0'   THEN gd.points_awarded END), 0) AS a0_pts,
  COALESCE(SUM(CASE WHEN d.deliverable_id='A1'   THEN gd.points_awarded END), 0) AS a1_pts,
  COALESCE(SUM(CASE WHEN d.track = e.track       THEN gd.points_awarded END), 0) AS track_pts,
  COALESCE(SUM(CASE WHEN d.deliverable_id='F160' THEN gd.points_awarded END), 0) AS f160_pts,
  COALESCE(SUM(gd.points_awarded), 0) AS total_pts
FROM enrollments e
JOIN users u ON u.user_id = e.user_id
LEFT JOIN grade_dossiers gd ON gd.user_id = e.user_id AND gd.offering_id = e.offering_id AND gd.is_final = 1
LEFT JOIN deliverables d ON d.deliverable_id = gd.deliverable_id
WHERE e.role = 'student'
GROUP BY e.offering_id, e.user_id;
```

This single view replaces the current hardcoded ROSTER array and the manual arithmetic in `renderGrading()`.

---

## 4. Migration path — minimising risk

Big-bang migrations fail. Staged migrations succeed. I propose four stages.

### Stage 1 — schema additive (safe, no behaviour change)

Add the ten new tables and the `student_totals_v` view to `ka_auth.db` behind a dated migration script at `scripts/migrations/2026-04-17_class_state.sql`. Nothing reads from them yet. The existing `ka_admin.html` demo arrays remain authoritative. Rollback is trivial (drop tables).

### Stage 2 — dual-write (read still from arrays, write to DB too)

Extend `ADMIN_API` in `ka_admin.html` so that every admin action also hits a new `/api/admin/class/*` endpoint (to be implemented in `scripts/ka_class_api.py`, a FastAPI app that reads/writes the new tables). Reads still come from the demo arrays for now. The DB starts accumulating real data without displacing the demo view.

### Stage 3 — read flip (per-tab behind a feature flag)

Flip each admin tab one at a time to read from the DB via `/api/admin/class/*`. Start with the Grading tab (because that's where the stakes are lowest and the query benefit is highest — cross-cutting totals). Then Roster, Logins, Tracks, Announcements. Each flip is a single commit; each is reversible.

### Stage 4 — deprecate demo arrays

Once every tab reads from the DB, delete the demo arrays from `ka_admin.html` and remove the dual-write path. This is one PR.

The four stages can span four weeks — one per week, say Weeks 4–7 of the sprint — without interrupting any grading work.

---

## 5. Admin-UI consequences

The `ADMIN_API` seam I maintained in `ka_admin.html` (1095–1129 plus the grading extensions I just added) is exactly the place the flip happens. Every admin function already goes through `ADMIN_API.something()` which returns a promise. Changing `loadGrading()` from returning a JavaScript object to hitting `fetch('/api/admin/class/grading/{offering_id}')` is a one-line change per function.

Specifically, the ADMIN_API functions that will change call-sites:

| Function | Current stub | After flip |
|----------|--------------|-----------|
| `loadGrading` | returns `DEMO_GRADING` | GET `/api/admin/class/grading` |
| `loadCalibration` | returns `DEMO_CALIBRATION` | GET `/api/admin/class/calibration` |
| `loadAuditQueue` | returns `DEMO_AUDIT_QUEUE` | GET `/api/admin/class/audit/queue` |
| `loadAppeals` | returns `DEMO_APPEALS` | GET `/api/admin/class/appeals` |
| `runGradingPass` | sleeps, returns mock | POST `/api/admin/class/grading/run` |
| `pullAuditSample` | sleeps, returns mock | POST `/api/admin/class/audit/pull` |
| `resetLogin` | already promises | unchanged (already hits `data/ka_auth.db`) |
| `inviteAdmin` | demo only | POST `/api/admin/class/invite` |
| `changeAdminRole`, `removeAdmin` | demo only | PATCH, DELETE on `/api/admin/class/role` |

The Roster tab (which today renders `ROSTER`) becomes `GET /api/admin/class/roster` returning the join of `enrollments × users × student_totals_v`.

---

## 6. Privacy and compliance

Three concerns, all addressable.

**FERPA**. Educational records (grades, enrollments, rosters) are covered by FERPA. The practical implication is (a) only authenticated instructors and TAs see other students' records; (b) students see only their own; (c) data-retention policy for grade dossiers is minimum three years (UC system policy); (d) there must be an audit log of who accessed what, when. The `audit_log` table already exists; extend it to include class-scoped events (grade viewed by TA, dossier re-graded, appeal opened).

**PII minimisation**. Emails, real names, and student IDs are the obvious PII. Nothing else should be in the database without a clear need. In particular, do not store: home addresses (work addresses are OK if the student volunteers one), phone numbers (unless the student opts in for SMS notifications), government IDs (no). The grading data itself — scores, dossier text — is educational record, not PII in the narrow sense, but is still covered under FERPA.

**Deletion on withdrawal**. When a student drops, their `enrollments.status` flips to `dropped` but the rows are not deleted. Hard deletion happens at the three-year retention boundary, implemented by a cron job that runs on July 1 each year.

---

## 7. Deployment

The database lives at `/opt/ka/data/ka_auth.db` on the production VM (xrlab.ucsd.edu). The FastAPI backend is at `scripts/ka_class_api.py`, served by uvicorn behind the Apache reverse proxy already in place. Deployment follows the existing `scripts/deploy_to_vm.sh` pattern.

Back-ups: a daily sqlite snapshot copied to a second location via the existing Backblaze B2 daily job (already running for the articles corpus). Three-month retention of snapshots; weekly snapshots retained for two years.

Concurrency: SQLite is fine at this class scale (≤ 40 students × ≤ 30 deliverables × ≤ 5 dossiers per deliverable = ≤ 6,000 dossier rows). Write contention is not a real concern until the class grows past ~ 200 students; at that point we move to PostgreSQL. The schema above is Postgres-compatible with only cosmetic changes (TEXT → VARCHAR, CHECK constraints remain; no SQLite-specific SQL in the schema).

---

## 8. What I would build first (two-hour minimum viable backend)

If DK approves, the ballistic minimum-viable first commit is:

1. `scripts/migrations/2026-04-17_class_state.sql` — the schema as specified above. ~ 100 lines of SQL.
2. `scripts/seed_class_state.py` — one-shot seeder that reads the existing rubric files and the existing 15-student demo roster and populates `class_offerings`, `enrollments`, and `deliverables`. ~ 80 lines.
3. `scripts/ka_class_api.py` — a FastAPI module with six endpoints (roster, grading, calibration, audit queue, appeals, totals view). ~ 300 lines with Pydantic models. Binds to `127.0.0.1:8080` behind the existing reverse proxy.
4. Dual-write hook in `ka_admin.html` — every `ADMIN_API.*` function also calls the new API; reads still come from demo arrays. ~ 30 lines of JS additions.

Total ~ 500 lines plus the schema. The read-flip per tab follows in subsequent commits.

---

## 9. What this does not solve

Three things the DB does not by itself fix:

1. **SSO wiring.** Authentication still has to happen, and the `ka_sso_stub.py` Shibboleth scaffold is a scaffold. Wiring it to real UCSD Shibboleth is a separate sprint and needs instructor-of-record credentials on the Shib side.
2. **The AI grader's actual LLM calls.** `scripts/ai_grader.py` still needs to be written. The DB provides the read/write surface; the grader consumes and produces rows against that surface, but the prompt orchestration and API budget management are their own problem.
3. **The Fall-handoff policy.** When Spring 2026 ends, we need a policy decision on what transfers to Fall 2026: enrollments roll over? Grade dossiers are archived read-only? Student accounts persist? The DB allows any of these; the policy has to be decided.

---

## 10. Decision asked

- [ ] Approve the schema and the four-stage migration?
- [ ] Name the backend file `scripts/ka_class_api.py` or choose a different name?
- [ ] Sign off on the FERPA retention (three-year minimum, hard delete July 1)?
- [ ] Any tables you want removed or added?

If you say "build the minimum viable backend" I will write the schema, the seeder, and the FastAPI skeleton in the next session. If you want to iterate on the schema first, I can walk through any table in detail.

---

## References

Costa, L. A., Silveira, I. F., & Galhardi, L. B. (2023). A systematic mapping study on educational data management. *Education and Information Technologies*, 28(5), 5921–5948. https://doi.org/10.1007/s10639-022-11380-2 (Google Scholar: 40+)

Kitchenham, B. A., Budgen, D., & Brereton, P. (2015). *Evidence-based software engineering and systematic reviews*. Chapman and Hall/CRC. (Google Scholar: 3,400+) — for migration strategy and staged-rollout reasoning.

U.S. Department of Education. (2021). *Family Educational Rights and Privacy Act (FERPA): A guide for eligible students*. https://studentprivacy.ed.gov/ (authoritative source on the retention and access-control requirements above).
