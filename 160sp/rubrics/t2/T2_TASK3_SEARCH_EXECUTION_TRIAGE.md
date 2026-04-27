# Track 2 · Task 3: Search Execution & Abstract-First Triage

**Track:** Article Finder  
**Prerequisite:** Task 2 (you need your ranked gap list and query pairs)  
**What you build:** Execute your search queries via SerpAPI (Google Scholar), collect abstracts through a multi-source fallback chain, triage papers at the abstract level, and report results in a PRISMA-style dashboard.  
**Core lesson:** Never download a PDF to decide if it's relevant. Triage at the cheapest level — abstracts — using free APIs. Then prove your pipeline works with real PRISMA funnel numbers.

---

## What Is PRISMA and Why You're Building One

PRISMA (**Preferred Reporting Items for Systematic Reviews and Meta-Analyses**) is the gold standard for reporting systematic literature searches. It forces you to document your funnel transparently:

```
Records identified through database searching        (n = ?)
    ↓
Duplicates removed                                    (n = ?)
    ↓
Records screened by title + abstract                  (n = ?)  →  Excluded (n = ?)
    ↓
Full-text articles assessed for eligibility           (n = ?)  →  Excluded with reasons (n = ?)
    ↓
Studies included in final synthesis                   (n = ?)
```

Your dashboard must show these numbers. This is proof that your pipeline works.

---

## Setup

### Get your SerpAPI key

1. Go to [serpapi.com](https://serpapi.com) and sign up (free plan)
2. Free plan gives you **250 searches/month** (non-commercial use)
3. After email + phone verification, get your API key from the dashboard
4. Store it as an environment variable: `export SERPAPI_KEY=your_key_here`

> **Budget your searches.** At 250/month, you have enough for ~10-15 gaps × 2 queries each, plus retries. Don't waste searches on test queries — test your Boolean syntax in Google Scholar manually first.

### Verify your Task 2 outputs

You need these files from Task 2:
- `gap_results.json` — ranked gaps with VOI scores
- `query_results.json` — AI Citation + Boolean query pairs per gap

---

## Phase 1: Understand the Search & Triage Architecture

### 1A. Understand SerpAPI

SerpAPI scrapes Google Scholar and returns structured JSON. Ask your AI:

> *"Read the SerpAPI Google Scholar documentation. What fields does it return per result? Does it return full abstracts? What about DOIs?"*

**What you should learn:** SerpAPI returns per result:
- `title`, `link`, `snippet` (2-3 sentence fragment, NOT the full abstract)
- `publication_info` (authors, venue, year)
- `inline_links.cited_by.total` (citation count)
- Sometimes a `resource.link` (direct PDF link)
- **It does NOT reliably return DOIs or full abstracts**

So after SerpAPI, you need a second step: look up each paper by title/DOI to get the full abstract.

### 1B. Understand the abstract fallback chain

The Article Eater has working API clients that return abstracts. When SerpAPI gives you a title but no abstract, you try each source in order:

```
SerpAPI result (title + snippet + maybe DOI)
  ↓ extract DOI from link if possible
  1. Semantic Scholar (fetch_by_doi or search by title) → abstract?
  2. CrossRef (fetch by DOI) → abstract?
  3. PubMed (search by title) → abstract?
  4. OpenAlex (api.openalex.org/works/doi:XXX) → abstract?
  5. If ALL fail → tag: MISSING_ABSTRACT
```

Ask your AI:

> *"Read `Article_Eater/src/services/paper_fetcher.py`. Find `SemanticScholarClient`, `CrossRefClient`, and `PubMedClient`. Each has a `search()` method and a `fetch()` or `fetch_by_doi()` method. Show me how I would: (1) take a title from SerpAPI, (2) search Semantic Scholar for it, (3) get the abstract from the result."*

### 1C. Understand the triage logic

After collecting abstracts, you classify each paper:

| Decision | Criteria | What happens |
|---|---|---|
| **ACCEPT** | On-topic (classifier) AND voi_score ≥ 0.5 | Stored in lifecycle DB |
| **EDGE_CASE** | On-topic but voi_score < 0.5, OR borderline topic match | Stored separately, flagged |
| **REJECT** | Off-topic per classifier | Logged but not stored |
| **MISSING_ABSTRACT** | No abstract found from any source | Stored with flag, not triaged |

Ask your AI:

> *"Read `Article_Eater/src/cmr/voi_scoring.py`. Find `score_voi()`. What does it score — the abstract text? The finding type? How does it decide between high (0.8+), medium (0.5-0.8), and low (< 0.5)?"*

---

## Phase 2: Build the Search Runner

### 2A. Write the contract

```markdown
## Search Runner Contract

### Inputs
- Query pairs from Task 2 (query_results.json)
- SerpAPI key (from environment variable SERPAPI_KEY)

### Processing
For each gap (top 10-15 by VOI):
1. Send the Boolean query to SerpAPI's Google Scholar endpoint
2. Collect top 10 results per query
3. Extract: title, snippet, link, publication_info, citation_count
4. Extract DOI from link URL if possible (regex: 10.\d{4,}/.+)
5. De-duplicate by title (fuzzy match)
6. Store raw results as JSON

### Outputs (per search)
- gap_id, query_used, query_type (boolean)
- results: [ { title, snippet, link, doi, authors, year, citations } ]
- result_count, search_timestamp
- serpapi_credits_used

### Success conditions
- At least 5 gaps searched
- Rate limits respected (don't burn all 250 searches)
- Results stored as structured JSON
- Null results recorded (gap searched, zero papers found)
```

### 2B. SerpAPI integration

Ask your AI to build it. Then verify:

> *"Show me the exact SerpAPI call. What engine are you using? What parameters?"*

The call should look like:
```python
import serpapi
params = {
    "engine": "google_scholar",
    "q": your_boolean_query,
    "api_key": os.environ["SERPAPI_KEY"],
    "num": 10
}
results = serpapi.search(params)
```

> *"What happens if a search returns zero results? Do you record it as a null result or skip it?"*

> *"How many API credits does each search cost? How many searches will my pipeline run total? Will I stay under 250?"*

---

## Phase 3: Collect Abstracts

### 3A. Write the abstract collector contract

```markdown
## Abstract Collector Contract

### Inputs
- Search results from the Search Runner (with DOIs where available)

### Processing
For each search result:
1. If DOI available:
   a. Try SemanticScholarClient.fetch_by_doi(doi) → check for abstract
   b. If no abstract: try CrossRefClient.fetch(doi) → check for abstract
   c. If no abstract: try OpenAlex (api.openalex.org/works/doi:XXX)
2. If no DOI:
   a. Try SemanticScholarClient.search(title) → check for abstract
   b. Try PubMedClient.search(title) → check for abstract
3. If all sources fail → tag as MISSING_ABSTRACT
4. Also collect: study_type (from estimate_study_type()), open_access status

### Outputs (per paper)
- title, doi, authors, year, venue
- abstract (full text or null)
- abstract_source (semantic_scholar / crossref / pubmed / openalex / none)
- study_type (rct, experimental, meta_analysis, review, etc.)
- open_access (true/false)

### Success conditions
- Abstract found for ≥ 70% of papers with DOIs
- MISSING_ABSTRACT papers logged (not silently dropped)
- Rate limits respected (Semantic Scholar: ≤ 20 req/min without API key)
```

### 3B. Verification questions

> *"Show me the fallback chain. If Semantic Scholar has no abstract for a DOI, what's the next source you try?"*

> *"How do you handle rate limits? Semantic Scholar throttles to ~20 req/min without an API key. Do you add delays?"*

> *"For papers without DOIs, how do you search by title? What happens if the title match is ambiguous?"*

---

## Phase 4: Triage Abstracts

### 4A. Write the triage contract

```markdown
## Abstract Triage Contract

### Inputs
- Papers with abstracts from the Abstract Collector

### Processing
For each paper with an abstract:
1. Run abstract through atlas_shared classifier:
   - Does this paper match one of Q01-Q30?
   - What topic? What confidence?
2. Score using score_voi() from cmr/voi_scoring.py
3. Classify:
   - ACCEPT: on-topic AND voi_score ≥ 0.5
   - EDGE_CASE: on-topic but voi_score < 0.5, OR borderline topic
   - REJECT: off-topic
   - MISSING_ABSTRACT: no abstract available (skip triage)

### Outputs (per paper)
- triage_decision: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT
- classifier_verdict: { matched_topic, confidence }
- voi_score, voi_bucket (high / medium / low)
- triage_reason: human-readable explanation

### Success conditions
- At least 30 papers triaged
- ACCEPT papers stored in lifecycle DB
- EDGE_CASE papers stored separately with flags
- REJECT and MISSING_ABSTRACT papers logged
```

---

## Phase 5: Build the PRISMA Dashboard

### 5A. Dashboard requirements

Create a web page (`ka_topic_proposer.html` or similar) that shows:

1. **Gap Summary** — how many gaps identified, top 5 by VOI
2. **Search Summary** — how many queries run, how many results returned
3. **Abstract Collection** — how many abstracts found vs. MISSING_ABSTRACT
4. **Triage Results** — ACCEPT / EDGE_CASE / REJECT counts
5. **PRISMA Funnel** — the complete funnel with real numbers
6. **Null Results** — gaps where no papers were found

Data must persist after page refresh (use JSON file, localStorage, or API endpoint).

### 5B. The PRISMA funnel table (required deliverable)

| Funnel Stage | Count |
|---|---|
| Gaps targeted (from Task 2) | |
| Queries executed (SerpAPI) | |
| Records returned | |
| Duplicates removed | |
| Abstracts collected | |
| MISSING_ABSTRACT (no abstract found) | |
| Screened by classifier | |
| → ACCEPT (on-topic, high VOI) | |
| → EDGE_CASE (borderline) | |
| → REJECT (off-topic) | |

---

## Phase 6: Prove It Works

### Step 1: Run the full pipeline

```bash
python3 search_runner.py --queries query_results.json
python3 abstract_collector.py --results search_results.json
python3 abstract_triage.py --papers papers_with_abstracts.json
```

### Step 2: Trace one paper end-to-end

Pick ONE paper that made it through the entire pipeline:

```
Gap source: Template T__ step __ (confidence: 0.__, VOI: 0.__)
  → Boolean query: "_______________"
  → SerpAPI result #__ of __
  → Title: [paper title]
  → DOI: [if found]
  → Abstract source: Semantic Scholar / CrossRef / PubMed / OpenAlex
  → Abstract: [first 100 chars...]
  → Classifier: topic=Q__, confidence=0.__
  → VOI score: 0.__, bucket=high/medium/low
  → Triage: ACCEPT / EDGE_CASE
  → Stored at: [DB entry or file path]
```

### Step 3: Report null results

For high-VOI gaps with zero search results:

```
Gap: Template T__ step __ (VOI: 0.__)
  Description: _______________
  Queries tried: [list]
  Result: NO PAPERS FOUND
  Implication: This gap may be genuinely unfilled in the literature.
```

### Step 4: Report MISSING_ABSTRACT papers

```
Papers with MISSING_ABSTRACT: N out of M total
  Example: [title] — no abstract from any source
  These papers cannot be triaged but are stored for future manual review.
```

---

## What You Submit

| Item | What it is |
|---|---|
| **Search results** | Raw SerpAPI results as JSON |
| **Abstract collection** | Papers with abstracts + source attribution |
| **Triage results** | ACCEPT/EDGE_CASE/REJECT/MISSING_ABSTRACT decisions |
| **PRISMA funnel** | Completed funnel table with real numbers |
| **Dashboard** | Working web page showing pipeline results |
| **End-to-end trace** | One paper from gap → SerpAPI → abstract → triage → store |
| **Null result report** | Gaps where no papers were found |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `search_runner.py` | New | Calls SerpAPI with Boolean queries |
| `abstract_collector.py` | New | Collects abstracts via fallback chain |
| `abstract_triage.py` | New | Runs classifier + VOI on abstracts |
| `search_results.json` | New | Raw SerpAPI results |
| `triage_results.json` | New | Triage decisions with reasons |
| `ka_topic_proposer.html` | New | PRISMA dashboard |
| Database | Modified | New entries for ACCEPT papers |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **SerpAPI integration** | 10 | Successfully queried Google Scholar, got results |
| **Abstract collection** | 15 | Fallback chain works; ≥70% abstract hit rate on DOI papers |
| **Abstract triage** | 15 | Classifier + VOI → defensible ACCEPT/EDGE_CASE/REJECT |
| **PRISMA funnel** | 10 | Dashboard shows real numbers at each stage |
| **End-to-end trace** | 10 | One paper fully traced through pipeline |
| **Null results + MISSING_ABSTRACT** | 5 | Documented, not treated as failures |
| **Verification questions** | 10 | Caught real problems in AI's implementation |

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/paper_fetcher.py` | `SemanticScholarClient.search()` + `fetch_by_doi()` |
| `src/services/paper_fetcher.py` | `CrossRefClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PubMedClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PaperFetcher.search()` — unified multi-source |
| `src/services/paper_fetcher.py` | `estimate_study_type()` — auto from abstract |
| `src/services/paper_fetcher.py` | `UnpaywallClient` — checks OA availability |
| `src/cmr/voi_scoring.py` | `score_voi()` — scores findings by information value |
| `src/services/discovery_funnel.py` | `classify_closure()` — FULL/PARTIAL/NONE/NEGATIVE |
| `atlas_shared` | Topic classifier (from Task 1) |
