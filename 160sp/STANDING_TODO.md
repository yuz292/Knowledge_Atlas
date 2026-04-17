# Knowledge Atlas — Standing Todo (session-spanning)

**Last updated**: 2026-04-17
**Purpose**: Cross-session task queue so work continues ballistically between sessions. AI workers pick up from this list when no new user directive is pending.

---

## Tier 1 — Active / in flight

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 1 | Retrofit ~30 remaining 160sp/ pages to canonical navbar | CW | Targets: ka_schedule, ka_track_signup, weekN_agenda, ka_admin, ka_dashboard. Each migration drops 3 validator errors. |
| 2 | Expand framework deep dives beyond current 1127–1605 word range when literature warrants | Panel | User confirmed frameworks vary with literature richness; not every framework needs 1500w |
| 3 | Visual regression baseline via scripts/visual_check.py | CW | Needs local Chromium via playwright; first run captures baselines; schedule weekly after |

## Tier 2 — Design review / decisions pending

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 4 | **Topic hierarchy review** | DK + panel | Current 18 topics in topics.json were cluster-generated. Names read as cluster labels ("Spatial Form × Aesthetic Preference (Neuroaesthetics)") rather than research topics. Need a considered top-down review that maps topics to T1.5 layer and renames for human meaning. Reference: docs/UNIFIED_PIPELINE_REFERENCE_FOR_ARTICLE_FINDER.md §4.2. |
| 5 | T1.5 pages creation | CW | 13 T1.5 domain theories need dedicated pages parallel to the 11 T1 framework pages. Each T1.5 page should have its own lattice (T1.5 → Topics) once topic hierarchy is reviewed. |
| 6 | Panel review of 11 T1 framework pages | Panel | LLM-drafted 2026-04-17, 1127–1605w each. Banner on every page flags the draft status. See ka_framework_pp.html as the gold standard. |
| 7 | Panel review of 71 mechanism profiles | Panel | 54 full (≥600w), 11 brief (300–599w), 6 stub (<300w). Only the 6 stubs need fresh authorship. |

## Tier 3 — Infrastructure / deploy

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 8 | Deploy ka_admin_refresh_endpoint.py to production | Ops | Follow SSH_SETUP_FOR_PNU_REFRESH.md. SSH key + forced-command entry + systemd + nginx. |
| 9 | Replace ka_admin.html demo gate with real SSO via ka_sso_stub.py | Ops | UCSD Shibboleth registration + env vars. See MIGRATION_NOTE in ka_sso_stub.py. |
| 10 | Wire ka_forgot_password.html to production SMTP | Ops | Currently points at localhost:8765 ka_auth_server.py. Either reverse-proxy that behind xrlab, or swap for UCSD institutional SMTP. |
| 11 | Wire ka_contribute.html form POST to /api/articles/submit | Ops | Currently stubs the submission. The endpoint exists from Track 2 intake; public form should call it with source_surface='public'. |

## Tier 4 — Polish and follow-through

| # | Task | Owner | Notes |
|---|------|-------|-------|
| 12 | Near-miss review queue in ka_admin.html | CW | §4.5 of pipeline reference doc. Classifier flags near-misses; no human-facing surface yet. |
| 13 | Classifier performance dashboard on admin Site Health tab | CW | §4.6 of pipeline reference. classifier_eval_*.json exists but has no dashboard. |
| 14 | atlas_shared usage cheat sheet | CW + Codex | §4.7. Help Track 2 students call HeuristicArticleTypeClassifier etc. from their own code. |
| 15 | Reconcile dual framework naming (T1-hierarchy PP/SN/DP/DT vs _index.md PP/SN/DP/DT where DP and DT mean different things) | Panel | Noted in §122.13 of master doc. |

## Recently completed (this sprint)

- 11 T1 framework deep-dive pages (PP SN NM EC IC DP IE_DPT DT MS CB MSI) with lattice graphs
- Canonical-nav global pages: ka_home, ka_articles, ka_contribute, ka_topics, ka_about
- Archive system: ka_archive.html + Track 4 link + admin tab + nav contract §8a
- Site validator + visual regression + SSO stub scripts
- Forgot-password migration + Evidence/Gaps redirect-to-Topics
- Master doc mirror in Knowledge_Atlas/docs/
- Unified pipeline reference doc for Article Finder track (with mermaid boxology and 7 improvement areas)
- Admin page with roster/login/track matrix/announcements/site-health/content/settings/access/archive/audit

## How to use this file

AI workers at the start of a session: read this, pick the highest-priority unblocked task, execute ballistically until blocked or complete, update this file at session end.

Human reviewers: edit this file directly to add, remove, or reorder tasks. Move completed items to the "Recently completed" section. The file is canonical; individual TODO markers scattered across code comments defer to this list.
