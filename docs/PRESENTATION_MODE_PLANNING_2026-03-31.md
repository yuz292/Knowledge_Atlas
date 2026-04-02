# Presentation Mode Planning (2026-03-31)

## Purpose
These are presentation modes to add to the Knowledge Atlas teaching and briefing layer. They are not merely visual themes. Each mode should answer a distinct class of question and should pull from a stable data source.

## Mode 1: What's New In The Field
### Question
What has changed in the last year, and what trends are becoming visible?

### Inputs
- canonical article payload
- year metadata
- topic memberships
- research fronts
- warrant and contradiction summaries
- method and sensor annotations

### Output
- top new topics
- top rising methods and sensors
- top new contradictions or reversals
- shifts in topic volume by year
- notable new clusters with weak or strong warrant

### UI expectation
- one overview page or briefing deck
- a year filter at the top
- compact trend cards
- a short "new this year" list
- links into evidence, topics, and fronts

## Mode 2: Mini-Reviews By Topic
### Question
What does the corpus currently support about one specific topic?

### Inputs
- topic memberships
- evidence rows
- warrant summaries
- related papers
- annotation layer
- theory and mechanism overlays

### Output
- one-page or short multi-section topic review
- core findings
- strongest evidence
- main caveats
- major contradictions
- frontier questions
- useful papers to read next

### UI expectation
- topic card opens a concise review
- one topic per page
- stable heading structure
- obvious next-step links

## Mode 3: Opportunities For Neuroscientific Grounding
### Question
Where does the corpus already have neural or physiological grounding, and where would such grounding most improve the field?

### Inputs
- sensor annotations
- method profiles
- topic memberships
- theory and mechanism pages
- evidence and contradiction structure

### Output
- topic areas with existing neural evidence
- topic areas that are mechanistically weak
- candidate sensors for each topic
- likely gains from EEG, fMRI, eye tracking, EDA, HRV, pupillometry, and related measures

### UI expectation
- mechanism-facing overlay, not a separate disconnected site
- topic-by-topic grounding suggestions
- links to theory and experiment-design pages

## Suggested Surfaces
- a dedicated presentation launcher page
- topic cards that expose mini-reviews
- a neuroscience overlay reachable from topic, theory, and experiment-design pages

## Build Order
1. `What's New In The Field`
2. `Mini-Reviews By Topic`
3. `Opportunities For Neuroscientific Grounding`

## Why This Order
- the first mode is immediately useful for class and talks
- the second gives durable topic teaching assets
- the third is strongest once topics and mechanisms are cleaner
