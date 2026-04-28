# Track 4 — Operational Brief

*Companion to `question_corpus_researcher_v1.md`. CW, 2026-04-27.*

The corpus document is long because it has to justify its choices. The brief
below is what a Track 4 student needs in order to act. It does three things:
extracts the directives that are buried in the corpus prose, assigns concrete
roles to a four-student team, and lays out a winnowing protocol that turns a
large pile of raw questions into a working corpus that journey designs can be
built against. The five answer-shape schemata that the brief refers to are
visualised in the companion page `answer_shape_catalogue.html`.

---

## A. Directives extracted from the corpus

These are the operational claims that survive when the prose is pared back.

**A1. The corpus precedes the journey.** A journey is a sequence of pages
designed to satisfy a question. One cannot design that sequence without first
knowing the question's *shape* and *adequacy condition*. Build the corpus
first, the journey second.

**A2. Tag every question on five axes.** Cognitive purpose, answer shape,
evidential demand, persona fit, theoretical commitment. Every question in the
corpus carries all five tags before it counts as classified.

**A3. The corpus is per-persona.** A researcher's corpus is not a student's,
not a contributor's, not a practitioner's. The Track 4 round produces *one*
persona's corpus; the other personas are listed in §7 of the corpus document
as next-passes and must each receive their own.

**A4. LLM panels are the user model, the corpus is ground truth.** Use panels
to *widen* the corpus, not to *generate* it from scratch. An item produced by
a panel earns its place in the corpus only after it survives a sanity, novelty,
and intra-panel-coherence check (Section 3.1 of the corpus).

**A5. Mine the templates and gold extractions.** Each PNU template
(`Article_Eater_PostQuinean_v1_recovery/data/templates/`) encodes a
question the field already thought worth asking. Reading one template
yields three to five candidate questions.

**A6. Walk the IV × DV product systematically.** The Tagging_Contractor's
roughly 440 active tags and the Outcome_Contractor's seven domains plus
eighty level-2 outcomes form a constitutive hierarchy on each side. Walking
both hierarchies up and down generates cross-product questions at four
informative corners (low/low, low/high, high/low, high/high).

**A7. Each question must come with its adequacy condition.** A question that
does not come with "what would make the answer feel insufficient" is a
question whose journey cannot be designed.

**A8. Make rebuttal economy a default of the journey, not an option.** For
roughly a quarter of researcher questions the journey will succeed or fail on
whether it surfaces the right defeaters. Every prototype journey should
expose a rebuttal panel — most simply, an instance of the Chinn-Brewer
seven-response widget — by default.

**A9. Resolve generic questions into specific ones.** A reader types
"how does spatial environment affect cognition" but the warranted answers
live at the lower cells of the cross-product. The journey must be designed
to walk a reader from the typed-in generic question to a sub-question they
can actually progress on.

**A10. Be honest about LLM-panel limits.** Document the panel
configurations, the prompts, and the failure modes. Treat the panel
output as a noisy signal that widens coverage, not as a substitute for
empirical user research.

---

## B. Student roles for a four-person team

Track 4 teams will typically be four students. The role structure below
front-loads creative work and then specialises. Each role has a deliverable
and a midpoint review.

| Role | Phase 1 (Weeks 1–2) | Phase 2 (Weeks 3–4) | Deliverable |
|------|---------------------|---------------------|-------------|
| **Panelist** | Configure and run three LLM panels of 8–12 agents each, varying career stage, discipline, and theoretical commitment. Pool raw questions. | Cross-examine candidate questions with adversarial agents (intra-panel coherence check). | Panel transcripts + raw question list (target ≥120 items per panel). |
| **Miner** | Sample 30–40 PNU templates and 10 gold-standard extractions. Extract questions the templates *answer* and the questions a researcher who arrived at those answers would *next* ask. | Document the mining provenance — every mined question carries its template ID. | Provenance-tagged mined-question list (target ≥100 items). |
| **Synthesist** | Walk Tagging × Outcome hierarchies. Generate cross-product questions at four corners (low/low, low/high, high/low, high/high). | Apply the constitutive-bridge inference rules from `constitutive_bridges.json` to identify which cross-products the existing literature can already address vs. which are open. | Cross-product question list with hierarchy coordinates (target ≥60 items, ≥15 per corner). |
| **Curator** | Build the master taxonomy spreadsheet; receive items from Panelist, Miner, Synthesist; tag every item on the five axes. Track duplicates. | Run the winnowing protocol (Section C below) and produce the working corpus. | Tagged master corpus + winnowed working corpus (target 40–60 items in the working corpus). |

The team rotates a midpoint review at the end of week two, where each role
shows its raw output and the team agrees on five to ten *exemplar*
questions that will go through the full schema-fitting pipeline as worked
examples. The four roles are not silos: every student should read every
other role's output, and the Curator's tagging is treated as draft until
the team has reviewed it together.

A two-person team collapses Panelist + Miner into one role and Synthesist +
Curator into the other. A three-person team makes the Curator a separate
role and shares Panelist–Miner–Synthesist between two students. The
Curator role should not be skipped at any team size: without a single
person responsible for the master corpus, the tags drift and duplicates
accumulate.

---

## C. Winnowing protocol

A pile of three to four hundred raw candidate questions has to become a
working corpus of forty to sixty. The protocol below is what the Curator
runs after the midpoint review. It is roughly equivalent to a four-stage
sieve.

**Stage 1 — Deduplicate.** Two questions are duplicates if they share the
same five-axis tags *and* would be answered by the same journey. Merge
duplicates and credit both sources. Expect this stage to cut roughly a
third.

**Stage 2 — Adequacy gate.** Drop any question whose adequacy condition
the team cannot articulate in one sentence. A question without an
adequacy condition cannot be journey-designed and must either be sharpened
or set aside. Expect this stage to cut another fifteen to twenty per cent.

**Stage 3 — Persona-fit gate.** Drop any question that does not plausibly
belong to the researcher persona — i.e., that the team would re-classify as
P1, P3, P4, P5, P7, or P8 if pressed. Move those items to the next-pass
backlog rather than discarding them. Expect this stage to cut ten per cent
and to populate the backlog usefully.

**Stage 4 — Coverage balance.** Inspect the surviving items against the
five axes and against the four cross-product corners. If any cell is
empty, surface the gap to the team and either commission a targeted
generation pass or accept the gap with a written note. Expect this stage
to *add* a small number of items rather than cut.

The working corpus is the output of Stage 4. It carries forward to the
schema-fitting pass.

A useful sanity check at the end of winnowing is the *journey-buildable*
criterion: pick three random items from the working corpus and ask the
team to sketch the answer-shape and at least one defeater for each, in
under five minutes per question. If the team cannot do this for a third of
the items, the winnowing is incomplete.

---

## D. Schema-fitting: from question to answer

After winnowing, every question in the working corpus is fitted to one of
five canonical answer shapes. The five shapes are listed below; the
companion page `answer_shape_catalogue.html` shows each shape as a
diagrammatic template with a worked example drawn from the corpus.

The five shapes are:

1. **Toulmin diagram.** Claim, data, warrant, backing, qualifier,
rebuttal. The default shape for theory-prober questions and for any
question whose adequacy condition is *causal-with-mechanism*. Worked
example: Q-29 (does Attention Restoration Theory survive the affective
confound).

2. **Field map.** A portrait of a literature with named camps, points of
agreement, and live disputes. The default shape for *discovery* questions
and for high/high cross-product questions. Worked example: Q-07 (an
honest summary of where attention-restoration theory stands in 2026).

3. **Procedure.** A step-by-step protocol with provenance for each step.
The default shape for sensors-seeker and tests-seeker questions whose
adequacy demand is *practical with regulatory or ethical gates*. Worked
example: Q-21 (instrumenting an apartment for indoor luminance, spectrum,
and occupancy).

4. **Contrast pair.** Two (or n) options laid out side-by-side with the
relevant differentia in rows. The default shape for measures-seeker and
sensors-seeker questions where the asker is choosing among instruments.
Worked example: Q-19 (Empatica EmbracePlus vs. BIOPAC dry-electrode vs.
research-grade cuff).

5. **Ranked brief.** A short list of options with criteria and evidence
quality, suitable for a busy practitioner or a senior PI. The default
shape for *deliberation* questions whose adequacy demand is *converging*
or *measurement-grade* with a brevity constraint. Worked example: Q-09
(best validated restorativeness instrument for repeated measures within a
workday).

The schemata are not exclusive. A field map may have a Toulmin nested
inside one of its branches; a contrast pair may dissolve into a ranked
brief once the differentia have been weighted. Students should learn to
*compose* shapes rather than treat them as a closed taxonomy. What they
should not do is let a question pass through schema-fitting without
*some* shape attached, because an unshaped question becomes an
unconstrained journey design and the journey's quality cannot be assessed.

The schema-fitting pass produces, for each question, three artefacts:
the chosen shape, a one-paragraph sketch of how the shape would be filled
in for *this* question, and at least one named defeater that the journey
must surface. Students can then choose a single question to take all the
way to a journey prototype in Track 4 Task 3.

---

## E. References to the long document

The corpus document remains the source of record. The brief above is
operational; the corpus document is justificatory. Students should read
the brief first and consult the corpus document when they need to know
*why* a directive is what it is. Section numbers cited above refer to
`question_corpus_researcher_v1.md`.
