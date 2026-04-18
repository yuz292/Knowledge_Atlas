# Track 1 — Image Tagging rubric overview

*Last updated: 2026-04-17*

## Track-level allocation (75 points)

| Deliverable | Span | Hardness | Points | Rubric file |
|-------------|:----:|:--------:|-------:|-------------|
| T1.a Tag-schema study + first 20 tagged images | Week 3 | Easy | 5 | `T1.a_schema_study.md` |
| T1.b Tag 100 images against the full schema | Weeks 3–4 | Medium | 10 | `T1.b_tag_100.md` |
| T1.c Inter-rater kappa with second tagger ≥ 0.7 | Week 4 | Medium-hard | 10 | `T1.c_interrater_kappa.md` |
| T1.d HITL validation on 50-image confusing-cases batch | Weeks 4–5 | Medium | 10 | `T1.d_hitl_validation.md` |
| T1.e Fine-tune / select classifier + error analysis | Weeks 5–6 | Hard | 15 | `T1.e_classifier.md` |
| T1.f Published tag set with provenance (500 images) | Weeks 6–7 | Hard | 15 | `T1.f_published_500.md` |
| T1.g Final report + reflection | Weeks 7–8 | Medium | 10 | `T1.g_final_report.md` |
| **Total** | | | **75** | |

## How the track grades

Every deliverable is scored on the three criteria in `rubrics/README.md` § 3 (Completeness / Quality / Reflection), with the scale rescaled to the deliverable's point value. Verification is automated wherever possible by querying the Atlas tag database (see `verification/t1_query.sql`) and supplemented by the inter-rater kappa protocol (see `verification/t1_kappa_protocol.md`).

## Track-specific conventions

- **Tag correctness is not a free variable.** Ground truth is defined either by the existing tag schema (for deliverables T1.a and T1.b) or by the resolved disagreements from the weekly kappa meeting (for deliverables T1.c onward).
- **Multi-label images are the norm.** A rural park photograph may carry three framework-relevant tags; a windowless office corridor may carry one. Students are not penalised for tagging multiple frameworks when the image genuinely warrants it.
- **Confidence ratings matter.** Each tag carries a 0–1 confidence score from the student. Confidence calibration is part of the Quality criterion at the higher deliverables (T1.e, T1.f).

## Track lead responsibilities

- Confirm the rubric is stable by Week 3 Friday.
- Run the weekly kappa meeting from Week 4 onward.
- Calibrate on a 20-image gold set with the TAs in Week 3 so that grader disagreement in T1.b and T1.c is < 0.15 on any criterion.
