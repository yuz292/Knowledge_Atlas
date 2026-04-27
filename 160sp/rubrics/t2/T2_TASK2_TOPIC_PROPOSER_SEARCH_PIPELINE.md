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

### 1C. Know what's already in the corpus

Before you search for new papers, you need to know what you already have. The lifecycle database tracks every PDF in the system.

**Primary source:** `pipeline_lifecycle_full.db`, table `pdf_corpus_inventory`

This table lists every known PDF and its state:
- Whether it's in `CURRENT_GOLD` (fully processed and validated)
- Whether it's admitted but not yet gold
- Whether it's staged only
- Whether it's registry-backed

**Easiest readable version:** `pdf_corpus_inventory/latest.csv`

The summary report is at `pdf_corpus_inventory/latest.md`.

Ask your AI:

> *"Read `pdf_corpus_inventory/latest.csv`. How many papers are in CURRENT_GOLD? What topics do they cover? This tells me what we already have — I should NOT generate search queries for papers that are already in the corpus."*

If you also need to check for duplicates (same paper under different filenames or DOIs), use the companion table:

**Dedupe source:** `pipeline_lifecycle_full.db`, table `pdf_identity_inventory`  
**CSV:** `pdf_identity_inventory/latest.csv`

### 1D. Understand the two query types

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

### 2A. Write YOUR OWN contract

> **Contract objective:** "I want a program that reads PNU template JSON files and tells me which knowledge gaps are most worth searching for."
> **Contract is with:** The `VOICalculator` in `Article_Eater/src/services/voi_search.py` and the PNU templates in `Article_Eater/data/templates/`.
> **Prompt hint:** *"I need to write a contract for a gap extraction program. The program reads PNU template JSON files, walks their mechanism_chain, and uses VOICalculator.calculate_voi() to score each gap. Help me write the Inputs, Processing, Outputs, and Success Conditions sections."*

Before you ask an AI to build anything, you must write the contract yourself. This is the most important skill in this course: **if you can't spec what you want, you can't verify what you get.**

Your contract must have these four sections:

1. **Inputs** — What files does the program read? What format are they?
2. **Processing** — What does the program do, step by step?
3. **Outputs** — What does the program produce? What fields? What format?
4. **Success conditions** — How do you know it worked? Be specific. "It works" is not a success condition. "Extracts at least 10 gaps across 166 templates, each with template_id, step_number, confidence < 0.5, and gap_type" IS a success condition.

**Minimum bar** (your contract must cover at least these):
- Reads PNU template JSON files and walks `mechanism_chain`
- Extracts steps with confidence below a threshold you specify
- Scores each gap using `VOICalculator.calculate_voi()`
- Outputs structured JSON with gap_type, voi_score, and what's missing

### 2B. Write your tests BEFORE building

Ask your AI:

> *"Given my contract, what are 5 things that could go wrong? For each, write a test I can run to check. For example: 'What if a template has no mechanism_chain field?'"*

Write your tests as a checklist:
- [ ] Handles templates with no low-confidence steps (skips, doesn't crash)
- [ ] VOI scores are between 0 and 1
- [ ] Output JSON is valid and parseable
- [ ] At least 10 gaps found (if fewer, is the threshold wrong?)
- [ ] Gaps are sorted by VOI (highest first)

### 2C. Delegate to your AI, then validate

Give your AI the contract and ask it to build a Python script. Then run your tests:

> *"Show me how you read the mechanism_chain from a template. Which field has the confidence? What threshold do you use?"*

> *"Show me the VOI scores for 3 gaps. Why does one score higher than another?"*

> *"Run the script on 3 templates. Does the output match my contract's output spec? Show me the JSON."*

---

## Phase 3: Generate Search Queries

### 3A. Write YOUR OWN query generator contract

> **Contract objective:** "I want a program that takes my ranked gap list and generates search queries I can use to find papers that fill those gaps."
> **Contract is with:** The `QueryGenerator` in `Article_Eater/src/services/voi_search.py` and the patterns in `ka_google_search_guide.html`.
> **Prompt hint:** *"I need to write a contract for a query generator. It takes a JSON list of knowledge gaps (with VOI scores) and produces two search queries per gap: a Google AI Citation natural-language query and a Google Scholar Boolean query. Help me write the contract."*

Same discipline as Phase 2: **you** write the contract. Include:
1. **Inputs** — the gap list from Phase 2
2. **Processing** — how queries are generated (reference `ka_google_search_guide.html`)
3. **Outputs** — what fields per gap (both query types + gap summary)
4. **Success conditions** — at minimum:
   - At least 10 gaps have both AI Citation and Boolean queries
   - AI Citation queries are full sentences following the 5-component pattern
   - Boolean queries use `"exact phrases"`, `AND`, `OR`, and `-review`
   - At least 3 queries tested manually in Google with relevant first-page results

### 3B. Write your validation tests

> *"What makes a bad Boolean query? Give me 3 examples of common mistakes and how to detect them automatically."*

Your validation checklist:
- [ ] No Boolean query is just comma-separated words (must have AND/OR)
- [ ] Every AI Citation query ends with `?` and is > 50 characters
- [ ] Every Boolean query has at least one `"exact phrase"`
- [ ] At least 3 queries produce relevant results when tested in Google

### 3C. Use the query generation prompt

We provide a prompt template to help generate high-quality queries. See `query_generator_skill.md` in this rubrics folder.

> *Give your AI the prompt template along with 3 gaps from your extractor. Ask it to generate queries. Then manually test one AI Citation query in Google — does the first page of results contain relevant papers?*

### 3D. Verification questions

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

## A Note About Reuse

The contract → success conditions → test → validate workflow you're learning here is not a one-off. **You will reuse this exact approach in Task 3** (where you execute searches and triage results through a PRISMA funnel) and in every subsequent task. The PRISMA funnel in particular becomes a recurring deliverable — any time you add papers to the corpus, you must show the funnel proving you did it rigorously.

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/voi_search.py` | `VOICalculator.calculate_voi()` — scores gaps |
| `src/services/voi_search.py` | `QueryGenerator.generate_queries()` — baseline query generation |
| `src/services/voi_search.py` | `CrossFieldVocabulary.expand_query()` — cross-discipline synonyms |
| `pipeline_lifecycle_full.db` | Table `pdf_corpus_inventory` — every PDF and its state (CURRENT_GOLD, staged, etc.) |
| `pdf_corpus_inventory/latest.csv` | Readable export of the corpus inventory — check what you already have |
| `pdf_identity_inventory/latest.csv` | Dedupe info — catch duplicate papers under different names |
| `build_pdf_corpus_inventory_surface.py` | Builds the inventory surface from the lifecycle DB |
| `refresh_v7_state_surfaces.py` | Regenerates all state surfaces (run this to get fresh data) |
| `160sp/ka_google_search_guide.html` | Full tutorial on writing AI Citation queries |
| `query_generator_skill.md` | Prompt template for generating queries from gaps |
