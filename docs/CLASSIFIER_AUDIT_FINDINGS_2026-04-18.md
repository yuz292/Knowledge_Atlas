# Classifier audit findings — what T2.d.2 can actually cross-check against

*Date*: 2026-04-18
*Author*: CW (per DK request to verify the classifier check-side before building T2.d.2)
*DB audited*: `Article_Eater_PostQuinean_v1_recovery/data/pipeline_registry_unified.db` (1,393 papers, 164 columns; `canonical_classifications` table covers 100 % of corpus with 1,428 rows)
*Audit script*: `scripts/audit_classifiers.py` (re-runnable; sample CSV at `/tmp/classifier_audit_sample.csv`)

---

## 1. Headline finding

The classifier surface is sound enough to support T2.d.2's RAG cross-check, but the topic taxonomy is meaningfully coarser than the rubric draft assumed. Specifically: the topic classifier is a 9 × 18 matrix of modality × outcome, not a free-form fine-grained topic hierarchy. The article-type classifier is rich and well-distributed. The RAG-audit deliverable is viable if we narrow it to checking against the surface that is actually populated, rather than the surface the rubric speculatively imagined.

## 2. What the classifier produces, by surface

### 2.1 Article-type classifier — strong

`canonical_classifications.canonical_article_type` is populated on ~ 1,000 of 1,393 papers with the following distribution:

| Article type | Count |
|---|---:|
| empirical_research | 536 |
| narrative_review | 178 |
| theoretical | 121 |
| qualitative_research | 38 |
| systematic_review | 35 |
| methods_protocol | 28 |
| meta_analysis | 25 |
| journal_article | 14 |
| commentary | 8 |
| (eight others) | 35 |

This is workable. RAG services routinely return papers labelled as "this is a systematic review" or "this is a primary study"; we can check those claims directly.

### 2.2 Topic classifier — coarse but two-dimensional

The topic surface is a Cartesian product of two fields, not a single deep hierarchy:

| Field | Values | Coverage |
|---|---|---:|
| `papers.topic_category` (modality) | 9 values: luminous, spatial, acoustic, natural, material, control, thermal, social_spatial, multisensory | 50 % |
| `papers.topic_subcategory` (outcome) | 18 values: cog.performance, affect.wellbeing, physio, neural, affect.negative.stress, cog.attention, social, affect.preference, affect.comfort, cog.memory, affect.restoration, behav.navigation, affect.soundscape, health, affect.satisfaction, cog.creativity, cog.cognitive_load, mechanism | 49 % |

Crossed, these give 162 possible cells (9 × 18); roughly 40 % are populated. A paper labelled `(luminous, cog.attention)` is "what does daylight do to attention"; `(natural, affect.restoration)` is "what does exposure to natural settings do to recovery". The taxonomy is psychologically sensible and matches how the field actually publishes.

It is **not** a fine-grained topic hierarchy of the sort the original rubric assumed. We do not have entries for "prospect-refuge in office design" or "biophilic effects on creativity in coworking spaces". The classifier's resolution is intentionally one level coarser than that.

### 2.3 `classification_confidence` — reasonable distribution

| Bin | Count |
|---|---:|
| < 0.20 | 5 |
| 0.20–0.40 | 2 |
| 0.40–0.60 | 3 |
| 0.60–0.70 | 5 |
| 0.70–0.80 | 9 |
| 0.80–0.90 | 30 |
| 0.90–0.95 | 46 |
| 0.95–0.99 | **430** |
| 0.99–1.00 | 85 |

Heavy skew toward 1.0 (mean 0.94), but not uniform — the column varies. A separate concern: the column type is TEXT and includes 12 string values (all "high"), which the audit script coerces away. This is an artefact worth fixing in the AE recovery repo (the canonical column should be numeric), but does not block T2.d.2.

### 2.4 What is *not* populated

- `papers.primary_topic_candidate` — 0 % populated (referenced in the design doc but never filled).
- `canonical_triage_decision` — empty across all 1,428 rows.
- `has_classifier_conflict` — flat 0 across all rows. Either no conflicts have ever been detected, or the field is not being written. Worth a separate audit.

These three columns are referenced in the original `UNIFIED_PIPELINE_REFERENCE_FOR_ARTICLE_FINDER.md` documentation but do not actually carry data. The T2.d.2 rubric should not depend on them.

## 3. Implications for T2.d.2

The original T2.d.2 rubric assumed a finer-grained topic classifier than the AE recovery repo actually provides. Three responses, ranked:

### Option A (recommended): narrow the cross-check to the populated surface

The RAG-audit cross-checks each returned paper against:

1. **Article type.** Does the RAG say "systematic review" / "primary study" / "narrative review" / etc., and does that match `canonical_article_type`?
2. **Modality + outcome cell.** Does the RAG-returned paper, when we look up its row in our DB (or run our classifier on its abstract if not present), fall in the same `(topic_category, topic_subcategory)` cell as the RAG implied?
3. **Confidence comparison.** When the RAG service returns its own confidence score (Elicit and Consensus do), how does it correlate with our `classification_confidence`?

This gives the student three concrete, verifiable cross-check axes. The disagreement set is well-defined: the cells where the RAG and our classifier disagree on type, on modality, on outcome, or on confidence calibration.

### Option B: extend the topic taxonomy first

We could extend the AE recovery repo's classifier to produce a finer topic label per paper before T2.d.2 ships. This is the more thorough approach but is a multi-week project: it needs a richer training set, a revised classifier, a re-run over the 1,393-paper corpus, and a reconciliation pass with the existing `canonical_classifications`. Worth doing, but not before the Spring 2026 cohort starts.

### Option C: defer T2.d.2 to Fall 2026

If we conclude that the 9 × 18 surface is too coarse for the audit to be pedagogically interesting, defer T2.d.2 entirely and revisit when the topic classifier has more resolution. I think this is too pessimistic — the article-type axis alone makes the audit interesting, and the modality cross-check on coarse labels still teaches the underlying skill.

**My recommendation: Option A.** Update the rubric to reference the actual classifier surface, build the harvest scripts now, ship T2.d.2 to the cohort with the caveat that the topic axis is coarse. Use student feedback in the first run to inform whether the finer-classifier project is worth queuing for Fall 2026.

## 4. What this audit does not cover

Three honest limitations:

1. **No content-quality assessment.** I did not hand-rate any predictions for correctness. The audit is structural: counts, distributions, coverage. A 20-paper hand-sample CSV is at `/tmp/classifier_audit_sample.csv` for instructor eyeballing — that's the next step if Option A is approved.
2. **No precision/recall against a gold standard.** There is no hand-labelled gold set in the repo. Building one is on the panel-review todo for the AE recovery work.
3. **No drift analysis.** I did not check whether classification_confidence has shifted over time as the corpus grew. The classifier might have been good early and degraded as the topic distribution broadened, or vice versa. This is the long-term dashboard work referenced in `UNIFIED_PIPELINE_REFERENCE_FOR_ARTICLE_FINDER.md` § 4.6.

## 5. Operational note: cross-repo DB path

The classifier DB lives at `Article_Eater_PostQuinean_v1_recovery/data/pipeline_registry_unified.db`, not in this repo. Several scripts in this repo (`scripts/ai_grader.py`, `scripts/audit_classifiers.py`, the FastAPI backend's grading endpoint) will reference this path. Three implementation choices:

1. **Hard-code the absolute path** — brittle on different machines.
2. **Symlink the DB into this repo** — pollutes git status if someone runs `git status` and the symlink isn't gitignored.
3. **Read from `KA_UNIFIED_REGISTRY_DB` env var with the AE recovery repo as default.** — clean, explicit, deploy-friendly.

I have used (3) in `scripts/audit_classifiers.py`. The same pattern should be applied to `scripts/ai_grader.py` and the FastAPI backend in a follow-on commit.

## 6. References

(No new academic references — this is an operational audit. The relevant prior literature on classifier evaluation in scholarly retrieval is cited in the T2.d.2 rubric: Khraisha et al. 2024 on LLM screening, Wang et al. 2024 on Boolean query generation, Thomas et al. 2023 on Elicit precision.)
