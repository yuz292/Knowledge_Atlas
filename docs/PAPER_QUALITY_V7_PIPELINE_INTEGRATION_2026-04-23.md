# Paper-Quality Layer — V7 Pipeline & Lifecycle-DB Integration

**Document**: `PAPER_QUALITY_V7_PIPELINE_INTEGRATION_2026-04-23.md`
**Companions**: panel consultation, system design, decision tree,
calibration strategy (all dated 2026-04-23).
**Date**: 2026-04-23.
**Purpose**: specify how the paper-quality fingerprint pipeline plugs
into the existing V7 extraction pipeline and the
`pipeline_lifecycle_full.db` so every paper's quality status is
observable from the canonical lifecycle view, and so the layer is not
a parallel system that the rest of the atlas does not see.

DK's question: "have you integrated this in the v7 pipeline including
lifecycle db". The answer in the original system design was "not
explicitly, but should be." This document closes that gap.

---

## 1. The integration principle

The paper-quality layer must be a stage of the V7 pipeline, not an
adjacent service that happens to share the same paper IDs. The reason
is observability: the lifecycle database is the canonical view of
"where is this paper in its journey", and any layer that reads or
writes per-paper data without registering as a stage is invisible to
the overseer, the admin console, and any downstream debugging.

The integration adds **two new lifecycle stages**, **three new
auxiliary tables**, **eleven new lifecycle-event types**, and one
modification to the existing `papers.current_stage` enumeration. No
existing stage is removed or renumbered; new stages slot in by
inserting at specific stage_order positions.

---

## 2. The two new lifecycle stages

The existing pipeline runs in stage_order from 1 (`acquisition`) to
28 (`site_display`), in eight layers (Intake → Extraction → Synthesis
→ Semantics → EN Layer → Reasoning → BN Layer → Presentation). The
paper-quality work is a Synthesis-layer activity (it operates on the
gold-validated paper to produce a structured per-paper artifact),
inserted between `tag_assignment` (current stage_order 17) and
`web_integration` (current stage_order 18).

Inserting two stages at stage_order 18 and 19 renumbers the existing
stages 18–28 to 20–30. The migration is mechanical because
stage_order is an integer column the lifecycle event-writer respects.
The new stages are:

### 2.1 Stage 18 — `paper_quality_extraction` (Synthesis)

Runs the multi-LLM extractor specified in
`PAPER_QUALITY_CALIBRATION_STRATEGY_2026-04-23.md` §2.2. Inputs: the
gold-accepted paper (stage 9) + the structured tags (stage 17).
Output: a `PaperQualityFingerprint` candidate written to the new
`fingerprint_staging` table, plus a lifecycle event recording per-field
confidences and the routing decision (auto-accept all fields,
adjudication-required for one or more fields, or reject due to
extractor error).

A paper at stage 18 with status `complete` and routing
`auto_accept` proceeds to stage 19 immediately. A paper with routing
`adjudication_required` halts at stage 18 with status `awaiting_human`
and waits for the adjudication queue to drain.

### 2.2 Stage 19 — `paper_quality_finalisation` (Synthesis)

Runs only when stage 18's adjudication is complete (or was
auto-accepted). Promotes the candidate fingerprint from
`fingerprint_staging` to `paper_quality_fingerprints`, recomputes
any claim-level aggregates that depend on this paper's warrants,
and emits the finalisation event. A paper at stage 19 with status
`complete` proceeds to stage 20 (the renumbered `web_integration`).

The split into two stages serves two purposes. First, it makes the
"awaiting human adjudication" state a first-class lifecycle state
visible in the overseer rollup. Second, it cleanly separates the
extractor's work (stage 18) from the aggregator's work (stage 19),
so a re-run of either does not necessarily re-run the other.

---

## 3. Lifecycle DB schema changes

Three sets of changes to `pipeline_lifecycle_full.db`. All are
additive; no existing column is removed or retyped.

### 3.1 `stage_definitions` — two new rows, others renumbered

```sql
-- Insert the two new stages at stage_order 18 and 19.
INSERT INTO stage_definitions
    (stage_id, stage_name, layer, description, typical_agent, stage_order)
VALUES
    (29, 'paper_quality_extraction',  'Synthesis',
     'Extract per-paper quality fingerprint via multi-LLM pass',
     'extractor', 18),
    (30, 'paper_quality_finalisation', 'Synthesis',
     'Promote candidate fingerprint to production after adjudication',
     'aggregator', 19);

-- Renumber existing stages 18..28 to 20..30. (One UPDATE per row;
-- shown abbreviated here.)
UPDATE stage_definitions SET stage_order = 20 WHERE stage_name = 'web_integration';
UPDATE stage_definitions SET stage_order = 21 WHERE stage_name = 'warrant_assignment';
-- ... continue through site_display → 30
```

The `stage_id` of new stages uses the next unused integers (29, 30)
to preserve referential integrity for any existing
`lifecycle_events.stage_id` foreign keys. The `stage_order` is the
visible ordering.

### 3.2 `papers.current_stage` enumeration

The existing column allows free-text values. Documented permitted
values gain `paper_quality_extraction` and `paper_quality_finalisation`.
A paper currently at `tag_assignment` (the prior stage 17) on the day
of migration moves to the new stage 18 by the migration script.

### 3.3 Three new auxiliary tables

```sql
-- 3.3.1 Staging area for candidate fingerprints awaiting adjudication.
CREATE TABLE fingerprint_staging (
    paper_id              TEXT    PRIMARY KEY,
    extracted_at          TEXT    NOT NULL,
    extractor_version     TEXT    NOT NULL,
    fingerprint_json      TEXT    NOT NULL,  -- candidate fingerprint
    confidence_per_field  TEXT    NOT NULL,  -- JSON map field→confidence
    routing_decision      TEXT    NOT NULL,
    fields_awaiting_adjudication TEXT  -- JSON array of field names
);

-- 3.3.2 Adjudication queue keyed by node, not by paper.
CREATE TABLE quality_adjudication_queue (
    queue_item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id            TEXT    NOT NULL,        -- e.g. '4.1.preregistration_url_valid'
    paper_id           TEXT    NOT NULL,
    field_name         TEXT    NOT NULL,
    llm_a_suggestion   TEXT,
    llm_b_suggestion   TEXT,
    llm_a_confidence   REAL,
    llm_b_confidence   REAL,
    excerpt_markdown   TEXT,                    -- the source excerpt
    created_at         TEXT    NOT NULL,
    adjudicated_at     TEXT,
    adjudicator_id     TEXT,
    final_value        TEXT,
    adjudicator_notes  TEXT,
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
);

-- 3.3.3 Per-field calibration history (anchor-set drift tracking).
CREATE TABLE quality_calibration_history (
    calibration_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    field_name            TEXT    NOT NULL,
    measured_at           TEXT    NOT NULL,
    extractor_version     TEXT    NOT NULL,
    anchor_agreement_pct  REAL    NOT NULL,
    n_anchor_papers       INTEGER NOT NULL,
    auto_accept_threshold REAL    NOT NULL,
    notes                 TEXT
);
```

Indexes: `quality_adjudication_queue(node_id, adjudicated_at)` for
the per-node-batch query; `fingerprint_staging(routing_decision)` for
the awaiting-adjudication count; `quality_calibration_history(field_name,
measured_at)` for drift charts.

### 3.4 Eleven new lifecycle-event types

The existing `lifecycle_events.evidence` JSON column accommodates new
event types without schema change. The new event types — recorded
when stage 18 or 19 emits them — are:

| Event type | Stage | Carries |
|------------|-------|---------|
| `quality_extracted` | 18 | per-field confidence vector |
| `quality_routing_auto_accept` | 18 | confirmation all fields ≥ threshold |
| `quality_routing_adjudication` | 18 | list of fields awaiting adjudication |
| `quality_routing_reject` | 18 | reason |
| `quality_field_adjudicated` | 19 (writes-back) | field name, adjudicator id, final value |
| `quality_promoted_to_production` | 19 | confirmation of staging → production move |
| `quality_aggregation_recomputed` | 19 | list of claim_ids whose claim-level aggregate changed |
| `quality_recalibration_run` | (cross-stage) | anchor-agreement statistics per field |
| `quality_drift_alert` | (cross-stage) | which field drifted, by how much |
| `quality_extractor_paused` | (cross-stage) | which field's auto-accept path was paused |
| `quality_extractor_resumed` | (cross-stage) | resumption confirmation |

The standard `lifecycle_events.evidence` JSON schema for each event
type is documented in
`atlas_shared/contracts/PAPER_QUALITY_LIFECYCLE_EVENTS_2026-04-23.md`
(produced by Codex during Pass 1 commit 4-bis).

---

## 4. The migration script

A new migration file at
`Article_Eater_PostQuinean_v1_recovery/scripts/migrations/2026_04_23_paper_quality_pipeline.sql`
applies the changes in this order:

1. Insert the two new `stage_definitions` rows.
2. Renumber existing stages 18–28 to 20–30 (eleven UPDATEs).
3. Create the three auxiliary tables with their indexes.
4. Update each paper's `current_stage` if the paper was at the old
   stage 17 (`tag_assignment`) and ready to advance: move to stage
   18 (`paper_quality_extraction`) status `pending`. All other papers
   keep their current_stage; they will pass through 18 and 19 only on
   re-run.
5. Backfill: for every paper currently past stage 17 and before
   stage 18 (in the renumbered ordering), the migration writes a
   placeholder lifecycle event indicating "pre-migration; will be
   fingerprinted in retrofit pass" to keep the lifecycle visible.
   The retrofit pass (separate run; see §6) processes these papers
   in batches.

The migration is idempotent. Running it twice produces the same
state; the script checks for the new stages' existence before
inserting and for the renumbering before re-running it.

---

## 5. Cross-system observability

The integration's payoff is that the existing lifecycle queries work
unchanged. The overseer rollup script and the admin console's
"per-paper journey" view show fingerprint progress alongside every
other stage, with no special-case code.

Specifically, three queries that already exist work without
modification:

```sql
-- "Where are my papers right now?"
SELECT current_stage, COUNT(*)
FROM papers
GROUP BY current_stage
ORDER BY current_stage;
```

Returns the same kind of bar chart as before, with two new bars for
the quality stages.

```sql
-- "Show me the journey of paper PDF-0042"
SELECT stage_name, status, entered_at, completed_at, agent
FROM lifecycle_events
WHERE paper_id = 'PDF-0042'
ORDER BY entered_at;
```

Shows the quality-extraction event in the chronological journey
alongside acquisition, OCR, extraction, and so on.

```sql
-- "Which papers are stuck?"
SELECT paper_id, current_stage, last_updated
FROM papers
WHERE current_status = 'awaiting_human'
ORDER BY last_updated ASC
LIMIT 50;
```

Returns the adjudication-queue backlog in the same view as any other
"awaiting human" status. The papers stuck at `paper_quality_extraction`
are visible in the same query that surfaces, say, papers stuck at
`gold_acceptance` for human review.

A new view at the application layer:

```sql
CREATE VIEW paper_quality_progress AS
    SELECT
        p.paper_id,
        p.title,
        p.current_stage,
        p.current_status,
        f.routing_decision,
        f.fields_awaiting_adjudication,
        (SELECT COUNT(*) FROM quality_adjudication_queue q
         WHERE q.paper_id = p.paper_id AND q.adjudicated_at IS NULL)
            AS open_adjudications,
        pq.human_adjudicated AS fingerprint_complete,
        pq.overall_confidence
    FROM papers p
    LEFT JOIN fingerprint_staging f ON p.paper_id = f.paper_id
    LEFT JOIN paper_quality_fingerprints pq ON p.paper_id = pq.paper_id;
```

This view is what the overseer rollup script and the admin console
both read from.

---

## 6. The retrofit pass

DK's instruction is that every paper gets the fingerprint. Once the
pipeline integration lands, the retrofit pass is a configurable run
of stages 18–19 over papers that were ingested before this date.

The retrofit script is a one-shot CLI invocation:

```bash
python3 scripts/retrofit_paper_quality.py \
    --batch-size 50 \
    --priority claim-leverage \
    --max-cost-usd 100 \
    --report retrofit_run_<date>.md
```

The `priority` flag governs the order in which the 1,400 existing
papers go through the new stages: `claim-leverage` runs the most
heavily-cited-by-current-claims papers first, so the
strengths-and-weaknesses block becomes useful on the most-read claims
first. Other priority options: `chronological` (oldest first),
`recent-first`, `random`.

The retrofit emits the same lifecycle events as the regular pipeline,
so the overseer rollup tracks retrofit progress alongside ongoing
ingestion.

The `--max-cost-usd` cap exists because the retrofit's dominant cost
is LLM API calls. Eleven fields × two LLMs × 1,400 papers, at
roughly $0.02 per paper, comes to ~$30; the $100 cap leaves margin
for retries and is a safety rail rather than a binding constraint.

---

## 7. Updates to the build prompt

The integration adds two new commits to the build plan in the
existing `PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23.md`:

**Pass 1 commit 4-bis** —
`atlas_shared/contracts/PAPER_QUALITY_LIFECYCLE_EVENTS_2026-04-23.md`:
the contract for the eleven new lifecycle-event types. Documents the
`evidence` JSON schema for each event type. Tested by golden-file
JSON validation in `atlas_shared/tests/test_lifecycle_events.py`.

**Pass 2 commit 6-bis** —
`Article_Eater_PostQuinean_v1_recovery/scripts/migrations/2026_04_23_paper_quality_pipeline.sql`
plus the runner that applies it. Idempotent; tested with
double-application unit test. The SQL is the migration in §4 of this
document.

**Pass 3 commit 11** is renamed from "overseer rollup script" to
"overseer rollup + lifecycle integration" and includes the
`paper_quality_progress` view's CREATE statement plus the rollup's
queries against it.

The build-prompt's deliverable checklist (§10 of the system design)
gains three rows:

| Artefact | Path |
|----------|------|
| Lifecycle-events contract | `atlas_shared/contracts/PAPER_QUALITY_LIFECYCLE_EVENTS_2026-04-23.md` |
| Migration script | `Article_Eater_PostQuinean_v1_recovery/scripts/migrations/2026_04_23_paper_quality_pipeline.sql` |
| Retrofit script | `Article_Eater_PostQuinean_v1_recovery/scripts/retrofit_paper_quality.py` |

---

## 8. What this gives DK

The integration delivers four practical affordances DK did not have
before.

First, the existing lifecycle dashboard shows per-paper quality state
without any new UI work — papers in `paper_quality_extraction` and
`paper_quality_finalisation` appear in the same per-stage histograms
the overseer already produces.

Second, the "stuck papers" query that surfaces every other human-review
bottleneck now also surfaces fingerprint adjudication backlog. DK
sees one queue, not two.

Third, the retrofit pass has the same observability as forward
ingestion: every paper that goes through stages 18–19 emits the
canonical lifecycle events, the per-event JSON evidence is captured,
and the rollup can be filtered to retrofit-only or
forward-ingestion-only as desired.

Fourth, the audit trail is complete. Every adjudication decision,
every drift alert, every extractor pause-and-resume is a lifecycle
event with its evidence JSON, queryable like any other event the
atlas records. A future thesis chapter that asks "how did this
fingerprint come to exist" has an unambiguous answer in the events
table.

---

*End of V7 pipeline integration specification.*
