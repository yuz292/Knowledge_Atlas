# Track 4 — Task Design and Pedagogical Arc

*CW, 2026-04-27. Updated 2026-04-27 with David's directives on persona
ownership, carried-exemplar approach, and revised budget.*

## How the design has been shaped by three directives

David's three governing directives shape what follows. (i) **Each
student owns one persona.** A four-student team is a constellation of
four parallel pipelines — one Maya, one researcher, one practitioner,
one PI, or whatever the term's allocation is — not a single shared
corpus with role specialisation. (ii) **The team's collective work is
peer review and critique** of the individual pipelines, not collective
ownership of any single pipeline; the team is the cross-persona
intelligence that pushes each student to defend their journey to
teammates working from different commitments. (iii) **The researcher
persona is carried all the way through the three tasks as the canonical
worked exemplar.** Students study the researcher artefacts at each task
to know what "done" looks like, then apply the same protocol to their
own persona. (A fourth task in COGS 160F, weeks 8–10, will be developed
separately by David.)

The budget is weeks 5, 6, and 7, with half of week 8 available if a
team needs it.

## The arc in one paragraph

A Track 4 student arrives in week five of the term having never
designed an evidential journey. By the end of week seven (or the
midpoint of week eight) they have built and prototyped one for their
chosen persona, after watching the researcher pipeline carried through
the same three tasks as a worked exemplar. In Task 1 the student
learns what *questions* look like by generating a corpus of them for
their persona and tagging it on the five axes; the worked exemplar is
the forty-question researcher corpus. In Task 2 the student learns
what *answers* look like by winnowing their corpus and fitting each
surviving question to one of the five canonical answer shapes; the
worked exemplar is a ten-question researcher fitting catalog covering
all five shapes with named defeaters. In Task 3 the student builds
one journey end-to-end as a working HTML prototype with a real
Chinn-Brewer rebuttal panel; the worked exemplar is the Q-29 journey
on Attention Restoration Theory and the affective confound, drawn
through Toulmin's canonical layout with a populated rebuttal panel.

The three tasks compound. Task 2 cannot be done well unless Task 1 is done
honestly — a corpus of inflated, unspecific, or untagged questions cannot
support fitting. Task 3 cannot be done well unless Task 2 is done
specifically — a journey prototype that has not committed to an answer
shape and a defeater catalogue produces a page sequence that wanders. The
scaffolds below are designed so a student who follows them produces
deliverables that compound rather than deliverables that have to be
rebuilt at the next stage.

The three weeks are tight. Each task is roughly a week of work for a team
of four. The midpoint of each week is a checkpoint; the end of each week
is a graded submission.

---

## Task 1 — Build a Persona Question Corpus

**Worth: 75 points. Due: end of week 5.**

### Why this task exists

The first move in designing for an audience is to know what the audience
is asking. A great deal of design work goes wrong because the designer
imagines a generic user with a generic question and engineers a generic
answer; the generic answer satisfies no one. The corpus you build in Task
1 is a corrective. It forces you to commit, on paper, to specific
questions phrased in the way a specific persona would phrase them, with
the *adequacy condition* — what would make the answer feel insufficient
— written out explicitly. Without an adequacy condition you cannot judge
whether a journey is succeeding; you can only judge whether it is
finishing.

A second reason to begin here. Researchers, students, contributors,
practitioners, theorists, and PIs do not ask the same questions. They do
not even ask the same kinds of questions. Treating the Atlas as if it
served a single user produces a system that is shaped to no actual user.
The corpus is the artefact that lets the team reason about persona
variability concretely rather than as a slogan.

### What the team produces

A spreadsheet (or equivalent JSON) with one row per question. Every row
carries the following fields. The first three are the question itself;
the next five are the axis tags from the canonical taxonomy; the last
three are provenance.

| Field | What it is |
|-------|-----------|
| `id` | Local ID, e.g., R-Q-014 for the fourteenth researcher question |
| `question` | The question, phrased in the asker's voice |
| `adequacy_condition` | One sentence describing what would make the answer feel insufficient |
| `cognitive_purpose` | information-seeking / inquiry / deliberation / persuasion / discovery |
| `answer_shape` | Toulmin / field-map / procedure / contrast-pair / ranked-brief |
| `evidential_demand` | suggestive / converging / mechanistic / causal-with-mechanism / measurement-grade |
| `persona_fit` | persona ID + sub-flavour |
| `theoretical_commitment` | the ontological or methodological assumption the question embeds |
| `source` | panel / mining / cross-product |
| `provenance` | panel ID, template ID, or hierarchy coordinates |
| `notes` | optional |

The team's persona for this term will be assigned. Most teams will work
on the researcher persona (P2) or the 160 student persona (P1). Whatever
the persona, the team produces 40 to 60 winnowed questions covering all
five sub-flavours appropriate to that persona.

### Scaffolds for Task 1

**Scaffold 1.1 — Persona ownership and shared-infrastructure roles.**
Each student owns the full pipeline for *their* persona — they
generate, mine, synthesise, tag, and curate their own forty-to-sixty
question corpus. To avoid each of the four students rebuilding the
same scaffolding four times, the team distributes four shared-
infrastructure roles. These are *infrastructure roles*, not
*ownership roles*; the artefacts each student delivers are their own.

| Shared-infrastructure role | Responsibility |
|---------------------------|---------------|
| Panel architect | Stands up the LLM-panel infrastructure: system-prompt template, scenario-card library, agent-configuration matrix. All four students draw from this infrastructure to run their own per-persona panels. |
| Mining lead | Maintains the team's running list of PNU templates and gold extractions to sample from; writes the mining-prompt template once, used by all four. |
| Cross-product lead | Maintains the team's working notes on the IV × DV hierarchies; writes the four-corner generation template once, used by all four. |
| Codebook custodian | Owns the team's shared tagging codebook so that the five-axis tags mean the same thing across the four corpora. Does *not* own anyone's tags; owns tagging consistency. |

**Scaffold 1.2 — LLM-panel system prompt template (Panelist role).** Use
this verbatim, substituting the bracketed fields. Run with at least eight
agent variants per panel, varying career stage, discipline, methodology,
and theoretical commitment.

> You are *[Persona Name]*, a *[career stage]* researcher in
> *[disciplinary home]*. Your methodological orientation is *[quantitative
> experimentalist / mixed-methods / computational / ethnographic /
> instrument-development / neuroimaging-led]*. Your theoretical
> commitments include *[neutral / Kaplan-loyalist / Ulrich-loyalist /
> predictive-processing-leaning / embodied-cognition-leaning /
> Stevens-style operationalist / pragmatist]*. You are not a chatbot
> playing a role; you are this researcher, with this researcher's
> instincts about what questions are worth asking and what kinds of
> answers would feel adequate.
>
> A scenario card follows. Read it. Then answer the four questions
> below, briefly, in the voice you would use if you were typing into a
> private notebook.
>
> **Scenario.** *[scenario text]*
>
> **Q1.** What would you type into the Atlas search bar right now?
> **Q2.** What kind of answer would satisfy you — what would the answer
> have to look like for you to close the tab and feel served?
> **Q3.** What would make the answer feel insufficient — what is the
> failure mode you fear?
> **Q4.** What is one further question you would want to ask once you
> received an initial answer?

**Scaffold 1.3 — Three example scenario cards.** A team should write
fifteen to twenty cards in total, varying scenario type. Three to seed
the writing.

> *Card A.* You are preparing a manuscript revision. Reviewer 2 asks
> whether you have considered restorativeness as a confound in your
> wayfinding study. You are not sure how to address this without
> running additional analyses.

> *Card B.* You have just been awarded a small pilot grant ($15K) to
> test whether daylight exposure during the workday improves cognitive
> performance in graduate students. You need to choose your dependent
> variable in the next two weeks.

> *Card C.* A colleague mentions at lunch that the field has moved away
> from Kaplan's Attention Restoration Theory. You have been citing it
> for years and feel embarrassed not to know the current consensus. You
> open the Atlas after lunch.

**Scaffold 1.4 — One worked panel run (sample output).** This is what a
single agent should produce for Card A. The Panelist student should run
many of these and discard ones that are vague.

> *Agent: Mid-PhD student, environmental psychology, mixed-methods,
> Kaplan-loyalist.*
>
> Q1: *"is restorativeness a confound for wayfinding"*
> Q2: A clear statement of whether restorativeness has been treated as a
> confound vs. a covariate in published wayfinding studies, ideally with
> a citation to a paper that reports the analysis both ways.
> Q3: If the answer is just a list of papers about restorativeness in
> general — that doesn't help me. I need to know whether there's a
> wayfinding study that handled this.
> Q4: If yes, how did they operationalise restorativeness during a
> wayfinding task? PRS retrospectively, or some momentary measure?

**Scaffold 1.5 — Mining prompt template (Miner role).** Run this prompt
against each sampled PNU template (`Article_Eater_PostQuinean_v1_recovery/data/templates/`).

> Below is a Predictive-Neural-Unit (PNU) template from the Knowledge
> Atlas. Read it.
>
> **Step 1.** State, in one sentence, the question this template
> answers.
> **Step 2.** State three to five questions that a researcher who had
> just received this template's answer would *next* ask.
> **Step 3.** For each follow-up question, state one sentence about what
> would make an answer feel insufficient (its adequacy condition).
> **Step 4.** Tag each follow-up question on persona — would a doctoral
> student, a postdoc, or a senior PI most plausibly ask it?
>
> *Template:*
> *[paste template JSON]*

**Scaffold 1.6 — Cross-product generator (Synthesist role).** Walk the
two hierarchies. Sample at least three IV domains and three DV domains.
For each (IV-level, DV-level) corner, generate three to five questions
in the form below.

> Generate a research question of the form: "How does *[IV at level k of
> the Tagging hierarchy]* affect *[DV at level m of the Outcome
> hierarchy]*, possibly moderated by *[third variable]*?"
>
> Then state: (a) what published evidence already exists on this question
> at the chosen levels; (b) what would constitute a falsifying finding;
> (c) which axis of the answer-shape taxonomy this question naturally
> demands.

**Scaffold 1.7 — Tagging coding scheme (Curator role).** Each axis has a
short list of allowed values; if a question doesn't fit, the Curator
either re-tags or flags for the team. The five-axis taxonomy is in §2
of the corpus document; the worked tagging below is the operational
form.

> Q-12 example:
> *"What's the appropriate dependent variable if my hypothesis is that
> high-ceiling rooms increase abstract thinking — measure abstract
> thinking directly, or measure the construal-level proxy?"*
>
> cognitive_purpose: deliberation
> answer_shape: contrast-pair
> evidential_demand: measurement-grade
> persona_fit: P2-measures-seeker
> theoretical_commitment: presupposes Meyers-Levy & Zhu construal-level
> account; the question would not arise without it
> adequacy_condition: fails if it does not name a specific instrument
> for each option and a specific reason to prefer one

### Grading rubric for Task 1

| Dimension | Points | What earns full credit |
|-----------|--------|----------------------|
| Coverage | 20 | Each of the five sub-flavours has at least five questions; cross-product corners are populated |
| Tagging quality | 20 | Five-axis tags are present, internally consistent, and survive a peer-review pass |
| Adequacy conditions | 15 | Every question has a sentence that names what would make the answer insufficient |
| Provenance | 10 | Every question is traced to its panel run, mined template, or hierarchy coordinates |
| Honest documentation | 10 | The methods file documents panel configurations, mining samples, and known LLM-panel limitations |

### Pitfalls

The single largest failure mode is questions that read smoothly but
cannot be journey-designed because their adequacy condition is "I will
know it when I see it". The Curator's job in week one is to gate hard on
adequacy conditions. A question without a one-sentence adequacy
condition does not enter the corpus; it goes back to the role that
produced it for revision.

A second failure mode is over-mining: producing 200 questions that all
follow the same pattern from one source. Coverage of all five
sub-flavours is the antidote, and the four-corner cross-product walk is
the structural prompt.

---

## Task 2 — Winnow and Fit Answer Shapes

**Worth: 75 points. Due: end of week 6.**

### Why this task exists

A corpus is necessary but not sufficient. Without commitment to *what
the answer to each question would look like*, the corpus is a list. The
fitting move — pairing a question with one of the five canonical answer
shapes and naming at least one defeater the answer must surface —
forces the team to anticipate the journey before the journey is built.
A page sequence that has not committed to an answer shape will wander;
a journey that has not named a defeater will surprise its reader (and
not in the helpful sense).

The pedagogical goal of Task 2 is to move the team from "questions exist
in five flavours" to "answers come in five shapes, and pairing question
to shape is itself a design move that can go right or wrong."

### What the team produces

Two artefacts.

**(a) The working corpus.** The Task-1 corpus, run through the
four-stage winnowing protocol, with three new fields added to each
surviving row.

| New field | What it is |
|-----------|-----------|
| `chosen_shape` | The answer shape from the catalogue: Toulmin / field-map / procedure / contrast-pair / ranked-brief |
| `shape_sketch` | One paragraph describing how the shape would be filled in for *this* question — what would go in each part of the diagram |
| `named_defeaters` | At least one and ideally two or three named defeaters: findings or arguments the journey must surface to be honest |

**(b) The winnowing log.** A short document recording how the corpus
was reduced and what was set aside. Records counts at each sieve stage,
notes which items were moved to the next-pass backlog (i.e., reclassified
as belonging to a different persona), and identifies any gaps the team
chose not to fill.

### Scaffolds for Task 2

**Scaffold 2.1 — The four-stage winnowing protocol (operational form).**
Run in this order. Track counts at each stage.

> **Stage 1 — Deduplicate.** Two questions are duplicates if they share
> all five tags *and* would be answered by the same journey. Merge,
> credit both sources. Expected attrition: ~33%.
>
> **Stage 2 — Adequacy gate.** Drop any row whose adequacy condition the
> team cannot articulate in one sentence after a five-minute discussion.
> Expected attrition: ~15-20%.
>
> **Stage 3 — Persona-fit gate.** Move any item the team would
> re-classify to a different persona to the next-pass backlog. Do not
> discard. Expected attrition: ~10%.
>
> **Stage 4 — Coverage balance.** Inspect the surviving items against
> the five axes and the four cross-product corners. Empty cells get
> targeted generation passes or written notes acknowledging the gap.
> Expected effect: small additions, not subtractions.

**Scaffold 2.2 — Schema-fitting decision tree.** This is the heuristic
for picking the right shape. The team should treat it as a starting
point, not a prescription; ambiguous cases get team discussion.

> If `cognitive_purpose` is **discovery**:
>   → answer shape is usually **field map**
>
> If `cognitive_purpose` is **inquiry** and `evidential_demand` is
> **causal-with-mechanism**:
>   → answer shape is usually **Toulmin**
>
> If `cognitive_purpose` is **deliberation** and the asker is choosing
> between two to four options:
>   → answer shape is **contrast pair**
>
> If `cognitive_purpose` is **deliberation** and the asker is choosing
> among five or more options under brevity constraint:
>   → answer shape is **ranked brief**
>
> If the question demands a step-by-step protocol with regulatory or
> ethical gates:
>   → answer shape is **procedure**
>
> If `theoretical_commitment` is *adversarial* — i.e., the asker is
> testing a theory against a competing one:
>   → answer shape is **Toulmin** with a mandatory rebuttal panel
>
> Composite shapes: a field map may have a Toulmin nested inside one of
> its branches; a contrast pair may resolve into a ranked brief once
> the differentia have been weighted. Composition is allowed; opacity
> is not — the chosen shape must be nameable.

**Scaffold 2.3 — Defeater identification heuristic.** For each surviving
question, ask the team to answer four sub-questions. At least one
*real* defeater — i.e., a finding or argument that exists in the
literature, not a hypothetical one — must be named per question.

> 1. *What study or finding would, if true, falsify the answer the
>    journey would deliver?*
> 2. *What alternative explanation does the answer not yet rule out?*
> 3. *What scope condition is the answer assuming — what populations,
>    settings, or instruments would the answer fail to cover?*
> 4. *What theoretical commitment does the question embed that a sceptic
>    would reject from outside?*
>
> A defeater that survives all four sub-questions and is grounded in a
> citable source is a *strong* defeater. The journey must surface at
> least one strong defeater; if the team cannot find one, the question
> is flagged for further mining.

**Scaffold 2.4 — Worked example: three questions through the full
pipeline.** This is the concrete deliverable shape the team should
imitate.

> **Q-29.** *"Does Kaplan's Attention Restoration Theory survive once you
> control for the affective confound?"*
>
> chosen_shape: **Toulmin**
> shape_sketch: Data — re-analyses controlling for affect attenuate the
> restoration effect by 40-60% (Joye & van den Berg, 2011). Claim — ART
> partly survives the affect control; mechanism uncertain. Warrant —
> if a putative mechanism is not separable from a confounder, it is not
> established. Backing — mediation-analysis norms (MacKinnon, 2008).
> Qualifier — adult, healthy samples; office and indoor-plant studies.
> Rebuttal — affect may mediate (not confound) the restoration effect.
> named_defeaters: (i) Joye & van den Berg's (2011) re-analysis as a
> primary defeater; (ii) mediation-vs-confound conceptual distinction
> as a secondary defeater that re-licenses the original ART claim if
> the team treats affect as mediator.
>
> **Q-09.** *"What's the best validated instrument for perceived
> restorativeness in office settings?"*
>
> chosen_shape: **ranked brief**
> shape_sketch: Five rows — PRS-11, ROS-6, SBE single-item probe,
> POMS-SF as proxy, custom VAS — with item count and evidence quality
> per row.
> named_defeaters: (i) PRS-11's validation samples are biased toward
> college-student populations and its measurement invariance across
> cultures has been challenged (Pasini et al., 2014); (ii) all
> instruments measure perceived restorativeness, not actual
> restoration outcome — a mood-improvement confound persists at the
> instrument level, not just at the theory level.
>
> **Q-21.** *"How do I instrument a residential apartment to measure
> indoor luminance, spectrum, and occupancy in a way an IRB will
> approve and tenants will tolerate?"*
>
> chosen_shape: **procedure**
> shape_sketch: Five numbered steps with provenance per step (sensor
> placement per CIE S 026; sampling rate per Brown et al. 2022; PIR
> occupancy per IRB norms; tenant negotiation per compliance literature;
> seven-day pilot per lab convention).
> named_defeaters: (i) any IRB will reject cameras in residential
> interiors absent extraordinary justification — the procedure must
> not assume cameras; (ii) sensor-failure modes (battery, occlusion)
> typically appear in week one — without a pilot the deployment data
> is unusable.

### Grading rubric for Task 2

| Dimension | Points | What earns full credit |
|-----------|--------|----------------------|
| Winnowing rigour | 15 | Counts at each sieve stage; backlog populated; gaps acknowledged |
| Shape fitting | 25 | Every surviving question has a chosen shape with a one-paragraph sketch; composite shapes are flagged and justified |
| Defeater quality | 25 | At least one strong (citable) defeater per question; the four-question heuristic is applied throughout |
| Honesty about uncertainty | 10 | Cases where the team's confidence is low are flagged, not hidden |

### Pitfalls

The most common failure mode is choosing a shape too quickly and
sketching it generically. A "Toulmin" sketch that does not actually
name the warrant is not yet a sketch; it is a label. The Curator's
job in this task is to gate hard on the *shape sketch* field — every
sketch must name every part of the chosen shape, with the data and
warrant grounded in actual literature where possible.

A second failure mode is defeater laundering: writing a defeater that
the team has invented rather than found. A defeater the journey must
surface should be a defeater that already exists in the literature; if
the team cannot find one, the question should be flagged as
under-supported rather than dressed up with a hypothetical defeater.

---

## Task 3 — Prototype an Evidential Journey

**Worth: 75 points. Due: end of week 7.**

### Why this task exists

The first two tasks produce paper artefacts; the third produces a working
artefact. A journey is not designed when it is described in prose; it is
designed when a reader can click through it from a typed-in question to
an answer that is properly warranted, qualified, and rebuttal-aware. The
move from spec to prototype reveals everything that the spec elided.

The pedagogical aim is integrative. Task 3 forces the team to make
choices the previous tasks could defer: which page does the reader land
on; what is on the page above the fold; how is the rebuttal exposed;
what is the next click. These choices are where journey design lives,
and they cannot be made well without the corpus and the shape catalogue
behind them.

### What the team produces

Three artefacts.

**(a) One working journey prototype.** A small set of HTML files (no
back-end required; no framework required) that together implement an
evidential journey for one question chosen from the team's working
corpus. The prototype must include:

> a landing page that accepts the typed-in question (or its rough form);
> a sequence of pages or a single page with disclosure regions that
> implements the chosen answer shape, drawing the diagram inline;
> at least one Chinn-Brewer rebuttal panel exposed by default and
> populated with the team's named defeaters;
> a closing page that asks the reader to indicate which Chinn-Brewer
> response they would take and why.

**(b) An LLM-panel reader test.** The team runs three to five LLM
agents through the prototype as readers and records, for each agent,
(i) where the agent stopped, (ii) which Chinn-Brewer response the
agent took, (iii) what the agent said would have made the journey more
adequate. This is not a substitute for human user testing but is a
defensible first-pass check.

**(c) A short written reflection.** Two pages, in academic prose. What
the team learned in moving from spec to prototype; what the prototype
revealed that the corpus and fitting passes had hidden; what the team
would change if they had three more weeks.

### Scaffolds for Task 3

**Scaffold 3.1 — HTML/CSS skeleton kit.** The team is given a starter
file for each answer shape with the diagram already wired and CSS
variables consistent with the rest of the site. The student fills in
the content. The shape catalogue page itself is the canonical reference.

> *Toulmin starter:* skeleton SVG with placeholder text in each of the
> six positions (data, claim, qualifier, warrant, backing, rebuttal).
> The student replaces placeholders with their question's content.
>
> *Field-map starter:* skeleton SVG with a vertical time axis and four
> empty node positions; the student adds nodes and labelled edges per
> Novak convention.
>
> *Procedure starter:* HTML ordered list with two-column layout (step
> text + provenance column).
>
> *Contrast-pair starter:* HTML grid table, three columns, six rows
> with row-label slots.
>
> *Ranked-brief starter:* HTML grid table, five columns (rank, option,
> reason, item count, evidence quality).
>
> *Chinn-Brewer widget:* the existing
> `chinn_brewer_response_widget.html` is included as an iframe. The
> student must populate the anomaly text with a defeater from their
> corpus.

**Scaffold 3.2 — A worked journey for Q-29 (Toulmin path).** The team
is given a fully-built reference journey. They are not asked to imitate
it slavishly; they are asked to use it as a calibration of what
"finished" looks like.

> *Page 1 — Landing.* Title: "Does Attention Restoration Theory
> survive the affective confound?" Single search box pre-populated
> with the question. One-paragraph orientation telling the reader what
> the journey will do (build a Toulmin, surface the affect-confound
> defeater, ask for the reader's response).
>
> *Page 2 — Data.* Visualisation of the affect-controlled re-analyses
> attenuating the restoration effect. Plain prose summary, citation to
> Joye & van den Berg (2011). One sentence on what the data does and
> does not show.
>
> *Page 3 — Warrant + Backing.* Statement of the warrant ("if a
> putative mechanism is not separable from a confounder, it is not
> established"). Backing in mediation-analysis norms with citation
> to MacKinnon (2008).
>
> *Page 4 — Claim with Qualifier.* "ART partly survives the affect
> control, but the mechanism is uncertain. Adult, healthy samples;
> office and indoor-plant studies."
>
> *Page 5 — Rebuttal.* The rebuttal panel: affect may mediate
> rather than confound. The Chinn-Brewer widget exposed inline.
>
> *Page 6 — Reader response.* The reader is asked which of the seven
> Chinn-Brewer responses they would take and why. Their answer is
> stored locally (no server); the journey ends.

**Scaffold 3.3 — LLM-panel reader-test prompt.** The team uses this
prompt to run three to five LLM-panel reader tests on the prototype.

> You are *[persona]*, a researcher with the following background and
> commitments: *[brief profile from Task 1's panel configurations]*.
> You have just opened the Knowledge Atlas and are walking through a
> journey on the question "*[journey question]*". The journey's
> sequence of pages is below.
>
> *[paste page contents]*
>
> Walk through the journey. After each page, briefly note: (a) what
> you understood; (b) what you wanted but did not get; (c) whether
> you would continue or close the tab. At the end, indicate which
> Chinn-Brewer response you would take and why.

**Scaffold 3.4 — Reflection prompt.** Two pages of academic prose. The
prompt is the prompt — students should not need a template, but they
will not know what is being asked of them without one.

> Write two pages, in academic prose, addressing the following.
> What did the move from corpus to prototype reveal that the corpus
> alone had hidden? Where did your spec turn out to be ambiguous when
> you tried to implement it? What would you do differently if you
> were to design a second journey? What did the LLM-panel reader
> test surface that you had not anticipated? What is one thing about
> your journey that you remain uncertain about, and what would resolve
> the uncertainty?

### Grading rubric for Task 3

| Dimension | Points | What earns full credit |
|-----------|--------|----------------------|
| Working prototype | 30 | Five+ pages or one rich disclosure page; correct diagram; Chinn-Brewer widget populated and exposed by default |
| Rebuttal economy | 15 | Defeaters from Task 2 are surfaced honestly; reader response stage works |
| LLM-panel reader test | 15 | Three to five readers run; per-reader notes recorded; failures of the journey are reported |
| Reflection | 10 | Two pages in academic prose, honest about ambiguities and uncertainties |
| Site integration | 5 | Top nav, breadcrumb, side-nav, footer; consistent with the rest of the Atlas |

### Pitfalls

The single largest failure mode is treating the prototype as a
front-end exercise and skipping the rebuttal panel. A journey without
an exposed Chinn-Brewer panel is not yet an evidential journey; it is
a tutorial. The grading rubric weights rebuttal economy at 15% of
Task 3 specifically because a beautiful prototype that hides its
defeaters has missed the point.

A second failure mode is over-engineering the prototype with
JavaScript frameworks and animations that do not serve the reader.
The Atlas's house style is plain HTML and minimal CSS, consistent with
the existing track pages. A team should be spending its last week on
content and on reader testing, not on build configuration.

---

## How the three tasks compound

The arc is best read in reverse. To produce a working evidential
journey (Task 3) the team needs three things behind it: a question
worth journey-designing for (Task 1), a chosen shape and a defeater
catalogue (Task 2), and the integrative skill of moving from spec to
prototype (Task 3 itself). Each task supplies what the next requires.

A team that does Task 1 honestly and Task 2 specifically arrives at
Task 3 with the inputs in hand: a question with an articulated
adequacy condition, a chosen shape with a paragraph-long sketch, and
at least one strong defeater. The prototype is the form the spec takes
when it is forced to commit to where the reader's eye falls. A team
that does Task 1 superficially or Task 2 generically will reach Task 3
and discover that they are designing without inputs — they will be
designing the journey *and* the spec at the same time, and the result
will be a wandering page sequence that does not surface its defeaters.

The grading is structured to reward the compounding rather than the
isolated tasks. A team that produces a flawless Task 3 prototype on
the back of an under-specified Task 1 corpus has not understood the
exercise; the rubric exists to make that visible.

---

## What I want from you before building the t4_*.html pages

Three reactions before I bake this into student-facing pages.

**(a) The arc.** Does the three-task progression (build → fit →
prototype) match how you want the term to unfold? Three weeks is tight.
If you would rather have students spend more time on Task 1 (because
the question corpus is the most fundamental artefact and benefits from
more time) or more time on Task 3 (because prototyping is where
integrative learning happens), I'll re-balance.

**(b) The scaffolds.** I have written some scaffolds as full prompts
(1.2, 1.5, 3.3), some as templates (1.4, 2.4), some as procedural
specs (2.1, 2.2, 2.3). Where did the level of detail feel right? Where
should I write actual prompts that I have left as specs, or vice versa?

**(c) The rubrics.** The grading dimensions are operational. The point
weights are first drafts. If the field-map shape ends up being the
primary teaching tool of the term, the rubric should reflect that. If
you want to weight the Chinn-Brewer rebuttal panel even more heavily —
on the grounds that rebuttal economy is the central design principle
— I'll adjust.

Once you've reacted on these three I'll build the t4_*.html pages
straight from this design document.
