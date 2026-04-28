# Usability Critique — Track 4 Pages (COGS 160 SP)

**Date**: 2026-04-27
**Critic**: K-ATLAS Usability Critic Agent
**Framework**: 35-dimension framework (Nielsen H1–H10, Shneiderman R1–R8, Visualization V1–V17)
**Audience under evaluation**: upper-division UCSD Cognitive Science undergraduates, working as student authors of evidential journeys
**Scope**: 8 pages — 5 track scaffold pages (`t4_intro`, `t4_task1`, `t4_task2`, `t4_task3`, `t4_submissions`) and 3 worked-exemplar pages in `track4/` (`answer_shape_catalogue`, `chinn_brewer_response_widget`, `journey_q29_art_affect_confound`)

Severity legend: **BLOCKER** (page cannot be used as intended) · **SHOULD-FIX** (real friction; degrades the pedagogy) · **MINOR** (notable but workable) · **NIT** (cosmetic).

---

## 0. Cross-cutting finding (applies to every page)

The five scaffold pages and the three worked-exemplar pages are visually two different sites. The scaffold pages use Arial sans-serif, navy `top-nav`, breadcrumb, side-nav twisties, and the cream/teal/amber palette of `_track_pages_shared.css`. The three worked exemplars in `track4/` use a self-contained inline `<style>` block with Iowan Old Style/Palatino serif and a brown/cream "paper" palette — no top nav, no breadcrumb, no side nav, no site footer. A student who clicks the "answer-shape catalogue" link from `t4_intro` is dropped into what looks like a different application entirely and has no way back except the browser back button.

- **H4 / R1 — Consistency and standards**: **SHOULD-FIX** on every exemplar page. Same task class (read course material), entirely different chrome.
- **H3 / R6 — User control / reversal**: **SHOULD-FIX**. The exemplar pages give the reader no return path to the parent task page; the only crumbs (in `journey_q29`) point to `../ka_home.html` and a sibling exemplar, not back to `t4_task3.html`.
- **R8 / H6 — Reduce memory load / recognition over recall**: **SHOULD-FIX**. Side-nav (twisties) is absent on exemplar pages; the reader has to remember the structure of Track 4 to navigate.

A single fix — wrapping each exemplar page in the same scaffold (top-nav, breadcrumb, optional side-nav, site-footer) and converting the inline `<style>` to consume `_track_pages_shared.css` plus a small page-local stylesheet — would clear three to four heuristic violations across all three exemplar pages at once.

---

## 1. `t4_intro.html` — Track 4 Overview

**Role / task**: undergraduate enrolled in COGS 160 SP, orienting to the three-task arc of Track 4 and the carried researcher exemplar.

**Strengths.** Clean scaffold; breadcrumb correct; hero uses the standard `hero-track` kicker; sectioning is well chunked; all five canonical answer shapes are introduced before they are referenced; the worked-exemplar pointer is explicit.

**Findings.**

- **H2 (real-world match) — MINOR.** The first paragraph deploys six heavy academic terms before the second paragraph: "evidential journey", "warranted", "qualified", "rebuttal-aware", "Toulmin sense", "defeasible". For an undergraduate landing here cold, "Toulmin" needs at least a parenthetical gloss before §"The methodological backbone" twelve scrolls later. *Fix*: add a one-sentence parenthetical on first use ("the Toulmin model — data, warrant, claim, rebuttal — is introduced in §Methodological backbone below").
- **H6 (recognition over recall) — MINOR.** The page references files that do not exist as HTML (`track4/track4_operational_brief.md`, `track4/researcher_fitting_catalog.md`, `track4/question_corpus_researcher_v1.md`, `track4/track4_task_design.md`, `ka_track4_persona_panel.html`). The student has to remember that Markdown links will render as raw text on GitHub, not in-browser. *Fix*: add a small note next to the first `.md` link ("opens as Markdown source on GitHub") OR render these as `.html` companions.
- **H10 (help & documentation) — MINOR.** "Five-axis question taxonomy" is named without a one-line gloss; the bullet list of axes appears one section down. *Fix*: add a tiny inline list `(cognitive purpose · answer shape · evidential demand · persona fit · theoretical commitment)` on first mention.
- **H8 (minimalist design) — MINOR.** §"What this track is and is not", §"Personas", §"The carried exemplar", §"Methodological backbone", §"Five canonical answer shapes" — five back-to-back prose sections of 120–200 words each before any visual landmark or scannable list. The reader hits a wall of paragraphs. *Fix*: convert §"Three tasks, in brief" to a 3-card grid (already used elsewhere in the site), add a tiny inline icon or kicker for each section, or pull the side-nav into view earlier.
- **R3 (informative feedback) — N/A** (no interaction).
- **R4 (closure) — MINOR.** "Where to start" is the closing section but does not lead the reader cleanly to a `next →` button to Task 1. The footer has the link, but a reader at the bottom of the main content does not get a CTA. *Fix*: add a `next-step` callout at the end pointing to `t4_task1.html`.

**Verdict**: 2 cross-cutting + 4 page-local issues, mostly MINOR, no BLOCKERs. The page's prose is excellent; the friction is in scannability and cross-links.

---

## 2. `t4_task1.html` — Build a Persona Question Corpus

**Role / task**: student starting work on the question-corpus deliverable for week 5.

**Findings.**

- **H1 (visibility of system status) — MINOR.** The hero says "Due end of week 5" but the page does not say *what calendar date that is*. A student in week 4 cannot tell if they have one week or three. *Fix*: replace "end of week 5" with the absolute date in parentheses on first mention; pull from the syllabus.
- **H2 — MINOR.** "Adequacy condition", "PNU template library", "five-axis tags", "cross-product corners", "sub-flavours", "winnowing protocol", "panel architect", "mining lead", "cross-product lead", "codebook custodian" — ten domain-specific terms, none with a glossary affordance. The role names (Panel Architect, Mining Lead, etc.) are referenced as if the student knows them, but they are introduced nowhere on this page. *Fix*: add a one-sentence gloss for each role on first use, or link to a Track 4 roles page.
- **H4 (consistency) — SHOULD-FIX.** The grading rubric table sums to **75 points** (20+20+15+10+10), but the section title says "75 points". 20+20+15+10+10 = 75. Correct, but the table has *only five rows*; a student would not be able to tell which row was inadvertently omitted if there were a sixth dimension. The hero says "75 points" — fine — but the rubric line items leave 0 free points and so any future addition silently breaks the total. *Fix*: add a `Total / 75` row, as `t4_task3` does implicitly. (Promoted to SHOULD-FIX because it affects student point-tracking.)
- **H6 — MINOR.** The corpus row schema (id, question, adequacy_condition, …) is a table, but the JSON/spreadsheet template is not provided. The student must recreate the schema from the table. *Fix*: link a starter `.csv` or `.json` template at the top of "What you produce".
- **H8 — MINOR.** §"How to generate questions" runs to 380+ words across three subsections, each citing a prerequisite agent role and an external `.md` file. Density is appropriate for the audience but the subsections look identical visually; no kicker, no icon, no number. *Fix*: number the three sources (Source 1 / 2 / 3 already in the H3s, but the H3 styling appears to be small caps — fine — they are just visually weak compared to the section's H2). Promote them to a 3-card grid.
- **H10 (help) — MINOR.** Pitfalls section is good. But there is no link to a worked example of an *acceptable* row vs. an *unacceptable* row; the student has to infer the difference from the verbal description. *Fix*: include 2 example rows (one passing the Codebook Custodian's adequacy gate, one failing) in the page itself.
- **R4 (closure) — MINOR.** Same as `t4_intro`: the page ends in a callout-amber that says "What you submit" but no inline `next: Task 2 →` link. The footer has it. *Fix*: add a `next-step` band.

---

## 3. `t4_task2.html` — Winnow & Fit Answer Shapes

**Findings.**

- **H1 — MINOR.** Same date-absent issue as Task 1.
- **H2 — MINOR.** "Defeater laundering" is excellent vocabulary but appears italicised inline as if it were a known term; needs a one-sentence definition on first use, not only in context. *Fix*: bold-define it on first mention ("**defeater laundering** — inventing a defeater rather than finding it in the literature").
- **H4 (consistency) — MINOR.** The rubric table sums to **75 points** in the page header, but the rows total 15+25+25+10 = **75**. ✓. However, Task 1's rubric has 5 rows summing to 75, and Task 2's has 4 rows summing to 75 — students comparing the two pages cannot infer a consistent rubric structure across tasks. *Fix*: align the rubric architecture across the three tasks (same dimension labels where possible), or add a one-line note explaining why dimensions differ per task.
- **H5 (error prevention) — SHOULD-FIX.** The "schema-fitting decision tree" inside the amber callout uses *six conditional clauses with `If…then…`* in plain prose. A student reading quickly will miss that the rules can fire in combination (cognitive purpose = inquiry AND evidential demand = causal-with-mechanism → Toulmin). *Fix*: render as a small flowchart (SVG, two-level branch) or as a 6-row decision table with columns `If cognitive purpose | And evidential demand | Then shape`.
- **H6 — MINOR.** Same pattern as Task 1: "Codebook Custodian", "fitting consistency", references to §1, §3 of the researcher fitting catalog with no in-page jump targets. *Fix*: link directly to anchors.
- **H8 — MINOR.** §"Stage C — Name the defeaters" italicises an entire sentence about defeater laundering; in body prose this reads as a side-comment rather than the moral of the section. *Fix*: pull the laundering warning into a small `callout-warn` block.
- **R3 / R4 — MINOR.** As Task 1: no inline `next →` link.

---

## 4. `t4_task3.html` — Prototype an Evidential Journey

**Findings.**

- **H1 — MINOR.** Same calendar-date issue.
- **H2 — MINOR.** "Reader-response stage", "disclosure region", "skeleton kit", "rebuttal economy" — all undefined on first use. The student is asked to "include a Chinn-Brewer rebuttal panel exposed by default" before they have necessarily read the widget page. *Fix*: link "Chinn-Brewer rebuttal panel" inline to the widget page on first mention.
- **H5 — SHOULD-FIX.** "(a) One working journey prototype" lists four required pieces (landing page, populated answer shape, Chinn-Brewer panel, closing reader-response page) in dense prose. The Pitfalls section says "A journey without an exposed Chinn-Brewer panel is not yet an evidential journey" — i.e. this is the most common failure mode. The required-pieces list should therefore be a checklist, not a paragraph. *Fix*: render (a) as a 4-item checklist with each checkbox tied to a rubric line.
- **H6 — MINOR.** Rubric mentions "Site integration: 5 — Top nav, breadcrumb, side-nav, footer; consistent with the rest of the Atlas." But the worked example provided (`journey_q29_art_affect_confound.html`) does *not* use top nav, breadcrumb, side-nav, or the site footer. The exemplar contradicts the rubric. *Fix*: either rewrite the exemplar to use the scaffold (preferred) or amend the rubric to say "the Q-29 exemplar is intentionally self-contained for hand-off as an iframe; your prototype, since it lives in the course site, should follow the scaffold". Currently this is a **silent contradiction** and will confuse every student who looks at both pages. (Promoted to **SHOULD-FIX**.)
- **H8 — MINOR.** Three artefacts in three back-to-back paragraphs (a, b, c), each starting with bold. Visually identical; not scannable. *Fix*: 3-card layout.
- **R4 (closure) — MINOR.** Same `next →` issue.

---

## 5. `t4_submissions.html` — Submissions

**Role**: student checking grading status; instructor verifying grade entry.

**Findings.**

- **H1 (visibility) — SHOULD-FIX.** The submission table contains four rows of `—` placeholders with no indication of whether (a) the grading backend is connected, (b) the student has not yet submitted, or (c) the page is a static mockup. The body says "auto-populates from the grading backend the moment a Pull Request is merged or graded" — but no live status indicator confirms the backend is reachable. A student looking at this page on Sunday week 5 will not know if `—` means "not submitted yet" or "submission failed to register". *Fix*: add a small status chip near the table title — "Status: not yet submitted" / "Status: submitted, awaiting grading" / "Status: grading backend offline" — that updates from a real (or stubbed) endpoint. At minimum, add explanatory text inside the empty cells: "(no submission recorded)" instead of `—`.
- **H6 — MINOR.** The branch-naming convention `track4/<your-name>` appears twice but the student must recall their actual git username. *Fix*: prefill or template-replace `<your-name>` with the logged-in user where possible.
- **H9 (error recovery) — SHOULD-FIX.** No information about what to do if a PR fails to register. The "How submissions are recorded" section says "the PR creation timestamp becomes the 'Submitted at' entry" but does not say what to do if 24h pass and the entry remains `—`. *Fix*: add a "If your submission does not appear within 24h…" mini-section with a contact link.
- **H10 — MINOR.** The "team-grade component" callout is a useful pointer but does not link to anywhere that explains how the team grade is computed. *Fix*: link to the relevant rubric section on the task pages.
- **R3 (feedback) — SHOULD-FIX.** Same point as H1: no live feedback that the page is connected to anything. The `data-submission-table="track4"` attribute hints at a live binding, but no script is referenced.

**Verdict**: this page is the lowest-risk of the five but has the most user-visible state-tracking gap. The placeholder-only state needs interpretive text.

---

## 6. `track4/answer_shape_catalogue.html` — Five Answer Shapes

This page contains five visualizations and is therefore the page most subject to V1–V17 evaluation.

**Strengths.** Each shape has: a description, a "use when", a worked example question, an assertion-style figure title (V15 ✓), the diagram, a long substantive caption, and a "how a journey fills it in" closer. This is exactly the assertion-evidence structure the science-comm skill calls for. The Toulmin SVG geometry is correct. The colour scheme is restrained and earns its place.

**Findings.**

- **H4 / R1 — SHOULD-FIX (cross-cutting).** No top-nav, no breadcrumb, no side-nav, no site-footer. See §0.
- **H3 / R6 — SHOULD-FIX.** No way back to `t4_intro.html` or `t4_task2.html`. The only navigation is the in-page TOC (which is good but local).
- **H8 — MINOR.** The page is a single 893-line scroll with no sticky TOC. Once a reader is at Shape 4 they have to scroll all the way back to the top to jump to Shape 5. *Fix*: make the TOC sticky on the right or top.
- **V1 (data-ink) — PASS.** Diagrams are clean; no chartjunk.
- **V3 (chartjunk) — PASS.** No 3-D, no gratuitous decoration.
- **V5 (perceptual encoding) — PASS for Toulmin/field-map (position is the carrier); PASS for contrast pair (position + colour-coded verdict words). The contrast-pair "verdict-good / verdict-mid / verdict-bad" colours (green / amber / red) appear without a key on the page; reader infers from context.
- **V6 (pattern discrimination, grayscale-survivable) — SHOULD-FIX.** The contrast pair table relies on three colours (green/amber/red text) to encode quality. Printed in greyscale or read by a colour-blind student, "High — wrist or body" and "Low — tethered" become indistinguishable. The verdict words ("High", "Medium", "Low", "Yes", "Possible", "No") do carry the meaning textually, which mitigates this — but the visual signal is colour-only. *Fix*: add a small icon (✓ / ◐ / ✗) before each verdict to provide a redundant non-colour channel. Same applies to the ranked-brief evidence column ("Strong / Moderate / Weak").
- **V8 (uncertainty) — MAJOR FAIL.** The Toulmin worked example states "≈ 40–60% attenuation" but this is presented as a *point estimate range with no confidence interval, no N, and no source-study count*. The same number reappears as a `stat-figure` chip on the journey page. For a page teaching Toulmin reasoning, the data step that omits its own uncertainty is a teaching failure. *Fix*: add `(pooled across N=k studies; CI not reported in source)` next to the number, OR mark the figure caption with the explicit acknowledgement that this is a meta-analytic range without a published CI.
- **V12 (one focal signal) — MINOR.** On the field map, the *Critique* node, the *operationalises* edges, and the *motivates* edges all compete visually. The reader's eye does not know whether the focal point is the foundation node (Kaplan & Kaplan), the critique node (Joye & van den Berg), or the descendant nodes. *Fix*: dim the non-focal nodes to a lighter shade and let the critique node carry the accent. The shape title says "a foundation, two operationalisations, a critique that ties them together" — the diagram should make the critique visually central.
- **V13 (declutter) — MINOR.** The contrast table has a heavy border on every cell. The ranked-brief table is similar. Tufte's declutter principle suggests light grey rules between rows and no vertical rules. *Fix*: drop vertical rules; lighten horizontal rules to `var(--rule)` at lower opacity.
- **V14 (direct labelling) — PASS.** All series and nodes are labelled directly.
- **V15 (assertion title) — PASS.** Every figure has an assertion-style title ("Attention Restoration Theory partly survives…", "The attention-restoration literature, 1989–2025: a foundation, two operationalisations…").
- **V17 (persistent context) — N/A** (no exploration interactivity).
- **R8 (memory load) — MINOR.** "Use when" descriptors reference cognitive purpose × evidential demand combinations the student must recall from `t4_task2.html`. *Fix*: link "cognitive purpose" inline to the taxonomy.

---

## 7. `track4/chinn_brewer_response_widget.html` — Seven-Response Widget

**Role / task**: drop-in component the student can iframe into a journey prototype; also functions as a teaching reference.

**Strengths.** Self-contained, no dependencies. The dispositional colour code (protective/flexible/revising) is principled. Open-all/close-all controls are present. Scenario switcher updates anomaly text and per-response example correctly.

**Findings.**

- **H4 / R1 — SHOULD-FIX (cross-cutting).** Same scaffolding-mismatch issue as the catalogue.
- **H1 (status) — MINOR.** When the scenario dropdown changes, the anomaly card and per-response "In this case" text update silently. There is no transient visual cue that something happened. *Fix*: add a brief 200ms highlight pulse on the anomaly card on scenario change.
- **H2 — MINOR.** "theory-protective / theory-flexible / theory-revising" labels in the legend are good vocabulary but appear without one-sentence definition. The student infers from context. *Fix*: hover-tooltip on each legend dot.
- **H4 (consistency) — SHOULD-FIX.** The standalone widget renders the disposition pill in three colour codes (red / amber / green). The journey page (`journey_q29`) renders the same disposition with: `protective` red, `flexible` brown (`var(--emphasis)`), `revising` green. The two pages assign **different colours to "flexible"**. A student moving between the standalone widget and the journey will see two visual systems that disagree on how to colour the middle category. *Fix*: align the journey page's `--warn` (or whichever variable maps to flexible) to match the widget's amber, or vice-versa. (Promoted to SHOULD-FIX because it's a teaching artefact about the same construct.)
- **H7 (efficiency) — MINOR.** No keyboard shortcut to step through the seven responses; an expert reader has to mouse-click each one. *Fix*: add j/k arrow-key navigation.
- **H10 — MINOR.** The widget assumes the reader knows what "anomalous data" means in Chinn & Brewer's sense. The lede is good but says only "evidence that conflicts with a theory they hold". For a sceptical undergraduate, one sentence on *why anomalies are pedagogically interesting* would help. *Fix*: add a sentence to the lede.
- **R3 (feedback) — PASS.** Disclosure is clearly fed back.
- **R6 (reversal) — PASS** (any opened response can be re-closed).
- **R8 (memory) — MINOR.** Once a response is opened, the previous one stays open — fine — but if the reader opens all seven, the page is very long and the disposition legend at the bottom is no longer in view. *Fix*: pin the legend to the bottom of the viewport.
- **V8 (uncertainty) — N/A** (this is a categorical taxonomy, not a quantitative display; no numeric estimate is shown).
- **V12 (focal signal) — PASS.** The currently-selected scenario's anomaly card carries the only orange-bar accent.

---

## 8. `track4/journey_q29_art_affect_confound.html` — Worked Journey

**Role / task**: the carried Task 3 exemplar — the student studies it before building their own journey.

**Strengths.** Six-step structure (Data, Warrant+Backing, Claim, Rebuttal, Chinn-Brewer panel, Reader response) maps cleanly onto Toulmin. The rebuttal panel uses a distinct background colour. The reader-response stage is functional. Citations are present.

**Findings.**

- **H4 / R1 — SHOULD-FIX (cross-cutting).** As §0. Compounded by the rubric on `t4_task3` saying "Site integration: 5 — Top nav, breadcrumb, side-nav, footer" — this exemplar should *be* the model.
- **H1 (visibility) — MINOR.** The "search box" at the top is a single text input with the question pre-filled and no submit button. A reader does not know whether the box is interactive (typing a different question would do nothing) or decorative. *Fix*: add `readonly` attribute and visually de-emphasise as a "frozen example", OR make it functional and route to a no-op page.
- **H1 — MINOR.** No visible step indicator showing "Step 4 of 6"; the student has to count. *Fix*: a small "Step N of 6" pill in each step header.
- **H2 — PASS.** Vocabulary is calibrated.
- **H3 (user control) — MINOR.** The reader-response form's `<button>Save my response</button>` writes to in-memory `SAVED` only — no localStorage, no server. A page refresh discards the response with no warning. The footer and the comment in the JS say this is intentional ("no localStorage per Atlas convention"), but the user is not told. *Fix*: change the "Save" button to "Record (this session only)" and put one line under it: "Refreshing the page clears your response."
- **H5 (error prevention) — MINOR.** The form `alert()`s if the dropdown is unselected but allows blank `cb-why` text. For an academic exercise asking "why this response", a minimum-length validator would prevent perfunctory submissions. *Fix*: warn (don't block) if the textarea is under 30 characters.
- **H8 — MINOR.** The `toulmin-mini` inline diagram inside Step 3 reproduces information already given in Step 1 and Step 3's prose. It is a useful summary, but visually it is the same accent-soft beige as the `stat-figure` and `ascii-fig` chips, which makes Step 3 feel busy. *Fix*: swap the mini-diagram's background to white with a thin border to differentiate it from the other accent chips.
- **H10 — MINOR.** "Toulmin shape" appears in the meta line but is not linked to the catalogue page. A student who has not read the catalogue first does not know what the six-step structure is implementing. *Fix*: link "Toulmin shape" to `answer_shape_catalogue.html#toulmin`.
- **R3 (feedback) — PASS for the save action; the `stored` div is shown.
- **R4 (closure) — MINOR.** After saving the response, no "next" affordance. The journey ends. *Fix*: a small closing message ("You have completed this journey. Return to the Q-29 corpus entry, or compare with another worked journey.") with one or two links.
- **R6 (reversal) — MINOR.** Once saved, the response cannot be edited and re-saved without re-typing. *Fix*: leave the form values in place and allow re-save (the current code does this, but the "Saved" block stays from the previous save and is not visually updated to "Updated").
- **V2 (lie factor) — PASS.** No graphical magnitudes used.
- **V8 (uncertainty) — MAJOR FAIL.** The same 40–60% number from the catalogue is repeated here in a `stat-figure` chip — large bold tabular-numeric — without a CI, an N, a study count, or a source-quality marker. The text below acknowledges interpretive ambiguity (confounder vs mediator) but the **numeric chip itself communicates point-estimate certainty**. For a journey whose pedagogical purpose is to teach honest defeater handling, the numeric display undermines the lesson. *Fix*: add `(meta-analytic range across re-analysed studies; individual study CIs not pooled)` directly under the number, in `.lbl` style.
- **V12 (focal signal) — MINOR.** The rebuttal step's red border is a strong focal cue (good); but the Chinn-Brewer panel below it has the same `accent-soft` beige as the data and warrant steps, which makes the rebuttal-then-Chinn-Brewer flow visually equal-weight. The page's argument is that the rebuttal is the *most important* step — that should be the visual climax. *Fix*: nothing to change in the rebuttal; consider giving the Chinn-Brewer panel a slightly recessed appearance so the rebuttal remains the peak.
- **V15 (assertion title) — PASS.** Every step's `h3` is an assertion, not a topic.
- **R8 — MINOR.** The reader is asked to choose a Chinn-Brewer response in Step 6, but the step-5 panel collapses by default — the reader has to remember the seven options (or scroll up and re-open them). *Fix*: when the reader reaches Step 6, auto-expand all seven items in the Step-5 panel, or render the seven options inline next to the dropdown as a quick-reference legend.

---

## Verdict summary table (per page)

| Page | BLOCKER | SHOULD-FIX | MINOR | NIT |
|------|---------|------------|-------|-----|
| `t4_intro` | 0 | 0 | 5 | 0 |
| `t4_task1` | 0 | 1 | 6 | 0 |
| `t4_task2` | 0 | 1 | 5 | 0 |
| `t4_task3` | 0 | 2 | 5 | 0 |
| `t4_submissions` | 0 | 2 | 3 | 0 |
| `answer_shape_catalogue` | 0 | 4 (incl. cross-cut) | 5 | 0 |
| `chinn_brewer_response_widget` | 0 | 3 (incl. cross-cut) | 4 | 0 |
| `journey_q29_art_affect_confound` | 0 | 3 (incl. cross-cut) | 8 | 0 |

(Cross-cutting H4/R1/H3 issues counted once per exemplar page.)

---

## Top-10 triaged punch list (all SHOULD-FIX or above, ordered by impact)

1. **Wrap the three `track4/` exemplar pages in the standard scaffold** (top-nav, breadcrumb, side-nav, site-footer) and migrate their inline styles to consume `_track_pages_shared.css` plus a small page-local stylesheet. *Why*: clears H4, R1, H3, R6, R8 violations across all three pages simultaneously. The contradiction with `t4_task3`'s "Site integration: 5 points" rubric goes away. **Effort: Medium.**

2. **Add CI / N / source-study count to the "≈ 40–60%" attenuation figure** on both the answer-shape catalogue (Toulmin example) and the Q-29 journey's `stat-figure` chip. *Why*: V8 MAJOR FAIL — a journey teaching defeater honesty cannot itself display a confidence-free point-estimate chip. **Effort: Low.**

3. **Reconcile the disposition colour scheme** between `chinn_brewer_response_widget.html` (amber for "flexible") and `journey_q29` (`var(--emphasis)` brown for "flexible"). Pick one, apply to both. *Why*: same construct, two visual codes, on adjacent pages — H4 / R1 violation that reads as a teaching error. **Effort: Low.**

4. **Replace `t4_task3`'s "(a) Working prototype" prose with a 4-item checklist** (landing page · populated answer shape · Chinn-Brewer panel exposed by default · reader-response stage), each tied to its rubric line. *Why*: this is the most-violated requirement per the page's own Pitfalls section; H5 / H8 fix that lifts the most-graded deliverable into clear view. **Effort: Low.**

5. **Either rewrite `journey_q29` to use the scaffold OR add a paragraph to `t4_task3`'s rubric** explaining why the exemplar intentionally does not. The current silent contradiction trains every student to ignore the rubric's "Site integration" line. *Why*: H4 + H6. (Folds into item 1 if you take the rewrite path.) **Effort: Low (rubric note) or Medium (rewrite).**

6. **Replace `t4_task2`'s six-conditional schema-fitting decision tree** with a 6-row decision table or a small SVG flowchart. *Why*: H5 — the single most cognitively demanding move in Track 4 is "fit a question to a shape", and the current prose tree obscures the rule structure. **Effort: Low.**

7. **Add status text inside the `t4_submissions` empty cells** ("(no submission recorded)") and a backend-status chip near the table title. *Why*: H1 + H9 + R3 — a student looking at four `—`s on a Sunday cannot tell whether the system is broken or they have not yet submitted. **Effort: Low.**

8. **Add icon redundancy to the contrast-pair and ranked-brief colour codes** on the catalogue (✓ / ◐ / ✗ before "High/Medium/Low" verdicts; before Strong/Moderate/Weak). *Why*: V6 — colour-only encoding fails grayscale and 8% of male readers. **Effort: Low.**

9. **Add absolute calendar dates** ("Due Friday 8 May 2026" rather than "Due end of week 5") on `t4_task1`, `t4_task2`, `t4_task3`. *Why*: H1 — a student in week 4 should not have to consult the syllabus to know the deadline. **Effort: Low.**

10. **Add a `next →` band** to the bottom of `t4_intro`, `t4_task1`, `t4_task2`, `t4_task3` linking to the next step in the sequence. *Why*: R4 — task pages currently end on a callout-amber box and offer no closure affordance toward the next deliverable; the footer is below the fold for a long page. **Effort: Low.**

---

## Recommended GUI Agent v3 brief

The Track 4 set is internally bifurcated: five scaffold pages that follow the canonical track conventions (Arial / navy / cream / amber callouts) and three worked-exemplar pages that follow a self-contained "paper" theme (serif / brown / beige). The bifurcation is the dominant usability problem and the source of a chain of secondary violations: missing top-nav, missing breadcrumb, missing side-nav, no return path, the disposition-colour clash for the Chinn-Brewer pill, and the silent contradiction with the Task 3 "site integration" rubric line. The first design pass should unify these by wrapping the three `track4/` exemplar pages in the same scaffold the five course pages use (preserving the inline visual style of each diagram block) and migrating their colour variables into named tokens in the shared stylesheet so that the Chinn-Brewer dispositional colours are defined once. The second pass should address the V8 uncertainty failure on the Toulmin worked example by adding a CI/N/source-quality marker beside the 40–60% attenuation figure on both the catalogue and the journey, and the V6 colour-only encoding by adding redundant icon glyphs to the contrast-pair and ranked-brief tables. The third pass should address pedagogical scannability: replace `t4_task3`'s prose deliverable list with a checklist, replace `t4_task2`'s schema-fitting prose tree with a decision table or SVG flowchart, add absolute dates to all task hero blocks, and add a `next →` closure band to each task page. The Q-29 journey is the most-cited exemplar in the track and bears the greatest rewrite weight; preserve every word of its existing copy and SVG geometry while replacing the page chrome.

---

*End of critique. Word count ≈ 2,950.*
