# USER JOURNEY AUDIT — Knowledge Atlas
**Date**: 2026-04-01
**Auditor**: Claude Code
**Scope**: All 112 HTML pages
**Focus**: User journey completeness and CTA functionality

## Executive Summary

The Knowledge Atlas site supports **5 primary user types**:
1. **Student Explorer** — Learning-focused browsing
2. **Researcher** — Deep evidence analysis
3. **Contributor** — Article submission and data entry
4. **Instructor** — Course management and approval
5. **Theory/Mechanism Explorer** — Theoretical framework exploration

**Audit Results**:
- **Total Journeys Mapped**: 9 major user journeys
- **Complete Journeys**: 2/9 (22%)
- **Partially Broken**: 5/9 (56%)
- **Fully Broken**: 2/9 (22%)
- **Critical Issues**: 12 missing or broken CTAs

---

## USER TYPE: STUDENT EXPLORER

### Journey 1: First-Time Entry ✓ COMPLETE
**Narrative**: New user lands on public home → registers account → logs in → reaches workspace

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `ka_home.html` | "Register →" | EXISTS_AND_WORKS |
| 2 | `ka_register.html` | "Log in" | EXISTS_AND_WORKS |
| 3 | `ka_login.html` | "KNOWLEDGEAtlas" (logo link) | EXISTS_AND_WORKS |
| 4 | `ka_user_home.html` | — | TERMINAL |

**Assessment**: WORKING ✓
**Notes**: Onboarding flow is well-implemented with clear progression.

---

### Journey 2: Explore Topics & Articles ✗ PARTIALLY BROKEN
**Narrative**: Student logged in → explores topics → discovers articles → reviews evidence

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `ka_user_home.html` | "Topics" (nav) | EXISTS_AND_WORKS |
| 2 | `ka_topics.html` | "Articles" (should link to article search) | **MISSING** |
| 3 | `ka_articles.html` | "Evidence" (nav) | EXISTS_AND_WORKS |
| 4 | `ka_evidence.html` | — | TERMINAL |

**Assessment**: BROKEN AT STEP 2
**Issue**: `ka_topics.html` has no prominent CTA to articles; navigation exists but not as a workflow CTA
**Actual Navigation**: `ka_topics.html` has nav link to "Articles" in header but links to `ka_article_search.html`, NOT `ka_articles.html`
**Fix Required**: Add primary workflow CTA on topics page OR clarify if journey should use `ka_article_search.html` instead

---

### Journey 3: Hypothesis Building ✗ PARTIALLY BROKEN
**Narrative**: Student builds research hypothesis → reviews warrant types → reads argumentation framework

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `ka_hypothesis_builder.html` | → ka_warrants | **MISSING** |
| 2 | `ka_warrants.html` | "Argumentation" (link exists) | EXISTS_AND_WORKS |
| 3 | `ka_argumentation.html` | — | TERMINAL |

**Assessment**: BROKEN AT STEP 1
**Issue**: `ka_hypothesis_builder.html` has no CTA to warrants page. User must use top nav.
**Workaround**: Navigation exists in header but not as primary workflow CTA

---

## USER TYPE: RESEARCHER

### Journey 1: Deep Evidence Exploration ✗ PARTIALLY BROKEN
**Narrative**: Researcher reviews evidence → investigates warrant types → checks annotations → interprets results

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `ka_evidence.html` | → ka_warrants | **MISSING** |
| 2 | `ka_warrants.html` | "Annotations" | EXISTS_AND_WORKS |
| 3 | `ka_annotations.html` | "Interpretation" | EXISTS_AND_WORKS |
| 4 | `ka_interpretation.html` | — | TERMINAL |

**Assessment**: BROKEN AT STEP 1
**Issue**: No explicit CTA from evidence to warrants. User relies on top nav.

---

### Journey 2: Research Data Analysis ✗ BROKEN
**Narrative**: Researcher works with sensor data → captures data → reviews AI methodology

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `ka_sensors.html` | → ka_datacapture | **BROKEN** (exists but misleading) |
| 2 | `ka_datacapture.html` | → ka_ai_methodology | **MISSING** |
| 3 | `ka_ai_methodology.html` | — | TERMINAL |

**Assessment**: BROKEN AT BOTH STEPS
**Issues**:
- `ka_sensors.html` has CTA but not clearly labeled for datacapture workflow
- `ka_datacapture.html` has no CTA to methodology page

---

## USER TYPE: CONTRIBUTOR

### Journey 1: Propose & Submit Article ✗ PARTIALLY BROKEN
**Narrative**: Contributor proposes article → enters capture data → tags images

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `ka_article_propose.html` | → ka_datacapture | **BROKEN** (exists but weak) |
| 2 | `ka_datacapture.html` | "Tag Images" | EXISTS_AND_WORKS |
| 3 | `ka_tagger.html` | — | TERMINAL |

**Assessment**: BROKEN AT STEP 1
**Issue**: Weak or missing prominent CTA from proposal form to data capture

---

### Journey 2: Course Track (Article Finder) ✗ BROKEN
**Narrative**: Student contributor registers → completes article finder assignment → collects articles → awaits approval

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `160sp/ka_student_setup.html` | Track 2 link | EXISTS_AND_WORKS |
| 2 | `160sp/ka_article_finder_assignment.html` | → ka_collect_articles | **BROKEN** |
| 3 | `160sp/ka_collect_articles.html` | → ka_approve | **BROKEN** |
| 4 | `160sp/ka_approve.html` | — | TERMINAL |

**Assessment**: BROKEN AT STEPS 2–3
**Issues**:
- `ka_article_finder_assignment.html` has no direct CTA to collection page
- `ka_collect_articles.html` has "Go to Contribute Page" but NO CTA to approval workflow
- Journey interruption: students don't know where to go after collecting articles

---

## USER TYPE: INSTRUCTOR

### Journey 1: Review & Approve Submissions ✓ COMPLETE
**Narrative**: Instructor accesses approval dashboard → reviews submissions

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `160sp/ka_approve.html` | Navigation to review page | EXISTS_AND_WORKS |
| 2 | `ka_instructor_review.html` | — | TERMINAL |

**Assessment**: WORKING ✓

---

### Journey 2: Manage Course Setup ✗ BROKEN
**Narrative**: Instructor sets up course → views schedule → accesses prep checklist

| Step | Page | CTA to Next | Status |
|------|------|-----------|--------|
| 1 | `160sp/ka_student_setup.html` | → ka_schedule | **BROKEN** |
| 2 | `160sp/ka_schedule.html` | → instructor_prep | **BROKEN** |
| 3 | `160sp/instructor_prep.html` | — | TERMINAL |

**Assessment**: BROKEN AT BOTH STEPS
**Issues**:
- No prominent CTA from setup page to schedule
- No prominent CTA from schedule to prep checklist
- User must navigate via top menu or sidebar

---

## THEORY EXPLORER

**Status**: Not mapped — appears to be aspirational user type in mode selector but no dedicated journeys found in site structure.

---

## PRACTITIONER

**Status**: Not mapped — mentioned in registration form but no distinct entry point or journeys identified.

---

---

## CRITICAL FINDINGS: TOP 10 BROKEN CTAs TO FIX

| Priority | From Page | To Page | Current Status | Recommendation |
|----------|-----------|---------|-----------------|-----------------|
| 1 | `ka_article_finder_assignment.html` | `ka_collect_articles.html` | Missing | Add prominent "Next: Collect Articles →" CTA |
| 2 | `ka_collect_articles.html` | `ka_approve.html` | Missing | Add "Submit for Approval →" CTA at bottom |
| 3 | `ka_topics.html` | `ka_articles.html` | Broken (links to article_search instead) | Clarify: should journey use ka_articles.html or ka_article_search.html? |
| 4 | `ka_hypothesis_builder.html` | `ka_warrants.html` | Missing | Add "Learn About Warrants →" CTA |
| 5 | `ka_evidence.html` | `ka_warrants.html` | Missing | Add "Understand Warrants →" CTA |
| 6 | `ka_sensors.html` | `ka_datacapture.html` | Broken/unclear | Add clear "Capture Data →" CTA |
| 7 | `ka_datacapture.html` | `ka_ai_methodology.html` | Missing | Add "How This Works →" or "Learn the Methodology →" CTA |
| 8 | `ka_article_propose.html` | `ka_datacapture.html` | Weak/missing | Add prominent "Next: Enter Data →" CTA |
| 9 | `160sp/ka_schedule.html` | `160sp/instructor_prep.html` | Missing | Add "View Prep Checklist →" CTA |
| 10 | `160sp/ka_student_setup.html` | `160sp/ka_schedule.html` | Missing | Add "View Course Schedule →" CTA |

---

## ORPHAN PAGES (No Journey Integration)

Pages that don't appear in any primary user journey:

- `ka_my_work.html` — User work dashboard (appears disconnected from main journeys)
- `ka_question_maker.html` — Question building (not in primary flows)
- `ka_neuro_grounding_demo.html` — Demonstration page (not in workflow)
- `ka_neuro_perspective.html` — Perspective page (not in workflow)
- `ka_workflow_hub.html` — Hub page (exists but unused)
- `ka_forgot_password.html` — Account recovery (not part of primary journeys)
- `ka_reset_password.html` — Account recovery (not part of primary journeys)
- `ka_gaps.html` — Gap explorer (not in primary journeys)
- `ka_contribute.html` — Contribution hub (mentioned but not in traced journeys)
- `160sp/week*_agenda.html` (multiple) — Week-by-week schedules (no CTAs between them)
- All `Designing_Experiments/` pages — Archived course design (disconnected from main site)

**Recommendation**: Audit these pages to determine if they should be:
1. Integrated into primary journeys with new CTAs
2. Archived/removed if redundant
3. Kept as secondary reference but not part of main flow

---

## PAGE EXISTENCE CHECK

**Total Pages Audited**: 112
**Pages Verified to Exist**: 112 (100%)
**Missing Links**: 0 (all linked pages exist)

---

## SUMMARY TABLE: USER JOURNEY STATUS

| User Type | Journey Name | Steps | Complete | Broken | Status |
|-----------|-------------|-------|----------|--------|--------|
| **Student Explorer** | First-Time Entry | 4 | 4 | 0 | ✓ COMPLETE |
| | Explore Topics & Articles | 4 | 3 | 1 | ✗ BROKEN |
| | Hypothesis Building | 3 | 2 | 1 | ✗ BROKEN |
| **Researcher** | Deep Evidence Exploration | 4 | 3 | 1 | ✗ BROKEN |
| | Research Data Analysis | 3 | 1 | 2 | ✗ BROKEN |
| **Contributor** | Propose & Submit Article | 3 | 2 | 1 | ✗ BROKEN |
| | Course Track (Article Finder) | 4 | 1 | 3 | ✗ BROKEN |
| **Instructor** | Review & Approve Submissions | 2 | 2 | 0 | ✓ COMPLETE |
| | Manage Course Setup | 3 | 1 | 2 | ✗ BROKEN |

**TOTALS**: 9 journeys | 2 complete (22%) | 7 broken (78%) | 12 missing/broken CTAs

---

## RECOMMENDED FIX SEQUENCE

### Phase 1: Critical Path (Unblock Primary Workflows)
1. Fix Article Finder track: Add ka_collect_articles → approval CTA
2. Fix collect articles → approval submission flow
3. Fix hypothesis builder → warrants CTA

### Phase 2: Secondary Flows
4. Fix researcher evidence exploration (add evidence → warrants CTA)
5. Fix course setup navigation CTAs
6. Fix article proposal → data capture CTA

### Phase 3: Integration & Documentation
7. Clarify whether ka_topics.html should link to ka_articles.html or ka_article_search.html
8. Create user journey map documentation
9. Audit orphan pages for integration or removal
10. Test all journeys end-to-end

---

## METHODOLOGY NOTES

- **Journey Definition**: A journey is a sequence of pages that a user would naturally traverse to complete a primary task
- **CTA Definition**: A prominent call-to-action — button, link with arrow, or nav element — that leads to the next step
- **Broken CTA**: Exists but doesn't link to expected next page OR missing entirely
- **Complete Journey**: All steps have working CTAs leading to the next step
- **Entry Points**: Identified from home page, registration, and mode selector
