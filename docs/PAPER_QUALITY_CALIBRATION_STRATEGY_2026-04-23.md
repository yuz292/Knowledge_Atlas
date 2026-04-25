# Paper-Quality Calibration Strategy

**Document**: `PAPER_QUALITY_CALIBRATION_STRATEGY_2026-04-23.md`
**Companions**: panel consultation, system design, decision tree, V7
pipeline integration (all dated 2026-04-23).
**Date**: 2026-04-23.
**Status**: design-frozen for the build prompt; supersedes the
"100-paper hand-curated calibration set" placeholder in the system
design document.

DK's instruction: every paper in the corpus gets a fingerprint, no
human reads 100 papers end to end, and calibration happens by
"choosing the hard questions from multiple papers" rather than the
hard papers from a single shelf. This document specifies how that
calibration cycle works.

---

## 1. The two reframings

DK's instruction reframes the calibration problem twice over. The
build prompt and overseer integration must both reflect both
reframings.

The first reframing is from *full-paper-adjudication* to
*hard-node-batch-adjudication*. The unit of human attention is no
longer the paper; it is the question. When the extractor processes
each paper it flags the specific decision-tree nodes whose answers
are uncertain. Those flagged nodes pool across all papers. DK then
adjudicates batches grouped by node — fifteen "is this preregistration
URL valid?" cases in one sitting, ten "is this construct validity
adequate?" cases in another. Cognitive load drops because every
adjudication in a batch is the same question; consistency rises
because side-by-side comparison surfaces edge cases that single-paper
review hides; and calibration rises because the model learns from
patterns across papers, not idiosyncrasies of any one.

The second reframing is from *hand-curated-anchor-set-of-100* to
*programmatic-and-multi-LLM-with-small-anchor-set*. Most fingerprint
fields can be calibrated without human intervention: URLs verify
themselves; OSF preregistrations are queryable directly; sample sizes
extract reliably enough that two independent LLM passes agreeing
within tolerance is itself the calibration. The small anchor set —
fifteen to twenty papers DK personally rates across all eleven fields
— exists to anchor the truly subjective judgements (construct
validity, rhetorical flags, COI severity), not to validate every
extraction.

The combined effect: DK never does a 100-paper sweep. He does a
20-paper anchor-set rating once, then sees a steady stream of
node-batch adjudication queues that drain in roughly fifteen
minutes per session.

---

## 2. The calibration sources, by field

The eleven extractable fields plus the four human-only sidecars,
each with the calibration source the build prompt configures.

### 2.1 Programmatic-only fields (no LLM judgement needed)

These fields verify against authoritative external sources. The
extractor's job is to *find* the value in the paper, but its
*correctness* is checked programmatically.

| Field | Authoritative source | Verification |
|-------|----------------------|--------------|
| Preregistration URL | OSF / AsPredicted / ClinicalTrials.gov API | URL HEAD-check; metadata fetch; hypothesis-text retrieval |
| Open-data URL | URL HEAD-check; content-type sniff | Verifies the URL resolves and returns data, not a landing page |
| DOI | Crossref API | Metadata cross-check |
| Author identifiers | ORCID API, OpenAlex | De-duplication; affiliation lookup |
| Citation count | OpenAlex / Semantic Scholar | Periodic refresh; recorded with timestamp |
| Replication status | OSF Replication Project, RIAT, Many Labs registry | Match by paper DOI |
| Retraction status | Retraction Watch Database | Match by paper DOI |
| Venue tier | Crossref + DOAJ + JCR (where available) | Look-up by ISSN |
| Predatory venue check | Cabells Predatory Reports + custom blacklist | Look-up by ISSN |

A field in this group does not enter the human adjudication queue.
If the URL fails or the metadata mismatches, the fingerprint records
the failure with reason; a human is asked only when the failure
pattern is novel.

### 2.2 Multi-LLM-agreement fields

The extractor runs two independent LLM passes (different models —
one Claude-class, one OpenAI-class — to maximise their independence).
A field whose two passes agree within tolerance is auto-accepted with
confidence reflecting the agreement strength. A field where the two
passes disagree routes to the node-batch adjudication queue grouped
by which field disagreed.

| Field | Agreement criterion |
|-------|---------------------|
| `n_total` | Both passes return the same integer (or both return None) |
| `design_type` | Both passes return the same categorical value |
| `sample_setting` | Both passes return the same categorical value |
| `age_distribution` | Means within 2 years, SDs within 1 year |
| `primary_effect_size` | Both report value within 5 % relative; metric matches |
| `statistical_power` | Both within 0.05; both report same origin |
| `primary_measure` (instrument name) | Embedding-cosine ≥ 0.9 between strings |

The build prompt's extractor calls both LLMs in the same pipeline
stage. Cost is doubled per paper but well below the threshold the
panel consultation flagged — the dominant cost remains human
adjudication time, which this scheme reduces.

### 2.3 Human-anchor-set fields

Four fields require a human-rated anchor to calibrate the LLM's
judgement: construct validity, COI severity, the three rhetorical
flags, and the field-specific-norms annotation. These are the
panel's "human-review-only sidecars" from §3 of the consultation.

The anchor set is fifteen to twenty papers, hand-rated by DK
across all four fields. DK rates each paper once; that's the human
investment. The build prompt's calibration script takes the anchor
ratings and (a) measures the LLM's agreement with the human ratings
on the anchor set, (b) configures the per-field auto-accept
threshold so that LLM agreement on the anchor exceeds 85 %, and
(c) reports any field where the LLM cannot reach 85 % agreement at
any threshold — that field becomes adjudication-required for every
paper, not just borderline cases.

DK's twenty hours spread across two weeks produce:
- Anchor papers spanning eras (5 pre-2010, 5 from 2010–2019, 10
  from 2020+).
- Anchor papers spanning design types (8 primary empirical, 2
  meta-analyses, 4 reviews, 2 theoretical, 4 methods/other).
- Anchor papers spanning quality (4 demonstrably high quality, 8
  middling, 4 demonstrably low — including one or two papers DK
  considers actively flawed, so the system learns to flag them).

The anchor set's annotations are stored in
`atlas_shared/tests/fixtures/paper_quality_anchor/` as a versioned
JSON, so the calibration is reproducible.

---

## 3. The hard-node-batch adjudication workflow

This is the workflow DK actually sees, replacing the per-paper
adjudication of the original design.

### 3.1 Triage at extraction time

When the extractor finishes a paper, it does not write the
fingerprint to the production store immediately. It writes a
candidate fingerprint with a per-field confidence vector to a
staging table (`fingerprint_staging`). For each field, if the
confidence is below the auto-accept threshold OR the
multi-LLM-agreement criterion failed OR the field is in the
human-only sidecar set, the field is added to the
`adjudication_queue` keyed not by paper but by node identifier.

A node identifier is the decision-tree node from the companion
document, e.g. `4.1.preregistration_url_valid` or
`6.1.construct_validity_dominant`. The queue is therefore organised
by question, not by paper.

### 3.2 The adjudication console

The instructor admin console gains a new "Quality Adjudication" tab
that shows queue depth per node, ordered by depth descending. DK
clicks a node and sees a batch of N items (default 10, configurable)
where each item shows:

- The paper's title and citation
- The relevant excerpt the LLM extracted
- The LLM's suggested value
- The LLM's confidence
- Other LLM's suggested value (if multi-LLM was attempted)
- Three keyboard-shortcut adjudication actions: accept, override
  (with a value), or skip-this-batch

DK can also bulk-accept all items in a batch where the LLM's
suggestion matches a per-batch default (e.g., "all of these are
preregistration URLs that 404 — treat them all as
unverifiable"). Bulk-accept writes one fingerprint update per item
but only requires one click.

### 3.3 Promotion from staging to production

When a fingerprint's adjudication queue is empty (all flagged fields
have been adjudicated), the candidate in `fingerprint_staging`
promotes to `paper_quality_fingerprints` with `human_adjudicated =
True` for the adjudicated fields and `human_adjudicated = False` for
the auto-accepted fields. The audit trail records both.

A paper whose adjudications have not all closed is still surfaced in
the claim aggregation, but with a flag indicating "fingerprint
incomplete; field X awaiting adjudication."

### 3.4 Throughput estimate

On the existing 1,400-paper corpus, with the multi-LLM agreement
scheme catching most cases, the realistic adjudication-queue volume
is:

- Construct validity: ~ 1,400 items (every paper) — the panel's
  rule that this is human-only.
- Rhetorical flags: ~ 100–300 items where the LLM detected a
  non-trivial flag.
- Preregistration URL invalidities: ~ 50–100 items.
- Multi-LLM disagreement on the auto-extractable fields: ~ 200–400
  items spread across the seven fields.
- COI severity adjudication: ~ 100–200 items.

Total: ~ 2,000–2,400 adjudication items. At 6 items per minute
(realistic rate when batching by question), that is roughly 6–7
hours of focused review, ideally split across multiple sessions.
This is two orders of magnitude lower than reading 1,400 papers
end to end.

---

## 4. Continuous re-calibration

The calibration is not one-and-done. Three mechanisms keep it honest.

The first is **anchor drift detection**. Every quarter, the
extractor re-runs on the anchor papers and the LLM agreement with
DK's anchor ratings is recomputed. Any field whose agreement falls
below 80 % triggers a yellow alert; below 70 % triggers red and
auto-pauses the auto-accept path for that field until DK reviews.

The second is **adjudication-rate monitoring**. If the rate at which
DK overrides the LLM in a particular node exceeds 30 %, the
field is degraded to human-required regardless of confidence. This
catches cases where the LLM is wrong in subtle, repeated ways the
multi-LLM agreement criterion misses.

The third is **calibration-set growth**. Every adjudicated case from
the queue feeds back into the calibration data. Over time the
calibration becomes more robust because it incorporates the
distribution of cases the system actually sees, not the distribution
DK initially anchored.

---

## 5. Updates to the build prompt

The build prompt at `PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23.md`
needs three amendments to reflect this calibration strategy. The
amendments are:

First, replace any reference to a "100-paper hand-curated calibration
set" with "20-paper anchor set + programmatic + multi-LLM agreement"
per this document. The anchor-set curation is DK's responsibility,
not Codex's.

Second, the extractor's pipeline at Stage A produces a candidate
fingerprint that writes to `fingerprint_staging` rather than to the
production store. The promotion step from staging to production
happens only when all flagged fields have been adjudicated. Codex
should add the staging table to the SQL schema in Pass 3 Commit 7.

Third, the adjudication console at Pass 3 Commit 9 is reorganised
by node identifier (one queue per decision-tree node) rather than
by paper. The UI shows queue depth per node and drills into
batches. The build-prompt's Pass 3 Commit 9 description in the
existing document is rewritten to reflect this.

A new commit is added to the build prompt as Commit 9-bis: the
anchor-set ingestion script that reads
`atlas_shared/tests/fixtures/paper_quality_anchor/` and uses it to
configure the per-field auto-accept thresholds at calibration time.
That commit ships with the calibration test that asserts the
configuration matches the anchor set's actual agreement statistics.

The amended build prompt is at
`PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23_AMENDED.md` (Codex
reads the amended version, not the original).

---

## 6. What DK is asked to do, concretely

To unblock the build:

1. **Anchor-set selection** — pick 15–20 papers from the existing
   1,400-paper corpus spanning the era / design-type / quality
   distribution named in §2.3. DK can do this by reading the titles
   and a paragraph of each, not the whole paper. Time: one to two
   hours.

2. **Anchor-set rating** — for each of the 20 papers, rate the four
   human-only sidecar fields (construct validity, COI severity,
   three rhetorical flags, field-specific-norms). The rating UI for
   this is a single web page generated by the build prompt's
   anchor-set ingestion commit. Time: ten to twenty hours, ideally
   spread across sittings.

3. **Decision-tree annotations** — walk through
   `PAPER_QUALITY_DECISION_TREE_2026-04-23.md` and fill the "DK
   preference" slots. Time: two to three hours of focused thinking.
   The build prompt's extractor reads the annotations to configure
   its per-field prompt library.

4. **Initial node-batch adjudication** — once the extractor has
   processed the corpus once and the queue has filled, DK
   adjudicates the batches by node. Time: six to seven hours
   spread across multiple sittings (per §3.4).

Total DK investment: roughly 25–35 hours, all of it in cognitively
homogeneous sittings (rate the anchor set, fill the decision tree,
clear the node batches), none of it requiring DK to read any paper
end to end.

---

*End of calibration strategy.*
