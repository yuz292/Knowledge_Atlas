# atlas_shared Track 2 intake cheat sheet

**Date**: 2026-04-22  
**Audience**: COGS 160 Track 2 (Article Finder) students and maintainers  
**Purpose**: Explain exactly how `atlas_shared` is used when Track 2 filters incoming candidate papers from `ka_contribute.html`, harvested references, and ROI search results.

---

## 1. What this module owns

`atlas_shared` is the canonical decision layer for:

- article identity
- article type
- question relevance
- topic constitution loading
- question-bundle routing
- conservative intake gating

Track 2 code may call this layer. It must not re-implement it.

The public API you should treat as canonical is:

- `atlas_shared.intake.PreExtractionIntakeGate`
- `atlas_shared.topic_bank.load_topic_constitution_bank`
- `atlas_shared.relevance.QuestionArticleRelevanceFilter`
- `atlas_shared.classifier_system.AdaptiveClassifierSubsystem`
- `atlas_shared.bundle_router.QuestionBundleRouter`

---

## 2. Canonical naming decisions

When a paper crosses the `atlas_shared` boundary, use these names:

- `paper_id` = canonical article identity field
- `article_type` = canonical type label emitted by the classifier of record
- `topic` / constitution topic = canonical topic label from the constitution bank
- `bundle_id` = canonical routed question-bundle identifier, assigned by the constitution/router layer rather than handwritten by students

Practical rule:

- Do not invent your own `article_id`.
- Do not hand-construct bundle IDs.
- Do not maintain a private article-type vocabulary in Track 2 code.

---

## 3. When to use it

Use the same `atlas_shared` sequence in all three Track 2 intake lanes:

1. incoming public or student submissions from `ka_contribute.html`
2. harvested references from T2.a / T2.d
3. retrieved candidates from ROI or PNU search lanes

The point is consistency. A paper should not receive one article type when it arrives through `ka_contribute.html` and a different one when it arrives through a reference-harvest queue.

---

## 4. The correct intake sequence

### Step 1 — normalise the candidate

Before any relevance decision, construct a single candidate record with as much arrival-time evidence as you actually have:

- `paper_id`
- `title`
- `abstract`
- `doi`
- `keywords`
- `first_page_text` if available
- local PDF path if available

If the input is sparse, say that honestly. Do not pad it.

### Step 2 — run the conservative intake gate first

Call `PreExtractionIntakeGate.assess(...)` on the candidate.

This gate is intentionally conservative. It is allowed to:

- accept a candidate
- send it to edge-case or manual review
- hold it for missing metadata
- reject only clear false positives

It is not a broad exclusion device.

### Step 3 — load the canonical topic constitutions

Use:

- `load_topic_constitution_bank()`

This gives you the panel-derived topic evidence base. Treat those constitutions as the source of canonical topic IDs and bundle logic.

### Step 4 — classify article type and relevance

Use:

- `AdaptiveClassifierSubsystem` for the staged article-level decision
- `QuestionArticleRelevanceFilter` for per-question relevance

The classifier is the article-type classifier of record. The relevance filter is the question-level on-topic test of record.

### Step 5 — route accepted papers to bundles

Once the paper is accepted or kept alive as a plausible edge case, route it with:

- `QuestionBundleRouter.route_article(...)`

This yields:

- `paper_id`
- `primary_topic`
- `primary_bundle_id`
- ranked candidate bundles

This is the canonical source for question-bundle assignment.

### Step 6 — write downstream facts using canonical fields

After routing, persist:

- `paper_id`
- `article_type`
- best question relevance verdict
- best question confidence
- `primary_topic`
- `primary_bundle_id`

If your queue writes registry facts, use the canonical field names and the real module dotted path in `source_subsystem`.

---

## 5. A minimal usage pattern

The exact wrapper differs by repo, but the logical sequence should look like this:

```python
from atlas_shared import (
    AdaptiveClassifierSubsystem,
    PreExtractionIntakeGate,
    QuestionBundleRouter,
    load_topic_constitution_bank,
)

bank = load_topic_constitution_bank()
constitutions = bank.constitutions

gate = PreExtractionIntakeGate(constitutions)
gate_result = gate.assess(candidate_mapping)

classifier = AdaptiveClassifierSubsystem(constitutions)
classification = classifier.classify(candidate_mapping)

router = QuestionBundleRouter(constitutions)
routing = router.route_article(candidate_mapping)
```

Use this as a sequence sketch, not as a copy-paste promise that every repo wrapper has the same local variable names.

---

## 6. What Track 2 students should do, and not do

### Do

- treat `paper_id` as canonical
- let `atlas_shared` decide article type
- let the constitution bank define topic boundaries
- let the router assign bundle membership
- send ambiguous or adjacent cases to review rather than forcing a reject

### Do not

- maintain a parallel private topic-ID system
- create Track 2-only article-type labels
- collapse manual-review and hard-reject into one bucket
- edit `atlas_shared` from the Track 2 repo
- silently discard candidates that merely lack abstracts

---

## 7. Where this matters most in Track 2

- **T2.a / T2.d**: filtering and deduplicating incoming referenced papers
- **T2.b**: screening candidate abstracts and assigning article type + question relevance
- **T2.e**: vetting ROI search results before they reach a researcher
- **T2.f**: routing neural-grounding papers through the same topic/bundle logic as every other paper

---

## 8. Contracts to read before editing intake logic

- `atlas_shared/contracts/PRE_EXTRACTION_INTAKE_CONTRACT_2026-04-17.md`
- `atlas_shared/contracts/PANEL_TOPIC_EVIDENCE_CONTRACT_2026-04-17.md`
- `Knowledge_Atlas/160sp/REGISTRY_NOTIFICATION_CONTRACT_2026-04-08.md`

---

## 9. One-sentence rule

If Track 2 is filtering incoming candidate papers, it should call `atlas_shared` and record the canonical outputs; it should not invent a second classification and ID system of its own.
