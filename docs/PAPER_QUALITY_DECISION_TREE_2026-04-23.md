# Paper-Quality Decision Tree — DK Walk-Through

**Document**: `PAPER_QUALITY_DECISION_TREE_2026-04-23.md`
**Companions**: `PAPER_QUALITY_PANEL_CONSULTATION_2026-04-23.md`,
`PAPER_QUALITY_SYSTEM_DESIGN_2026-04-23.md`.
**Purpose**: surface every choice point the fingerprint extractor will
encounter on a given paper, so DK can walk through and record an
elaborated preference at each branch. The annotated version of this
document becomes the canonical preference set the build prompt's
extractor consults.

---

## How to use this document

Each node is a question the extractor must answer about the paper in
front of it. Each option lists the auto-detection signal, the
consequence for the fingerprint, and a confidence floor below which
the result routes to adjudication. After each node there is a
**DK preference** slot. Replace the underline with two to four
sentences explaining your judgement and any qualifications. The
extractor's prompt library will be regenerated from your annotated
copy.

### Write-in convention (added 2026-04-25, per DK Q20)

Every option table below carries an *implicit* "Other / write in"
choice. If none of the listed options matches your preference, you
may either (a) name a new option directly in the DK preference slot
and explain why the listed options were inadequate, or (b) propose a
modification to one of the listed options. The extractor's prompt
library will be regenerated from your annotated copy regardless of
whether you picked a listed option, modified one, or wrote in your
own.

Format for write-in answers:

```
**DK preference**: [Other — write in]
[Two to four sentences explaining the new option, why the listed
options didn't fit, and what consequence the new option should have
for the fingerprint.]
```

Format for modification answers:

```
**DK preference**: [Option <letter>, modified]
[Two to four sentences explaining the modification and the rationale.]
```

The interactive walkthrough page (PQ-WALKTHRU-001, in development)
will surface this choice as an explicit "Other — write in" radio
button at every node. Until it ships, the markdown above is the
working interface; this convention is the markdown analogue.

### Ballistic operation (added 2026-04-25, per DK Q15)

When the build runs, hard-rule violations on individual papers do
not halt the pipeline; they are recorded in the
`hard_rule_violations` table and the next paper is processed. Your
preferences below should treat each node as setting policy for the
*aggregate* run rather than as guarding a specific paper. Where
appropriate, your preference may include a "queue for review at this
threshold" qualifier rather than an absolute rule.

### Tree traversal

The tree branches but does not dead-end. Every paper traverses every
branch in order; later branches may be marked "skip" for a specific
paper type (a theoretical paper has no N), but the schema records the
skip explicitly so consumers can see why a field is absent.

### Notation conventions

- **Auto** — extractable by a single subscription-LLM conversation
  pass over the paper text.
- **Programmatic** — verifiable against an external database (Crossref,
  OSF, Retraction Watch, OpenAlex) without LLM involvement. Per build
  prompt §1.5 and Hard Rule 7, only four fields are
  programmatic-eligible (preregistration URL, data-availability
  statement text, code-availability statement text, raw N digits) and
  programmatic verification is always a redundant check after the LLM
  call, never instead of it.
- **Multi-LLM** — extractable by independent Claude (subscription)
  and ChatGPT (subscription) conversation passes with two-model
  agreement at confidence ≥ 0.85.
- **Human** — requires adjudication; LLM may suggest, never decide.

---

## Branch 1 — Document type

What kind of paper is this? Subsequent branches behave differently for
each type.

### Node 1.1 — Primary empirical, review, meta-analysis, theoretical, methods, or other?

| Option | Auto-detection | Consequence | Confidence floor |
|--------|----------------|-------------|------------------|
| Primary empirical | Section structure (Methods, Results), N reported | All eleven fields apply | 0.90 |
| Systematic review | "systematic review", PRISMA flowchart, search-strategy section | N applies as the count of studies reviewed; design-type = "review_systematic"; preregistration field applies | 0.90 |
| Narrative review | Review structure but no PRISMA / search strategy | N skipped; design-type = "review_narrative"; rhetorical-flag scrutiny tightened | 0.85 |
| Meta-analysis | Forest plot, pooled effect size, heterogeneity statistics | N = total participants across studies; effect-size and heterogeneity fields elevated to primary | 0.90 |
| Theoretical | No data, no Methods, formal-argument structure | Sample fields skipped; construct-validity becomes the dominant field | 0.85 |
| Methods paper | Validates a measurement instrument or procedure | Construct-validity field elevated; sample fields apply but interpretation differs | 0.85 |
| Editorial / commentary | Short, opinion-framed, low citation count of primary sources | All quantitative fields skipped; rhetorical flags surfaced; not aggregated into claim-strength | n/a |
| Preprint (any of the above) | Venue field begins with arXiv, bioRxiv, PsyArXiv, OSF Preprints | Tag the paper but treat the document type per its content; record `peer_reviewed = False` | 0.95 |

**DK preference**: ______________________________________________

### Node 1.2 — How should claim-level aggregation handle the mix?

When a claim is supported by a heterogeneous set (one meta-analysis,
three primaries, one theoretical paper), the aggregator can either
weight by document type or treat each warrant equally and let the
weighting function produced by the panel handle it.

| Option | Consequence |
|--------|-------------|
| Weight by document type | Meta-analyses count more than primaries; primaries more than narrative reviews; theoretical papers contribute zero to numeric aggregation |
| Equal weight, panel-function only | Document type informs the prose summary but does not enter the numeric weighting function explicitly |
| Document-type tiers (3-tier) | Tier 1 = meta-analysis + systematic review; Tier 2 = primary; Tier 3 = narrative review + theoretical; the weighting function uses tier as a multiplier |

**DK preference**: ______________________________________________

---

## Branch 2 — Era and venue

Open-science norms date. Penalising a 2008 paper for having no
preregistration produces nonsense.

### Node 2.1 — What era is the paper from?

The era determines what "missing fields" mean.

| Era | Open-science expectation | Implication |
|-----|--------------------------|-------------|
| Pre-2010 | None (preregistration unusual) | Missing preregistration is not a deduction; the field is marked `expected = False` |
| 2010–2014 | Emerging (preregistration possible but not standard) | Missing preregistration noted but not weighted negatively |
| 2015–2019 | Increasingly expected in psychology, neuroscience | Missing preregistration noted; in fields with PRO norms (e.g., social psych post-OSC2015), weighted moderately negative |
| 2020+ | Standard expectation for new empirical work | Missing preregistration weighted negative; explicit `not_preregistered_no_reason_given` if the paper does not address why |

**DK preference**: ______________________________________________

### Node 2.2 — Venue tier

| Option | Auto-detection | Consequence |
|--------|----------------|-------------|
| Top-tier general journal | Crossref + JIF lookup; venue in a configurable list | No automatic adjustment, but venue recorded |
| Society / specialty journal | Same lookup, mid-tier list | Recorded |
| Open-access journal in good standing | DOAJ membership check via API | Recorded; not penalised |
| Predatory or borderline | Beall list (legacy) + Cabells check + venue blacklist | Flagged for adjudication; not used in aggregation until cleared |
| Preprint server only, never published | Crossref returns no DOI for a journal version; preprint timestamp older than 18 months | Flagged; surfaced as "preprint, not peer-reviewed as of <date>" |
| Conference paper | Venue fields indicate proceedings | Recorded with conference name and field-specific quality (e.g., NeurIPS = high; obscure proceedings = noted) |

**DK preference on the venue list and the predatory check**:
______________________________________________

---

## Branch 3 — Sample size and provenance

### Node 3.1 — Is N reported?

| Option | Auto-detection | Consequence |
|--------|----------------|-------------|
| Yes, single N | Pattern match on "N = NNN", "n = NNN", participants table | Record N with high confidence |
| Yes, multiple N (per condition / per study) | Multiple matches in same paper | Record total N; record per-condition Ns in `age_distribution_json` field as a sub-structure |
| Reported as a range | "between 200 and 250 participants" | Record midpoint with `n_total_confidence = 0.5` and route to adjudication |
| Not reported | No N pattern found | Skip; flag with `n_reported = False`; in primary empirical papers this is itself a quality concern |

**DK preference**: ______________________________________________

### Node 3.2 — Is N adequate for the design type?

| Design type | "Adequate" benchmark (post-2015 norms) |
|-------------|----------------------------------------|
| Lab experiment, between-subjects, single comparison | N ≥ 50 per cell for 80 % power on d = 0.5 |
| Lab experiment, within-subjects | N ≥ 30 |
| fMRI, between-subjects | N ≥ 25 per group; smaller is flagged but not auto-deducted (field contested) |
| Field experiment | N ≥ 100 |
| Observational cohort | N ≥ 200 |
| Online study with attention-check exclusions | N ≥ 200 (post-exclusion) |
| Meta-analysis | k ≥ 10 primary studies |

The fingerprint records `n_adequacy = "adequate" | "marginal" | "underpowered"` based on these benchmarks. Benchmarks are versioned (`n_adequacy_norms_version`) so the call can be re-run when norms shift.

**DK preference on the benchmarks**:
______________________________________________

### Node 3.3 — Sample provenance

WEIRD-bias check per Henrich et al. (2010). Country and setting are
extracted; the WEIRD flag is derived.

| Option | Derivation |
|--------|-----------|
| WEIRD | Sample drawn from Western, educated, industrialised, rich, democratic country, primarily university student or research-volunteer setting |
| Partially WEIRD | Mixed sample, e.g. clinical sample drawn from US hospitals plus Latin-American satellite sites |
| Non-WEIRD | Sample drawn primarily outside the WEIRD set |
| Mixed (intentional) | Cross-cultural design, claim of generalisation tested |

**DK preference on what the WEIRD flag implies for aggregation**:
______________________________________________

---

## Branch 4 — Preregistration and open data

### Node 4.1 — Preregistration claimed?

| Option | Auto-detection | Programmatic verification |
|--------|----------------|---------------------------|
| Yes, with URL | "preregistered at" + URL pattern; OSF / AsPredicted / ClinicalTrials.gov links | HEAD-check URL; fetch metadata; compare hypothesis text to the paper's hypothesis |
| Yes, claimed without URL | "this study was preregistered" with no link | Flag for adjudication; do not record `preregistered = True` until a URL is found |
| Registered report (in-principle accepted) | Journal label "registered report" or similar | Verify against journal's RR list |
| No | Absence of any preregistration language | Record `preregistered = False`; combine with era from Branch 2 |

**DK preference on the verification step**:
______________________________________________

### Node 4.2 — Hypothesis match (if preregistered)

When the paper is preregistered with a URL, does the registered
hypothesis match the paper's tested hypothesis?

| Option | Auto-detection | Consequence |
|--------|----------------|-------------|
| Match (close) | Embedding-similarity ≥ 0.85 between registered and paper hypothesis text | Record `hypothesis_match = "good"` |
| Match (loose) | Similarity 0.6–0.85 | Record `hypothesis_match = "partial"`; adjudication queue |
| Mismatch | Similarity < 0.6 | Record `hypothesis_match = "mismatch"`; this is a substantial flag, not a minor one |
| Cannot retrieve registration | URL 404, OSF private, etc. | `hypothesis_match = "unverifiable"`; record reason |

**DK preference on the embedding threshold and what mismatch means
for aggregation**: ______________________________________________

### Node 4.3 — Open data

| Option | Auto-detection | Programmatic verification |
|--------|----------------|---------------------------|
| Open data with URL | "data available at" + URL | HEAD-check URL; verify content type is data, not just a landing page |
| Available on request | "available from authors on reasonable request" | Record as `open_data_partial`; this language has known compliance issues (Gabelica et al. 2022 found ≈ 6 % comply); not credited as open |
| Restricted (clinical / privacy) | Specific language about IRB or PII | Record reason; not penalised |
| Not addressed | No data-availability statement | Record `open_data_addressed = False`; era-dependent interpretation |

**DK preference**: ______________________________________________

---

## Branch 5 — Statistical reporting

### Node 5.1 — Effect size reported?

| Option | Auto-detection | Consequence |
|--------|----------------|-------------|
| Yes, with CI | Cohen's d / r / OR + a CI in the same neighbourhood | Record value, metric, CI |
| Yes, no CI | Effect size without CI | Record value, metric, `ci_present = False` |
| Implicit (extractable from t/F + N) | Reported t-statistic + N → compute d | Record computed d; flag `effect_size_origin = "computed"` |
| Not reported and not extractable | Only p-values, no effect size, no test statistic | `effect_size = None` |

**DK preference**: ______________________________________________

### Node 5.2 — Power analysis

| Option | Auto-detection | Consequence |
|--------|----------------|-------------|
| A priori power analysis reported | "G*Power", "a priori power calculation" + computed N | Record value with `origin = "a_priori"` |
| Sensitivity power analysis (post-hoc but principled) | "smallest detectable effect" language | Record with `origin = "sensitivity"` |
| Post-hoc power retrospectively (Hoenig & Heisey 2001 caution) | Power computed from observed effect | Record with `origin = "retrospective"`; surface the caution in the prose |
| Not reported | No power analysis | Compute retrospectively from N and effect size if both available; record with `origin = "computed_from_results"` |

**DK preference on retrospective power**:
______________________________________________

---

## Branch 6 — Construct validity (human-only)

This is the hardest fingerprint field and the panel rejected automatic
extraction. The decision tree records the LLM's *suggestion* alongside
the source excerpt; a human adjudicator decides.

### Node 6.1 — Is the operationalisation adequate for the construct?

| Option | LLM suggestion source | Adjudicator question |
|--------|----------------------|----------------------|
| Good | Paper cites psychometric validation of its instrument; instrument standard in the field | Does the cited validation actually support the measure for this population and use? |
| Questionable | Instrument is non-standard or used outside its validated population | Is the deviation justified? |
| Mixed | Multiple instruments, some validated and some ad hoc | Which instrument is doing the work for the headline claim? |
| Not assessed | Paper does not discuss construct validity | Why not? Is this a methods paper that should have? |

**DK preference on what the adjudicator is asked**:
______________________________________________

### Node 6.2 — Is the construct itself stable in the literature?

Some constructs (working memory, RMSSD) are stable; others (mindfulness,
"presence" in VR research) are contested. This shapes how a single
paper's measurement decision is read.

| Option | Source |
|--------|--------|
| Stable construct | Cross-paper agreement on operationalisation in the topic ontology |
| Contested construct | Multiple operationalisations co-exist; field has not converged |
| Novel construct | Paper introduces a new construct |

**DK preference**: ______________________________________________

---

## Branch 7 — Citation and replication profile

### Node 7.1 — Citation count and pattern

| Option | Auto-detection | Consequence |
|--------|----------------|-------------|
| Highly cited as foundational | Citation count > field median × 5; cited in many subsequent reviews | Recorded; the prose summary names the foundational status |
| Heavily cited as contested | High citation count + many citing papers contradict | Record `citation_pattern = "contested"`; surface as a strength of the disagreement, not a deduction |
| Moderately cited | Within field's typical range | Recorded as baseline |
| Niche or recent | Low citation count + recent publication | Recorded with reason |

**DK preference on what citation count is used for**:
______________________________________________

### Node 7.2 — Replication status

| Option | Auto-detection | Source |
|--------|----------------|--------|
| Replicated successfully (preregistered) | Match against Many Labs, Reproducibility Project, RIAT registry | Programmatic |
| Failed replication on record | Same source plus retraction registry | Programmatic |
| Mixed replication record | Multiple replications with conflicting outcomes | Programmatic |
| No replication on record | No match in replication registries | Recorded as `replication_status = "untested"` |

**DK preference on the registries to consult**:
______________________________________________

---

## Branch 8 — Rhetorical flags (LLM-assisted, human-decided)

The panel ruled that rhetorical flags are surfaced to readers as
observations and never aggregated into numeric scores. The decision
tree records the LLM's read of the rhetoric alongside excerpts.

### Node 8.1 — Overclaiming in abstract

LLM checks: does the abstract make claims that the Methods cannot
support? Common examples — "this study demonstrates" when the design
is correlational; generalising to "humans" from a WEIRD sample;
discussing causal direction when only association is tested.

| Option | LLM signal | Surface |
|--------|-----------|---------|
| No flag | Abstract claims match design strength | None |
| Mild flag | Abstract uses cautious language but has minor reach | Recorded with excerpt |
| Strong flag | Causal language, "demonstrates", broad generalisation | Recorded with excerpts; adjudicator confirms |

**DK preference**: ______________________________________________

### Node 8.2 — Null-result handling

| Option | LLM signal | Surface |
|--------|-----------|---------|
| Null results discussed | Section explicitly addresses null findings | None |
| Null results buried | Multiple comparisons performed, only the significant ones in the abstract | Recorded; adjudicator confirms |
| Pre-registered nulls included | Registered report or preregistration shows nulls reported | Recorded as a strength |

**DK preference**: ______________________________________________

### Node 8.3 — Correlation as causation

| Option | LLM signal |
|--------|-----------|
| Clean | Causal language matches design (RCT → causal; observational → associational) |
| Slippage | Observational design with causal-language Discussion |
| Strong slippage | Observational with causal Conclusions and policy recommendations |

**DK preference**: ______________________________________________

---

## Branch 9 — Conflict of interest

### Node 9.1 — COI declaration extracted

| Option | Auto-detection | Consequence |
|--------|----------------|-------------|
| None declared | Standard "no COI" language | Recorded |
| Funding only | Funder named, no consultancy or ownership | Recorded with funder name |
| Consultancy / ownership | Author employed by, advises, or owns equity in commercial entity related to claim | Flagged; severity adjudicated by human |
| Disclosed but author asserts no influence | Both elements present | Recorded with both fields |
| Not addressed | No COI statement | Era-dependent: pre-2005 acceptable, post-2010 noted |

**DK preference on the severity scale**:
______________________________________________

---

## Branch 10 — Final routing

After Branches 1–9 have populated, the fingerprint is routed.

### Node 10.1 — Routing decision

| Outcome | Trigger |
|---------|---------|
| Auto-accept | All eleven extractable fields above 0.85 confidence; no human-only sidecar fields populated by LLM (or all populated sidecars match expert defaults) |
| Adjudication queue | Any extractable field below 0.85 confidence OR any human-only sidecar field populated by LLM with non-trivial value |
| Reject for re-extraction | The extraction errored partway through; re-run after fixing the source |
| Manual entry | The PDF could not be parsed; admin enters manually |

**DK preference on the auto-accept / adjudication threshold**:
______________________________________________

### Node 10.2 — Adjudication priority

When the queue has many entries, what gets adjudicated first?

| Option | Sort key |
|--------|---------|
| FIFO | Order of arrival |
| Citation-weighted | Papers with more citations adjudicated first |
| Claim-leverage-weighted | Papers cited by claims with many downstream consumers adjudicated first |
| Era-balanced | Mix old and new so the calibration set stays representative |

**DK preference**: ______________________________________________

---

## Closing — what you do with the annotated tree

When you have walked through and annotated each "DK preference" slot,
the build prompt's extractor regenerates its per-field prompt library
from your annotations. The annotations also become the canonical
defence for any methodological choice when a thesis chapter cites the
atlas's quality judgement. Send the annotated copy back here and I
will update the panel consultation document and the build prompt with
your decisions before Codex begins the build.
