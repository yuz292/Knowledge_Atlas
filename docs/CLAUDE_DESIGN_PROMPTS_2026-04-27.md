# Claude Design Prompts for Knowledge Atlas

*CW, 2026-04-27. Three prompts for DK to paste into claude.ai/design.
DK runs Claude Design in the browser; CW picks up the code-handoff
bundle each prompt produces and integrates it back into the Atlas.*

---

## Prompt 1 — Build the Knowledge Atlas Design System

**Use this first.** Claude Design's onboarding can ingest your
codebase to build a team design system; this prompt frames that
ingest so the resulting system matches what already exists rather
than fighting it.

> Build me a design system for the Knowledge Atlas project.
>
> **Codebase to ingest:** the `.css` files at
> `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/_track_pages_shared.css`
> (the canonical track-page stylesheet used across Tracks 1–3, now
> 4) and `/Users/davidusa/REPOS/Knowledge_Atlas/ka_styles.css` if
> present. Also ingest five representative pages so the system
> matches lived practice:
> `/Users/davidusa/REPOS/Knowledge_Atlas/ka_home.html`,
> `/Users/davidusa/REPOS/Knowledge_Atlas/ka_admin.html`,
> `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/t1_intro.html`,
> `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/t4_intro.html`,
> `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/track4/answer_shape_catalogue.html`.
>
> Extract: the colour palette (paper/ink/accent/muted/rule
> conventions); typography (the Iowan Old Style serif stack);
> spacing scale; the canonical track-page scaffold (top nav,
> breadcrumb, page-grid with side-nav, hero, content sections,
> site-footer); the hero patterns (`hero-track` micro-label,
> `hero-sub` lede); the callout patterns (`callout-amber`); the
> data-table patterns; the badge / pill conventions
> (`mode-pill`); the side-nav twistie patterns from
> `_track_side_nav.js`. Note that two voices co-exist in the
> ingested files: a "paper" voice (warm cream background, brown
> accents, serif body) used on Track 4 exemplar pages, and a
> "navy" voice used on the main Atlas pages. Keep both as named
> sub-themes inside one design system rather than collapsing
> them.
>
> Produce a design system page with: colour tokens, type tokens,
> spacing tokens, components (top nav, breadcrumb, hero,
> content section, callout, data table, side nav, footer),
> and example compositions. Export the design system as a code
> handoff bundle so I can pass it to my engineer for
> integration.

---

## Prompt 2 — Polish the Track 4 Student-Page Design

**Use after Prompt 1.** This prompt asks for a polished design
that CW will use to re-skin the five `t4_*.html` pages.

> Using the Knowledge Atlas design system you built (the "paper"
> sub-theme), redesign the five Track 4 student-facing pages:
>
> - `t4_intro.html` — the track overview (currently at
>   `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/t4_intro.html`)
> - `t4_task1.html` — Build a Persona Question Corpus
> - `t4_task2.html` — Winnow & Fit Answer Shapes
> - `t4_task3.html` — Prototype an Evidential Journey
> - `t4_submissions.html` — submissions tracker
>
> The pages currently use the canonical Track scaffold (which
> works) but have several known usability defects flagged in
> `/Users/davidusa/REPOS/Knowledge_Atlas/docs/USABILITY_CRITIQUE_TRACK4_2026-04-27.md`.
> Address at minimum the top-10 punch list from that critique:
> add absolute dates to the "end of week 5/6/7" labels; convert
> the t4_task2 schema-fitting decision tree from prose to a
> decision table or compact SVG flowchart; convert the t4_task3
> deliverables list from prose paragraphs to a 4-item checklist;
> add visible "next →" affordances at the end of each task page;
> add status indicators to the empty `—` cells on
> t4_submissions; reconcile the disposition-colour clash on the
> Chinn-Brewer panel; add a CI / N / source-study count next to
> the "≈ 40–60% attenuation" stat figure rather than presenting
> it as a single confident chip.
>
> Audience is upper-division Cognitive Science undergraduates at
> UCSD; tone should match the existing science-writer voice (no
> emojis, no marketing fluff, no patronising microcopy). The
> redesign should preserve the substantive content; this is a
> visual and interactional polish, not a rewrite.
>
> Export as a code-handoff bundle. The engineer (CW) will
> integrate.

---

## Prompt 3 — Polish the Q-29 Journey Prototype

**Use after Prompts 1 and 2.** Q-29 is the carried Task-3 worked
exemplar (Toulmin journey on ART vs the affective confound). It is
the artefact every student studies before building their own
prototype, so the design quality matters disproportionately.

> Using the Knowledge Atlas design system you built (the "paper"
> sub-theme), polish the Q-29 evidential journey prototype at
> `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/track4/journey_q29_art_affect_confound.html`.
>
> The journey takes a reader from a typed-in question
> ("Does Attention Restoration Theory survive the affective
> confound?") through a six-step Toulmin sequence: Data →
> Warrant + Backing → Qualified Claim → Rebuttal → Chinn-Brewer
> seven-response panel → Reader response. The current
> implementation is functional but has design defects flagged in
> `/Users/davidusa/REPOS/Knowledge_Atlas/docs/USABILITY_CRITIQUE_TRACK4_2026-04-27.md`
> §journey_q29.
>
> Specific design moves to consider, in priority order: (1) wrap
> the page in the canonical Track scaffold (top nav, breadcrumb
> "Home / 160 Student / Track 4 / Worked example: Q-29",
> side-nav, footer) — current page has none of these, which
> contradicts the t4_task3 rubric that requires site
> integration. (2) Make the rebuttal step (Step 4) visually
> equal to the data step (Step 1), not subordinate; the journey
> teaches that rebuttal economy is the central design
> commitment, and the visual hierarchy should reflect this. (3)
> Add inline source citations for the "≈ 40–60% attenuation"
> figure (study count, N, CI bounds) rather than presenting it
> as a confident chip — the journey is teaching defeater
> honesty and the figure should model it. (4) Reconcile the
> disposition colour palette on the Chinn-Brewer panel with
> the standalone widget at
> `chinn_brewer_response_widget.html` so the same construct
> uses the same colour everywhere. (5) Add a "Save and resume
> later" affordance for the reader-response stage so a reader
> who is interrupted does not lose their state.
>
> Audience and tone as in Prompt 2. Export as a code-handoff
> bundle for CW.

---

## Notes on the workflow

After each prompt's code-handoff bundle is produced:

1. DK exports the bundle from Claude Design.
2. DK either drops the bundle into `/Users/davidusa/REPOS/Knowledge_Atlas/incoming/`
   or pastes the file paths into a Cowork prompt for CW.
3. CW reads the bundle, integrates it into the relevant Atlas pages,
   commits locally, and asks Codex to push to GitHub for staging
   and production deployment.

Claude Design's design system (Prompt 1) should be re-ingested
whenever the Atlas's CSS conventions change, so the system stays
in sync with lived practice rather than drifting.
