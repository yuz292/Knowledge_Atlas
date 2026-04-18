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

## Proposed framework (REVISED 2026-04-17 per DK)

To close the gap, I recommend the following three-layer structure. It is deliberately simple — a full rubric system is a multi-quarter effort; this is what can land in one sprint and be improved over time.

### Layer 1: Class-level point allocation (per DK 2026-04-17)

DK's decision: **100 points for the whole class**, not per track, with the following split:

| Component | Points | Notes |
|-----------|-------:|-------|
| **A0** (common, Week 1–2) | 5 | Orientation / environment / first article find |
| **A1** (common, Week 2–3) | 5 | Second common deliverable; calibration exercise |
| **Track work** (one of T1/T2/T3/T4 per student) | **75** | Distributed across Weeks 3–10; points by assignment hardness, NOT uniform per week |
| **Work on 160F** (Fall 2026 contribution) | 15 | Student contributions to the Fall 2026 restart — site improvements, documentation, transfer packets, next-cohort scaffolding |
| **Total** | **100** | |

**Key corrections from the earlier draft**:

1. Points are allocated by **hardness of the assignment**, not by time elapsed. A single hard deliverable may be worth 15 points; a routine weekly submission may be worth 3.
2. **Assignments may span more than one week.** The rubric file names are anchored to the deliverable, not to the week number. A single rubric may cover a multi-week arc.
3. The 75 track points are sub-allocated per track by the track lead, subject to the constraint that the sub-totals sum to 75 and each track produces roughly 6–9 gradable deliverables over the sprint (Weeks 3–10).
4. The 15 Work-on-160F points recognise that each student's sprint output must, by policy, contribute to the Fall 2026 next-cohort startup. Points are earned for documented artefacts that a Fall student or the Fall instructor can actually use.

See per-track allocation tables below (§ Per-track hardness-weighted allocation) for the 75-point split within each track.

### Per-track hardness-weighted allocation

Each track lead distributes 75 points across 6–9 deliverables. The allocation is not uniform: harder assignments get more points. The tables below are **starting proposals** that track leads should refine at the Week 3 planning meeting.

#### Track 1 — Image Tagging (75 points)

| Deliverable | Span | Hardness | Points |
|-------------|:----:|:--------:|-------:|
| T1.a Tag-schema study + first 20 tagged images | Week 3 | Easy | 5 |
| T1.b Tag 100 images against the full schema | Weeks 3–4 | Medium | 10 |
| T1.c Inter-rater kappa with second tagger ≥ 0.7 | Week 4 | Medium-hard | 10 |
| T1.d HITL validation on 50-image confusing-cases batch | Weeks 4–5 | Medium | 10 |
| T1.e Fine-tune / select classifier + error analysis | Weeks 5–6 | Hard | 15 |
| T1.f Published tag set with provenance (500 images) | Weeks 6–7 | Hard | 15 |
| T1.g Final report + reflection | Weeks 7–8 | Medium | 10 |
| **Total** | | | **75** |

#### Track 2 — Article Finder (75 points)

| Deliverable | Span | Hardness | Points |
|-------------|:----:|:--------:|-------:|
| T2.a Pipeline onboarding + first 15 articles | Week 3 | Easy | 5 |
| T2.b Weekly 20-article batch × 3 weeks (60 articles) | Weeks 3–5 | Medium | 15 (5×3) |
| T2.c VOI-banding calibration against 20-article gold set | Week 5 | Medium-hard | 10 |
| T2.d 50-article topical-coverage sweep (one sub-topic) | Weeks 5–6 | Hard | 15 |
| T2.e Near-miss triage: adjudicate 30 near-miss cases | Week 6 | Medium | 10 |
| T2.f 150-article cumulative target + dedup + topic coverage audit | Weeks 7–8 | Hard | 15 |
| T2.g Final report + reflection | Week 8 | Easy | 5 |
| **Total** | | | **75** |

#### Track 3 — VR (75 points)

| Deliverable | Span | Hardness | Points |
|-------------|:----:|:--------:|-------:|
| T3.a Unity environment + hello-scene commit | Week 3 | Easy | 5 |
| T3.b First interactive scene (one T1-framework mapping) | Weeks 3–4 | Medium | 10 |
| T3.c Second scene + reusable component library | Weeks 4–5 | Medium-hard | 12 |
| T3.d Performance pass — 72 Hz on target hardware | Week 5 | Hard | 10 |
| T3.e User-study pilot (n = 3) with pre/post survey | Weeks 6–7 | Hard | 15 |
| T3.f Polish + documentation for Fall handoff | Weeks 7–8 | Medium-hard | 13 |
| T3.g Final demo + reflection | Week 8 | Easy | 10 |
| **Total** | | | **75** |

Note: T3 totals sum to 75 precisely (5+10+12+10+15+13+10).

#### Track 4 — UX Research (75 points)

| Deliverable | Span | Hardness | Points |
|-------------|:----:|:--------:|-------:|
| T4.a Heuristic audit of K-Atlas public site (10 findings) | Weeks 3–4 | Medium | 12 |
| T4.b Scenario-based walkthrough on 3 archetype user roles | Week 4 | Medium | 10 |
| T4.c Moderated usability pilot (n = 5) | Weeks 5–6 | Hard | 15 |
| T4.d Friction-point severity rubric + prioritised backlog | Week 6 | Medium-hard | 10 |
| T4.e Reproducibility check — second student confirms 5 findings | Week 7 | Hard | 13 |
| T4.f Redesign proposal for one high-severity finding | Weeks 7–8 | Medium | 10 |
| T4.g Final report + reflection | Week 8 | Easy | 5 |
| **Total** | | | **75** |

#### A0 and A1 common work (10 points total across the class)

| Deliverable | Span | Hardness | Points |
|-------------|:----:|:--------:|-------:|
| **A0** — orientation, environment check, first 5 articles into the pipeline | Weeks 1–2 | Easy | 5 |
| **A1** — schema-study submission + 15 additional articles + first reflection | Weeks 2–3 | Medium | 5 |

Within each 5-point assignment, the three-criterion rubric below scales to 0–5 instead of 0–9: criterion scores (0–3 × three criteria) are rescaled to the available points. Straight rescaling: raw 0 → 0 pts; raw 9 → 5 pts; raw 1–8 → round(raw × 5 / 9). A time-on-submission point is already folded in.

#### Work on 160F (15 points across the sprint)

The Fall-2026 contribution is not a weekly assignment — it is an integrated obligation. Each student chooses one of four contribution tracks at the Week 3 planning meeting and delivers across Weeks 5–10.

| Contribution track | Description | Hardness | Points |
|--------------------|-------------|:--------:|-------:|
| **F160.a Documentation** | Write up one workflow (pipeline, tagging, VR build, research protocol) in Fall-ready form | Medium | 15 |
| **F160.b Site improvement** | Land one reviewed PR on K-Atlas (bug fix, feature, accessibility repair) | Medium | 15 |
| **F160.c Transfer packet** | Write the Week-0 onboarding packet the Fall cohort will read first | Medium-hard | 15 |
| **F160.d Scaffolding artefact** | Build one piece of infrastructure (template, rubric draft, sample dataset, tutorial) the Fall instructor can reuse | Hard | 15 |

The 15 points split 5 / 5 / 5 across **shipment** (was it submitted on time and complete?), **usability by a Fall student or instructor who has never seen it** (Fall-reader test, graded at Week 10 review), and **integration** (was it actually merged/linked/cited in the Fall repo before the quarter closes?).

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

## Proposed scaffold — what I am building in this session

1. **`160sp/rubrics/README.md`** — the revised framework, canonicalised, with filing rules.
2. **`160sp/rubrics/{t1,t2,t3,t4}/{deliverable}.md`** — rubric files per deliverable (not per week), pre-populated with the 3-criterion × 4-level table and track-specific language from the existing assignment descriptions.
3. **`160sp/rubrics/common/{a0,a1}.md`** — the two common-work rubrics (A0 and A1) with their 5-point rescaling.
4. **`160sp/rubrics/f160/README.md`** — the Work-on-160F rubric with the four contribution options and the shipment / usability / integration split.
5. **`160sp/rubrics/verification/README.md`** — a how-to for TAs showing the automated queries (for Track 1 and Track 2), the manual checklists (for Track 3 and Track 4), and the inter-rater protocol (for Track 1 image tagging).
6. **`160sp/rubrics/grading_sheet_template.md`** — a per-student grading sheet specification (the actual .xlsx can be generated from this spec using the xlsx skill in a follow-on session, but the spec is the load-bearing artefact).
7. **Admin page integration** — a new "Grading" tab on `ka_admin.html` that surfaces the per-student current-grade view by joining the grading sheet with the unified registry.

The scaffold work is about 8–10 hours of CW time. The FILL-IN work (writing 20+ specific rubrics) is another 8–12 hours of track-lead time, split across TAs if available. The verification queries for Track 1 and Track 2 are 2–3 hours because they can use the unified pipeline registry directly.

---

## Trust question: can you currently grade each assignment reliably?

The honest answer is **no, not yet**. The assignment descriptions tell a student what to produce, but the scoring decisions would depend on each TA's read of what "excellent" versus "good" means. Two TAs grading the same submission would likely arrive at different scores because there is no shared rubric to anchor against. This is not a criticism of the course design — it is where every new curriculum lives before rubrics are written; the choice is whether to write them before or after first contact with student work.

For Spring 2026, the pragmatic path is: write the scaffold in Week 3 (before track-specific grading begins), get DK to approve the rubric anchors, run Weeks 3–5 with the rubrics in place, revise at the Week 5 mid-sprint checkpoint based on what turned out to be ambiguous, and ship the revised rubric set for Weeks 6–7. The verification layer can come online the same week: Track 1 and Track 2 can go fully automated immediately; Track 3 and Track 4 use the manual checklist.

**Status 2026-04-17**: DK resolved the first open question by picking option (a) — 100 points for the whole class, with 5/5/75/15 split across A0/A1/Track/Work-on-160F. The second question (10-point weekly granularity) is also resolved: points are now allocated by hardness, not by week. The third question (the three criteria) remains as drafted — completeness / quality / reflection survive, with the scoring scale rescaled to the point total of each deliverable.

Scaffold files produced in this session:

| File | Purpose |
|------|---------|
| `160sp/rubrics/README.md` | Framework canonical doc |
| `160sp/rubrics/t1/*.md` | Seven T1 deliverable rubrics |
| `160sp/rubrics/t2/*.md` | Seven T2 deliverable rubrics |
| `160sp/rubrics/t3/*.md` | Seven T3 deliverable rubrics |
| `160sp/rubrics/t4/*.md` | Seven T4 deliverable rubrics |
| `160sp/rubrics/common/a0.md`, `common/a1.md` | A0 + A1 rubrics |
| `160sp/rubrics/f160/README.md` | Work-on-160F rubric |
| `160sp/rubrics/verification/README.md` | TA verification procedures |
| `160sp/rubrics/grading_sheet_template.md` | Per-student grading-sheet spec |
