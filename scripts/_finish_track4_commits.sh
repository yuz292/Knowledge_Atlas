#!/usr/bin/env bash
# Finish the Track 4 + AF spec + grader-integration commit sequence.
# Run from your terminal at /Users/davidusa/REPOS/Knowledge_Atlas/
# CW could not finish from the Cowork sandbox because a stale
# .git/index.lock file resists removal due to file-ownership in the
# mount. Run this once that lock is cleared.
#
# Author: CW (Cowork session) for Prof. David Kirsh, COGS 160 SP, 2026-04-27.
set -euo pipefail

cd "$(dirname "$0")/.."

# Prerequisite: clear any stale lock from the sandbox's interrupted commit.
if [ -f .git/index.lock ]; then
  echo "Clearing stale .git/index.lock …"
  rm -f .git/index.lock
fi

# Commit 1 of 4 already landed in the sandbox. Verify before continuing.
LATEST=$(git log -1 --pretty=format:'%s')
if [[ "$LATEST" != "Site infrastructure: canonical search, navbar grader pill, Track 4 wiring" ]]; then
  echo "WARNING: latest commit is not the expected first commit."
  echo "Latest: $LATEST"
  echo "Expected: Site infrastructure: canonical search, navbar grader pill, Track 4 wiring"
  echo "Aborting so a human can verify what happened."
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────
# Commit 2 of 5 — Tracks 1-3 student pages with AF spec updates
# ─────────────────────────────────────────────────────────────────────
git add 160sp/t1_intro.html 160sp/t1_task1.html 160sp/t1_task2.html \
        160sp/t1_task3.html 160sp/t1_submissions.html \
        160sp/t2_intro.html 160sp/t2_task1.html 160sp/t2_task2.html \
        160sp/t2_task3.html 160sp/t2_submissions.html \
        160sp/t3_intro.html 160sp/t3_task1.html 160sp/t3_task2.html \
        160sp/t3_task3.html 160sp/t3_submissions.html

git commit -m "Tracks 1-3 student pages: canonical scaffold + AF four-scraper / lifecycle DB updates

Promotes the t1, t2, t3 student-facing pages from the live snapshot mirror
into canonical Atlas pages. All fifteen pages share the same scaffold
(top-nav, breadcrumb, page-grid with side-nav, hero, content sections,
site-footer) and the same submissions-table schema.

Track 2 (Article Finder) carries substantive AF spec updates:
- t2_intro.html adds two new sections — How the pipeline is organised
  (introduces the four-scraper layer SerpAPI / scholarly / paper-scraper /
  scidownl and the three-stage triage funnel) and Where harvested
  references live (introduces the article_references table as the
  candidate buffer between harvest and acquisition).
- t2_task2.html adds a new forward-pointer section explaining which
  scraper takes which kind of query, and an amber callout pointing
  students at the existing 46-review reference harvest for query
  prototyping before SerpAPI credits are spent.
- t2_task3.html restructures into seven phases with two new phases:
  Phase 3 (the article_references table — schema columns to populate,
  deduplication rules, and the explicit instruction to consume the
  existing AE coordination scripts rather than reinvent reference
  parsing) and Phase 5 (PDF acquisition cascade and the scidownl policy
  gate, with the four-condition gate spelled out: config flag, policy
  clearance file, prior failure of Unpaywall+OpenAlex, ACCEPT decision).
  Grading rubric updated: new rows for article_references wiring (10),
  three-other-scrapers wiring (5), scidownl policy gate (5); existing
  rows rebalanced; total still 75.

Submissions pages: instructor-only critique-link hydration. A small JS
hook rewrites td[data-field='critique_link'] cells to point at
http://localhost:5050/?track=tN&task=N when sessionStorage['ka.admin']
is set; students see the same em-dashes they always have."

# ─────────────────────────────────────────────────────────────────────
# Commit 3 of 5 — Track 4 student pages + carried researcher exemplar
# ─────────────────────────────────────────────────────────────────────
git add 160sp/t4_intro.html 160sp/t4_task1.html 160sp/t4_task2.html \
        160sp/t4_task3.html 160sp/t4_submissions.html \
        160sp/track4/

git commit -m "Track 4: student pages, researcher carried exemplar, working Q-29 journey

Track 4 (GUI / Interactivity) ships its first canonical pages plus the
worked researcher exemplar carried through all three tasks.

Student-facing pages (canonical track scaffold; calendar dates Fri 1, 8,
15 May 2026 with mid-week-8 extension):
  t4_intro.html — track overview, methodology (evidential journeys,
    multi-modal answer shapes, Chinn-Brewer rebuttal economy), persona
    model (each student owns one persona, team collective discussion),
    three-task arc, carried-exemplar approach.
  t4_task1.html — Build a Persona Question Corpus (5-axis tagging,
    LLM-panel + literature-mining + cross-product methodology, four
    shared-infrastructure roles).
  t4_task2.html — Winnow & Fit Answer Shapes (four-stage winnowing
    sieve, schema-fitting decision table, defeater-identification
    heuristic, named failure mode 'defeater laundering').
  t4_task3.html — Prototype an Evidential Journey (4-item required-pieces
    checklist, LLM-panel reader test, two-page reflection, site-
    integration rubric line).
  t4_submissions.html — submissions tracker (status indicator on empty
    cells; GRADER LIVE pill).
  All four task pages carry next-→ closure bands.

Researcher carried exemplar (track4/):
  question_corpus_researcher_v1.md — 40 questions across five
    sub-flavours, tagged on five axes, with adequacy conditions and APA
    references.
  researcher_fitting_catalog.md — winnowing log + ten worked fittings
    covering all five answer shapes with named defeaters.
  journey_q29_art_affect_confound.html — working Toulmin journey on ART
    vs the affective confound; six-step disclosure (Data → Warrant +
    Backing → Qualified Claim → Rebuttal → Chinn-Brewer panel → Reader
    response). Wrapped in canonical scaffold; CI / N / source-study
    annotation on the 40-60% attenuation stat-figure.
  answer_shape_catalogue.html — the five canonical answer shapes
    visualised with science-writer captions and worked examples
    (Toulmin diagram canonical layout; field map after Novak & Gowin
    1984 with directional labelled edges and time axis; procedure with
    provenance column; contrast pair with EmotiBit/BIOPAC/cuff;
    ranked brief with administration-time column). Wrapped in
    canonical scaffold.
  chinn_brewer_response_widget.html — drop-in 7-response widget. Three
    scenarios; theory-protective / theory-flexible / theory-revising
    disposition coding. Wrapped in canonical scaffold.
  track4_operational_brief.md — directives extracted from the corpus
    prose (10 numbered claims), four-role team structure, four-stage
    winnowing protocol, schema-fitting decision tree.
  track4_task_design.md — the full task-design document with student
    arc, scaffolds (LLM-panel system prompt template, scenario cards,
    mining prompt template, schema-fitting decision tree, defeater
    identification heuristic, worked examples, rubrics)."

# ─────────────────────────────────────────────────────────────────────
# Commit 4 of 5 — Track 4 autograders + grader chrome integration
# ─────────────────────────────────────────────────────────────────────
git add 160sp/autograders/t4_task1_grader.py \
        160sp/autograders/t4_task2_grader.py \
        160sp/autograders/t4_task3_grader.py \
        160sp/autograders/run_all.py \
        160sp/ka_admin.html

git commit -m "Track 4 autograders + grader-page integration into ka_admin

Three new autograders in the same shape as AG's existing nine:

  t4_task1_grader.py (~210 lines) — checks corpus size against the 40-60
    window, five-axis tagging completeness, adequacy-condition presence,
    provenance, and the methods file. Contract-gate on adequacy-condition
    discipline. Rubric: 15+20+15+10+10+5 = 75.

  t4_task2_grader.py (~170 lines) — checks the four-stage winnowing log
    (gate), working-corpus presence, shape-fit completeness across the
    five canonical shapes (toulmin, field-map, procedure, contrast-pair,
    ranked-brief), defeater quality including a heuristic for citable
    defeaters (year-marked citation pattern), and team fitting-critique
    notes. Rubric: 15+10+25+15+10 = 75.

  t4_task3_grader.py (~220 lines) — locates the prototype HTML, checks
    for all four required pieces (landing, populated answer-shape diagram,
    Chinn-Brewer panel, reader-response stage) with a contract-gate;
    inspects the Chinn-Brewer panel for the seven response dispositions
    actually in the DOM (catches 'panel exists but is hidden behind a
    click'); counts reader-test transcript files; validates the
    reflection length window; checks for site-scaffold integration
    (top-nav + breadcrumb + footer). Rubric: 30+15+15+10+5 = 75.

run_all.py — registers the three new graders; --track now accepts t4.
All twelve graders pass --self-test cleanly on an empty submission.

ka_admin.html — Grading tab now carries a primary 'Open Grader Dashboard'
button at the top of the Class grading summary card and a one-line note
explaining the automated-check layer at 160sp/autograders/ (twelve graders
including Track 4) and how to start AG's stdlib grader_page server."

# ─────────────────────────────────────────────────────────────────────
# Commit 5 of 5 — design documentation
# ─────────────────────────────────────────────────────────────────────
git add docs/AF_PIPELINE_RECON_2026-04-27.md \
        docs/ATLAS_SCIENCE_COPY_PACK_T2_AF_2026-04-27.md \
        docs/CLAUDE_DESIGN_PROMPTS_2026-04-27.md \
        docs/USABILITY_CRITIQUE_TRACK4_2026-04-27.md \
        docs/GRADER_INTEGRATION_RECON_2026-04-27.md

git commit -m "Track 4 / AF design docs: recon, copy pack, critique, Claude Design prompts

Five companion documents that drove the page-level changes:

  AF_PIPELINE_RECON_2026-04-27.md — reconnaissance over Article_Finder
    v3.2.3 plus the lifecycle DB schema; proposed article_references
    table DDL; identifies the existing AE coordination scripts AF should
    consume (extract_neuro_key_review_references.py and
    build_neuro_review_acquisition_queue.py) rather than reinvent;
    three-stage triage protocol with placements for all four scrapers.

  ATLAS_SCIENCE_COPY_PACK_T2_AF_2026-04-27.md — the 13-item copy pack
    per t2 page (39 items total) produced by the K-ATLAS Science-Writing
    Agent. Authoritative source for the t2 page rewrites in commit 2.

  CLAUDE_DESIGN_PROMPTS_2026-04-27.md — three prompts DK can paste into
    claude.ai/design to (1) build an Atlas design system from the
    existing CSS, (2) polish the t4_*.html pages, (3) polish the Q-29
    journey prototype.

  USABILITY_CRITIQUE_TRACK4_2026-04-27.md — 35-dimension usability
    critique (Nielsen H1-H10, Shneiderman R1-R8, Visualisation V1-V17)
    over the eight Track 4 pages. Top-10 punch-list items have been
    addressed in commits 1 and 3; lower-priority items deferred.

  GRADER_INTEGRATION_RECON_2026-04-27.md — reconnaissance over AG's
    grader_page + autograders, ka_canonical_navbar, and ka_admin's
    Grading tab; the integration design implemented in commit 4."

echo
echo "All five commits landed."
git log -5 --oneline
