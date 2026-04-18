# Assignment rubrics, point allocation, and verification — audit and scaffold

**Date**: 2026-04-17
**Status**: AUDIT — what exists, what's missing, and a proposed framework
**Audience**: DK (instructor), TAs, track leads
**Scope**: All four 160sp tracks plus the Week 1–2 common work

---

## Summary of findings

After a systematic sweep of the 160sp/ directory and repo root for rubric, point-allocation, and verification content:

- **No per-assignment rubrics exist.** The schedule page (`ka_schedule.html`) explicitly promises "Detailed grading rubrics for the track work (Weeks 3–7) ... will be posted on this page before those phases begin" — but no rubric file, table, or inline section has been authored yet.
- **No point allocation exists.** There is no grade breakdown at any level — no "Track 1 worth X%", no "A0 worth Y points", no "this deliverable = Z points of the track total". Grading appears to be on "completion + specificity" per the schedule-page paragraph, which is informal and hard to apply consistently.
- **No verification tests exist for student work.** There are content rubrics (VOI banding for evidence grading, HITL rating rubric for image tags) — those grade the Atlas's CONTENT, not student WORK. There is no automated check, manual checklist, or submission-diff procedure that a TA or the instructor could run to confirm "student X actually did task Y to the required standard."

This is a load-bearing gap. Students cannot know what they are being graded on, TAs cannot grade consistently, and the instructor cannot audit grade decisions after the fact.

---

## Per-track inventory

### Track 1 — Image Tagger

| Artefact | Exists? | Notes |
|----------|:-:|-------|
| Assignment description | yes | `ka_track1_tagging.html` (rich, 3000+ lines) |
| Deliverable list | yes | Tables in the page and in `ka_track1_hub.html` |
| Per-deliverable rubric | **no** | — |
| Point allocation | **no** | — |
| Inter-rater agreement target | partial | Kappa ≥ 0.7 target mentioned informally |
| Verification test | **no** | No automated check of tag correctness |
| Mid-sprint checkpoint | yes | End of Week 5, TA-run 30-minute meeting |

**What a reviewer would want to see:** per-tag-type scoring (crop quality 0-3, tag accuracy 0-3, rationale quality 0-3), a formal kappa-with-second-rater threshold, and a sample-audit protocol the TA can run each week.

### Track 2 — Article Finder

| Artefact | Exists? | Notes |
|----------|:-:|-------|
| Assignment description | yes | `ka_article_finder_assignment.html`, `ka_track2_pipeline.html` |
| Weekly milestones | yes | 15 → 20 → 50 → 150 article targets, phase by phase |
| Per-deliverable rubric | **no** | — |
| Point allocation | **no** | — |
| Evidentiary quality rubric | yes | VOI-banding rubric at `rubrics/voi_banding.md` — grades article quality not student work |
| Verification test | **partial** | Pipeline auto-dedupes and flags relevance; not surfaced as a grading signal |
| Submission checkpoints | yes | Weekly Monday submission expected |

**What a reviewer would want to see:** per-article scoring (relevance 0-3, metadata quality 0-3, evidentiary tagging 0-3), a weekly-submission count target with clear pass/fail thresholds, and a TA-accessible query of the unified registry that surfaces "student X submitted N articles this week, of which M passed relevance."

### Track 3 — VR

| Artefact | Exists? | Notes |
|----------|:-:|-------|
| Assignment description | yes | `ka_track3_vr.html`, `ka_vr_assignment.html` |
| Deliverable list | yes | Per-week in `track3_week_*.html` |
| Per-deliverable rubric | **no** | — |
| Point allocation | **no** | — |
| Demo verification | **no** | No spec for what a passing VR scene looks like |
| Code-review checkpoint | **no** | No spec for what Unity-project structure the TA reviews |

**What a reviewer would want to see:** per-scene scoring (interaction fidelity 0-3, performance 0-3, documentation 0-3), a defined "minimum viable scene" the TA can open in Unity and run a 10-point inspection against, and a per-week code-review checklist.

### Track 4 — UX Research

| Artefact | Exists? | Notes |
|----------|:-:|-------|
| Assignment description | yes | `ka_track4_ux.html`, `ka_gui_assignment.html` |
| Phase-by-phase tasks | yes | `ka_gui_assignment.html` has a detailed walkthrough |
| Per-deliverable rubric | **no** | — |
| Point allocation | **no** | — |
| Heuristic-audit criteria | **partial** | Friction-point taxonomy and severity scoring mentioned |
| Verification test | **no** | No reproducible procedure for validating a usability finding |

**What a reviewer would want to see:** per-finding scoring (specificity 0-3, severity-justification 0-3, recommendation-actionability 0-3), a minimum finding count per week, and a reproducibility check — "can a second student land on the same friction point given the same scenario?"

### Week 1–2 common work (article finding)

| Artefact | Exists? | Notes |
|----------|:-:|-------|
| Task description | yes | Schedule + `week1_agenda.html`, `week2_agenda.html` |
| Minimum count | yes | 20 PDFs by Monday of Week 2, continued submissions |
| Grading basis | **informal** | Schedule page: "completion + specificity" — no scoring rubric |
| Verification | **no** | No automated count, no per-PDF relevance check surfaced to grader |

---

## Proposed framework

To close the gap, I recommend the following three-layer structure. It is deliberately simple — a full rubric system is a multi-quarter effort; this is what can land in one sprint and be improved over time.

### Layer 1: Track-level point allocation

Each track is worth 100 points total, distributed across the 7–8 weeks of track work. Suggested starting allocation (subject to DK's final call):

| Component | Points |
|-----------|-------:|
| Environment setup + Week 1 orientation | 10 |
| A0 + A1 (weeks 2–3 common work) | 20 |
| Per-week track deliverable × 5 weeks | 50 (10 × 5) |
| Mid-sprint checkpoint + quality of collaboration | 10 |
| Final presentation + reflection paper | 10 |
| **Total** | **100** |

### Layer 2: Per-deliverable rubric

Every week's deliverable gets a rubric with three criteria, each scored 0–3 (unacceptable, marginal, good, excellent). Per-week deliverable is worth 10 points, with 1 point awarded per criterion-point above baseline:

| Criterion | 0 (unacceptable) | 1 (marginal) | 2 (good) | 3 (excellent) |
|-----------|------------------|--------------|----------|---------------|
| **Completeness** — did the student produce the expected artefact? | Missing or severely incomplete | < half of expected quantity or major gaps | Meets minimum spec | Exceeds spec with room to spare |
| **Quality** — does the artefact meet the track's quality bar? | Requires full redo | Significant TA corrections needed | Clean after minor polish | Publication-quality as submitted |
| **Reflection** — does the student demonstrate understanding of why this matters? | No evidence of reflection | Surface-level comment | Clear articulation of one aspect | Integrated view across the week's work |

That's 9 possible points across the three criteria; adding 1 point for simply submitting on time gives the 10-point total.

### Layer 3: Verification

Every assignment gets a verification procedure that a TA can run in under ten minutes. Three kinds:

1. **Automated verification** — for tracks where the deliverable lands in a queryable system. Track 1 (image tags → Atlas tag database), Track 2 (articles → unified registry), Track 3 (VR commits → Git). The TA runs one query, sees "student X contributed N items this week, of which M passed downstream validation," grades Completeness and Quality from those numbers.

2. **Manual checklist verification** — for deliverables that don't land in a queryable system. Track 4 (UX findings), reflection papers, presentations. The TA works down a 5–7-item checklist per deliverable with explicit pass/fail language.

3. **Inter-rater verification** — for the assignments where ground truth is itself contested. Track 1 image tagging requires kappa ≥ 0.7 between two independent taggers; if kappa is below threshold, the disagreements are resolved in the weekly sync meeting.

Every verification procedure is documented in a per-assignment Markdown file at `160sp/rubrics/{track}/{week}_{deliverable}.md`. The TA grading sheet records, per student per week, the criterion scores and the verification result. If verification fails (e.g., TA cannot find the student's submissions in the registry), the student has until the next Monday to resolve — but the late flag is recorded permanently.

---

## Proposed scaffold — what I would build next

I can produce the following in one additional session, if you approve:

1. **`160sp/rubrics/README.md`** — the framework above, canonicalised, with a filing system.
2. **`160sp/rubrics/{t1,t2,t3,t4}/week{3..7}_{deliverable}.md`** — twenty rubric files, five per track, each with the 3-criterion × 4-level table pre-populated with track-specific language from the existing assignment descriptions.
3. **`160sp/rubrics/verification/README.md`** — a how-to for TAs showing the automated queries (for Track 1 and Track 2), the manual checklists (for Track 3 and Track 4), and the inter-rater protocol (for Track 1 image tagging).
4. **`160sp/rubrics/grading_sheet_template.xlsx`** — a per-student grading sheet with one row per student per week, pre-populated columns for the three criteria, and auto-summing total columns.
5. **Admin page integration** — a new "Grading" tab on `ka_admin.html` that surfaces the per-student current-grade view by joining the grading sheet with the unified registry.

The scaffold work is about 8–10 hours. The FILL-IN work (writing 20 specific rubrics) is another 8–12 hours of track-lead time, split across TAs if you have them. The verification queries for Track 1 and Track 2 are maybe 2–3 hours since they can use the unified pipeline registry directly.

---

## Trust question: can you currently grade each assignment reliably?

The honest answer is **no, not yet**. The assignment descriptions tell a student what to produce, but the scoring decisions would depend on each TA's read of what "excellent" versus "good" means. Two TAs grading the same submission would likely arrive at different scores because there is no shared rubric to anchor against. This is not a criticism of the course design — it is where every new curriculum lives before rubrics are written; the choice is whether to write them before or after first contact with student work.

For Spring 2026, the pragmatic path is: write the scaffold in Week 3 (before track-specific grading begins), get DK to approve the rubric anchors, run Weeks 3–5 with the rubrics in place, revise at the Week 5 mid-sprint checkpoint based on what turned out to be ambiguous, and ship the revised rubric set for Weeks 6–7. The verification layer can come online the same week: Track 1 and Track 2 can go fully automated immediately; Track 3 and Track 4 use the manual checklist.

If this proposal is approved, say "build the scaffold" and I will produce §1–§5 in the next session. If it needs revision first, the three places most worth questioning are: (a) whether 100 points per track is the right total (could be 100 points for the whole class with tracks weighted), (b) whether 10 points per weekly deliverable is fine-grained enough, and (c) whether the three criteria (completeness / quality / reflection) are the right three or should be four or five.
