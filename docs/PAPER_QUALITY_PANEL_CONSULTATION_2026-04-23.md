# Paper-Quality Fingerprint Layer — Expert Panel Consultation

**Document**: `PAPER_QUALITY_PANEL_CONSULTATION_2026-04-23.md`
**Subject**: Design of a strengths-and-weaknesses analysis layer for the
Knowledge Atlas. Adds per-paper quality fingerprints, per-claim
aggregation, and per-literature-body quality reports. Exposed in the
interpretation layer so every evidence-backed answer can be accompanied
by a defensible account of how good the evidence actually is.
**Panel**: John P. A. Ioannidis (Stanford, meta-research); Brian A. Nosek
(Center for Open Science, replication and preregistration); Denny
Borsboom (University of Amsterdam, psychometrics and construct validity);
Paul Glasziou (Bond University, evidence-based medicine and
avoidable-waste research); Joseph P. Simmons (Wharton, false-positive
psychology and p-hacking).
**Date of record**: 23 April 2026.
**Status of the instrument**: design-stage; this consultation precedes
implementation and freezes the scope that the build prompt will execute.

---

## 1. The design question the panel addresses

The Knowledge Atlas already represents claims, warrants, and defeat
relations. It can tell a user which papers support a claim and which
contradict it. It cannot yet tell the user whether those papers are any
good. The missing layer is a structured account of methodological
strengths and weaknesses at three granularities — paper, claim, and
literature body — that plugs into the existing warrant graph without
requiring ontology changes downstream.

The design choice to be made here is not whether to add the layer. That
was settled by DK's decision on 2026-04-23 after the argument that a
large knowledge model's most distinctive affordance over a Bayesian
network is its ability to reason about the *quality* of evidence, not
only its content. The question this panel addresses is narrower and
harder: which fields to extract per paper, how to handle the
inevitable extraction errors, how to aggregate across heterogeneous
evidence bases, and how to render the result so that a student
chapter can cite the atlas's judgement responsibly.

## 2. Principles the panel endorses

The panel endorses five design principles up front, before discussing
specific fields.

The first is that *quality is multidimensional and non-reducible to a
single score*. Ioannidis's position, long established in the
meta-research literature (Ioannidis 2005; Ioannidis et al. 2017),
is that composite quality scores correlate poorly with actual
replicability because the weights are always disputable and the
component dimensions trade off in field-specific ways. The panel adopts
his recommendation: publish the decomposition, never a single number.

The second is that *the fingerprint must be reproducible*. Nosek's
contribution, drawing on the Center for Open Science's experience with
the Reproducibility Project (Open Science Collaboration 2015), is that
the quality fingerprint itself must be computed by a procedure that a
second lab could run and get within a declared agreement threshold.
That means every extracted field needs a declared extraction rule, a
human-adjudicated calibration set, and a published inter-rater
agreement statistic.

The third is that *construct validity sits above measurement detail*.
Borsboom's position, from the psychometric-network tradition (Borsboom
2006; Borsboom et al. 2021), is that the question "does this
instrument measure what it claims to measure" dominates all other
methodological concerns; a large N with a poor construct is worse than
a small N with a good one. The panel adopts a specific consequence:
the fingerprint carries a construct-validity flag as a first-class
field, and the claim-level aggregator weights construct validity
above sample-size considerations where they conflict.

The fourth is that *open-science norms date*. Glasziou's point, in
conversation with the 2009 Lancet avoidable-waste series (Chalmers
and Glasziou 2009), is that pre-2015 papers did not have the
preregistration and open-data infrastructure to meet the norms now
applied to new papers. Penalising them for the absence produces
systematically biased quality estimates that favour recent work
regardless of its scientific content. The panel adopts the rule that
the extraction schema carries an `open_science_expected` flag derived
from publication year and venue; papers published before the relevant
norm was established in their field are marked not-expected rather
than failing.

The fifth is that *p-hacking signals are ambiguous without
preregistration*. Simmons's position, from the false-positive
psychology line of work (Simmons, Nelson, and Simonsohn 2011), is that
the rhetorical flags an LLM can extract — overclaiming language,
buried null results, correlation-as-causation framing — are
informative but should never rise to a quality deduction on their
own, because the same patterns appear in legitimate exploratory
work when properly framed. The panel adopts the rule that rhetorical
flags are surfaced to readers as observations requiring human
interpretation, never aggregated into numeric scores.

## 3. The fifteen-field fingerprint, winnowed to eleven

DK's initial proposal listed fifteen fields. The panel's review
reduced this to eleven reliably-extractable fields grouped into four
clusters, with four of the original fifteen reclassified as
human-review-only because the panel judged them unsafe for automatic
extraction.

**Sample cluster — four fields.** Total N, sample provenance
(country of data collection plus the institutional setting — research
university, community clinic, online panel, industrial setting),
WEIRD-bias flag derived from the Henrich, Heine, and Norenzayan
(2010) criterion on the sample provenance, and age-range
distribution. The WEIRD flag is a derived field, not independently
extracted; this removes an error-prone extraction and makes the
criterion applied transparent.

**Design cluster — three fields.** Design type (laboratory
experiment, field study, observational cohort, online, secondary
analysis, meta-analysis, theoretical), preregistration status
(yes/no with a URL and a verification timestamp — the pipeline
periodically re-checks that the URL resolves and the stated
hypotheses match the registered ones), and the replication status of
the primary claim as indexed against external databases like Many
Labs and the Reproducibility Project when applicable.

**Statistical cluster — two fields.** Primary-effect-size with its
confidence interval and the metric used (Cohen's d, Pearson r, odds
ratio, hazard ratio, Bayes factor), plus statistical-power of the
primary test computed a priori if reported and retrospectively from
effect size and N if not. The panel notes Hoenig and Heisey (2001) on
the limits of post-hoc power and requires the fingerprint to
annotate which of the two origins the reported power came from.

**Measurement and openness cluster — two fields.** Primary measurement
instrument with a citation to its psychometric validation if one
exists in the paper or can be located externally, and open-data URL
with verification that the URL resolves and contains the declared
content.

**Reclassified as human-review-only — four fields.** Construct-validity
flag (requires expert judgement that a single LLM pass cannot be
trusted to deliver); conflict-of-interest severity (declared COI is
easy to extract, but the judgement of whether the declared conflict
matters for the particular claim is not); rhetorical flags
(overclaiming, null-result burial, correlation-as-causation —
Simmons's point, above, is that these require framing-sensitive
judgement); and field-specific-norms check (is this N small for
neuroimaging, large for fMRI, etc. — the norms shift quickly and the
system should not pretend to know them all).

The eleven extractable fields are what the pipeline targets. The four
reclassified fields populate a parallel adjudication queue where they
are presented to the human reviewer alongside the LLM's suggested
values; no claim-level aggregation depends on them until the human has
adjudicated.

## 4. Aggregation across papers — the panel's recommendations

Per-claim aggregation takes the fingerprints of every warrant that
supports or defeats the claim and produces a structured strengths-and-
weaknesses summary. The panel's prescriptions, which the build prompt
will implement:

**Sample-size aggregation uses the cumulative N only when the samples
are approximately independent.** If three papers share an author and
use overlapping datasets, the aggregator counts the dataset once and
flags the overlap. This requires a separate `sample_overlap_graph`
structure that the extraction pipeline populates by parsing
data-availability statements and cross-referencing author IDs.

**Heterogeneity is reported via I² (Higgins and Thompson 2002) rather
than by declaring the evidence base "consistent" or "inconsistent".**
I² above 50 % means the claim-level summary names the heterogeneity
explicitly; above 75 % means the summary refuses to give a
weighted-average effect size and instead describes the range.

**Funnel-plot asymmetry is reported but not interpreted mechanically.**
Sterne et al. (2011) on the multiple legitimate and illegitimate
sources of asymmetry is the canonical caveat. The atlas reports
Egger-test p-value alongside a sentence naming that low values are
consistent with publication bias, small-study effects, or
between-study heterogeneity, and that the three are not distinguishable
from the funnel plot alone.

**Replication-rate estimates come from preregistered replication
projects where available and are declared unavailable otherwise.** The
panel rejects the alternative of imputing a replication rate from
field-wide estimates because, per Nosek's experience, field-wide
estimates vary enormously across subfields and applying one subfield's
rate to another produces misleading confidence.

**The aggregate weighting function is intentionally simple.** Papers
are weighted by (construct-validity flag) × (sample-size log) ×
(preregistration indicator + 1), with the construct-validity flag
dominating by design (Borsboom's point). The weighting function is
part of the contract; changing it ships a new contract, not a patch.

## 5. The literature-body layer

At the literature-body level, the atlas reports five summary
statistics that give a researcher a sense of the health of the
subfield: total primary-paper count and its growth rate over the
past five years; preregistration share among papers from 2018
forward; replication-rate estimate from preregistered replication
studies where available; a network-density statistic of
cross-citations among the primary papers; and a diversity index
over lab provenance computed as the Herfindahl-Hirschman index
applied to first-author institutional affiliations.

These statistics do not attempt to rate the field's importance or
interestingness. They describe its methodological state. A field can
be scientifically vital and methodologically immature at the same
time; the atlas should not conflate the two.

## 6. Known risks and the panel's acceptance of them

Three risks the panel names as unavoidable and acceptable.

Extraction error will be non-zero. The panel requires that the
pipeline report its own precision and recall against a
human-adjudicated calibration set of at least 100 papers, and that
any field with below 85 % agreement with human extraction be flagged
in the fingerprint as low-confidence and automatically routed to the
adjudication queue. The alternative — refusing to publish fingerprints
for any paper until every field is certain — would reduce the system
to silence.

Field-specific norms will drift faster than the atlas can update.
What counts as an adequate N for a particular design changes with
new methodological papers and new simulations. The panel accepts
that the atlas will occasionally render judgement based on outdated
norms and requires a `norms_version` field on every literature-body
summary so that consumers can see which calibration was used.

The judgement produced will sometimes disagree with senior
researchers in the subfield. That is the point; the atlas's value is
that it exposes the decomposition, so that a senior researcher who
disagrees can say exactly which component they disagree with and
why. The panel's stance, voiced most clearly by Ioannidis, is that
disagreement at this granularity is science working correctly, not
a system failure.

## 7. What students should write in their thesis chapters

The panel's guidance to COGS 160 students citing a quality-weighted
atlas answer. Describe the fingerprint's origin — an automated
extraction from the primary paper with a declared inter-rater
agreement statistic — and the aggregation procedure used. When the
atlas flags a paper as low-construct-validity and the student's
argument depends on the paper, discuss the flag in the thesis rather
than omitting the paper. When the atlas reports I² above 75 %,
describe the heterogeneity rather than the weighted-average effect.
When the field-level statistics show a new subfield (few papers,
high lab concentration, low replication-rate data), name this
explicitly rather than writing as if the evidence base were mature.

The composite advice is simple: treat the atlas's strengths-and-
weaknesses layer as what a senior colleague would point out. The
student's job is not to override the analysis but to incorporate it
into their own reasoning visibly.

## 8. Load-bearing references

Borsboom, D. (2006). The attack of the psychometricians.
*Psychometrika*, 71(3), 425–440.
https://doi.org/10.1007/s11336-006-1447-6

Borsboom, D., Deserno, M. K., Rhemtulla, M., Epskamp, S.,
Fried, E. I., McNally, R. J., Robinaugh, D. J., Perugini, M.,
Dalege, J., Costantini, G., Isvoranu, A.-M., Wysocki, A. C.,
van Borkulo, C. D., van Bork, R., & Waldorp, L. J. (2021).
Network analysis of multivariate data in psychological science.
*Nature Reviews Methods Primers*, 1, 58.
https://doi.org/10.1038/s43586-021-00055-w

Chalmers, I., & Glasziou, P. (2009). Avoidable waste in the
production and reporting of research evidence. *The Lancet*,
374(9683), 86–89.
https://doi.org/10.1016/S0140-6736(09)60329-9

Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest
people in the world? *Behavioral and Brain Sciences*, 33(2–3),
61–83. https://doi.org/10.1017/S0140525X0999152X

Higgins, J. P. T., & Thompson, S. G. (2002). Quantifying
heterogeneity in a meta-analysis. *Statistics in Medicine*,
21(11), 1539–1558. https://doi.org/10.1002/sim.1186

Hoenig, J. M., & Heisey, D. M. (2001). The abuse of power: The
pervasive fallacy of power calculations for data analysis.
*The American Statistician*, 55(1), 19–24.
https://doi.org/10.1198/000313001300339897

Ioannidis, J. P. A. (2005). Why most published research findings
are false. *PLoS Medicine*, 2(8), e124.
https://doi.org/10.1371/journal.pmed.0020124

Ioannidis, J. P. A., Fanelli, D., Dunne, D. D., & Goodman, S. N.
(2017). Meta-research: Evaluation and improvement of research
methods and practices. *PLoS Biology*, 13(10), e1002264.
https://doi.org/10.1371/journal.pbio.1002264

Open Science Collaboration. (2015). Estimating the reproducibility
of psychological science. *Science*, 349(6251), aac4716.
https://doi.org/10.1126/science.aac4716

Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011).
False-positive psychology: Undisclosed flexibility in data
collection and analysis allows presenting anything as significant.
*Psychological Science*, 22(11), 1359–1366.
https://doi.org/10.1177/0956797611417632

Sterne, J. A. C., Sutton, A. J., Ioannidis, J. P. A., Terrin, N.,
Jones, D. R., Lau, J., Carpenter, J., Rücker, G., Harbord, R. M.,
Schmid, C. H., Tetzlaff, J., Deeks, J. J., Peters, J., Macaskill,
P., Schwarzer, G., Duval, S., Altman, D. G., Moher, D., &
Higgins, J. P. T. (2011). Recommendations for examining and
interpreting funnel plot asymmetry in meta-analyses of randomised
controlled trials. *BMJ*, 343, d4002.
https://doi.org/10.1136/bmj.d4002

---

*End of panel consultation record.*
