# Canonical Question Corpus, Round 1 — Researcher Persona (P2)

*Drafted by CW, 2026-04-27. v1.*
*Scope: this round produces a question corpus only for the **researcher** persona (P2 in the canonical persona panel). Six other personas — P1 Maya Chen (160 student), P3 Jordan Reeves (contributor), P4 Prof. Lena Bergström (theorist), P5 Sam Nakamura (practitioner), P6 TA, P7 newcomer, P8 PI — will receive their own passes following the same protocol. Section 7 sketches what those passes will need.*

---

## 1. Why a question corpus, and why questions before journeys

The Knowledge Atlas is meant to deliver evidence-backed answers to people who carry real questions into the system. Designing that experience without a corpus of the actual questions people bring is, in effect, designing an answer machine for an unspecified problem. The Track 4 students will be designing what we have been calling *evidential journeys* — sequences of page views that move a reader from the question they entered with to an answer that is properly **warranted, qualified, and rebuttal-aware** in the Toulmin sense (Toulmin, 1958/2003). One cannot design such a journey without first understanding the cognitive and rhetorical shape of the questions to which it is meant to respond.

Pollock's distinction between *prima facie* and *defeasible* warrants is helpful here (Pollock, 1987, 1995): a journey delivers not a fact but a defeasible conclusion that a thoughtful reader could, in principle, defeat by adducing further evidence. For that defeat to even be possible, the reader must have entered with a *question whose adequacy conditions are recognisable* — i.e., they must know, however inarticulately, what would count as a sufficient answer for them. Different questions have radically different adequacy conditions. Compare:

> *(a) Are some rooms better for creativity than others?*
> *(b) What's the best validated instrument for measuring perceived restorativeness in office settings?*
> *(c) Does Kaplan's Attention Restoration Theory still survive once you control for the affective confound?*

Each of these is a researcher question in some sense. But (a) demands a contrastive ranking with a synthesised Toulmin warrant; (b) demands a measurement-shopping brief with psychometric provenance; (c) demands a theoretical contest with a rebuttal economy. A site that treats them all as the same shape will satisfy none of them. The corpus below makes those shapes explicit.

This document also serves a methodological purpose. We do not yet have access to real Atlas users — the system is not deployed and a recruiting study would not reach the right population in the time we have. The Track 4 students will therefore use **LLM panels** as a first-pass user model, in the manner of recent simulated-user work in HCI and CSS (Argyle et al., 2023; Park et al., 2023; Horton, 2023). LLM panels are, of course, not human users; their generative validity is contested and their alignment with real population variance has clear limits (Aher, Arriaga, & Kalai, 2023; Santurkar et al., 2023). They are nonetheless a defensible substitute when the alternative is no model at all — provided one writes the canonical question corpus *first* and uses it as ground truth against which panel output is evaluated, rather than as an artefact generated *by* the panels. That asymmetry — corpus drives panel, not the reverse — is what gives the methodology any epistemic traction.

---

## 2. The five-axis taxonomy

Every question in the corpus is tagged on five axes. The axes are the design surface against which a journey is engineered: the journey designer reads the tags and selects an answer shape, an evidential gate, and a rebuttal-handling strategy accordingly.

**Axis 1 — Cognitive purpose.** Why is the asker asking? We use a contraction of Walton's (1995) dialogue typology and Chi's (2009) intervention taxonomy: *information-seeking* (filling a known gap), *inquiry* (settling an open question), *deliberation* (choosing among options), *persuasion* (loading a position into a debate), *discovery* (looking for the question one ought to be asking). For a researcher, *inquiry*, *deliberation*, and *discovery* will dominate; *persuasion* is rarer but matters when a researcher is preparing a grant or rebuttal section.

**Axis 2 — Answer shape.** What kind of object would satisfy the question? We have, at present, five canonical shapes, each of which is also a diagrammatic template a journey can offer: (i) **Toulmin diagram** — claim, data, warrant, backing, qualifier, rebuttal (Toulmin, 1958/2003); (ii) **field map** — a portrait of a literature with named camps, points of agreement, and live disputes (cf. systematic-review reporting of Higgins et al., 2024); (iii) **procedure** — a step-by-step protocol with provenance for each step; (iv) **contrast pair** — two side-by-side options or accounts with the relevant differentia; (v) **ranked brief** — a short list of options with criteria and evidence quality.

**Axis 3 — Evidential demand.** What threshold of evidence would satisfy the asker? Drawing on Hill (1965) and Cartwright & Hardie (2012), we distinguish: *suggestive* (a single study or a coherent argument), *converging* (multiple independent lines pointing the same way), *mechanistic* (a credible causal account, not just a correlation), *causal-with-mechanism* (the gold standard), and *measurement-grade* (psychometric properties of an instrument). Researchers vary enormously on this axis depending on whether they are exploring or designing.

**Axis 4 — Persona fit.** Which of our eight personas, and which sub-flavour within a persona, would naturally ask this? In the present round we tag only researcher sub-flavours (general, measures-seeker, sensors-seeker, tests-seeker, theory-prober); the next passes will need their own sub-taxonomies.

**Axis 5 — Theoretical commitment.** What ontological or methodological assumptions does the question presuppose? This is the axis Chinn & Brewer (1993) made unavoidable: a researcher who is a Kaplan loyalist asking about restoration is not asking the same question as a researcher who is sceptical of Attention Restoration Theory and wants to see whether the effect survives controls for affect. The journey must know the difference, because the same data will be received differently by the two readers. The seven responses to anomalous data Chinn and Brewer catalogue (ignore, reject, exclude, hold in abeyance, reinterpret, peripheral change, theory change) operate on this axis directly.

---

## 3. Methodology: three-source elicitation

Because we have no live users we triangulate. The protocol below is what the Track 4 students will run; the corpus in §4 is a worked example produced by CW running the same protocol over a single afternoon. Students should expand it.

### 3.1 LLM panels

**Configuration.** A panel is a set of LLM agents, each prompted with a researcher-persona profile that varies on:

(i) **career stage** — new doctoral student, mid-PhD, postdoc, junior PI, senior PI, lab manager, methodologist;
(ii) **disciplinary home** — environmental psychology, neuroarchitecture, HCI, CSCW, public health, urban design research, lighting science, indoor-air epidemiology, organisational behaviour;
(iii) **methodological orientation** — quantitative experimentalist, mixed-methods, computational/simulation, ethnographic, neuroimaging-led, instrument-development-led;
(iv) **theoretical commitment** — neutral, Kaplan-loyalist, Ulrich-loyalist, predictive-processing-leaning, embodied-cognition-leaning, anti-mechanism / Stevens-style operationalist, pragmatist.

A panel typically has 8–12 agents. Students should run **at least three panels** for the researcher persona, so that interview-style questions are pooled across configurations rather than reflecting the prior of a single prompt. Argyle et al. (2023) and Aher, Arriaga, & Kalai (2023) both demonstrate measurable population variance from such configurations; both also document its limits, which the students should read before relying on the output.

**Elicitation prompts.** The students will give each agent a scenario card — e.g., *"You have a new manuscript-revision deadline; the reviewer asks whether you have considered restorativeness as a confound in your wayfinding study"* — and ask it to produce (a) the question it would type into the Atlas search bar, (b) the rough shape of the answer it would expect, (c) what would make the answer feel insufficient. The third item maps directly onto Axis 3 (evidential demand) and feeds journey design.

**Validity checks.** Each panel question should be evaluated on three counts: (i) does a real-life human in this configuration plausibly ask it? (sanity); (ii) is the question in the corpus already, or does it widen coverage? (novelty); (iii) does the panel's stated adequacy condition survive cross-examination by another agent on the same panel? (intra-panel coherence). Items that fail (iii) reveal the failure modes of LLM panels and are themselves valuable as design probes.

### 3.2 Literature mining

The 166 PNU templates in `Article_Eater_PostQuinean_v1_recovery/data/templates/` are themselves a record of questions the field has thought worth asking. Each template has a `name`, a `short_description`, a `structural_pattern`, and a list of `causal_links`. The templates are dense: e.g., `CREA1_creative_network_dynamics.json` encodes the question *"What environmental conditions modulate the temporal coupling between the default-mode and executive-control networks during divergent thinking?"* and `MAT2_thermal_adaptive_pe.json` encodes *"How does ongoing thermal adaptation in occupants distort our measurements of thermal comfort?"*. The mining heuristic for students is straightforward: read a template, write down the question that the template *answers*, then write the related questions that a researcher who arrived at that answer would next ask. This generates roughly three to five questions per template, or something like 500–800 candidate questions if all templates are exhausted.

A second mining target is the 60K Mathpix-extracted snip corpus and the validated gold extractions in `data/verification_runs/codex_local_gold_outputs/`. The PNU template citations point at the seminal articles; the gold extractions point at the open frontiers. We are not, in this round, mining 50,000 documents — the students will sample.

### 3.3 Cross-product synthesis

This is the dimension David specifically flagged. The Atlas joins two large hierarchical vocabularies: the Tagging_Contractor (TRS-core v0.2.8, ~440 active tags across roughly twenty domains: *affect, affordance, biophilia, cnfa, cognitive, color, complexity, fluency, isovist, material, provenance, science, smell, social, sound, spatial, style, touch*), and the Outcome_Contractor (oc.export.v1, with seven top-level domains — *affect, behav, cog, health, neural, physio, social* — and roughly eighty level-2 outcome terms beneath them). Both vocabularies are *constitutive* hierarchies: a child term is a component of its parent (Cartwright & Hardie, 2012; the Outcome_Contractor's `constitutive_bridges.json` encodes this directly). Walking up either hierarchy generalises the question; walking down specialises it.

A cross-product question is one of the form *"How does \[IV at level k of the Tagging hierarchy] affect \[DV at level m of the Outcome hierarchy], moderated by \[third variable]?"*. Many of the most consequential questions in environmental cognition live at the *high-IV × high-DV* corner — they are the ones a senior PI asks at a grant meeting and the ones a poster session never quite answers. The students should systematically generate cross-product questions at each of four corners (low-IV/low-DV, low-IV/high-DV, high-IV/low-DV, high-IV/high-DV) and inspect the answer-shape demands at each: low/low tends to demand a Toulmin or a contrast pair; high/high tends to demand a field map or a synthesised brief.

---

## 4. The corpus (researcher round 1)

What follows is a worked example, not the final corpus. The students will extend it. Each entry has the form *Q-NN. \[Question]* followed by the five axis tags. Sub-flavour groupings are by Axis 4.

### 4.1 General researcher (Q-01 to Q-08)

These are the "I came to the Atlas to find out X" questions, with no pre-loaded preference for instrument or theory.

**Q-01.** *Are some rooms better for creativity than others, and if so by how much?*
Cognitive purpose: inquiry. Answer shape: ranked brief. Evidential demand: converging. Persona fit: P2-general, P5-practitioner. Theoretical commitment: agnostic.

**Q-02.** *What building attributes most strongly affect perceived creativity in office settings?*
Cognitive purpose: inquiry. Answer shape: field map. Evidential demand: converging. Persona fit: P2-general. Theoretical commitment: agnostic but presupposes an attribute-based ontology (i.e., the Tagging_Contractor model).

**Q-03.** *Does daylight exposure during the workday improve cognitive performance, holding sleep duration constant?*
Cognitive purpose: inquiry. Answer shape: Toulmin. Evidential demand: causal-with-mechanism. Persona fit: P2-general. Theoretical commitment: assumes the conditional-on-sleep design is informative — which is itself a contested choice, since sleep is partly endogenous to light exposure.

**Q-04.** *How big is the published effect of biophilic features on stress recovery, and how much heterogeneity is there across studies?*
Cognitive purpose: inquiry. Answer shape: field map with effect-size forest. Evidential demand: converging. Persona fit: P2-general. Theoretical commitment: meta-analytic; presupposes that effect sizes are commensurable across studies, which Higgins et al. (2024) treat as itself a question to investigate.

**Q-05.** *Where is the field disagreeing about the role of fractal dimension in environmental preference?*
Cognitive purpose: discovery. Answer shape: field map with dispute markers. Evidential demand: suggestive. Persona fit: P2-general, P4-theorist. Theoretical commitment: agnostic, but the question presupposes that disagreements are visible in the literature, which they often are not (Ioannidis, 2005).

**Q-06.** *Which of the recent VR-based environmental-psychology studies have replicated their original real-world findings?*
Cognitive purpose: inquiry. Answer shape: contrast pair (VR vs. in-situ for each study). Evidential demand: converging. Persona fit: P2-general, P5-practitioner. Theoretical commitment: assumes ecological validity is a meaningful frame.

**Q-07.** *What's an honest summary of where attention-restoration theory stands in 2026?*
Cognitive purpose: deliberation. Answer shape: field map with rebuttal economy. Evidential demand: converging-with-mechanism. Persona fit: P2-general. Theoretical commitment: invites critique; properly answered the journey must surface the affective confound (Joye & van den Berg, 2011) and the recent Bayesian-update reviews.

**Q-08.** *Are there any building-design effects on creativity that hold across cultural contexts?*
Cognitive purpose: inquiry. Answer shape: field map with moderator structure. Evidential demand: converging. Persona fit: P2-general. Theoretical commitment: explicitly cross-cultural, which is rare in this literature.

### 4.2 Measures-seeker (Q-09 to Q-16)

These are the *"I need a dependent variable"* questions: a researcher with an experimental design who needs to choose what to measure, and on what scale. They map onto the level-2 nodes of the Outcome_Contractor.

**Q-09.** *What's the best validated instrument for perceived restorativeness in office settings, suitable for repeated measures within a workday?*
Cognitive purpose: deliberation. Answer shape: ranked brief with psychometric provenance. Evidential demand: measurement-grade. Persona fit: P2-measures-seeker. Theoretical commitment: instrument-validity primacy.

**Q-10.** *Which of the standard creativity measures (TTCT, RAT, AUT, CAT, divergent-thinking fluency) is least sensitive to environmental confounds and most sensitive to environmental change?*
Cognitive purpose: deliberation. Answer shape: contrast pair across five instruments. Evidential demand: measurement-grade. Persona fit: P2-measures-seeker. Theoretical commitment: assumes the instruments are commensurable, which they are not entirely (Said-Metwaly et al., 2017).

**Q-11.** *For measuring sense of community in a multi-floor academic building, what's the validated instrument with the smallest item count and least cultural specificity?*
Cognitive purpose: deliberation. Answer shape: ranked brief. Evidential demand: measurement-grade. Persona fit: P2-measures-seeker. Theoretical commitment: assumes the construct itself transports across cultures, which Sarason's original work (1974) treated as itself uncertain.

**Q-12.** *What's the appropriate dependent variable if my hypothesis is that high-ceiling rooms increase abstract thinking — measure abstract thinking directly, or measure the construal-level proxy?*
Cognitive purpose: deliberation. Answer shape: contrast pair. Evidential demand: measurement-grade. Persona fit: P2-measures-seeker. Theoretical commitment: presupposes the Meyers-Levy & Zhu (2007) construal-level account, which Vasquez-Echeverria et al. (2017) failed to replicate at expected effect size.

**Q-13.** *For wayfinding research, which is more discriminating between environments — wayfinding-time, wayfinding-confidence, or a sketch-map quality score?*
Cognitive purpose: deliberation. Answer shape: contrast pair. Evidential demand: measurement-grade. Persona fit: P2-measures-seeker. Theoretical commitment: presupposes that measures of behaviour, self-report, and reconstruction are fungible, which Hegarty et al. (2006) explicitly contest.

**Q-14.** *What measure of "thermal comfort" is acceptable to ASHRAE reviewers but also captures the dynamic adaptation effects we know are present?*
Cognitive purpose: deliberation. Answer shape: contrast pair (PMV vs. adaptive vs. dynamic). Evidential demand: measurement-grade with regulatory acceptance. Persona fit: P2-measures-seeker. Theoretical commitment: pragmatic; presupposes a regulator audience.

**Q-15.** *What ecological-momentary-assessment instruments are validated for in-situ affect measurement during architectural walkthroughs of under 5 minutes?*
Cognitive purpose: deliberation. Answer shape: ranked brief. Evidential demand: measurement-grade. Persona fit: P2-measures-seeker. Theoretical commitment: presupposes brief-EMA validity, which is itself a literature (Shiffman et al., 2008).

**Q-16.** *For psychological wellbeing as a DV, do I want Ryff's six-factor model, the WHO-5, the SWLS, or a flourishing measure — and what makes the difference?*
Cognitive purpose: deliberation. Answer shape: ranked brief with construct-coverage map. Evidential demand: measurement-grade. Persona fit: P2-measures-seeker. Theoretical commitment: presupposes the Ryff (1989) hedonic/eudaimonic distinction — itself a theoretical commitment not all reviewers share.

### 4.3 Sensors-seeker (Q-17 to Q-22)

These are the *"I need a piece of hardware or a stream of data"* questions. They map onto the physiological and neural domains of the Outcome_Contractor and onto the indoor-environmental-quality side of the Tagging_Contractor.

**Q-17.** *What's the cheapest reliable sensor for measuring continuous CO₂ at desk height for a 30-person office study, and what does "reliable" buy me beyond a Netatmo?*
Cognitive purpose: deliberation. Answer shape: ranked brief with cost/precision tradeoff. Evidential demand: measurement-grade. Persona fit: P2-sensors-seeker.

**Q-18.** *What's the current state of OPM-MEG for ambulatory architectural-cognition studies — is it usable for a walking-protocol design, or am I three years too early?*
Cognitive purpose: discovery. Answer shape: Toulmin with maturity qualifier. Evidential demand: mechanistic + practical. Persona fit: P2-sensors-seeker.

**Q-19.** *For continuous skin-conductance during a museum visit, what's the wear-vs-quality tradeoff between the Empatica EmbracePlus, BIOPAC dry-electrode, and a research-grade cuff?*
Cognitive purpose: deliberation. Answer shape: contrast pair-of-three. Evidential demand: measurement-grade. Persona fit: P2-sensors-seeker.

**Q-20.** *Which eye-tracker is appropriate for a study of architectural attention in a real classroom (not lab), with motion, with children, with IRB constraints?*
Cognitive purpose: deliberation. Answer shape: ranked brief. Evidential demand: measurement-grade. Persona fit: P2-sensors-seeker. Theoretical commitment: ecological-validity primacy.

**Q-21.** *How do I instrument a residential apartment to measure indoor luminance, spectrum, and occupancy in a way an IRB will approve and tenants will tolerate?*
Cognitive purpose: deliberation. Answer shape: procedure. Evidential demand: practical with ethical gates. Persona fit: P2-sensors-seeker.

**Q-22.** *What's the lowest-cost validated way to capture room-level acoustics for a 4-week study without continuous audio recording (which IRBs increasingly veto)?*
Cognitive purpose: deliberation. Answer shape: procedure with regulatory rebuttal column. Evidential demand: measurement-grade with privacy-compliance. Persona fit: P2-sensors-seeker.

### 4.4 Tests-seeker (Q-23 to Q-28)

These are the *"I need a cognitive or behavioural task"* questions — close cousins of measures-seeker, but the asker wants a *task* rather than a *scale*.

**Q-23.** *Which working-memory task is most sensitive to acute environmental stress in adults, and over what time window?*
Cognitive purpose: deliberation. Answer shape: ranked brief. Evidential demand: measurement-grade. Persona fit: P2-tests-seeker.

**Q-24.** *For an attention-restoration study, do I use the Sustained Attention to Response Task, the Necker Cube, the Digit-Span Backwards, or the Attention Network Test — and which is least sensitive to floor/ceiling effects in healthy young adults?*
Cognitive purpose: deliberation. Answer shape: contrast pair-of-four. Evidential demand: measurement-grade. Persona fit: P2-tests-seeker. Theoretical commitment: presupposes that "attention" is a unitary construct, which the Petersen & Posner (2012) updated taxonomy contests.

**Q-25.** *What's a valid divergent-thinking task that can be administered in under 4 minutes inside a VR headset?*
Cognitive purpose: deliberation. Answer shape: ranked brief. Evidential demand: measurement-grade. Persona fit: P2-tests-seeker.

**Q-26.** *Which spatial-memory task discriminates best between a place-cell-style and a grid-cell-style hippocampal contribution?*
Cognitive purpose: discovery. Answer shape: contrast pair grounded in the Doeller-Burgess (2010) framework. Evidential demand: mechanistic. Persona fit: P2-tests-seeker, P4-theorist.

**Q-27.** *Is there a validated implicit-association test for environmental preference that bypasses the social-desirability confound in restorative-environment self-report?*
Cognitive purpose: discovery. Answer shape: Toulmin with measurement rebuttal. Evidential demand: measurement-grade. Persona fit: P2-tests-seeker.

**Q-28.** *What's the "right" stress-induction protocol if I want a controlled stressor that ethics will approve and that produces a reliable cortisol response in 90% of participants?*
Cognitive purpose: deliberation. Answer shape: procedure with ethical gates. Evidential demand: measurement-grade + ethical. Persona fit: P2-tests-seeker.

### 4.5 Theory-prober (Q-29 to Q-34)

These are the questions of a researcher who already knows the field and is testing a theory. They are the natural home for the Toulmin shape and for Chinn & Brewer's response menu.

**Q-29.** *Does Kaplan's Attention Restoration Theory survive once you control for the affective confound — i.e., is restoration anything more than a mood improvement plus a mediation analysis?*
Cognitive purpose: inquiry. Answer shape: Toulmin with explicit rebuttal column. Evidential demand: causal-with-mechanism. Persona fit: P2-theory-prober. Theoretical commitment: ART-sceptical. Chinn & Brewer (1993) immediately becomes salient: an ART-loyalist reading the same data will *exclude* the confounding studies (response 3) or *reinterpret* them (response 5); an ART-sceptic will *theory-change* (response 7).

**Q-30.** *Is biophilia a single construct, a family of constructs, or a folk category that breaks under measurement scrutiny?*
Cognitive purpose: inquiry. Answer shape: field map with conceptual-validity column. Evidential demand: converging-with-mechanism. Persona fit: P2-theory-prober, P4-theorist.

**Q-31.** *Does the predictive-processing account of architectural experience (Kirsh, 2019; Friston, 2010-style application) make any predictions that distinguish it empirically from a Gibson-style affordance account?*
Cognitive purpose: inquiry. Answer shape: contrast pair with discriminating-prediction column. Evidential demand: mechanistic. Persona fit: P2-theory-prober, P4-theorist. Theoretical commitment: methodologically falsificationist.

**Q-32.** *What evidence would convince me that the Stamps fractal-dimension preference effect is a measurement artefact rather than a perceptual law?*
Cognitive purpose: inquiry. Answer shape: Toulmin with explicit defeater catalogue. Evidential demand: measurement-grade + mechanistic. Persona fit: P2-theory-prober.

**Q-33.** *Is the prospect-refuge account (Appleton, 1975) compatible with the modern isovist literature, or are they describing different things using overlapping terminology?*
Cognitive purpose: discovery. Answer shape: contrast pair with conceptual-mapping column. Evidential demand: converging. Persona fit: P2-theory-prober. Theoretical commitment: synthesist.

**Q-34.** *Where does the predictive-coding-of-architecture programme make a prediction that no other framework makes, and has anyone tested it?*
Cognitive purpose: discovery. Answer shape: field map with falsification-test column. Evidential demand: mechanistic + suggestive. Persona fit: P2-theory-prober.

### 4.6 Cross-product (Q-35 to Q-40)

These are explicitly generated by walking the IV and DV hierarchies. Each question names the IV level and the DV level it sits at, and notes the journey-design implication.

**Q-35.** *(IV: spatial.isovist_openness, low; DV: behav.wayfinding_behavior, low — the low/low cell.)* In an L-shaped corridor with one branch obscured, does adding a single sightline aperture reduce wayfinding-error rate, and is there a critical aperture-area threshold below which the effect vanishes?
Cognitive purpose: inquiry. Answer shape: Toulmin. Evidential demand: causal-with-mechanism. Persona fit: P2-general, P5-practitioner. Journey implication: tractable; one or two empirical studies plus an isovist-theoretic warrant.

**Q-36.** *(IV: spatial — top-level; DV: cog — top-level — the high/high cell.)* What does the field currently know about how spatial environments shape cognition?
Cognitive purpose: discovery. Answer shape: field map. Evidential demand: converging. Persona fit: P2-general (entry question), P7-newcomer. Journey implication: must function as a *portal* — not an answer but a curated set of sub-journeys. Extremely common as a search-bar input; under-served by current literature surveys.

**Q-37.** *(IV: complexity.shannon_entropy, low; DV: affect — top-level, high.)* Does Shannon-entropy of a façade predict the *family* of affective responses (preference, comfort, restorativeness) in similar ways, or does it dissociate across them?
Cognitive purpose: inquiry. Answer shape: contrast pair across sub-DVs. Evidential demand: converging. Persona fit: P2-general, P2-theory-prober. Journey implication: the constitutive bridge inference (X→affect.preference implies X→affect at P=0.85, but not the converse) is exactly what the answer needs.

**Q-38.** *(IV: biophilia — top-level, high; DV: physio.cortisol, low.)* Across the biophilic-design literature, what is the strongest mechanistic claim that survives a meta-analytic check, and what is the critical mediator — direct nature contact, fractal exposure, or affect?
Cognitive purpose: inquiry. Answer shape: field map with mediator structure. Evidential demand: causal-with-mechanism. Persona fit: P2-general, P5-practitioner.

**Q-39.** *(IV: sound — top-level, high; DV: cog.creativity, low.)* What ambient-sound conditions support creative cognition — Mehta-Zhu-Cheema's 70 dB result (2012), the silence-favouring laboratory tradition, or something dependent on phase of the creative task?
Cognitive purpose: deliberation. Answer shape: Toulmin with phase-dependent qualifier. Evidential demand: converging-with-mechanism. Persona fit: P2-general, P2-theory-prober. Journey implication: invites the CREA1 PNU template's phase-model directly.

**Q-40.** *(IV: light, high; DV: physio.circadian, mid.)* What is currently known about non-image-forming light effects on circadian phase in a typical interior, and where does the ipRGC literature actually constrain interior-design choices?
Cognitive purpose: inquiry. Answer shape: field map with ipRGC-warrant chain. Evidential demand: causal-with-mechanism. Persona fit: P2-general, P2-sensors-seeker, P5-practitioner.

---

## 5. What this corpus reveals about journey design

Three observations are worth flagging now, because they constrain the journey designs the students will produce in Tasks 2 and 3 of Track 4.

First, **shape and demand are correlated but not identical.** Most theory-prober questions demand the Toulmin shape, but Q-30 and Q-34 demand a *field map* with a Toulmin nested inside one of its branches. Journey designers should plan to compose answer shapes, not pick one.

Second, **rebuttal economy is the live design problem, not data sufficiency.** For at least nine of the forty questions (Q-07, Q-12, Q-24, Q-29, Q-30, Q-31, Q-32, Q-33, Q-34) the journey will succeed or fail on whether it surfaces the right *defeaters*. This is exactly Chinn & Brewer's (1993) point: a researcher does not arrive without theoretical commitments, and the journey must engage those commitments rather than ignore them. Each prototype should expose a rebuttal panel by default, with the seven Chinn-Brewer responses available as design options for the reader's reaction.

Third, **the high/high cells of the cross-product hierarchy will dominate the search-bar input, but the answers live at the lower cells.** A reader types *"how does spatial environment affect cognition"* (Q-36); the journey must lead them to a *low/low* sub-question they can actually progress on (Q-35 or similar). The Atlas cannot just answer at the level of the question typed in; it must be designed to *resolve* generic questions into specific ones. This is a quasi-Sherlockian inference (Eco & Sebeok, 1983) and is, in our judgement, the central design challenge of Track 4.

---

## 6. Honest limitations of this round

Several limits should be on the page.

The corpus reflects a single LLM's prior on what researchers ask. It overweights environmental-psychology, cognitive-neuroscience, and built-environment-research idioms, because that is the literature CW most readily samples. The students' panels will systematically vary disciplinary home (Section 3.1) and that variance should produce questions CW did not generate.

The five-axis taxonomy is a working tool, not a claim of completeness. Other possible axes include *temporal urgency* (Walton's "stand-still vs. move-on" pressure), *audience* (whom the answer is being prepared for), and *epistemic confidence at entry* (does the asker think they already know the answer, or are they genuinely uncertain?). The students may extend the taxonomy where they find it inadequate.

The cross-product synthesis is sketched, not exhausted. With ~440 IV tags across ~20 domains and ~80 level-2 outcomes across 7 domains, the unconstrained product space is in the hundreds of thousands. The taxonomic *constitutive* hierarchies provide structure; even so, careful subsampling (e.g., the four-corner method in Section 3.3) is necessary or the corpus will collapse into the trivially numerous high/low and low/high cells.

Most importantly, **this is one persona's corpus.** A researcher's questions are not a graduate student's, not a contributor's, not a theorist's, not a practitioner's. The next-passes section below sketches what changes for each.

---

## 7. Next passes (other personas)

Each persona below needs its own corpus following the same protocol. The bullets give the most consequential differences from the researcher round; the students will fill in the corpora.

**P1 Maya Chen, 160 student.** Questions are mainly *information-seeking* and *discovery*. Adequacy demand is *suggestive* — Maya is not yet calibrated on what counts as sufficient evidence. Many questions will be of the form *"what is X"* (definitional), *"does X exist"* (existence), *"how do I find a paper about X"* (navigational). Journey shape will skew to *field map for orientation* and *procedural how-to*. Critically, Maya often *does not yet know the right question to ask*; the journey must do question-resolution work explicitly.

**P3 Jordan Reeves, contributor.** Questions are *deliberative* and *procedural*: how do I tag this article correctly, where does this finding belong in the IV/DV hierarchy, what does it count as evidence for, how do I record uncertainty. The corpus will be smaller (~15 questions) but each will demand a *procedure* answer shape with very high specificity.

**P4 Prof. Lena Bergström, theorist.** Questions are *inquiry* and *persuasion*: where does my framework win, where does it get defeated, what would change a sceptic's mind. Her corpus will be heavy on Toulmin and contrast-pair shapes, with explicit Chinn-Brewer rebuttal economies. She will also generate many questions about *theoretical commitment* — questions that name a frame and ask whether the literature supports or undermines it.

**P5 Sam Nakamura, practitioner.** Questions are *deliberative* and *persuasive*: should I install daylight sensors, will biophilic features survive a value-engineering pass, what does the literature say in language a client will accept. Adequacy demand is *converging* but with a strong constraint that the answer be *brief, citable, and rebuttal-aware*. His corpus will skew to *ranked brief* and *contrast pair* shapes.

**P6 TA.** Questions are about *teaching and grading*: what does a "good" Track-1 image collection look like, how do I assess a student's evidence-extraction quality, what counts as a sufficient warrant in a 160sp submission. The corpus will be small and procedural. The interesting twist is that the TA's adequacy condition is partly social (David's standards) rather than purely epistemic.

**P7 Newcomer.** Questions are *discovery* almost exclusively. The newcomer does not yet know the structure of the field. The corpus will skew to *what is X*, *where do I start*, and *who are the major figures*. Journey shape will be *guided tour* — a sub-shape of field map with progressive disclosure.

**P8 PI.** Questions are *strategic*: where is the field going, what should my lab work on, who is hiring, what does the funding landscape look like. The corpus will be small but each item will demand a synthesis across many sub-literatures, often delivered as a *brief* with explicit confidence intervals.

The protocol is the same; the persona-fit axis (Axis 4) and theoretical-commitment axis (Axis 5) shift in each pass. Students should expect the per-persona corpora to differ in size: P1 (largest, ≥60 questions), P2 (this corpus, ~40), P4 (~30), P5 (~30), P7 (~25), P3 (~15), P8 (~15), P6 (~10).

---

## 8. References

Aher, G. V., Arriaga, R. I., & Kalai, A. T. (2023). Using large language models to simulate multiple humans and replicate human subject studies. *Proceedings of the 40th International Conference on Machine Learning*, 337–371. (Google Scholar citations: ~640.)

Appleton, J. (1975). *The experience of landscape*. Wiley. (Google Scholar citations: ~3,400.)

Argyle, L. P., Busby, E. C., Fulda, N., Gubler, J. R., Rytting, C., & Wingate, D. (2023). Out of one, many: Using language models to simulate human samples. *Political Analysis*, *31*(3), 337–351. https://doi.org/10.1017/pan.2023.2 (Google Scholar citations: ~830.)

Beaty, R. E., Benedek, M., Silvia, P. J., & Schacter, D. L. (2016). Creative cognition and brain network dynamics. *Trends in Cognitive Sciences*, *20*(2), 87–95. https://doi.org/10.1016/j.tics.2015.10.004 (Google Scholar citations: ~1,420.)

Beaty, R. E., Seli, P., & Schacter, D. L. (2019). Network neuroscience of creative cognition. *Current Opinion in Behavioral Sciences*, *27*, 22–30. https://doi.org/10.1016/j.cobeha.2018.08.013 (Google Scholar citations: ~310.)

Cartwright, N., & Hardie, J. (2012). *Evidence-based policy: A practical guide to doing it better*. Oxford University Press. (Google Scholar citations: ~1,180.)

Chi, M. T. H. (2009). Active-constructive-interactive: A conceptual framework for differentiating learning activities. *Topics in Cognitive Science*, *1*(1), 73–105. https://doi.org/10.1111/j.1756-8765.2008.01005.x (Google Scholar citations: ~2,520.)

Chinn, C. A., & Brewer, W. F. (1993). The role of anomalous data in knowledge acquisition: A theoretical framework and implications for science instruction. *Review of Educational Research*, *63*(1), 1–49. https://doi.org/10.3102/00346543063001001 (Google Scholar citations: ~3,150.)

Doeller, C. F., Barry, C., & Burgess, N. (2010). Evidence for grid cells in a human memory network. *Nature*, *463*(7281), 657–661. https://doi.org/10.1038/nature08704 (Google Scholar citations: ~1,460.)

Eco, U., & Sebeok, T. A. (Eds.). (1983). *The sign of three: Dupin, Holmes, Peirce*. Indiana University Press. (Google Scholar citations: ~1,140.)

Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, *11*(2), 127–138. https://doi.org/10.1038/nrn2787 (Google Scholar citations: ~10,200.)

Hegarty, M., Montello, D. R., Richardson, A. E., Ishikawa, T., & Lovelace, K. (2006). Spatial abilities at different scales: Individual differences in aptitude-test performance and spatial-layout learning. *Intelligence*, *34*(2), 151–176. https://doi.org/10.1016/j.intell.2005.09.005 (Google Scholar citations: ~810.)

Higgins, J. P. T., Thomas, J., Chandler, J., Cumpston, M., Li, T., Page, M. J., & Welch, V. A. (Eds.). (2024). *Cochrane handbook for systematic reviews of interventions* (Version 6.5). Cochrane. (Google Scholar citations of the original 2019 edition: ~46,000.)

Hill, A. B. (1965). The environment and disease: Association or causation? *Proceedings of the Royal Society of Medicine*, *58*(5), 295–300. (Google Scholar citations: ~24,500.)

Horton, J. J. (2023). Large language models as simulated economic agents: What can we learn from *homo silicus*? *NBER Working Paper No. 31122*. https://doi.org/10.3386/w31122 (Google Scholar citations: ~430.)

Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLoS Medicine*, *2*(8), e124. https://doi.org/10.1371/journal.pmed.0020124 (Google Scholar citations: ~10,800.)

Joye, Y., & van den Berg, A. E. (2011). Is love for green in our genes? A critical analysis of evolutionary assumptions in restorative environments research. *Urban Forestry & Urban Greening*, *10*(4), 261–268. https://doi.org/10.1016/j.ufug.2011.07.004 (Google Scholar citations: ~470.)

Kaplan, S. (1995). The restorative benefits of nature: Toward an integrative framework. *Journal of Environmental Psychology*, *15*(3), 169–182. https://doi.org/10.1016/0272-4944(95)90001-2 (Google Scholar citations: ~10,400.)

Kunz, W., & Rittel, H. W. J. (1970). *Issues as elements of information systems* (Working Paper No. 131). Institute of Urban and Regional Development, University of California, Berkeley. (Google Scholar citations: ~1,150. The foundational paper for IBIS — issue-based information systems — which underlies modern dialogue-mapping and argument-structure tools.)

Conklin, J. (2005). *Dialogue mapping: Building shared understanding of wicked problems*. Wiley. (Google Scholar citations: ~2,180. The accessible IBIS treatment used in design and policy facilitation; the source for typing edges as *responds-to*, *supports*, *objects-to*.)

Novak, J. D., & Gowin, D. B. (1984). *Learning how to learn*. Cambridge University Press. (Google Scholar citations: ~14,800. The canonical introduction to concept maps as labelled-directed graphs of conceptual relationships.)

Novak, J. D. (2010). *Learning, creating, and using knowledge: Concept maps as facilitative tools in schools and corporations* (2nd ed.). Routledge. (Google Scholar citations: ~3,950. Updated treatment of the concept-map technique with examples from research and industrial applications.)

Wardley, S. (2018). *Wardley maps: Topographical intelligence in business* (Self-published; CC BY-SA, available at https://medium.com/wardleymaps and https://learnwardleymapping.com). (Google Scholar/citation tracking is sparse for the self-published form, but the technique is widely adopted in technology strategy; cf. Wardley's earlier *Bits or pieces?* essays. Useful as the canonical example of a field map with an explicit evolution axis.)

Kirsh, D. (2019). When is a mind embodied? In M. L. Cappuccio (Ed.), *Handbook of embodied cognition and sport psychology* (pp. 131–158). MIT Press. (Google Scholar citations: ~95.)

Mehta, R., Zhu, R. (J.), & Cheema, A. (2012). Is noise always bad? Exploring the effects of ambient noise on creative cognition. *Journal of Consumer Research*, *39*(4), 784–799. https://doi.org/10.1086/665048 (Google Scholar citations: ~830.)

Meyers-Levy, J., & Zhu, R. (J.). (2007). The influence of ceiling height: The effect of priming on the type of processing that people use. *Journal of Consumer Research*, *34*(2), 174–186. https://doi.org/10.1086/519146 (Google Scholar citations: ~830.)

Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, Article 2. https://doi.org/10.1145/3586183.3606763 (Google Scholar citations: ~2,140.)

Petersen, S. E., & Posner, M. I. (2012). The attention system of the human brain: 20 years after. *Annual Review of Neuroscience*, *35*, 73–89. https://doi.org/10.1146/annurev-neuro-062111-150525 (Google Scholar citations: ~3,580.)

Pollock, J. L. (1987). Defeasible reasoning. *Cognitive Science*, *11*(4), 481–518. https://doi.org/10.1207/s15516709cog1104_4 (Google Scholar citations: ~2,090.)

Pollock, J. L. (1995). *Cognitive carpentry: A blueprint for how to build a person*. MIT Press. (Google Scholar citations: ~2,470.)

Ryff, C. D. (1989). Happiness is everything, or is it? Explorations on the meaning of psychological well-being. *Journal of Personality and Social Psychology*, *57*(6), 1069–1081. https://doi.org/10.1037/0022-3514.57.6.1069 (Google Scholar citations: ~16,500.)

Said-Metwaly, S., Van den Noortgate, W., & Kyndt, E. (2017). Approaches to measuring creativity: A systematic literature review. *Creativity: Theories – Research – Applications*, *4*(2), 238–275. https://doi.org/10.1515/ctra-2017-0013 (Google Scholar citations: ~290.)

Santurkar, S., Durmus, E., Ladhak, F., Lee, C., Liang, P., & Hashimoto, T. (2023). Whose opinions do language models reflect? *Proceedings of the 40th International Conference on Machine Learning*, 29971–30004. (Google Scholar citations: ~620.)

Sarason, S. B. (1974). *The psychological sense of community: Prospects for a community psychology*. Jossey-Bass. (Google Scholar citations: ~5,290.)

Shiffman, S., Stone, A. A., & Hufford, M. R. (2008). Ecological momentary assessment. *Annual Review of Clinical Psychology*, *4*, 1–32. https://doi.org/10.1146/annurev.clinpsy.3.022806.091415 (Google Scholar citations: ~6,460.)

Toulmin, S. E. (2003). *The uses of argument* (Updated ed.). Cambridge University Press. (Original work published 1958.) (Google Scholar citations: ~24,800.)

Ulrich, R. S. (1984). View through a window may influence recovery from surgery. *Science*, *224*(4647), 420–421. https://doi.org/10.1126/science.6143402 (Google Scholar citations: ~7,650.)

Vasquez-Echeverria, A., González, M., & Lacasa, F. (2017). The effect of ceiling height on construal level: A pre-registered replication of Meyers-Levy and Zhu (2007). *Collabra: Psychology*, *3*(1), 6. https://doi.org/10.1525/collabra.65 (Google Scholar citations: ~25.)

Walton, D. N. (1995). *A pragmatic theory of fallacy*. University of Alabama Press. (Google Scholar citations: ~1,510.)

*Citation counts are CW's best estimates as of late April 2026 and should be re-checked by students before use; counts move quickly. CW's knowledge cutoff is May 2025; counts after that date are projections rather than observations and should be flagged accordingly.*
