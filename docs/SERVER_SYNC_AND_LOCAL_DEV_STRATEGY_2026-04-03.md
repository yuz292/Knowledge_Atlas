# Server Sync & Local Dev Strategy

**Date**: 2026-04-03
**Problem**: The server (xrlab.ucsd.edu) has direct edits (auth, A0 workflow, student task flow) that may not be in the git repo. The local repo has new user-type home pages that aren't on the server. There is no local dev server for testing. Multiple versions of files exist without a clear canonical source.

---

## Phase 1: Pull Everything From the Server

**Script**: `scripts/pull_full_server.sh`
**Time**: ~2 minutes
**What it does**: Downloads every web-facing file from xrlab.ucsd.edu/ka/ into `server_snapshot/`, preserving directory structure.

```bash
cd ~/REPOS/Knowledge_Atlas
bash scripts/pull_full_server.sh
```

**What gets downloaded**:

| Directory | Contents | Count |
|-----------|----------|-------|
| `server_snapshot/` | All root HTML pages + Python backend | ~36 HTML + 2 .py |
| `server_snapshot/160sp/` | Course pages including any new A0 pages | ~30 HTML |
| `server_snapshot/Designing_Experiments/` | Course design tools | ~12 HTML |
| `server_snapshot/data/ka_payloads/` | JSON data files (not the SQLite DB) | varies |

**After the download**, tell Cowork: "server_snapshot is ready" — and we diff everything automatically.

---

## Phase 2: Diff and Merge

Once `server_snapshot/` is populated, Cowork will run an automated diff of every file:

1. **Files identical on both sides** → No action needed (already in sync)
2. **Files only on server** → These are David's direct additions. Copy into repo, commit.
3. **Files only in local repo** → New pages (the 6 user-type homes, new docs). Upload to server.
4. **Files that differ** → The critical category. For each:
   - Generate a side-by-side diff
   - Identify which changes are from the server (auth, A0, student flow) vs. local (nav, footers, design fixes)
   - Merge both sets of changes into a canonical version
   - Present the merge for review

**Expected conflicts** (based on what we know):

| File | Server changes | Local changes | Merge strategy |
|------|---------------|---------------|----------------|
| `ka_home.html` | Auth buttons, possible tweaks | MODE_HOME_PAGES routing | Additive — both sets are independent |
| `ka_user_home.html` | Possibly small A0/auth tweaks | ROLE_HOME_PAGES banner | Additive — both sets are independent |
| `160sp/collect-articles-upload.html` | Backend hookup fixes | Classify badges, real-time feedback | Need to check overlap |
| `ka_auth_server.py` | Production fixes | student_router addition | Check if both present |
| `ka_article_endpoints.py` | A0 endpoints, fixes | Classification heuristics | Check if both present |

---

## Phase 3: Local Dev Server

**Script**: `scripts/start_local_server.sh`
**What it does**: Starts `ka_auth_server.py` which serves ALL static files AND the FastAPI backend on `http://localhost:8765`.

```bash
bash scripts/start_local_server.sh
```

**Key URLs once running**:

| Page | URL |
|------|-----|
| Landing | http://localhost:8765/ka_home.html |
| User dashboard | http://localhost:8765/ka_user_home.html |
| Student home | http://localhost:8765/ka_home_student.html |
| Article upload | http://localhost:8765/160sp/collect-articles-upload.html |
| API docs | http://localhost:8765/docs |
| Health check | http://localhost:8765/health |

**Auth credentials for testing**:
- Instructor: dkirsh@ucsd.edu / value of `KA_BOOTSTRAP_INSTRUCTOR_PASSWORD`
- Students: register via ka_register.html, then approve via ka_approve.html

**Important**: The server auto-reloads when you edit any file, so you can make changes and refresh the browser immediately.

---

## Phase 4: Establish Canonical Structure

After merging, the repo should have this clean layout:

```
Knowledge_Atlas/
├── ka_home.html                    # Landing page (mode selector)
├── ka_user_home.html               # Authenticated dashboard
├── ka_home_student.html            # ← NEW: Student-specific home
├── ka_home_contributor.html        # ← NEW: Contributor-specific home
├── ka_home_instructor.html         # ← NEW: Instructor-specific home
├── ka_home_practitioner.html       # ← NEW: Practitioner-specific home
├── ka_home_researcher.html         # ← NEW: Researcher-specific home
├── ka_home_theory.html             # ← NEW: Theory Explorer home
├── ka_login.html                   # Auth: login
├── ka_register.html                # Auth: registration
├── ka_forgot_password.html         # Auth: password recovery
├── ka_reset_password.html          # Auth: password reset
├── ka_topics.html                  # Topic browser
├── ka_topic_hierarchy.html         # Topic tree view
├── ka_evidence.html                # Evidence browser
├── ka_gaps.html                    # Gap explorer
├── ka_warrants.html                # Warrant inspector
├── ka_articles.html                # Article management
├── ka_article_search.html          # Article search
├── ka_article_propose.html         # Article proposal
├── ka_annotations.html             # Annotation tool
├── ka_argumentation.html           # Argumentation view
├── ka_interpretation.html          # Interpretation tool
├── ka_contribute.html              # Contribution workflow
├── ka_datacapture.html             # Data capture
├── ka_tagger.html                  # Image tagger
├── ka_my_work.html                 # User workspace
├── ka_workflow_hub.html            # Workflow hub
├── ka_hypothesis_builder.html      # Hypothesis builder
├── ka_question_maker.html          # Question maker
├── ka_sensors.html                 # Sensor catalogue
├── ka_neuro_perspective.html       # Neural perspective
├── ka_neuro_grounding_demo.html    # Neural grounding demo
├── ka_explain_system.html          # System explainer
├── ka_ai_methodology.html          # AI methodology
├── ka_ai_system_failures.html      # AI failure documentation
├── ka_instructor_review.html       # Instructor review panel
├── ka_demo.html                    # Demo (legacy)
├── ka_demo_v04.html                # Demo v0.4
├── ka_sitemap.html                 # Sitemap
├── SITEMAP_HIERARCHICAL.html       # Hierarchical sitemap
├── fall160_schedule.html           # Fall schedule
│
├── ka_auth_server.py               # FastAPI backend (auth + static serving)
├── ka_article_endpoints.py         # Article API endpoints
│
├── 160sp/                          # Spring 2026 course pages
│   ├── collect-articles-upload.html
│   ├── ka_student_setup.html
│   ├── ... (28 more course pages)
│   └── context/                    # Course context docs
│
├── Designing_Experiments/          # Course design tools
│   ├── knowledge_navigator.html
│   ├── experiment_wizard.html
│   └── ... (11 more tools)
│
├── data/
│   ├── ka_auth.db                  # SQLite auth database
│   ├── ka_workflow.db              # Workflow state
│   └── ka_payloads/                # JSON data
│       ├── evidence.json
│       ├── workflow.json
│       └── article_visuals/        # Extracted article images
│
├── docs/                           # Architecture & design docs
├── scripts/                        # Utility scripts
├── config/                         # Configuration files
├── tests/                          # Test suite
│
├── server_snapshot/                # ← Downloaded server copy (for diffing)
│   └── (mirrors the above structure)
│
└── quarantine/                     # Archived/deprecated files
```

**Rule going forward**: Every web-facing file has exactly ONE canonical version in the repo root (or its proper subdirectory). `server_snapshot/` is read-only reference. Edits happen in the repo, get tested locally at localhost:8765, then deploy to xrlab via sftp.

---

## Execution Order

| Step | Command | Who | Time |
|------|---------|-----|------|
| 1 | `bash scripts/pull_full_server.sh` | David (Mac terminal) | 2 min |
| 2 | Tell Cowork "server_snapshot is ready" | David | 5 sec |
| 3 | Automated diff + merge report | Cowork | 3–5 min |
| 4 | Review merge decisions | David + Cowork | 10 min |
| 5 | `bash scripts/start_local_server.sh` | David (Mac terminal) | 10 sec |
| 6 | Test merged pages at localhost:8765 | David (browser) | varies |
| 7 | `bash scripts/deploy_home_pages.sh` | David (Mac terminal) | 1 min |
| 8 | Verify on xrlab.ucsd.edu | David (browser) | 2 min |
