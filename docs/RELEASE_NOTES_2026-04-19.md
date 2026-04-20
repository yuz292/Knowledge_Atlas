# Release notes — Knowledge Atlas, staging deploy 2026-04-19

*Tag*: `v2026-04-19-staging`
*Branch*: `master`
*Scope*: everything committed between the last production push and this release-candidate tag

---

## What changed, at a glance

This release turns the Knowledge Atlas from a largely static reference site into a **class-state-aware teaching platform with a working AI-grading pipeline, a 102-bundle topic crosswalk, a per-persona front door, and the infrastructure to run an end-to-end smoke test before every deploy**. It lands three weeks of dense work in one version bump.

The site remains a primarily static HTML + JSON-payload codebase. The two Python backends — the FastAPI class-state API at `scripts/ka_class_api.py` and the classifier endpoint at `ka_article_endpoints.py` — are optional in the sense that the front end falls back to demo data when they are offline, but admin-side workflows (grading, audit, class-state view) require them.

## User-visible changes (the front-door differences a visitor will see)

- **New per-persona topic-page variants.** The main topic entry point now has five sibling variants plus the original Classic View. `ka_topic_facet_view.html` is the progressive-disclosure default for first-time visitors. The row across the top of every variant lets you jump between them. For the UX evaluation rubric, the full six-variant comparison lives at `ka_topics.html`.
- **New public-facing variant pages.** `ka_topics_public_view.html` and `ka_topics_student_view.html` are two further variants tailored to the public-visitor and 160-student personas respectively — each of which the home page's role router now points at directly.
- **A dynamic per-article page.** `ka_article_view.html?id=PDF-XXXX` renders one paper from `articles.json` with metadata, abstract, main conclusion, Atlas classification, theory tags, instruments, sensor summary, and related papers. Replaces the stale `data/pnu_articles/` path pattern the topic page used to link to.
- **A simpler public contribute page.** `ka_contribute_public.html` is a one-page "suggest a paper" flow with a PDF dropzone, a citation/DOI fallback, and a thank-you modal. The full contributor tools remain at `ka_contribute.html`.
- **A rebalanced home role router.** The four persona buttons on `ka_home.html` are now equal-weight (no visual primary), reordered (Researcher / Practitioner / Contributor / 160 Student), and re-pointed at the persona-appropriate surfaces. The 160-student route finally follows the documented default rule to `ka_student_setup.html` (not the schedule).
- **T1 framework pages have a clearer banner.** The former "Draft — pending neuroscience panel review" label on the 11 framework explainer pages now reads "Working draft · expert review in progress" with public-facing copy.
- **13 T1.5 domain-theory pages.** ART is a full 300w + 1,500w treatment with 10 references; the other twelve are panel-review stubs with real references and 150–250w summaries.
- **A coverage heatmap.** `ka_topic_heatmap_view.html` renders the 9 × 18 modality × outcome grid with paper-count colour, for honest evidence-gap inspection.
- **Better article links on the topic page.** `ka_topics.html` now hydrates paper IDs into title + author + year from `articles.json` rather than showing "Metadata from articles.json (pending)".
- **An empty-state message you can actually use.** `ka_article_view.html` with a missing `?id=` no longer says "No article id specified"; it tells the visitor two ways to recover.

## Backend and data-layer changes (invisible to visitors, but load-bearing)

- **Class-state database backend.** New SQL migration adds ten tables plus a `student_totals_v` view to `data/ka_auth.db`: `class_offerings`, `enrollments`, `deliverables`, `submissions`, `grade_dossiers`, `calibration_runs`, `audit_samples`, `appeals`, `announcements`, `audit_log_class`. Partial unique index on `grade_dossiers` enforces one final per student-deliverable. Applied and seeded on local dev DB.
- **FastAPI class-state API.** `scripts/ka_class_api.py` serves `/api/admin/class/{health,roster,grading,calibration,audit/queue,appeals,grading/run,audit/pull}`. Fail-closed auth gate via `X-Admin-Token` header against `/etc/ka/admin_token.txt` or `KA_ADMIN_TOKEN` env var; development bypass via `KA_ADMIN_ALLOW_OPEN=1`.
- **Grading pipeline.** `scripts/ai_grader.py` is a subscription-LLM-compatible grading orchestrator (builds briefings, dispatches subagents via the Task tool, writes dossiers). `scripts/export_egrades.py` produces UCSD-Registrar-compliant CSV for end-of-quarter upload. `scripts/smoke_test_e2e.sh` is the one-command system check (11 stages, currently all green).
- **Roster import.** `scripts/import_roster.py` ingests a Registrar CSV into the `enrollments` table; supports dry-run, drop-demo, and audit-log entries.
- **RAG-audit scaffolding.** `scripts/rag_harvest.py` + `scripts/rag_classify_check.py` + `data/rag_services.yaml` ready the T2.d.2 deliverable's plumbing. Real service adapters deferred until DK confirms the services list and credentials.
- **Classifier audit.** `scripts/audit_classifiers.py` runs against the cross-repo `pipeline_registry_unified.db`; findings documented in `docs/CLASSIFIER_AUDIT_FINDINGS_2026-04-18.md` (1,393 papers; 9 × 18 modality × outcome taxonomy; several columns 0 %-populated and flagged).
- **Dual-write shim on the admin page.** `ka_admin.html` reads from `/api/admin/class/*` with automatic fallback to demo data when the backend is offline. Admin token stored in sessionStorage at key `ka.adminToken`.

## Rubric + design artefacts (maintainer-side)

- Complete T1–T4 rubric scaffold at `160sp/rubrics/` — 40 files covering every deliverable, plus the A0/A1 common-work rubrics and the Work-on-160F rubric.
- AI-grading design document `160sp/rubrics/AI_GRADING_DESIGN_2026-04-17.md` (371 lines, 9 peer-reviewed references).
- T4.b.2 Topic-page variant evaluation deliverable tying the UX-track scenarios to the five-variant comparison.
- Class-state database design doc.
- End-of-quarter workflow doc (eGrades export + 5 TB retention).
- Class-start deployment checklist (17-step runbook for going live).
- Per-persona usability audit (5,200 words, 14 academic refs).
- Strategic thinking doc on complicated pages, user journeys, and the panel discovery method.

## Policy decisions embedded in this release

Three DK decisions landed as canonical during the sprint:

1. **100-point class-level grading allocation.** 5 A0 + 5 A1 + 75 track + 15 Work-on-160F. Track budgets are hardness-weighted, not uniformly weekly.
2. **Subscription-LLM grading, not API.** The AI grader runs on DK's Claude subscription via the Task tool; no API keys required, no per-token budget.
3. **No cohort rollover.** Each COGS 160 offering is independent. Every class-state table carries `offering_id`; queries that omit it are bugs.

## Known deferrals

- Real RAG service adapters (blocked on DK's services list + credentials).
- Shibboleth SSO (deferred to Fall 2026; interim password auth against `data/ka_auth.db`).
- Exemplar authoring for AI-grading rubrics (Week-3 track-lead deliverable; without these, grading runs in degraded mode with `confidence=low` and a `degraded_mode_no_exemplars` flag).
- The classifier-repair sprint (the 0 %-populated `primary_topic_candidate`, `canonical_triage_decision`, `has_classifier_conflict` columns).
- SMTP wiring for password reset.
- 5 TB backup rsync script.
- Nine-panel deliberation series (first-wave four panels proposed in the strategic thinking doc; awaiting DK roster sign-off).

## Commits in this release (tip first)

Run `git log --oneline <last-production-tag>..HEAD` for the full list. Key commits:

- Audit follow-throughs + strategic panels doc (`ad71e25`)
- Per-persona usability audit + quick-win fixes + first persona-specific variant (`2f988b9`)
- Topic-page review fixes + dynamic article page (`e7ec006`)
- Option A approved: T4 point reallocation canonical (`44bfda1`)
- Tightening batch + 5 topic-page variants + T4.b.2 evaluation rubric (`07e9abb`)
- Crosswalk GUI Pattern 5: progressive-disclosure facets (`bf39a8f`)
- Codex's atlas_shared classifier integration (`f87c2c9`, attributed to Codex)
- Codex review fixes: two P1 correctness bugs + two P2 hardenings (`94d07f9`)
- Class-state backend: migration + seeder + FastAPI + admin dual-write (`9408a6e`)
- AI grader + eGrades exporter + policy clarifications (`40f187b`)
- Rubric scaffold for COGS 160sp with AI-primary grading design (`0e365f0`)

## Upgrade notes

1. **Apply the class-state migration** on any existing `data/ka_auth.db` before first use: `python3 -c "import sqlite3; sqlite3.connect('data/ka_auth.db').executescript(open('scripts/migrations/2026-04-17_class_state.sql').read())"`. Idempotent.
2. **Seed the offering** if you want the admin grading view to have data: `python3 scripts/seed_class_state.py`. Populates one demo offering + 31 deliverables + 15 demo students.
3. **Set the admin token** before the FastAPI backend is reachable: either `export KA_ADMIN_TOKEN=<value>` or `echo <value> > /etc/ka/admin_token.txt` with 600 perms.
4. **Run the smoke test** as the deploy gate: `bash scripts/smoke_test_e2e.sh` — must pass all 11 stages before production swap.

## What to watch after deploy

- The `ka.adminToken` sessionStorage key must match the backend's `KA_ADMIN_TOKEN` or the admin grading view falls back to demo data.
- The classifier DB is in the sibling AE-recovery repo on DK's Mac; on the server it may need to be cloned separately or the `KA_UNIFIED_REGISTRY_DB` env var set to a different path.
- The topic crosswalk payload at `data/ka_payloads/topic_crosswalk.json` is regenerated by `scripts/build_ka_adapter_payloads.py` (Codex-owned). If it drifts, the five variant pages show stale data.

## Rollback plan

See Phase 8 of `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md`. One-line symlink flip back to the previous production directory. Keep the pre-swap directory for at least two weeks.
