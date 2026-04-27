# Track 2 · Task 2: Gap Targeting & Query Generation

**Track:** Article Finder  
**What you build:** A gap extractor that reads the Article Eater's 166 PNU templates, identifies knowledge gaps, scores them by Value of Information (VOI), and generates targeted search queries in two formats: Google AI Citation (natural language) and Google Scholar Boolean.  
**Core lesson:** Before you search for anything, you must know *what* you're looking for and *why*. VOI scoring tells you which gaps matter most. Query design determines whether you find relevant papers or noise.

---

## Setup

You should already have the four repositories from Task 1:
- `Knowledge_Atlas` — the site (with your fixed contribute page)
- `Article_Finder` — the discovery pipeline  
- `Article_Eater` — the extraction engine (contains the gap data AND the VOI functions)
- `atlas_shared` — the shared classifier (installed as `pip install -e .`)

---

## Phase 1: Understand the Gap Data and VOI System

### 1A. Understand the PNU templates

The Article Eater has 166 PNU (Plausible Neural Underpinning) templates. Each describes a mechanism chain: how an environmental feature (e.g., ceiling height) leads to a psychological outcome (e.g., creativity) through neural processes. Each step has a **confidence score**. Low-confidence steps are **knowledge gaps**.

Pick 3 templates from `Article_Eater/data/templates/`. Ask your AI:

> *"These are PNU templates from the Knowledge Atlas. Walk me through one template completely: what does each step in the `mechanism_chain` represent, what does `confidence` mean for each step, and what does a low-confidence step (< 0.5) tell us about what's missing from the research corpus?"*

> *"Now look at all three templates and identify: which steps have confidence below 0.5? For each gap, tell me what specific study would fill it."*

### 1B. Understand the VOI scoring system

The Article Eater has VOI functions for scoring knowledge gaps. You will use one in this task. Ask your AI:

> *"Read `Article_Eater/src/services/voi_search.py`. Find `VOICalculator` and its `calculate_voi()` method. What inputs does it take? What does the combined VOI score mean? When would a gap get a HIGH score vs. a LOW score?"*

**What you should learn:** A gap at a hub in the belief network (high centrality, many downstream beliefs) with confidence ~0.4 scores much higher VOI than an isolated gap with confidence 0.45. VOI = "how much would knowing this change our predictions?"

### 1C. Understand the two query types

You will generate queries in two formats. Read `160sp/ka_google_search_guide.html` for the full tutorial, then ask your AI:

> *"Explain the difference between a Google AI Citation query and a Google Scholar Boolean query. When would I use each? What makes one better than the other for finding specific mechanism-level evidence?"*

**Google AI Citation** (natural language — what you type into Google):
```
What neuroimaging evidence shows that exposure to natural versus urban 
environments reduces amygdala reactivity, and does this explain the 
stress-buffering effect attributed to Stress Recovery Theory?
```

**Google Scholar Boolean** (structured — what SerpAPI sends to Google Scholar):
```
("amygdala" OR "amygdala reactivity") AND ("natural environment" OR 
"nature exposure") AND ("stress" OR "cortisol") AND ("fMRI" OR 
"neuroimaging") -review
```

The key differences:
- **AI Citation** uses full sentences with theory names and mechanism descriptions. Google's AI understands synonyms and intent.
- **Boolean** uses exact keywords connected by AND/OR with quotes for phrases. Add `-review` to exclude review articles when you want primary research. Use `intitle:` to require terms in the title.

### 1D. Get a boxology diagram of the full pipeline

> *"Draw a box-and-arrow diagram of this complete pipeline (Tasks 2 and 3 combined):*
> 1. *Read PNU templates → extract gaps with confidence < 0.5*
> 2. *Score gaps using VOICalculator → sort by priority*
> 3. *Generate search queries (AI Citation + Boolean)*
> 4. *Execute searches via SerpAPI → get titles, snippets, DOIs*
> 5. *Collect full abstracts via Semantic Scholar / CrossRef / PubMed / OpenAlex*
> 6. *Triage abstracts through classifier + VOI scoring*
> 7. *Classify papers: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT*
> 8. *Display PRISMA funnel on dashboard"*

**Your deliverable:** The boxology diagram, plus a list of 5 specific gaps with confidence scores.

---

## Phase 2: Build the Gap Extractor

### 2A. Write the contract

```markdown
## Gap Extractor Contract

### Inputs
- PNU template JSON files from Article_Eater/data/templates/

### Processing
For each template:
1. Walk the mechanism_chain
2. Extract steps with confidence < 0.5
3. Also extract: key_references not in our corpus,
   competing_accounts, and falsification_conditions
4. Score each gap using VOICalculator.calculate_voi()

### Outputs (per gap)
- template_id, step_number, step_description
- gap_type (MECHANISM, VALIDATION, DIRECTION, BOUNDARY)
- confidence_current
- voi_score (combined)
- description of what knowledge is missing

### Success conditions
- At least 10 gaps identified across the 166 templates
- Gaps sorted by VOI score (highest priority first)
- Each gap has a gap_type and description
```

### 2B. Delegate to your AI

Give your AI the contract and ask it to build a Python script. Then verify:

> *"Show me how you read the mechanism_chain from a template. Which field has the confidence? What threshold do you use?"*

> *"Show me the VOI scores for 3 gaps. Why does one score higher than another?"*

> *"What happens if a template has no low-confidence steps? Do you skip it silently or log it?"*

---

## Phase 3: Generate Search Queries

### 3A. Write the query generator contract

```markdown
## Query Generator Contract

### Inputs
- Ranked gap list from the Gap Extractor (top 20 by VOI)

### Processing
For each gap:
1. Read the gap description and the template's mechanism chain
2. Generate a Google AI Citation query using the patterns from 
   ka_google_search_guide.html (evidence-seeking or mechanism patterns)
3. Generate a Google Scholar Boolean query using:
   - Exact-phrase quotes for key concepts
   - OR for synonyms  
   - AND to combine facets
   - -review to exclude review articles (when seeking primary research)
   - intitle: for high-precision searches

### Outputs (per gap)
- gap_id, template_id, voi_score
- ai_citation_query: full natural language question
- boolean_query: structured keyword query
- gap_summary: 2-3 sentence description for human review

### Success conditions
- At least 10 gaps have both query types
- AI Citation queries follow the 5-component pattern 
  (evidence type, mechanism, environment, population, theory)
- Boolean queries use proper operators (not just comma-separated words)
- Queries are specific enough to find relevant papers
```

### 3B. Use the query generation prompt

We provide a prompt template to help generate high-quality queries. See `query_generator_skill.md` in this rubrics folder.

> *Give your AI the prompt template along with 3 gaps from your extractor. Ask it to generate queries. Then manually test one AI Citation query in Google — does the first page of results contain relevant papers?*

### 3C. Verification questions

> *"Show me the Boolean query for one gap. Does it use exact-phrase quotes? Does it have OR groups for synonyms? Would Google Scholar parse this correctly?"*

> *"Show me the AI Citation query for the same gap. Does it follow the 5-component pattern? Could a researcher read this as a real research question?"*

> *"Take a gap about [specific mechanism]. Generate both query types. Now explain: which query would find a broader set of papers, and which would find more precisely targeted papers?"*

---

## Phase 4: Prove It Works

### Step 1: Run the gap extractor

```bash
python3 gap_extractor.py --templates Article_Eater/data/templates/
```

Verify:
- [ ] At least 10 gaps identified
- [ ] Gaps sorted by VOI score
- [ ] Each gap has template_id, step number, confidence, gap_type, voi_score

### Step 2: Generate queries for top 10 gaps

```bash
python3 query_generator.py --gaps gap_results.json
```

Verify:
- [ ] Each gap has both AI Citation and Boolean queries
- [ ] AI Citation queries are full sentences (not keyword lists)
- [ ] Boolean queries use AND/OR/quotes properly

### Step 3: Manual spot-check

Pick 3 queries and paste the AI Citation version into Google. For each:

| Gap | Query (first 50 chars) | First-page relevant? | Top result title |
|-----|----------------------|---------------------|-----------------|
| 1 | | Yes / No / Partial | |
| 2 | | | |
| 3 | | | |

### Step 4: Review your query quality

> *Ask your AI: "Review these 10 queries against the patterns in ka_google_search_guide.html. Which queries are strong? Which are weak? How would you improve the weak ones?"*

**Your deliverable:** Gap list, query pairs, spot-check table, and AI review of query quality.

---

## What You Submit

| Item | What it is |
|---|---|
| **Gap analysis** (Phase 1) | Boxology diagram + 5 gaps with VOI scores |
| **Gap extractor** (Phase 2) | Working script + contract |
| **Query pairs** (Phase 3) | 10+ gaps with AI Citation + Boolean queries |
| **Spot-check** (Phase 4) | Manual test of 3 queries in Google |
| **Query review** (Phase 4) | AI review of query quality |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `gap_extractor.py` | New | Reads templates, extracts gaps, scores by VOI |
| `query_generator.py` | New | Generates AI Citation + Boolean queries per gap |
| `gap_results.json` | New | Ranked gap list with VOI scores |
| `query_results.json` | New | Query pairs for each gap |

---

## Grading (60 points)

| Criterion | Points | What we check |
|---|---|---|
| **Gap extraction** | 15 | Correctly identified low-confidence steps from templates |
| **VOI scoring** | 10 | Gaps ranked by VOI; can explain why one scores higher |
| **AI Citation queries** | 10 | Follow 5-component pattern, specific enough for retrieval |
| **Boolean queries** | 10 | Proper AND/OR/quotes, not just comma-separated words |
| **Spot-check** | 5 | Tested 3 queries manually in Google, reported results |
| **Verification questions** | 10 | Caught problems in AI's implementation |

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/voi_search.py` | `VOICalculator.calculate_voi()` — scores gaps |
| `src/services/voi_search.py` | `QueryGenerator.generate_queries()` — baseline query generation |
| `src/services/voi_search.py` | `CrossFieldVocabulary.expand_query()` — cross-discipline synonyms |
| `160sp/ka_google_search_guide.html` | Full tutorial on writing AI Citation queries |
| `query_generator_skill.md` | Prompt template for generating queries from gaps |
