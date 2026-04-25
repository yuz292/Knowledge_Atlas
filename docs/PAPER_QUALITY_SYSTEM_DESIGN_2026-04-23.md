# Paper-Quality System Design

**Document**: `PAPER_QUALITY_SYSTEM_DESIGN_2026-04-23.md`
**Companion**: `PAPER_QUALITY_PANEL_CONSULTATION_2026-04-23.md`
(methodological justification for the design choices below).
**Status**: design-frozen; implementation prompt at
`PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23.md`.

This document specifies the end-to-end pipeline, contracts, database
schema, test plan, overseer reporting, and master-doc integration for
the paper-quality fingerprint layer. The build prompt executes against
this specification verbatim; any change to the design ships as a new
dated version, not as a patch.

---

## 1. System view

Five stages, implemented in order. Each stage is contract-bounded and
independently testable.

**Stage A — Extraction.** Per-paper fingerprint extracted from the
primary-paper PDF and metadata by an LLM pass, with confidence scores
per field and a routing decision (auto-accept, adjudication-queue,
reject).

**Stage B — Adjudication.** A human-in-the-loop surface where the
admin adjudicates fingerprints flagged for review. Writes back into
the fingerprint store with `human_adjudicated = TRUE`.

**Stage C — Paper store.** Adjudicated fingerprints live in a
`paper_quality_fingerprints` table, keyed on `paper_id` with the same
identity convention as the rest of the atlas (`atlas_shared` `paper_id`
as the canonical name; see atlas_shared `ATLAS_SHARED_SCOPE_CONTRACT`).

**Stage D — Aggregation.** Claim-level and literature-body-level
aggregation modules read fingerprints and warrants, compute the
strengths-and-weaknesses summaries, and write them to materialised
views refreshed on every corpus change.

**Stage E — Surface.** An HTTP endpoint and a UI component on the
interpretation page render the summaries alongside the evidence
citations. Overseer reports weekly rollups and flags drift.

The boxology:

```
 primary paper + metadata
          │
          ▼
 ┌───────────────────────┐
 │  A. Extraction        │  LLM, 11 fields, per-field confidence
 └──────────┬────────────┘
            │
       confidence ≥ 0.85?
            │
     ┌──────┴──────┐
  yes│             │ no
     ▼             ▼
 ┌───────┐   ┌───────────────────────┐
 │Auto-  │   │ B. Adjudication queue │
 │accept │   │ (admin UI)            │
 └───┬───┘   └──────────┬────────────┘
     │                  │
     └──────┬───────────┘
            ▼
 ┌───────────────────────┐
 │ C. paper_quality_     │
 │    fingerprints store │
 └──────────┬────────────┘
            ▼
 ┌───────────────────────┐
 │ D. Aggregation        │
 │  ├─ per-claim         │
 │  └─ per-body          │
 └──────────┬────────────┘
            ▼
 ┌───────────────────────┐
 │ E. HTTP + UI surface  │
 │    + overseer reports │
 └───────────────────────┘
```

---

## 2. Stage A — Extraction: contract sketch

Canonical filename at implementation time:
`atlas_shared/contracts/PAPER_QUALITY_EXTRACTION_CONTRACT_2026-04-23.md`.

**Scope**: extract an eleven-field fingerprint from a primary paper's
PDF plus its metadata.

**Inputs**: `paper_id: str` (canonical atlas_shared id), `pdf_path:
Path`, `metadata: ArticleCandidate` (reusing the atlas_shared type).

**Outputs**: `PaperQualityFingerprint` dataclass with the eleven
fields named in the panel consultation, each wrapped as
`FingerprintField(value, confidence, extractor_version, notes)`.
`confidence` is a float in [0, 1]; `extractor_version` is a semver
string.

**Eleven fields**:

1. `n_total: int | None` — sample size
2. `sample_country: list[str]` — ISO-3166 country codes
3. `sample_setting: Literal["research_university", "community",
   "online_panel", "industrial", "clinical", "mixed", "other"]`
4. `sample_weird: bool` — derived from country + setting per Henrich
   et al. (2010). NOT independently extracted.
5. `age_distribution: dict[str, float]` — e.g.
   `{"mean": 23.5, "sd": 4.1, "min": 18, "max": 35}`
6. `design_type: Literal["lab_experiment", "field_experiment",
   "observational_cohort", "online", "secondary_analysis",
   "meta_analysis", "theoretical"]`
7. `preregistered: bool`
8. `preregistration: PreregRecord | None` — includes URL,
   platform, and verification status from a periodic HEAD check
9. `primary_effect_size: EffectSize | None` — value, CI, metric
   (`"d" | "r" | "or" | "hr" | "bayes_factor"`)
10. `statistical_power: PowerRecord` — value, origin
    (`"a_priori_reported" | "retrospective_computed" |
    "not_reported"`)
11. `open_data_url: str | None` — URL with a verification field.

**Human-review-only sidecars**, surfaced alongside but not
aggregated: construct-validity flag, conflict-of-interest severity,
three rhetorical flags (overclaiming, null-suppression,
correlation-as-causation), and field-specific-norms annotation.

**Success conditions**:

1. Extraction precision and recall against a human-adjudicated
   100-paper calibration set is ≥ 85 % per field (for fields that
   apply — not every paper has a primary-effect-size). Failing
   fields are marked low-confidence and routed to adjudication
   queue rather than suppressed.
2. The `PaperQualityFingerprint` is valid JSON under its Pydantic
   schema for 100 % of inputs that return non-null.
3. Preregistration URL verification runs in background with at most
   1 HEAD request per URL per 24 hours. Failed URLs flip
   `preregistration.verified = False` with an explanatory note.
4. No field extracted by the pipeline is written to the fingerprint
   store without `human_adjudicated = True` OR per-field confidence
   ≥ 0.85. Auto-accept threshold is the confidence band.

**Non-promises**:

- The extractor does **not** attempt to extract construct-validity
  flag, COI severity, or rhetorical flags automatically; these are
  human-adjudication-only per the panel's decision.
- The extractor does **not** invent values when the paper is silent.
  Absent means `None`, not a default.
- The extractor does **not** correct known errors in the source
  paper; if the paper reports an impossible N it carries through to
  the fingerprint with a flag, not a fix.

**Tests required**:

- Golden-file tests on 20 hand-curated papers spanning the design
  types, with expected fingerprints checked into `tests/fixtures/`.
- Precision/recall regression against the 100-paper calibration
  set, run weekly and reported to the overseer.
- Roundtrip test: Pydantic → JSON → Pydantic preserves all values.
- URL verification test with a mocked HEAD-request adapter.

---

## 3. Stage B — Adjudication queue: contract sketch

Canonical filename:
`Knowledge_Atlas/contracts/ADJUDICATION_QUEUE_CONTRACT_2026-04-23.md`.

**Scope**: a FIFO queue of fingerprint-extraction events that require
human adjudication, served via the existing instructor admin console
at `/160sp/ka_admin.html`.

**Inputs**: a `FingerprintExtractionEvent` written by Stage A when
one or more fields fall below the auto-accept confidence threshold,
OR when any human-review-only sidecar field has non-null values from
the LLM that require confirmation.

**Outputs**: an adjudicated `PaperQualityFingerprint` with
`human_adjudicated = True`, an `adjudicator_id`, a timestamp, and
optional markdown notes. Writes back to Stage C store.

**Success conditions**:

1. Adjudication queue depth is reported to the overseer daily; depth
   above 50 items triggers a red notification.
2. Adjudicator can see the LLM's suggested value, the primary-paper
   excerpt that justified the suggestion, and the confidence score,
   for every field.
3. The UI exposes the eleven extractable fields and the four
   human-review-only sidecars in the same page.
4. Adjudication events are immutable once written; a correction
   ships as a new event, not an in-place edit.

**Non-promises**:

- No bulk-accept feature. Every adjudication is per-field,
  deliberately.
- No delegation outside instructor accounts.
- Not exposed to any student-tier user.

**Tests required**:

- Integration test with a synthetic low-confidence fingerprint
  written to the queue and read back through the admin UI.
- Authorization test: a student-tier account receives 403 on the
  admin adjudication endpoint.
- Audit-trail test: a written adjudication event cannot be rewritten.

---

## 4. Stage C — Database schema

Three tables and two materialised views. SQL dialect: SQLite for
development, PostgreSQL for deployment. Schema under
`contracts/schemas/paper_quality.sql`.

```sql
-- 4.1 Per-paper fingerprint (one row per paper).
CREATE TABLE paper_quality_fingerprints (
    paper_id              TEXT    PRIMARY KEY,
    extracted_at          TEXT    NOT NULL,
    extractor_version     TEXT    NOT NULL,
    human_adjudicated     INTEGER NOT NULL DEFAULT 0,
    adjudicator_id        TEXT,
    adjudicated_at        TEXT,
    -- Sample cluster
    n_total               INTEGER,
    n_total_confidence    REAL,
    sample_country        TEXT,   -- JSON array of ISO codes
    sample_setting        TEXT,
    sample_weird          INTEGER,
    age_distribution_json TEXT,
    -- Design cluster
    design_type           TEXT,
    preregistered         INTEGER,
    preregistration_url   TEXT,
    preregistration_verified INTEGER,
    preregistration_verified_at TEXT,
    replication_count     INTEGER,
    -- Statistical cluster
    primary_effect_size   REAL,
    primary_ci_lower      REAL,
    primary_ci_upper      REAL,
    primary_metric        TEXT,
    statistical_power     REAL,
    power_origin          TEXT,
    -- Measurement and openness cluster
    primary_measure       TEXT,
    primary_measure_psychometric_ref TEXT,
    open_data_url         TEXT,
    open_data_verified    INTEGER,
    -- Human-review-only sidecars (nullable until adjudicated)
    construct_validity_flag       TEXT,
    construct_validity_notes      TEXT,
    conflict_of_interest_severity TEXT,
    rhetorical_flags_json         TEXT,
    field_norms_version           TEXT,
    -- Aggregate
    overall_confidence    REAL,
    notes_markdown        TEXT
);

-- 4.2 Sample-overlap graph for claim-level N aggregation.
CREATE TABLE sample_overlap_edges (
    paper_id_a  TEXT NOT NULL,
    paper_id_b  TEXT NOT NULL,
    overlap_kind TEXT NOT NULL,  -- "shared_dataset", "shared_authors",
                                 -- "shared_subjects", "meta_of_meta"
    confidence  REAL NOT NULL,
    detected_by TEXT NOT NULL,   -- "author_id", "dataset_doi",
                                 -- "manual", "llm"
    PRIMARY KEY (paper_id_a, paper_id_b, overlap_kind)
);

-- 4.3 Extraction-event audit trail (immutable log).
CREATE TABLE fingerprint_extraction_events (
    event_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id           TEXT    NOT NULL,
    extracted_at       TEXT    NOT NULL,
    extractor_version  TEXT    NOT NULL,
    fingerprint_json   TEXT    NOT NULL,
    routing_decision   TEXT    NOT NULL,  -- "auto_accept",
                                          -- "adjudication_queue",
                                          -- "reject"
    rejection_reason   TEXT,
    FOREIGN KEY (paper_id) REFERENCES paper_quality_fingerprints(paper_id)
);

-- 4.4 Materialised view: claim-level strengths-and-weaknesses.
CREATE VIEW claim_strengths_weaknesses AS
    SELECT
        claim_id,
        -- aggregate fields — see §5 for the computation
        ...
    FROM warrants
    JOIN paper_quality_fingerprints ON warrants.paper_id = ...
    GROUP BY claim_id;

-- 4.5 Materialised view: literature-body-level quality.
CREATE VIEW literature_body_quality AS
    SELECT
        topic_id,
        -- aggregate fields — see §6
        ...
    FROM claims
    JOIN ...
    GROUP BY topic_id;
```

Indexes on `paper_id`, `extracted_at`, and `(human_adjudicated,
overall_confidence)` for the adjudication queue query.

---

## 5. Stage D — Claim-level aggregation: contract sketch

Canonical filename:
`atlas_shared/contracts/CLAIM_STRENGTHS_AGGREGATION_CONTRACT_2026-04-23.md`.

**Scope**: for every claim in the Epistemic Network, compute a
`ClaimStrengthsWeaknesses` structure from the fingerprints of every
warrant that supports or defeats it.

**Inputs**: a `claim_id`, the set of supporting and defeating
warrants, and their papers' fingerprints.

**Outputs**:

```python
@dataclass(frozen=True)
class ClaimStrengthsWeaknesses:
    claim_id: str
    n_supporting: int
    n_defeating: int
    cumulative_n_unique: int         # per panel §4 overlap rule
    cumulative_n_overlap_flagged: bool
    heterogeneity_i_squared: float | None
    heterogeneity_band: Literal["low", "moderate", "high", "n/a"]
    weighted_effect_size: EffectSize | None  # suppressed if I² > 75
    funnel_asymmetry_egger_p: float | None
    replication_rate: float | None    # only if preregistered
                                      # replications exist
    lab_diversity_hhi: float
    construct_validity_dominant: Literal["good", "questionable",
                                          "mixed", "not_assessed"]
    preregistration_share: float
    strengths_markdown: str            # prose summary for UI
    weaknesses_markdown: str
    generated_at: str
    weighting_function_version: str
```

**Success conditions**:

1. Recomputes in O(n_papers_in_claim) per claim; full corpus
   refresh under 90 seconds on the current 1 400-paper corpus.
2. When I² > 75, `weighted_effect_size` is `None` and
   `heterogeneity_band` is `"high"`. Enforced by unit test.
3. `cumulative_n_unique` correctly excludes overlapping samples
   per the `sample_overlap_edges` table. Tested with a fixture of
   three papers where two share a dataset.
4. `construct_validity_dominant` reflects the majority vote across
   adjudicated warrants; "not_assessed" when fewer than two
   warrants have a human-adjudicated flag.
5. Prose summaries are generated by a template with named slots, not
   by an LLM. Deterministic. Tested with snapshot comparisons.

**Non-promises**:

- No adjustment for paper-age within the aggregator; aggregation
  consumes whatever fingerprints Stage A produced without
  re-evaluating publication-year effects.
- No imputation of missing fields from field-wide priors. Missing
  stays missing.
- No ranking of claims by quality. The atlas does not return "best
  claim first"; it returns claims with their quality decomposition.

**Tests**:

- Heterogeneity edge cases: all papers identical (I² near 0), wildly
  different (I² near 100).
- Sample overlap: three papers with known overlap should produce a
  cumulative-N lower than the sum.
- Weighting function snapshot test: given a fixture of five papers
  with known fingerprints, the weighted output matches a
  hand-computed reference.
- Missing-field robustness: one paper with `primary_effect_size =
  None` does not crash the aggregation.

---

## 6. Stage D bis — Literature-body aggregation: contract sketch

Canonical filename:
`atlas_shared/contracts/LITERATURE_BODY_QUALITY_CONTRACT_2026-04-23.md`.

Five summary statistics per topic, per the panel's §5:

1. Total primary-paper count; five-year growth rate.
2. Preregistration share among papers published 2018 or later.
3. Replication-rate estimate (only when preregistered replications
   are indexed; `None` otherwise, with a reason).
4. Cross-citation network density via the
   `cross_citation_graph` maintained in `atlas_shared`.
5. Lab-diversity Herfindahl-Hirschman index over first-author
   institutional affiliations.

**Success conditions**:

1. Full recompute under 5 minutes on current corpus.
2. Handles empty topics without error (returns the structure with
   every field set to `None` and a `reason_empty` field).
3. Preregistration-share numerator includes only papers with
   verified URLs (Stage A verification flag).
4. HHI computed on normalised affiliation names (`atlas_shared`
   affiliation normaliser, which already exists for author
   deduplication).

**Tests**:

- Empty-topic fixture.
- Two-author-per-paper concentration test (HHI lower-bound check).
- Growth-rate regression on a synthetic corpus with known growth.

---

## 7. Stage E — HTTP surface

**New endpoint in the Knowledge Atlas backend**:

```
GET /api/v1/claims/{claim_id}/strengths_and_weaknesses
    → 200 with ClaimStrengthsWeaknesses JSON
    → 404 if claim_id unknown
    → 503 if the materialised view is refreshing (retry-after header)

GET /api/v1/topics/{topic_id}/literature_body_quality
    → 200 with LiteratureBodyQuality JSON
    → 404 if topic_id unknown

GET /api/v1/papers/{paper_id}/fingerprint
    → 200 with PaperQualityFingerprint JSON (instructor/admin only)
    → 403 for non-instructor callers
```

**UI component**: an expandable "Strengths and weaknesses" block on
`ka_journey_interpretation.html` and every claim-detail page. The
block renders the two markdown summaries inline and links to a
second-tier view that shows each supporting warrant with its
fingerprint decomposition.

---

## 8. Overseer integration

The overseer — here meaning the atlas's automation-monitoring role
currently filled by AG with assistance from Codex — receives three
rollups.

**Daily rollup**:

- Adjudication queue depth (count, plus the five oldest items).
- Stage-A extraction volume (papers processed, fields extracted).
- URL verification failures (preregistration, open-data).

**Weekly rollup**:

- Precision/recall against the 100-paper calibration set, with
  field-level breakdown.
- Fields that fell below the 85 % threshold this week.
- Corpus-wide average confidence by field.
- Top ten claims whose strengths-and-weaknesses block changed
  materially this week.

**Alert triggers**:

- Adjudication queue depth > 50 → red.
- Any field's precision falls below 70 % on the calibration set →
  red, with extractor auto-paused for that field pending human
  review.
- Preregistration URL verification failure rate > 20 % in a week →
  yellow (could indicate URL infrastructure drift).

The overseer publishes the rollups to `COORDINATION.md` under a
dedicated heading and to a new
`docs/PAPER_QUALITY_OVERSEER_LOG_<date>.md` file.

---

## 9. Master-doc update

The canonical atlas master document
(`docs/MASTER_DOC_CMR_ASSEMBLED.md`) gains a new section headed
"Paper-Quality Fingerprint Layer", placed between the warrant layer
and the interpretation layer. The section summarises the pipeline in
the boxology of §1, names the contracts under `atlas_shared/contracts/`,
and points at this design document as the source of truth for
questions about specific fields.

An entry in the `docs/AUDIT_README.md` records the 2026-04-23 panel
consultation and commits by SHA the panel document, this design
document, the extraction contract, the two aggregation contracts, the
adjudication queue contract, and the build prompt.

---

## 10. Deliverable checklist (what the build prompt must produce)

| Artefact | Path |
|----------|------|
| `PaperQualityFingerprint` dataclass + Pydantic schema | `atlas_shared/src/atlas_shared/paper_quality.py` |
| Eleven-field extractor with confidence scoring | `Article_Eater/src/services/paper_quality_extraction.py` |
| Adjudication-queue UI | `Knowledge_Atlas/160sp/ka_admin.html` (new tab) |
| Three tables + two views SQL | `contracts/schemas/paper_quality.sql` |
| Claim-level aggregator | `atlas_shared/src/atlas_shared/claim_strengths.py` |
| Literature-body aggregator | `atlas_shared/src/atlas_shared/literature_body.py` |
| HTTP endpoints | `Knowledge_Atlas/backend/app/api/v1/routes/quality.py` |
| UI component | `Knowledge_Atlas/ka_claim_quality.js` plus block on `ka_journey_interpretation.html` |
| Overseer rollup script | `Knowledge_Atlas/scripts/overseer_paper_quality_rollup.py` |
| Master-doc update | `Knowledge_Atlas/docs/MASTER_DOC_CMR_ASSEMBLED.md` |
| Audit-log update | `Knowledge_Atlas/docs/AUDIT_README.md` |
| Eleven contract docs | `atlas_shared/contracts/*_2026-04-23.md` |
| 100-paper calibration-set fixture | `atlas_shared/tests/fixtures/paper_quality_calibration/` |
| Twenty golden-file extraction tests | `Article_Eater/tests/test_paper_quality_extraction.py` |
| Aggregation snapshot tests | `atlas_shared/tests/test_claim_strengths.py`, `test_literature_body.py` |

---
