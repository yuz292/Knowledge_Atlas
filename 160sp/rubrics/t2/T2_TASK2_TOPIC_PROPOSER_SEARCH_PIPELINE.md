# Track 2 · Task 2: Build the Topic Proposer & Search Pipeline

**Track:** Article Finder  
**What it does:** Reads the gap analysis data in Article Eater's 166 PNU templates, proposes searches to fill those gaps, runs the searches, collects citations, and vets them through the contribute page you fixed in Task 1.  
**What you build:** A pipeline with a visible dashboard showing what gaps exist, what searches were proposed, and what the results were.

---

## What This Assignment Teaches

Task 1 taught you to **fix** existing code by wiring things together. Task 2 teaches you to **design** a new pipeline from scratch — using AI to build it, but owning the spec, the data flow, and the proof that it works.

The pipeline has three stages:

```
GAPS in the knowledge base → SEARCHES to fill them → RESULTS vetted by the classifier
```

You need to spec each stage, delegate the build, and prove the pipeline produces useful results.

---

## Setup

You should already have the four repositories from Task 1:
- `Knowledge_Atlas` — the site (with your fixed contribute page from Task 1)
- `Article_Finder` — the discovery pipeline
- `Article_Eater` — the extraction engine (contains the gap data)
- `atlas_shared` — the shared classifier (installed as `pip install -e .`)

---

## Phase 1: Understand the Gap Data

The Article Eater has 166 PNU (Plausible Neural Underpinning) templates. Each template describes a mechanism chain — how an environmental feature (e.g., ceiling height) leads to a psychological outcome (e.g., creativity) through neural processes. Each step in the chain has a **confidence score**. Low-confidence steps are **gaps** — places where the evidence is thin.

### 1A. Ask your AI to explain the template structure

Pick 3 templates from `Article_Eater/data/templates/` (e.g., `T2.json`, `T4.json`, `T13.json`). Give them to your AI and ask:

> *"These are PNU templates from the Knowledge Atlas. Each one has a `mechanism_chain` — a series of steps linking an environmental feature to a psychological outcome. Walk me through one template completely: what does each step represent, what does `confidence` mean for each step, and what does a low-confidence step tell us?"*

> *"Then look at all three templates and identify: which steps have confidence below 0.5? Those are the gaps. For each gap, tell me: what specific knowledge is missing, and what kind of study would fill it?"*

### 1B. Ask your AI to explain the 4 types of VOI analysis

The Article Eater also has an Expected Value of Information (EVOI) framework that prioritizes which gaps matter most. Ask:

> *"The Knowledge Atlas uses Value of Information analysis to prioritize research gaps. There are four types of gaps that VOI can identify. Look at this gap type enum from `Article_Eater/src/types/reduction.ts`:*
> ```
> MISSING_NODE — A required mechanism is completely unknown
> MISSING_EDGE — Connection between known nodes is unproven  
> AMBIGUOUS_DIRECTION — Correlation exists, direction unknown
> UNKNOWN_INTERACTION — How two mechanisms combine is unknown
> ```
> *Also look at `GapReport` in `src/types/crossReference.ts` which tracks `missing_mechanisms` and `recommendation` per template domain.*
> 
> *Explain each gap type with a concrete example from neuroarchitecture. Then explain: if I wanted to find papers that could fill a MISSING_EDGE gap, what kind of search query would I need? How would it differ from a search to fill an AMBIGUOUS_DIRECTION gap?"*

### 1C. Get a boxology diagram of the full pipeline you'll build

> *"I need to build a pipeline that: (1) reads gap data from PNU templates, (2) proposes search queries to fill those gaps, (3) runs the searches, (4) collects citations, and (5) vets them through a classifier. Draw a box-and-arrow diagram showing the entire data flow, from template gaps to vetted citations."*

**Your deliverable:** The boxology diagram, plus a list of 5 specific gaps you found in the templates with their confidence scores and what's missing.

---

## Phase 2: Spec — Write the Pipeline Contract

Your contract must specify three sub-systems:

### 2A. The Topic Proposer

This reads template gaps and outputs search proposals.

```markdown
## Topic Proposer Contract

### Inputs
- PNU template JSON files from Article_Eater/data/templates/
- The 30 research questions from the atlas (Q01–Q30, as defined in ka_auth_server.py)

### Processing
For each template with low-confidence steps (< 0.5):
1. Identify the gap: which step, what type, what's missing
2. Map the gap to the closest research question(s) from Q01–Q30
3. Generate search queries in THREE formats:
   a. Google AI Scholar search query (natural language question)
   b. Google Scholar keyword query (structured keywords + boolean operators)
   c. A 2–3 sentence summary of the topic for human review

### Outputs (per gap)
- template_id and step number
- gap_type (MISSING_NODE, MISSING_EDGE, AMBIGUOUS_DIRECTION, UNKNOWN_INTERACTION)
- confidence_current (the step's current confidence)
- matched_question_ids (which of Q01–Q30 this maps to)
- search_queries: { ai_scholar: "...", keyword: "...", summary: "..." }

### Success conditions
- At least 10 gaps identified across the 166 templates
- Each gap has all three query formats
- Queries are specific enough to find relevant papers (not just "neuroarchitecture")
```

### 2B. The Search Runner

This takes the proposed queries and runs them.

> *Ask your AI: "What APIs or methods can I use to search Google Scholar programmatically? What about the new Google AI Scholar? What are the rate limits and terms of service? If programmatic access isn't available, what's the best manual workflow?"*

```markdown
## Search Runner Contract

### Inputs
- Search proposals from the Topic Proposer

### Processing
For each search proposal:
1. Run the AI Scholar query OR the keyword query
2. Collect the top 10–20 results (title, authors, year, DOI/URL, snippet)
3. Store results as structured JSON

### Outputs (per search)
- search_query used
- results: [ { title, authors, year, doi, url, snippet } ]
- result_count
- search_timestamp

### Success conditions
- At least 5 searches executed
- Results are structured JSON, not raw HTML
- Each result has at least title and either DOI or URL
```

### 2C. The Vetting Pipeline

This takes collected citations and runs them through the classifier (your Task 1 contribute page).

```markdown
## Vetting Pipeline Contract

### Inputs
- Citation results from the Search Runner

### Processing
For each citation:
1. Submit to the contribute endpoint (from Task 1)
2. Receive classification: accepted / edge_case / rejected
3. Accepted and edge-case papers are stored

### Outputs
- Per citation: article_type, verdict, matched_topic, confidence
- Summary: N searched → M accepted → K edge cases → J rejected

### Success conditions
- At least 20 citations vetted
- Accepted papers appear in the database
- The full pipeline runs end-to-end: gap → search → citation → vet → store
```

### 2D. The Dashboard

> *Ask your AI: "I need a web page that shows the status of this pipeline. It should display: (1) which gaps were identified and their priority, (2) what searches were proposed, (3) what results came back, and (4) which results passed vetting. Design a layout for this dashboard. It should update as the pipeline runs."*

**Your deliverable:** The complete contract for all four sub-systems, plus the dashboard wireframe.

---

## Phase 3: Fix — Delegate to Your AI

Give your AI the four contracts and ask it to build:

1. A Python script that reads templates, identifies gaps, and generates search proposals
2. A search execution module (automated if possible, manual-assist if not)
3. Integration with the Task 1 contribute endpoint for vetting
4. A dashboard page (`ka_topic_proposer.html` or similar)

### Questions you must ask your AI to verify the build

> *"Show me how you read the mechanism_chain from a template JSON. Which field do you check for low confidence? What threshold do you use?"*

> *"Show me the search queries you generate for a specific gap. Are they specific enough? If I searched Google Scholar for your keyword query right now, would the first page of results be relevant to the gap?"*

> *"How do you connect the search results to the vetting endpoint from Task 1? Show me the exact API call."*

> *"What happens if a search returns zero results? Does the pipeline crash or handle it gracefully?"*

> *"How does the dashboard get its data? Does it read from a file, a database, or the pipeline's memory? What happens if I refresh the page — do I lose the data?"*

> *"Show me how you distinguish which research question (Q01–Q30) a gap maps to. What matching logic do you use?"*

**Your deliverable:** Working code, plus a log of which verification questions revealed problems.

---

## Phase 4: Prove — Run the Pipeline End-to-End

### Step 1: Run the Topic Proposer

```bash
python3 topic_proposer.py --templates Article_Eater/data/templates/
```

Verify:
- [ ] At least 10 gaps identified
- [ ] Each gap has template_id, step number, confidence, gap_type
- [ ] Each gap has 3 search query formats
- [ ] Queries are specific (not just "neuroscience")

### Step 2: Run at least 5 searches

Either automated or manual — but record each search:

| Search # | Gap source | Query used | Results found | Top result relevant? |
|----------|-----------|-----------|---------------|---------------------|
| 1 | T2 step 3 | "resolvable prediction error aesthetic pleasure architecture" | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Step 3: Vet at least 20 citations through the classifier

Submit the collected citations through your Task 1 contribute endpoint:

| Total citations vetted | Accepted | Edge cases | Rejected |
|-----------------------|----------|------------|----------|
| | | | |

### Step 4: Check the dashboard

- [ ] Dashboard shows the identified gaps
- [ ] Dashboard shows the search queries and result counts
- [ ] Dashboard shows the vetting results (accepted/edge/rejected)
- [ ] Dashboard data persists after page refresh

### Step 5: Trace one paper end-to-end

Pick ONE paper that made it through the entire pipeline and document its journey:

```
Gap: Template T__ step __ (confidence: 0.__)  
  → Gap type: _______________
  → Search query: "_______________"
  → Found: [paper title] by [authors] ([year])
  → Vetted: [accepted / edge_case]
  → Article type: [empirical / review / ...]
  → Stored at: [path]
  → DB entry: [paper_id]
```

**Your deliverable:** The validation matrix, the vetting summary, and one end-to-end trace.

---

## What You Submit

| Item | What it is |
|------|-----------|
| **Gap analysis** (Phase 1) | Boxology diagram + 5 specific gaps from templates |
| **Pipeline contract** (Phase 2) | Spec for Topic Proposer, Search Runner, Vetting Pipeline, and Dashboard |
| **Working code** (Phase 3) | Topic proposer script, search runner, dashboard page |
| **Verification log** (Phase 3) | Which questions you asked AI, which revealed problems |
| **Validation results** (Phase 4) | Gap count, search results, vetting summary, end-to-end trace |
| **File manifest** (Phase 4) | `git diff` and `git status` output |

**How to generate your manifest:**
```bash
cd Knowledge_Atlas
git diff --name-only HEAD
git status --short
```

---

## Files You Must Submit

| File | Change Type | What It Does |
|------|------------|-------------|
| `topic_proposer.py` (or similar) | New | Reads templates, identifies gaps, generates search proposals |
| Search results JSON | New | Structured results from executed searches |
| Dashboard page (e.g., `ka_topic_proposer.html`) | New | Shows gaps, searches, and vetting results |
| `data/storage/` | New files | Stored PDFs/citations for accepted papers |
| Database | Modified | New entries for vetted papers |

---

## Grading

| Criterion | What we check |
|-----------|--------------|
| **Gap analysis** | You correctly identified low-confidence steps and their gap types |
| **Spec quality** | Contract covers all 4 sub-systems with testable success conditions |
| **Search quality** | Generated queries are specific enough to find relevant papers |
| **End-to-end pipeline** | At least one paper traced from gap → search → vet → store |
| **Dashboard** | Shows pipeline status, persists data |
| **Verification questions** | You caught problems in the AI's implementation |
