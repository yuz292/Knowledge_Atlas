# Track 2 — Article Finder rubric overview

*Last updated: 2026-04-17*

## Track-level allocation (75 points)

| Deliverable | Span | Hardness | Points | Rubric file |
|-------------|:----:|:--------:|-------:|-------------|
| T2.a Pipeline onboarding + first 15 articles | Week 3 | Easy | 5 | `T2.a_onboarding.md` |
| T2.b Weekly 20-article batch × 3 weeks | Weeks 3–5 | Medium | 15 (5 × 3) | `T2.b_weekly_batches.md` |
| T2.c VOI-banding calibration against 20-article gold set | Week 5 | Medium-hard | 10 | `T2.c_voi_calibration.md` |
| T2.d 50-article topical-coverage sweep (one sub-topic) | Weeks 5–6 | Hard | 15 | `T2.d_topical_sweep.md` |
| T2.e Near-miss triage: adjudicate 30 near-miss cases | Week 6 | Medium | 10 | `T2.e_near_miss_triage.md` |
| T2.f 150-article cumulative target + dedup + coverage audit | Weeks 7–8 | Hard | 15 | `T2.f_cumulative_150.md` |
| T2.g Final report + reflection | Week 8 | Easy | 5 | `T2.g_final_report.md` |
| **Total** | | | **75** | |

## Primary signal: the unified pipeline registry

Every Track 2 deliverable lands in `pipeline_registry_unified.db` (see `docs/UNIFIED_PIPELINE_REFERENCE_FOR_ARTICLE_FINDER.md`). The AI grader reads the registry directly. For the Completeness criterion, a single SQL query covers the count, the dedup check, and the downstream-validation flag. For Quality, the grader reads the full-text PDF paths from the registry and spot-checks relevance against the student's declared sub-topic.

## VOI-banding

The evidentiary quality rubric is at `rubrics/voi_banding.md` (authored separately and referenced from T2.c onward). Students assign each article a VOI band (Very Low / Low / Medium / High / Very High) with a brief justification. The grader verifies band assignment on the calibration set by recomputing the band with the grader's own prompt.

## Track-specific conventions

- **Dedup is a prerequisite.** An article submitted twice by the same student counts once. The pipeline's auto-dedup (DOI match + title-near-match) catches most; the student must not try to defeat it.
- **Relevance is defined against the student's sub-topic, not the course's whole scope.** If a student declares their sub-topic is "soundscape effects on cognitive restoration in urban parks", an article about soundscape perception in concert halls is off-topic for them even though it's on-topic for the course. The grader enforces this at the student level.
- **Abstracts must be pasted, not summarised.** The pipeline's NLP layers read the pasted abstract; a one-sentence summary in place of the abstract will degrade downstream indexing and will cost Completeness points.
