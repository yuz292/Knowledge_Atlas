# Site Review Prompt: K-ATLAS Functional & UX Audit

**Date**: 2026-04-12
**From**: David Kirsh (via CW)
**To**: AG and Codex
**Action requested**: Two independent reviews — one functional/interactivity, one user-experience/clarity
**Priority**: HIGH — We are going live with students next week (Week 3). Blocking bugs must be found now.

---

## Context

The K-ATLAS site is running locally at `http://localhost:8765` and mirrors the production server at `https://xrlab.ucsd.edu/ka/`. CW has completed a full integration pass:

- **All static pages** serve from a single FastAPI process (ka_auth_server.py) with a catch-all static file route
- **21/21 API endpoint tests pass** (registration, login, profile, track signup, article submission, question claiming, password/email changes, refresh tokens, student progress)
- **Track names standardized** across 20+ files to the canonical four: Track 1: Image Tagger, Track 2: Article Finder, Track 3: AI & VR, Track 4: Interaction Design
- **Track signup form** wired to POST /auth/update-track with auth-gating, profile pre-fill, and success/error states
- **Production bug fixed**: ka_article_endpoints.py had an undefined variable (`task1_experimental`) in the my_claim endpoint that would have caused 500 errors for all students checking A0 progress

**Local server startup**: `bash scripts/run_local_site.sh` (port 8765)
**Test credentials**: dkirsh@ucsd.edu / value of `KA_BOOTSTRAP_INSTRUCTOR_PASSWORD`
**API docs**: http://localhost:8765/docs

### What has NOT been reviewed yet

1. End-to-end user flows from the student's perspective (not just API calls)
2. Whether help modals, tooltips, and instructional text are sufficient for first-time users
3. Whether the A0 assignment flow is clear enough for students who have never used the system
4. Whether non-student user types can accomplish their tasks
5. Cross-browser behavior, responsive/mobile layout
6. Error recovery paths (what happens when things go wrong mid-flow)

---

## The Two Reviews

### REVIEW 1: Functional Interactivity Audit

**Goal**: Find every bug, broken flow, or silent failure a real user would encounter.

Test every interactive element on the site. For each page that has auth, forms, uploads, or dynamic content, walk through the flow as a real user would. Report bugs in a table with: page, action, expected behavior, actual behavior, severity (P0 critical / P1 major / P2 minor).

#### Specific flows to test

**A. Authentication flows**

| Flow | Entry point | What to test |
|------|------------|--------------|
| Registration | ka_register.html | Does the form submit? Does validation work (email format, password length, required fields)? What happens if email is already registered? Is the success/error feedback clear? |
| Login | ka_login.html | Does login work with valid credentials? What happens with wrong password? Is the JWT stored in localStorage? Does the page redirect correctly? |
| Forgot password | ka_forgot_password.html | Does the flow work end-to-end? What feedback does the user get? |
| Session expiry | Any auth-gated page | What happens when the JWT expires mid-session? Is there a graceful redirect to login, or does the page silently break? |
| Logout | Nav bar logout button | Does it clear localStorage? Does it redirect? Can the user access auth-gated pages after logout? |

**B. Article upload pipeline (collect-articles-upload.html)**

This is the most complex interactive page on the site. Test thoroughly:

| Flow | What to test |
|------|-------------|
| Tab switching | Do the Q1 (Task 1) and Q2 (Task 2) tabs work? Does the tab state persist? |
| PDF upload | Drag-and-drop and click-to-upload. Does the file appear? Can you remove it? Multiple files? |
| Metadata auto-fill | After uploading a PDF, does the system attempt to extract title/authors? |
| Duplicate check | POST /articles/check-duplicate — does it fire before submission? What feedback? |
| Submission | POST /articles/submit — does it work with valid data? What about missing fields? |
| Progress bars | Do the Task 1 and Task 2 progress cards update after submission? |
| Brownie offer | After completing 10 articles in Task 1, does the brownie/extra-credit offer appear? |
| Error states | What happens if the server is unreachable? If the upload fails? If the PDF is too large? |

**C. Track signup (ka_track_signup.html)**

| Flow | What to test |
|------|-------------|
| Auth gate | Does the page show "Login Required" when not authenticated? |
| Profile pre-fill | After login, does it pre-fill name and email from /auth/me? |
| Track selection | Does the dropdown show all 4 tracks with correct names? |
| Submission | Does POST /auth/update-track work? What feedback on success? |
| Already signed up | If the user already has a track, does it show their current track and prevent re-signup (or allow change)? |

**D. Question claiming (collect-articles-upload.html)**

| Flow | What to test |
|------|-------------|
| Available questions | GET /articles/available-questions — does the list load? |
| Claiming | POST /articles/claim — does it work? What if the question is already claimed by max students? |
| My claim | GET /articles/my-claim — does it reflect the claimed question? |
| Release | POST /articles/release — can the student release a claim? |

**E. Other auth-gated pages**

| Page | What to test |
|------|-------------|
| ka_account_settings.html | Can user change password, email? Does validation work? |
| ka_approve.html (instructor) | Does the approval queue load? Can instructor approve/reject articles? |
| ka_dashboard.html | Does it show the student's progress? Correct data? |
| 160sp/instructor_prep.html | Does it load instructor-specific data? |

**F. Navigation and linking**

| Test | What to check |
|------|--------------|
| All nav links | Click every link in the nav bar on at least 5 representative pages. Do they all resolve? |
| Breadcrumbs | Are breadcrumbs present and correct on course (160sp/) pages? |
| 404 behavior | What happens when you navigate to a nonexistent page? |
| Back button | Does the browser back button work correctly after form submissions? |
| Deep linking | Can you bookmark and return to auth-gated pages? Does it redirect to login and then back? |

#### Output format for Review 1

```markdown
## Bug Report

| # | Page | Action | Expected | Actual | Severity | Notes |
|---|------|--------|----------|--------|----------|-------|
| 1 | ... | ... | ... | ... | P0/P1/P2 | ... |

## Flows That Work Correctly
[List flows that passed without issues — important for confidence]

## Recommendations
[Prioritized list of fixes needed before go-live]
```

---

### REVIEW 2: User Experience & Clarity Audit

**Goal**: Evaluate whether each user type can accomplish their tasks with reasonable clarity, and identify the worst UX friction points before students arrive.

This review is about comprehension, not bugs. A page can be "working" (Review 1 passes) but incomprehensible to its intended user.

#### The six K-ATLAS user types

From `agents/GUI_AGENT_V3.md` and `ka_workflows.js`:

| Role | Display name | Primary need | Key pages |
|------|-------------|--------------|-----------|
| `student_explorer` | Student Explorer | Orient, browse, find first questions | ka_student_setup.html, collect-articles-upload.html, ka_schedule.html, ka_tracks.html, ka_track_signup.html, week*_agenda.html |
| `contributor` | Contributor | Add articles, tag evidence, expand corpus | ka_home_contributor.html, ka_contribute.html, collect-articles-upload.html |
| `researcher` | Researcher / PI | Synthesize evidence, test hypotheses, find gaps | ka_home_researcher.html, ka_evidence.html, ka_article_search.html, ka_gaps.html |
| `practitioner` | Practitioner | Design decisions backed by evidence | ka_home_practitioner.html, ka_evidence.html |
| `instructor` | Instructor | Student onboarding, assignment scaffolding, grading | ka_home_instructor.html, instructor_prep.html, ka_approve.html, ka_schedule.html |
| `theory_mechanism_explorer` | Theory / Mechanism Explorer | Trace mechanisms, test competing accounts | ka_home_theory.html, ka_argumentation.html, ka_evidence.html |

#### Critical UX issues already identified

**A0 Task 2 Topic Selection — KNOWN BAD DESIGN**

David has flagged this explicitly: "the current A0 is badly designed because students barely see how to create the topic list of task 2."

Here is what we found:

1. **Topic selection is buried in a tab**. On `collect-articles-upload.html`, Task 2 is the second tab. The tab badge says "Choose topic" but students who are focused on Task 1 (their assigned question) may never click it.

2. **The topic selector is a cramped select-size-10 dropdown** inside the Task 2 tab panel. The questions are rendered as plain text in a narrow box. There is no search, no filtering, no categorization, no preview of what the question means or why it matters.

3. **No modal help or tooltip** explains what Task 2 is, why it matters, or how to choose a good topic. The instructional text is a paragraph above the selector that students will likely skim.

4. **No first-time-use guidance**. When a student first arrives at the upload page, there is no onboarding flow, no "Step 1: Choose your question, Step 2: Upload articles" wizard, no visual indication of which task to do first.

5. **Q2 feels secondary**. The page structure implies Q1 is the "real" task and Q2 is optional or supplementary. In reality, both are required components of A0.

6. **No way to preview or change topic easily**. Once selected, the topic is locked by a claim. Students who chose hastily have no obvious recourse.

**Your job**: Propose concrete design improvements for the A0 Task 2 flow. Consider: dedicated onboarding modal on first visit, split-screen Task 1 / Task 2 view, topic cards with descriptions instead of a flat dropdown, prominent "Choose Your Topic" CTA before any uploads are enabled, progress indicators that show both tasks are required.

#### Questions for each page

For every student-facing page (listed below), answer:

1. **3-second test**: If a student lands on this page for the first time, what will they think it is for within 3 seconds? Is that correct?
2. **Primary action clarity**: Is the single most important thing to do on this page visually obvious? Or does the student have to read paragraphs to figure out what to do?
3. **Help availability**: If the student doesn't understand something, is there a help modal, tooltip, FAQ section, or link to guidance? Or are they left to figure it out?
4. **Error recovery**: If the student makes a mistake (wrong file, wrong field, wrong choice), how do they recover? Is the recovery path obvious?
5. **Progress visibility**: Can the student see where they are in the overall assignment flow? Do they know what they've done and what's left?
6. **Mobile usability**: Is this page usable on a phone or tablet? Students often work from mobile devices.

#### Pages to evaluate

**High priority (students will use these in Week 3)**:

| Page | Why it matters |
|------|---------------|
| `ka_student_setup.html` | First page students see after registration. Must orient them clearly. |
| `ka_schedule.html` | Course schedule. Students need to find what's due and when. |
| `collect-articles-upload.html` | The A0 assignment hub. Most complex student page. |
| `ka_track_signup.html` | Track selection. Must be completed before Week 3 labs. |
| `ka_tracks.html` | Track overview. Students browse before choosing. |
| `ka_technical_setup.html` | Technical requirements for each track. |
| `week1_agenda.html` through `week3_agenda.html` | Weekly session agendas. Students reference during class. |

**Medium priority (students will use later)**:

| Page | Why it matters |
|------|---------------|
| `ka_track1_tagging.html` | Track 1 portal. Image Tagger students need clear instructions. |
| `ka_track2_pipeline.html` | Track 2 portal. Article Finder instructions. |
| `ka_track3_vr.html` | Track 3 portal. AI & VR instructions. |
| `ka_track4_ux.html` | Track 4 portal. Interaction Design instructions. |
| `ka_dashboard.html` | Student progress dashboard. |
| `ka_google_search_guide.html` | Guide for finding scientific articles. |
| `ka_article_finder_assignment.html` | Detailed A0 instructions. |

**Lower priority (non-student users)**:

| Page | Why it matters |
|------|---------------|
| `ka_home.html` | Landing page for all user types. |
| `ka_home_contributor.html` | Contributor home. |
| `ka_home_researcher.html` | Researcher home. |
| `ka_home_instructor.html` | Instructor home. |
| `ka_evidence.html` | Evidence browser. Core research tool. |
| `ka_article_search.html` | Article search. |
| `ka_gaps.html` | Research gap finder. |

#### Output format for Review 2

```markdown
## Page-by-Page UX Assessment

### [Page name] — [page file]
- **3-second impression**: [what user thinks this page is for]
- **Correct?**: Yes / Partially / No
- **Primary action clarity**: [Clear / Ambiguous / Buried]
- **Help availability**: [Good / Partial / Missing]
- **Error recovery**: [Good / Partial / Missing]
- **Progress visibility**: [Good / Partial / Missing]
- **Mobile usability**: [Good / Acceptable / Poor]
- **Key issues**: [bulleted list of specific problems]
- **Recommended fixes**: [bulleted list of concrete improvements]

## A0 Task 2 Redesign Proposal
[Detailed proposal addressing the 6 issues listed above]

## Cross-Cutting UX Issues
[Problems that affect multiple pages — inconsistent patterns, missing conventions, etc.]

## Priority Matrix
| Fix | Impact | Effort | Priority |
|-----|--------|--------|----------|
| ... | High/Med/Low | High/Med/Low | P0/P1/P2 |
```

---

## Reference Documents

Read these before starting your review:

| Document | Location | Why |
|----------|----------|-----|
| GUI Agent v3 spec | `agents/GUI_AGENT_V3.md` | Defines the 6 user roles, design principles, 32-item page evaluation framework, V1-V17 viz checklist |
| KA User Personas | `../Article_Eater_PostQuinean_v1_recovery/docs/KA_USER_PERSONAS_AND_USE_CASES_2026-03-16.md` | Detailed persona profiles, goals, pain points |
| Navigation Architecture Plan v2 | `160sp/KA_NAVIGATION_ARCHITECTURE_PLAN_v2.md` | The nav redesign plan (already sent for review separately) |
| ka_workflows.js | `ka_workflows.js` | Role to workflow mapping; 6 roles, 9 workflows |
| API docs | http://localhost:8765/docs | FastAPI auto-generated endpoint documentation |
| Test harness | `scripts/ka_test_harness.py` | Shows all 21 tested endpoints and expected responses |
| Earlier nav review prompt | `160sp/REVIEW_PROMPT_FOR_AG_AND_CODEX.md` | The navigation architecture review (different scope — that was architecture, this is live functionality) |

---

## Coordination Notes

- **This is a NEW review**, distinct from the navigation architecture review at `REVIEW_PROMPT_FOR_AG_AND_CODEX.md`. That review was about the proposed nav redesign. This review is about the current live site functionality and UX.
- **Split the work**: AG takes Review 1 (functional), Codex takes Review 2 (UX), or vice versa. Or both do both independently for cross-validation. David's preference is for independent assessments that can be compared.
- **Severity definitions**: P0 = students cannot complete a required task (blocks go-live). P1 = students will be confused but can work around it. P2 = polish issue, fix when convenient.
- **Timeline**: We need this before the Week 3 push to production. Findings should be committed to `160sp/` so CW can pick up fixes.
- **Output files**: Save your review as `160sp/SITE_REVIEW_AG_2026-04-12.md` or `160sp/SITE_REVIEW_CODEX_2026-04-12.md` respectively.

---

## Summary of What Matters Most

In priority order:

1. **A0 upload flow** (collect-articles-upload.html) — the most complex page, the one students must use first, and the one David has flagged as having bad Task 2 discoverability
2. **Auth flows** — registration to login to session persistence to logout must work flawlessly; any break here blocks everything
3. **Track signup** — must work before Week 3 labs
4. **Student orientation** — ka_student_setup.html and ka_schedule.html are students' first contact with the system; they must be crystal clear
5. **Error recovery everywhere** — students will make mistakes; the system must help them recover gracefully, not fail silently
6. **Non-student user types** — lower priority but these pages represent the broader K-ATLAS vision; flag issues for later

Thank you. This is the last review gate before students start using the system.
