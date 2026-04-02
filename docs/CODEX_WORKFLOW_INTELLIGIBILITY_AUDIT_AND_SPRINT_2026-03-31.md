# Codex Workflow Intelligibility Audit And Sprint (2026-03-31)

Author: Codex

## Purpose
This note evaluates how intelligible the current Knowledge Atlas workflow is across pages for each user type, identifies what is missing, and proposes a sprint that would make the workflows substantially more coherent and useful.

## General Judgment
The site now has real route structure. It is no longer a loose cabinet of pages. But its saving model is still fragmented, and several user types are forced to carry too much of the workflow in their heads.

The current strengths are these:
- role pathways exist and are explicit
- the workflow hub preserves step progress and notes
- route banners now connect key pages back to guided paths
- the article collector gives the beginning of a cross-page working memory

The main weaknesses are these:
- saving is fragmented across several local mechanisms rather than one workspace model
- some workflows still point at pages that are semantically adjacent rather than truly purpose-built
- the user is often told what page they are on, but not what durable artifact they are building
- there is still no strong notion of a dossier, brief, folder, basket, or notebook that survives across tasks

## Current Save Tools
At present the site has four distinct save patterns.

### 1. Workflow Step Notes
Source:
- [ka_workflow_hub.html](/Users/davidusa/REPOS/Knowledge_Atlas/ka_workflow_hub.html)

What it does:
- saves per-step notes in `localStorage`
- saves current step progress

What is good:
- adequate for lightweight guided reflection

What is weak:
- notes do not become a larger artifact
- notes are trapped inside one workflow
- no export

### 2. Article Collector
Source:
- [ka_article_collector.js](/Users/davidusa/REPOS/Knowledge_Atlas/ka_article_collector.js)

What it does:
- persists a floating cross-page article basket
- deduplicates by URL or DOI
- can be opened from workflow steps

What is good:
- the most useful current cross-page memory tool

What is weak:
- it only stores articles
- no folders
- no relation to topics, claims, questions, evidence cards, or fronts
- weak export

### 3. Contribution Intake Queue
Source:
- [ka_article_propose.html](/Users/davidusa/REPOS/Knowledge_Atlas/ka_article_propose.html)
- [ka_contribute.html](/Users/davidusa/REPOS/Knowledge_Atlas/ka_contribute.html)

What it does:
- persists submission-state data
- separates pending, approved, duplicate, rejected

What is good:
- gives contributors a real task state

What is weak:
- it is intake-oriented, not research-oriented
- not a general workspace

### 4. Miscellaneous Local Session Saves
Examples:
- usability critic sessions
- login and workflow overlay state

What is good:
- enough for demos and internal testing

What is weak:
- too many unrelated local stores
- no unified user-facing concept

## User-Type Audit

## Student Explorer
### Current routes
- `first-questions`
- `deep-dive`

### What currently works
- starting with Did You Know is good
- moving from one finding into the topic hierarchy is sensible
- the route encourages curiosity before contribution

### What is still confusing
- the student is not yet clearly building anything
- after curiosity is sharpened, the site does not give a durable place to keep a question set
- the jump from exploration to contribution is still too abrupt

### What this user should really be building
- a question notebook
- a topic shortlist
- a reading basket
- a small dossier for one promising topic

### Recommended improvements
- keep `first-questions` as the first route
- add a `Topic Dossier` workflow:
  - Did You Know
  - Topic Hierarchy
  - Topics
  - Evidence
  - Question Maker
  - save as dossier
- make `deep-dive` explicitly produce a saved question-and-evidence brief

## Contributor
### Current routes
- `evidence-pipeline`
- `deep-dive`
- `first-questions`

### What currently works
- article search to evidence to tagging to submission is a proper contribution skeleton
- the route is concrete and finite

### What is still confusing
- there is no strong triage stage before submission
- the contributor can collect articles, but cannot easily group them into a batch folder
- there is no obvious artifact like `submission packet` or `review bundle`

### What this user should really be building
- a candidate-paper basket
- a batch folder
- a submission packet
- a duplicate-check and rationale note

### Recommended improvements
- split contribution into two workflows:
  - `Find and Triage Papers`
  - `Process and Submit Evidence`
- add a `Batch Folder` artifact that groups collected papers, notes, and intended topic

## Researcher
### Current routes
- `hypothesis-test`
- `lit-synthesis`
- `evidence-pipeline`
- `deep-dive`

### What currently works
- the hypothesis route is strong
- the synthesis route is strong in principle
- the researcher has the richest current path family

### What is still confusing
- synthesis ends in annotations, which is too small a terminal artifact
- there is no research dossier or literature matrix
- support and contradiction inspection are separated, but not gathered into one saved object

### What this user should really be building
- a research dossier
- a literature synthesis notebook
- a contradiction map
- a candidate experiment brief

### Recommended improvements
- keep `hypothesis-test`
- keep `lit-synthesis`
- add:
  - `Contradiction Review`
  - `Research Front Review`
  - `Neuroscience Grounding Review`
- make the output a `Research Dossier`, not just saved notes

## Practitioner
### Current routes
- `design-decision`
- `client-brief`
- `deep-dive`

### What currently works
- the idea of starting from an image or design option is right
- the client-brief route is pragmatically useful

### What is still confusing
- the practitioner route still leans too heavily on researcher-style pages
- the image tagger is an entry point, but the consequence chain is not yet presented as a simple design-facing storyline
- there is no clean `brief packet` output

### What this user should really be building
- a design consequence brief
- an image-to-consequence note
- a client packet
- a decision memo

### Recommended improvements
- add a `Design Consequence Trace` workflow:
  - image tagger
  - topic hierarchy or topics
  - evidence
  - warrants
  - brief builder
- add a `Compare Design Options` workflow

## Instructor
### Current routes
- `student-onboarding`

### What currently works
- the approval queue and dashboard path is coherent

### What is still confusing
- too narrow
- no route for monitoring workflow health after onboarding
- no route for producing teaching packets or assigning topic packets

### What this user should really be building
- a cohort oversight view
- an assignment packet
- a roster progress brief

### Recommended improvements
- keep `student-onboarding`
- add:
  - `Cohort Monitoring`
  - `Assignment Pack Builder`
  - `Teaching Demo Route`

## Theory Explorer
### Current routes
- `mechanism-trace`
- `hypothesis-test`
- `deep-dive`

### What currently works
- the mechanism-trace route is conceptually correct
- the system explanation page is now in the path, which is important

### What is still confusing
- there is no dedicated theory page distinct from the broader theory-and-experiment page
- there is no dedicated mechanism atlas page
- the user does not yet leave with a saved `critical experiment` brief

### What this user should really be building
- a theory comparison sheet
- a mechanism chain
- a critical experiment brief

### Recommended improvements
- keep `mechanism-trace`
- add:
  - `Theory Comparison`
  - `Mechanism Chain`
  - `Critical Experiment`
- eventually create separate theory and mechanism landing pages instead of making one page bear the whole load

## Additional Plausible Workflows
These are plausible, useful, and well-motivated by the present system.

### 1. Topic Dossier
Best for:
- student explorer
- researcher

Output:
- saved topic dossier with topic notes, evidence picks, open questions, and next papers

### 2. Contradiction Review
Best for:
- researcher
- theory explorer

Output:
- contradiction brief with support, attack, and unresolved question summary

### 3. Research Front Review
Best for:
- researcher
- instructor

Output:
- front card collection with maturity, contradictions, and methods trends

### 4. Design Consequence Trace
Best for:
- practitioner

Output:
- image or design option -> likely consequences -> evidence -> caution note

### 5. Mini-Review Builder
Best for:
- researcher
- instructor

Output:
- compact topic review suitable for teaching or briefing

### 6. Neuroscience Grounding Review
Best for:
- researcher
- theory explorer
- practitioner

Output:
- where current claims are neurally grounded and where stronger physiological grounding is needed

### 7. Assignment Pack Builder
Best for:
- instructor

Output:
- a packet for one student or one track containing topic, question, starter papers, and next steps

### 8. New-In-The-Field Review
Best for:
- instructor
- researcher
- practitioner

Output:
- recent-year changes, trends, rising methods, and notable contradictions

## Saving And Workspace Tools To Add
The central recommendation is to stop treating saving as several small unrelated local tricks. Atlas needs a unified user-facing concept.

## Proposed Core Concept: Workspace
A workspace should be a user-named container that can hold mixed items:
- articles
- evidence cards
- topics
- research fronts
- questions
- hypotheses
- notes
- images
- argument clusters

Each workspace can then expose smaller views:
- basket
- folder
- notebook
- brief
- export

## Recommended Tools

### 1. Free Basket
Purpose:
- one-click save-anything tool

Should hold:
- articles
- evidence cards
- topics
- fronts
- questions

### 2. Folders
Purpose:
- organise saved items by project or objective

Examples:
- `Lighting and Mood`
- `Track 2 Candidate Papers`
- `Client A Acoustic Brief`

### 3. Notebook
Purpose:
- a growing markdown-like note attached to a folder or workflow

Should support:
- step notes
- pasted excerpts
- linked saved items

### 4. Dossier Builder
Purpose:
- compile a folder into a structured artifact

Examples:
- topic dossier
- research dossier
- client brief
- contradiction brief

### 5. Export Tools
Minimum exports:
- Markdown
- HTML
- plain text

Later exports:
- `.docx`
- Google Doc handoff
- PDF brief

### 6. Saved Searches
Purpose:
- preserve article-search or evidence-search criteria

### 7. Comparison Board
Purpose:
- compare two topics, two theories, two design options, or two papers

### 8. Reading Queue
Purpose:
- mark saved papers as:
  - queued
  - read
  - used
  - submitted

### 9. Citation Bundle
Purpose:
- export saved articles as:
  - DOI list
  - citation text
  - BibTeX or RIS later

### 10. Shareable Brief Links
Purpose:
- allow a practitioner or instructor to share a stable dossier or brief

## Intelligibility Recommendations By Priority
1. Give every workflow a clear output artifact.
2. Unify all save behaviour under one visible workspace model.
3. Add folders and dossiers before adding more clever pages.
4. Keep route banners, but let them route into saved work, not merely into the next page.
5. Separate theory pages from mechanism pages when possible.
6. Make practitioner routes visibly different from researcher routes.
7. Make student exploration culminate in a saved topic dossier.

## Sprint Proposal
Title:
`Workflow Intelligibility And Workspace Sprint`

Duration:
`5 to 7 days`

## Sprint Goal
Make Atlas feel like one coherent guided instrument rather than a set of strong pages loosely connected by navigation.

## Phase 1: Workspace Foundations
Deliverables:
- global basket for mixed items
- folder model
- notebook model
- unified local persistence abstraction

Files likely affected:
- new shared workspace JS module
- route banner integration
- article collector upgrade

## Phase 2: Role Output Artifacts
Deliverables:
- topic dossier
- research dossier
- design brief
- critical experiment brief
- assignment pack

This phase makes each route end in something tangible.

## Phase 3: Workflow Revision
Deliverables:
- revise role routes to point toward output artifacts
- add new workflows:
  - topic dossier
  - contradiction review
  - design consequence trace
  - mini-review builder
  - neuroscience grounding review

## Phase 4: Export Layer
Deliverables:
- export workspace or dossier to Markdown
- export brief to HTML
- prepare `.docx` handoff path
- define future Google Doc export path

## Phase 5: QA And Teaching Readiness
Deliverables:
- click-through audit for all route pages
- route completion tests
- saved-state tests
- one demo script per user type

## Definition Of Done
- every user type has at least one route with a clear saved output
- all key workflows can save mixed items, not just articles
- a user can leave and return without losing place or notes
- a folder can be exported to Markdown
- practitioners can produce a brief
- researchers can produce a dossier
- theory explorers can produce a critical experiment brief
- students can produce a topic dossier
- instructors can produce an assignment packet

## Final Recommendation
The next decisive move is not to add more isolated pages. It is to give the existing routes a common workspace model and a proper output artifact. Once that exists, the site will become much easier to understand, teach from, and extend.
