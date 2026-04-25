# Factors Affecting the Quality of an Experimental Paper

**Document**: `EXPERIMENTAL_PAPER_QUALITY_FACTORS_2026-04-23.md`
**Audience**: Knowledge Atlas users — students, researchers, and any
worker (human or AI) reading or producing the paper-quality
fingerprint described in `PAPER_QUALITY_SYSTEM_DESIGN_2026-04-23.md`.
**Scope**: the quality of an *experiment*, not of a paper as a piece
of writing. Rhetorical strengths and weaknesses are surfaced
elsewhere; this paper concerns the design, conduct, measurement,
analysis, and replication record of the empirical work the paper
reports.

---

## Abstract

A paper reporting an experiment can be evaluated along five broad
axes: internal validity, external validity, construct validity,
statistical conclusion validity, and open-science transparency. The
first four were named by Cook and Campbell (1979) and updated by
Shadish, Cook, and Campbell (2002); the fifth has emerged from the
last decade of replication research and the methodological reform
movement (Open Science Collaboration 2015; Munafò et al. 2017).
Together they identify the factors by which a competent reviewer —
or a research-assistant system aspiring to a reviewer's reliability
— evaluates an experiment. This document walks through each axis,
names the factors that move quality up or down, and notes where the
field has reached consensus and where it has not. The goal is to
give the Knowledge Atlas a defensible normative ground for the
strengths-and-weaknesses analysis it produces, and to give a thesis
chapter citing such an analysis a citable reference for what was
evaluated and why.

## 1. Internal validity — protecting causal inference

Internal validity is the question of whether the experiment's design
permits the causal inference its conclusions draw. An experiment with
strong internal validity rules out plausible alternative explanations
for any observed relationship between the manipulation and the
outcome. Cook and Campbell (1979) identified eight standard threats
to internal validity, each with a corresponding design feature that
mitigates it. Modern methodology (Shadish, Cook, and Campbell 2002;
Imai et al. 2011) has refined the list but not displaced it.

The first threat is **history**: events occurring during the experiment
that are not the manipulation but could affect the outcome. A study
of a workplace intervention that runs through a corporate
restructuring loses internal validity because the restructuring is a
plausible alternative cause. The mitigation is a control group running
in the same calendar period.

The second is **maturation**: change in participants over time
attributable to development or fatigue rather than to the
intervention. A six-month study of children's reading must distinguish
the curriculum's effect from natural maturation; this requires a
control group not receiving the curriculum.

The third is **testing**: an effect of the measurement itself on the
outcome being measured. If participants are asked the same survey
twice, their second answers are partly conditioned on having taken
the survey once. The mitigation is a Solomon four-group design or
the use of equivalent alternative forms.

The fourth is **instrumentation**: changes in the measurement
instrument or in the calibration of human raters across measurement
points. A study using observational ratings must train and calibrate
raters and demonstrate inter-rater agreement; instrument drift is a
particular concern in physiological recording, where sensor
calibration may drift across a day.

The fifth is **statistical regression to the mean**: the tendency
for extreme initial scores to move toward the mean on subsequent
measurement, regardless of any intervention. This threat is severe
when participants are selected because they scored at the extreme
on a screening measure.

The sixth is **selection**: pre-existing differences between
treatment and control groups. Random assignment is the canonical
mitigation; Imai, King, and Stuart (2008) provide the modern
analysis of when randomisation succeeds and when matching or
stratification are required.

The seventh is **mortality** (or attrition): differential dropout
between conditions. An intervention study where the treatment group
is more likely to drop out leaves the analyst comparing self-selected
completers, not randomised participants. The mitigation is intent-to-
treat analysis with multiple-imputation sensitivity checks; the
preregistered analysis plan should specify how attrition will be
handled before data collection ends.

The eighth is **ambiguity about direction of causal influence**: the
question of whether X caused Y or Y caused X, particularly in
longitudinal observational studies. Granger-causality tests, lagged
panel models, and instrumental-variable designs each address this
threat in their own scope.

A factor not on Cook and Campbell's original list but central to
contemporary methodology is **researcher degrees of freedom** in the
experimental procedure itself — the choices a researcher makes about
when to stop collecting data, which conditions to drop, which
covariates to include. Simmons, Nelson, and Simonsohn (2011)
demonstrated that flexible analytic choices, even within an apparently
sound design, can produce false-positive rates orders of magnitude
above the nominal alpha. Preregistration of the analysis plan,
including stopping rules, is the modern mitigation.

## 2. External validity — protecting generalisation

External validity concerns the question of whether the experiment's
findings generalise beyond the specific sample, setting, treatment,
and time of the study. Cook and Campbell named five domains of
generalisation; Yarkoni (2020) recently argued that the field's
inattention to external validity constitutes a "generalisability
crisis" rivalling the replication crisis in severity.

**Population generalisation** asks whether the findings hold beyond
the studied sample. Most psychology research samples
disproportionately from undergraduate students at Western
universities — Henrich, Heine, and Norenzayan's (2010) WEIRD
critique. A finding established only in WEIRD samples cannot be
asserted as a finding about humans without further work.

**Setting generalisation** asks whether laboratory findings hold in
field contexts. A finding that highly-controlled laboratory
manipulation X produces outcome Y does not imply that the same X
produces Y in the noisy environment of an office, a hospital, or a
school. The generalisation requires a field replication, not an
inference.

**Treatment generalisation** asks whether the experimental
manipulation captures the construct it claims to. A study of "stress"
that operationalises stress as a single ten-minute mental-arithmetic
task generalises to that operationalisation, not to all stress; a
manipulation of "biophilic design" implemented as a single potted
plant on a desk does not generalise to all biophilic-design
interventions.

**Outcome generalisation** asks the same question on the dependent
variable side. A study measuring "wellbeing" via a single five-item
self-report scale at one time point captures a slice of the construct;
multi-method, multi-time-point measurement is the methodological
standard for outcomes that purport to generalise (Campbell and Fiske
1959 on multi-trait multi-method matrices).

**Time generalisation** asks whether findings hold at different
historical moments. Effects that depend on cultural or technological
context can fail to replicate decades later not because the original
study was wrong but because the context changed (Stroebe and Strack
2014 develop this point).

Yarkoni's (2020) generalisability-crisis paper argues that most
psychology results are over-generalised at the rhetorical level
because the statistical models used implicitly assume the studied
sample, setting, treatment, and outcome are the population from
which generalisation is sought. Westfall and Yarkoni (2016) develop
the formal critique. The practical consequence: a quality fingerprint
should record the generalisation scope the paper actually warrants
and should not credit a paper for claims it cannot defend on its
sample alone.

## 3. Construct validity — protecting the operationalisation

Construct validity is the question of whether the experiment's
operations correspond to the theoretical constructs the experiment
claims to study. Cronbach and Meehl (1955) established the concept;
Borsboom, Mellenbergh, and van Heerden (2004) reframed it for
contemporary measurement theory; Borsboom et al. (2021) extend it to
network-psychometric models.

The first construct-validity question is **whether the measurement
instrument has been validated against the construct**. A study using
the State-Trait Anxiety Inventory has decades of psychometric
literature behind the instrument; a study using a bespoke five-item
scale invented for the paper does not. The validity-of-the-instrument
question is itself a literature, with standards of evidence that
include exploratory and confirmatory factor analysis, criterion
validity against external markers, predictive validity over time,
and increasingly invariance testing across populations.

The second is **whether the manipulation operationalises the
construct it claims to manipulate**. A study claiming to manipulate
"power" via a brief writing task generalises to a particular
operationalisation of priming-induced felt-power, not to power as
deployed in any organisational sense; the field's struggle with the
power-pose literature (Carney, Cuddy, and Yap 2010; Ranehill et al.
2015) is in part a struggle with whether the manipulation
operationalised what its name claimed.

The third is **whether the operationalisation is contaminated by
demand characteristics or by Hawthorne effects**. Participants in
psychological experiments are often aware they are being studied and
adjust their behaviour to match what they think the experimenter
wants (Orne 1962). The mitigation is single-blind or double-blind
designs where feasible, post-experimental probes for participant
hypotheses, and replication using cover stories that hide the true
manipulation.

The fourth is **whether the construct itself is well-defined and
stable across the field**. This concern, from Cronbach (1957)
forward, is foundational: a study of "presence" in virtual reality
research operates against a dozen co-existing operationalisations,
not one. The atlas's quality fingerprint records both the
instrument-validity flag and the field-stability flag; a paper using
a well-validated instrument for a contested construct is not the
same as one using an ad hoc instrument for a stable construct, and
the fingerprint should not collapse the two.

A modern addition to the construct-validity literature is
**measurement invariance**: the question of whether an instrument
measures the same thing across the populations to which it is
applied. A scale validated on undergraduates cannot be assumed to
measure the same construct in clinical samples or cross-cultural
samples without invariance testing (Putnick and Bornstein 2016
review the modern methodology). The fingerprint records whether
invariance has been tested and at what level (configural, metric,
scalar) it holds.

## 4. Statistical conclusion validity — protecting the inference

Statistical conclusion validity is the question of whether the
conclusions drawn from the data analysis are defensible given the
data. The threats here are partly about the analysis as performed
and partly about what the analyst might have done.

**Statistical power** is the most basic. A study with low power has
low probability of detecting a true effect; it is also, less
intuitively, more likely to overestimate effect size when an effect
is detected (Gelman and Carlin 2014 on Type M errors; Button et al.
2013 on power and reliability in neuroscience). The fingerprint
records reported power, distinguishes a-priori from retrospective
calculations (Hoenig and Heisey 2001), and computes power from
reported effect size and N where neither is reported.

**Multiple comparisons** are the second concern. Running many tests
without correction inflates the family-wise error rate. Bonferroni
remains the conservative default; Benjamini and Hochberg's (1995)
false-discovery-rate procedure is more powerful and now standard.
The fingerprint records whether multiple-comparisons corrections are
applied and at what level. A paper performing thirty comparisons
without correction is in a different epistemic position from one
performing the same thirty with FDR.

**Researcher-degrees-of-freedom in the analysis** are the third.
Simmons, Nelson, and Simonsohn (2011), Gelman and Loken (2013), and
Steegen et al. (2016) develop the case that analytic flexibility —
choices about which covariates to include, which exclusions to apply,
which transformations to use — can inflate false-positive rates above
nominal alpha by orders of magnitude. The mitigations are
preregistration of the analysis plan, multiverse analyses showing
robustness across reasonable analytic choices, and transparent
reporting of all decisions made.

**Effect-size reporting** is the fourth. A statistically significant
result that is practically tiny is not the same as one that is
meaningful in context; the field has moved toward effect-size
reporting as a standard expectation (Lakens 2013 on practical effect-
size calculation). The fingerprint records the primary effect size
with its confidence interval and the unit. A paper reporting only
p-values is in worse epistemic shape than one reporting effect sizes
with intervals, even when the underlying experiment is identical.

**Confidence-interval coverage** is the fifth. A 95 % confidence
interval communicates uncertainty in a way a single p-value does
not. Modern best practice (Cumming 2014; the New Statistics
movement) is intervals over null-hypothesis tests where the inference
permits.

**Bayesian reporting** is the sixth. Where the inferential
framework is Bayesian, a quality fingerprint records the prior
specification, the posterior, the Bayes factor or comparable summary
statistic, and the sensitivity of the conclusion to alternative
priors. Bayesian and frequentist analyses are both legitimate; what
distinguishes a quality paper from a poor one is the transparency of
the chosen framework, not the choice between them.

## 5. Open-science transparency — protecting the system

The fifth axis is the youngest. Cook and Campbell did not name it
because the methodological infrastructure did not yet exist. The
last fifteen years of replication research (Open Science
Collaboration 2015; Camerer et al. 2018; Klein et al. 2018) have
established that open-science practices — preregistration, open data,
open code, and open materials — produce more reliable inference
because they reduce the unaccountable researcher-degrees-of-freedom
that earlier sections name as threats.

**Preregistration** is the commitment, before data collection ends,
to a specific analysis plan. Nosek et al. (2018) detail the
methodology. The atlas's fingerprint records preregistration with
URL verification (the URL must resolve and the registered
hypotheses must match the paper's tested hypotheses within an
embedding-similarity threshold, per the panel consultation).

**Registered reports** are the strong form of preregistration: the
journal commits to publication based on the design, before the
results are known (Chambers and Tzavella 2022 review the format's
evidence base). A registered report is methodologically distinct
from a standard preregistration and the fingerprint records the
distinction.

**Open data** permits independent re-analysis. Gabelica, Bojčić, and
Puljak (2022) found that papers stating data is "available on
request" comply with such requests at a rate near 6 %, which is to
say the language is rhetorical. The fingerprint records both the
declared data-availability statement and the verified state (HEAD-
check on the URL, content-type check, basic schema sanity).

**Open code** permits computational reproduction. The increasing
prevalence of computational analyses — whether traditional statistical
modelling or machine-learning pipelines — makes open code as
important as open data for reproducibility. The fingerprint records
whether code is published and at what URL.

**Open materials** permit independent operationalisation of the same
manipulation in replication studies. The fingerprint records the
declared and verified open-materials state.

A paper meeting all five open-science criteria — preregistered,
open data, open code, open materials, and (where applicable)
registered-report status — is in the strongest possible epistemic
position the modern infrastructure supports. A paper meeting none of
them is not therefore wrong; pre-2010 papers had no infrastructure
for any of these. The fingerprint records the era-appropriate
expectation per the panel's principle that open-science norms date.

## 6. Beyond Cook and Campbell — contemporary additions

Three further factors affect experimental paper quality and do not
fit cleanly into the four-validities frame.

**Replication record**. A finding that has been independently
replicated, ideally in a preregistered registered-replication report,
has a different quality status from one that has not. Klein et al.
(2018) provide the methodological standard. The fingerprint records
replication status against the registries of Many Labs, the
Reproducibility Project, RIAT, and any field-specific registered
replication network.

**Effect-size precision and stability**. A finding whose effect
size has tightened across multiple studies is in a different
status from one whose effect size has wandered or shrunk in
subsequent work (Schimmack 2020 on the unreliability of single
findings). Meta-analyses with adequate heterogeneity reporting
(Higgins and Thompson 2002 on I²; the random-effects model with
Hartung-Knapp-Sidik-Jonkman adjustment, IntHout et al. 2014, as the
modern standard) are the synthesising vehicle.

**Computational reproducibility**. Stodden, Seiler, and Ma (2018)
documented that most computational analyses in published papers
cannot be reproduced even when the data and code are nominally
available, because of dependency-version drift, undocumented
preprocessing steps, and platform-specific behaviour. Containerised
distributions (Docker, Apptainer) and dependency lockfiles
(pyproject.toml + poetry.lock; renv for R) are the modern remediation.
The fingerprint records whether the computational environment is
documented and whether a containerised reproduction has been
attempted by an independent party.

## 7. What the Knowledge Atlas's fingerprint maps to

The eleven extractable fields and four human-only sidecars in the
atlas's per-paper fingerprint map onto the five quality axes above as
follows.

**Internal-validity coverage** is partial. The fingerprint records
the design type (lab experiment, field study, observational cohort,
meta-analysis, theoretical), preregistration status, sample size,
and statistical power. It does not record specific protections
against history, maturation, instrumentation, regression-to-the-mean,
or attrition; these are surfaced as part of the construct-validity
sidecar that requires human judgement, because reliable automatic
extraction is beyond the LLM's current capabilities for these
threats.

**External-validity coverage** records sample provenance (country,
setting, WEIRD-bias derivation), age distribution, and design type
(lab vs field). The atlas's claim-level aggregator weights papers in
part by sample diversity (the lab-diversity Herfindahl-Hirschman
index) so that a claim resting on five papers from a single lab is
penalised relative to one resting on five from independent labs,
addressing setting and population generalisation explicitly.

**Construct-validity coverage** records the primary measurement
instrument and its psychometric reference where the paper supplies
one, plus a human-adjudicated construct-validity flag covering the
operationalisation of both manipulation and outcome. The flag's
human-only routing is direct application of the panel's principle
that this is the hardest field and the LLM is not trustworthy on it.

**Statistical-conclusion-validity coverage** records primary effect
size with confidence interval, statistical power and origin, and
preregistration (which addresses researcher-degrees-of-freedom
indirectly). Multiple-comparisons handling and analytic flexibility
remain in the human-review sidecar.

**Open-science coverage** records preregistration with URL
verification, open-data URL with verification, and registered-report
status. Open-code and open-materials are indexed where the paper
explicitly names them; otherwise marked as "not addressed".

**Replication-record coverage** is via the programmatic source
(OSF Replication Project, Many Labs, RIAT, Retraction Watch). The
fingerprint records replication count and status; the claim-level
aggregator surfaces this as a strength when present and as
"untested" when absent.

The mapping is not exhaustive. The Knowledge Atlas's fingerprint is
a pragmatic subset of what an ideal expert reviewer would assess —
constrained by what an LLM can extract reliably, what a programmatic
verifier can check, and what a human adjudicator can review at scale.
A thesis chapter using the atlas's strengths-and-weaknesses output
should cite this document for the framework and should not represent
the fingerprint as a complete quality assessment.

## 8. Where consensus exists and where it does not

The methodology literature has consensus on most of the structure
above and disagreement on specific instances and weights.

There is broad consensus that internal validity, external validity,
construct validity, and statistical conclusion validity are the
right four-fold frame for evaluating experiments (Shadish, Cook, and
Campbell 2002 carries the field). There is consensus that
preregistration, open data, and open code reduce false-positive
rates and improve reproducibility (Munafò et al. 2017; Nosek et al.
2018). There is consensus that effect-size reporting with confidence
intervals is preferable to bare null-hypothesis-significance tests
(Cumming 2014; the American Statistical Association's 2016 statement
on p-values, Wasserstein and Lazar 2016).

There is genuine disagreement on several specific questions the
fingerprint must take a position on. The relative weighting of
sample-size versus construct-validity remains contested; the panel
consultation followed Borsboom in giving construct validity priority
where they conflict, but a Bayesian methodologist would weight
sample-size more heavily in some inference frameworks. The treatment
of underpowered fMRI work is contested (Button et al. 2013 made the
case for power-based exclusion of older small-N studies; others argue
that exclusion is excessive given that pre-2012 fMRI norms were what
they were). The handling of the WEIRD-sample problem is contested:
Henrich et al.'s (2010) critique is widely accepted in the abstract
and unevenly applied in practice. The status of post-publication
peer review (PubPeer, retraction announcements, social-media
critique) is contested; the panel consultation declined to weight
post-publication signals because their reliability and coverage are
uneven.

A thesis chapter citing the atlas's quality assessment should
acknowledge the points of disagreement explicitly when they bear on
the chapter's argument. The atlas's fingerprint is a position; it
is not the only defensible position; and the panel's wager is that
making the position explicit, citable, and decomposable is more
useful than refusing to take a position because reasonable
methodologists disagree.

## References

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false
discovery rate: A practical and powerful approach to multiple
testing. *Journal of the Royal Statistical Society: Series B*,
57(1), 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x
(~104,000 citations)

Borsboom, D., Mellenbergh, G. J., & van Heerden, J. (2004). The
concept of validity. *Psychological Review*, 111(4), 1061–1071.
https://doi.org/10.1037/0033-295X.111.4.1061 (~3,400 citations)

Borsboom, D., Deserno, M. K., Rhemtulla, M., Epskamp, S., Fried,
E. I., McNally, R. J., et al. (2021). Network analysis of
multivariate data in psychological science. *Nature Reviews Methods
Primers*, 1, 58. https://doi.org/10.1038/s43586-021-00055-w
(~2,000 citations)

Button, K. S., Ioannidis, J. P. A., Mokrysz, C., Nosek, B. A.,
Flint, J., Robinson, E. S. J., & Munafò, M. R. (2013). Power
failure: Why small sample size undermines the reliability of
neuroscience. *Nature Reviews Neuroscience*, 14(5), 365–376.
https://doi.org/10.1038/nrn3475 (~7,000 citations)

Camerer, C. F., Dreber, A., Holzmeister, F., Ho, T.-H., Huber, J.,
Johannesson, M., et al. (2018). Evaluating the replicability of
social science experiments in Nature and Science between 2010 and
2015. *Nature Human Behaviour*, 2(9), 637–644.
https://doi.org/10.1038/s41562-018-0399-z (~2,200 citations)

Campbell, D. T., & Fiske, D. W. (1959). Convergent and discriminant
validation by the multitrait-multimethod matrix. *Psychological
Bulletin*, 56(2), 81–105. https://doi.org/10.1037/h0046016
(~22,000 citations)

Carney, D. R., Cuddy, A. J. C., & Yap, A. J. (2010). Power posing:
Brief nonverbal displays affect neuroendocrine levels and risk
tolerance. *Psychological Science*, 21(10), 1363–1368.
https://doi.org/10.1177/0956797610383437 (~1,400 citations)

Chambers, C. D., & Tzavella, L. (2022). The past, present and future
of registered reports. *Nature Human Behaviour*, 6(1), 29–42.
https://doi.org/10.1038/s41562-021-01193-7 (~700 citations)

Cook, T. D., & Campbell, D. T. (1979). *Quasi-experimentation:
Design and analysis issues for field settings*. Houghton Mifflin.
(~38,000 citations)

Cronbach, L. J. (1957). The two disciplines of scientific psychology.
*American Psychologist*, 12(11), 671–684.
https://doi.org/10.1037/h0043943 (~6,000 citations)

Cronbach, L. J., & Meehl, P. E. (1955). Construct validity in
psychological tests. *Psychological Bulletin*, 52(4), 281–302.
https://doi.org/10.1037/h0040957 (~13,000 citations)

Cumming, G. (2014). The new statistics: Why and how. *Psychological
Science*, 25(1), 7–29. https://doi.org/10.1177/0956797613504966
(~5,500 citations)

Gabelica, M., Bojčić, R., & Puljak, L. (2022). Many researchers
were not compliant with their published data sharing statement: A
mixed-methods study. *Journal of Clinical Epidemiology*, 150,
33–41. https://doi.org/10.1016/j.jclinepi.2022.05.019 (~150
citations)

Gelman, A., & Carlin, J. (2014). Beyond power calculations:
Assessing Type S (sign) and Type M (magnitude) errors. *Perspectives
on Psychological Science*, 9(6), 641–651.
https://doi.org/10.1177/1745691614551642 (~1,800 citations)

Gelman, A., & Loken, E. (2013). The garden of forking paths.
Working paper. (~1,700 citations)

Henrich, J., Heine, S. J., & Norenzayan, A. (2010). The weirdest
people in the world? *Behavioral and Brain Sciences*, 33(2–3),
61–83. https://doi.org/10.1017/S0140525X0999152X (~11,500
citations)

Higgins, J. P. T., & Thompson, S. G. (2002). Quantifying
heterogeneity in a meta-analysis. *Statistics in Medicine*, 21(11),
1539–1558. https://doi.org/10.1002/sim.1186 (~50,000 citations)

Hoenig, J. M., & Heisey, D. M. (2001). The abuse of power.
*The American Statistician*, 55(1), 19–24.
https://doi.org/10.1198/000313001300339897 (~3,400 citations)

Imai, K., King, G., & Stuart, E. A. (2008). Misunderstandings
between experimentalists and observationalists about causal
inference. *Journal of the Royal Statistical Society: Series A*,
171(2), 481–502. https://doi.org/10.1111/j.1467-985X.2007.00527.x
(~1,300 citations)

IntHout, J., Ioannidis, J. P. A., & Borm, G. F. (2014). The
Hartung-Knapp-Sidik-Jonkman method for random effects meta-analysis
is straightforward and considerably outperforms the standard
DerSimonian-Laird method. *BMC Medical Research Methodology*, 14,
25. https://doi.org/10.1186/1471-2288-14-25 (~2,100 citations)

Klein, R. A., Vianello, M., Hasselman, F., et al. (2018). Many
Labs 2: Investigating variation in replicability across samples
and settings. *Advances in Methods and Practices in Psychological
Science*, 1(4), 443–490.
https://doi.org/10.1177/2515245918810225 (~2,500 citations)

Lakens, D. (2013). Calculating and reporting effect sizes to
facilitate cumulative science: A practical primer for t-tests and
ANOVAs. *Frontiers in Psychology*, 4, 863.
https://doi.org/10.3389/fpsyg.2013.00863 (~9,500 citations)

Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S.,
Chambers, C. D., du Sert, N. P., et al. (2017). A manifesto for
reproducible science. *Nature Human Behaviour*, 1, 0021.
https://doi.org/10.1038/s41562-016-0021 (~7,500 citations)

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T.
(2018). The preregistration revolution. *Proceedings of the
National Academy of Sciences*, 115(11), 2600–2606.
https://doi.org/10.1073/pnas.1708274114 (~2,300 citations)

Open Science Collaboration. (2015). Estimating the reproducibility
of psychological science. *Science*, 349(6251), aac4716.
https://doi.org/10.1126/science.aac4716 (~9,000 citations)

Orne, M. T. (1962). On the social psychology of the psychological
experiment. *American Psychologist*, 17(11), 776–783.
https://doi.org/10.1037/h0043424 (~6,000 citations)

Putnick, D. L., & Bornstein, M. H. (2016). Measurement invariance
conventions and reporting: The state of the art and future
directions for psychological research. *Developmental Review*,
41, 71–90. https://doi.org/10.1016/j.dr.2016.06.004 (~3,500
citations)

Ranehill, E., Dreber, A., Johannesson, M., Leiberg, S., Sul, S.,
& Weber, R. A. (2015). Assessing the robustness of power posing.
*Psychological Science*, 26(5), 653–656.
https://doi.org/10.1177/0956797614553946 (~700 citations)

Schimmack, U. (2020). A meta-psychological perspective on the
decade of replication failures in social psychology. *Canadian
Psychology*, 61(4), 364–376. https://doi.org/10.1037/cap0000246
(~150 citations)

Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002).
*Experimental and quasi-experimental designs for generalized causal
inference*. Houghton Mifflin. (~58,000 citations)

Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-
positive psychology. *Psychological Science*, 22(11), 1359–1366.
https://doi.org/10.1177/0956797611417632 (~7,500 citations)

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016).
Increasing transparency through a multiverse analysis. *Perspectives
on Psychological Science*, 11(5), 702–712.
https://doi.org/10.1177/1745691616658637 (~1,600 citations)

Stodden, V., Seiler, J., & Ma, Z. (2018). An empirical analysis
of journal policy effectiveness for computational reproducibility.
*Proceedings of the National Academy of Sciences*, 115(11),
2584–2589. https://doi.org/10.1073/pnas.1708290115 (~600
citations)

Stroebe, W., & Strack, F. (2014). The alleged crisis and the
illusion of exact replication. *Perspectives on Psychological
Science*, 9(1), 59–71. https://doi.org/10.1177/1745691613514450
(~600 citations)

Wasserstein, R. L., & Lazar, N. A. (2016). The ASA's statement on
p-values: Context, process, and purpose. *The American Statistician*,
70(2), 129–133. https://doi.org/10.1080/00031305.2016.1154108
(~5,200 citations)

Westfall, J., & Yarkoni, T. (2016). Statistically controlling for
confounding constructs is harder than you think. *PLoS ONE*,
11(3), e0152719. https://doi.org/10.1371/journal.pone.0152719
(~700 citations)

Yarkoni, T. (2020). The generalizability crisis. *Behavioral and
Brain Sciences*, 45, e1. https://doi.org/10.1017/S0140525X20001685
(~600 citations)

---

*End of document.*
