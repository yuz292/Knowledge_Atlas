# Track 2: Article Finder — All Tasks

**Track overview:** You will build and run a literature-discovery pipeline for the Knowledge Atlas that follows the PRISMA reporting standard (Preferred Reporting Items for Systematic Reviews and Meta-Analyses — the gold-standard checklist for documenting how you found, screened, and selected papers). You start with a broken contribute page. You wire in a working classifier, pull knowledge gaps from the Article Eater's PNU mechanism templates, turn those gaps into targeted search queries, run the queries through SerpAPI, triage the returned papers at the abstract level, and report every step of the funnel on a dashboard.

**Three tasks, one pipeline:**

| Task | What you build | Points |
|---|---|---|
| Task 1 | Fix the contribute page — wire in the classifier | Graded on diagnosis, spec, fix, and validation |
| Task 2 | Gap targeting — extract gaps, score them by VOI, generate queries | 60 points |
| Task 3 | Search execution — SerpAPI, abstract collection, triage, PRISMA | 75 points |

**Contract gate (all tasks):** Every task requires a written contract that specifies inputs, processing, outputs, success conditions, and a test checklist. A weak contract means weak work; we will flag it as not ready for integration. Tasks 2 and 3 each award 20 bonus points for contract quality.

---

# Task 1: Fix the Contribute Page

**Track:** Article Finder
**What's wrong:** The contribute page accepts PDFs but does nothing with them — no classification, no storage, no feedback to the user.
**Your job:** Repair it so submitted papers get classified, stored in the right place, and reported back to the user.

---

## What This Assignment Teaches

You will use AI to fix a broken page. The point, though, is not the fix — the AI will write the code. The point is the three skills around the AI:

- Can you **diagnose** what is broken by asking your AI the right questions?
- Can you **specify** the fix precisely enough that the AI builds the right thing?
- Can you **verify** that the fix actually works — and catch the silent failures the AI hides from you?

---

## Setup: Clone the Repositories

You need four repositories. All live at [github.com/dkirsh](https://github.com/dkirsh):

```bash
# 1. The Knowledge Atlas site (contains the contribute page you'll fix)
git clone https://github.com/dkirsh/Knowledge_Atlas.git

# 2. The Article Finder pipeline (the discovery half of the system)
git clone https://github.com/dkirsh/Article_Finder.git

# 3. The Article Eater extraction engine (the processing half)
git clone https://github.com/dkirsh/Article_Eater.git

# 4. The shared classifier module (the ID function you'll wire in)
git clone https://github.com/dkirsh/atlas_shared.git
cd atlas_shared && pip install -e . && cd ..
```

Confirm `atlas_shared` installed cleanly:
```bash
python3 -c "from atlas_shared.classifier_system import AdaptiveClassifierSubsystem; print('OK')"
```

---

## Phase 1: Diagnose — What's Broken?

Before you can connect two programs, you have to understand both. This phase walks you through each one separately, then asks you to name the gap between them.

### 1A. Ask your AI to explain the contribute page

Open `Knowledge_Atlas/ka_contribute_public.html`. Hand the full source to your AI and ask:

> *"Walk me through exactly what happens when a user drops a PDF and clicks 'Send suggestion.' For each step, tell me: what function runs, what data is created, and where it goes. Then tell me everything that is MISSING that a working version would need."*

Then ask:

> *"Draw a box-and-arrow diagram showing the data flow. Label every missing component."*

**Your deliverable:** A boxology diagram and a short "Current State" paragraph describing what the page does and does not do.

### 1B. Ask your AI to explain the classifier

Now do the same for the classifier. Open `atlas_shared/src/atlas_shared/classifier_system.py`, give it to your AI, and ask:

> *"This is the classifier for the Knowledge Atlas. Explain two things:*
> 1. *How does it decide what TYPE of article a PDF is? (empirical, review, theoretical, etc.)*
> 2. *How does it decide what TOPIC a paper belongs to? (daylight + cognition, ceiling height + creativity, etc.)*
>
> *For each, tell me the class name, the method, and what data it looks at. Then draw a box-and-arrow diagram showing what happens inside `classify()`."*

**Your deliverable:** A boxology diagram of the classifier's internal steps.

### 1C. Name the gap between them

You now have two diagrams: one of what the contribute page does, one of what the classifier does. The gap between them is your assignment.

> *Ask your AI: "Given these two programs, what would I need to build to connect them? Be specific — what endpoint, what data transformations, what storage?"*

> *Also ask: "Are there any existing files in the Knowledge Atlas repo that already handle article submission? Search for files with 'article' or 'submit' in their names."*

This second question is critical. The repo already contains partial infrastructure, and your AI should find it. Make the AI tell you what is already built so you do not redo it.

**Your deliverable:** A one-paragraph gap statement of the form: "The contribute page currently does X. The classifier can do Y. The existing backend already does Z. To finish the integration, we need W."

---

## Phase 2: Spec — Write the Contract

A contract is the spec you write before any code is written. It tells the AI — and the grader — what "done" means. Write a contract called the **Classifier Integration Contract** that nails down:

- **Inputs:** What the user provides (PDF, citation, or both)
- **Processing:** What the backend does with it (build the evidence object, call the classifier)
- **Outputs on the page:** For each submitted paper, the user sees in a results section:
  - The verdict — **accepted**, **edge case**, or **rejected**
  - The article type
  - The topic(s) it matches
  - The classifier's confidence score
- **Storage rules:**
  - Accepted papers — store both the PDF and a database entry
  - Edge-case papers — store, but flag as edge cases
  - Rejected papers — show in the results panel but do NOT store
- **Success conditions:** At least three specific test cases with expected outcomes

### Check for duplicates before you store

Do not let the page store a paper that is already in the corpus. We give you a foolproof probe that works even on hard-to-read PDFs:

```bash
python3 /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/scripts/course_scaffolding.py \
  probe-collection-pdf --pdf-path /absolute/path/to/file.pdf
```

**How to read the result:**
- `sha256_exact` or `doi_exact` → **The file is already in the corpus. Do not re-ingest it.**
- `title_fuzzy` or `page_text_match` → Possible duplicate. Inspect by hand before deciding.
- No match → Safe to store as a new paper.

If you are calling this from inside Article Finder code rather than from the shell, use the function `probe_pdf_against_article_eater(...)` in `ae_waiting_room_probe.py`.

Your contract's storage rules must include this check. A submission flow that stores duplicates is a bug.

### Ask your AI about storage layout

You also need to know where the PDFs live and where the database entries live. Ask:

> *"In the Knowledge Atlas project, where are article PDFs stored? There is a lifecycle database (a SQLite database that tracks every paper's stage in the pipeline) — what tables does it have, and what should a new paper's entry look like when it first arrives? Show me the schema."*

> *"The pipeline has defined stages. What is the first stage a newly contributed paper should be at? What status should it have?"*

Do not take the AI's answer on faith. Open the database yourself and verify:

```bash
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema papers"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema lifecycle_events"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db "SELECT stage_name, stage_order FROM stage_definitions ORDER BY stage_order;"
```

**Your deliverable:** The completed contract with concrete storage paths, database column values, and duplicate-check logic filled in.

---

## Phase 3: Fix — Delegate to Your AI

Now hand the work to the AI. Give it:
1. Your contract
2. The source of `ka_contribute_public.html`
3. The source of `classifier_system.py`
4. Any existing backend files your AI surfaced in Phase 1C

Ask it to build:
1. A backend endpoint that receives the form submission and runs the classifier
2. A results section on the contribute page that displays the classifier's verdict
3. Storage logic for accepted and edge-case papers

### Verification questions you must ask before you trust the code

When the AI hands you code, do not just run it. Interrogate it first. These questions catch the failures the AI will not volunteer:

> *"Show me exactly where in your code the PDF file gets saved to disk. What path does it use? What happens if that directory does not exist?"*

> *"Show me the line where you call `AdaptiveClassifierSubsystem.classify()`. What are you passing in as the `evidence_like` argument? Walk me through which fields of ClassificationEvidence get populated from the user's submission."*

> *"Show me where you write to the database. Which table? What values go in each column? What happens if the paper_id already exists?"*

> *"What happens when the classifier returns `next_action = 'need_abstract_or_keywords'`? Does your code handle that case, or does it silently ignore it?"*

> *"How do you distinguish an accepted paper from an edge case in storage? Show me the exact field or flag."*

> *"If I submit five PDFs in one session, does the results section show all five? Or does each new submission overwrite the previous one?"*

If the AI cannot answer any of these clearly, the fix is incomplete. Push back.

**Your deliverable:** The working code, plus a log of which verification questions surfaced problems and how you fixed each one.

---

## Phase 4: Prove — Run the Tests

A spec is worthless without execution proof. This phase produces the evidence that the system actually works.

### Prepare test papers

Get at least four PDFs:
1. A known on-topic empirical paper (one already in the Atlas works well)
2. A clearly off-topic paper (a machine-learning paper, for example)
3. An edge case (an architectural-theory paper with no empirical data)
4. A citation-only submission (no PDF attached)

### Run each test and record the result

| Test | Input | Expected verdict | Actual verdict | Expected type | Actual type | Stored? | DB entry? | PASS? |
|------|-------|-----------------|----------------|---------------|-------------|---------|-----------|-------|
| 1 | On-topic PDF | accept | | empirical | | yes | yes | |
| 2 | Off-topic PDF | reject | | — | | no | no | |
| 3 | Edge-case PDF | edge_case | | theoretical | | yes (flagged) | yes | |
| 4 | Citation only | varies | | varies | | — | — | |

### Verify storage

For every paper that should be stored, check both the file system and the database:

```bash
# Does the PDF file exist?
ls -la <expected_path>

# Does the database entry exist?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, article_type, current_stage, current_status FROM papers WHERE paper_id='<id>';"

# Is there a lifecycle event?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT stage_name, status, agent FROM lifecycle_events WHERE paper_id='<id>';"

# Is the edge case distinguishable from the accepted paper?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, current_status FROM papers ORDER BY created_at DESC LIMIT 5;"
```

### When a test fails — diagnose where the bug lives

For each failure, decide: **is the spec wrong, or is the AI's implementation wrong?**

- If the classifier returns the wrong verdict, the spec may be right but the constitution data may not yet cover the topic. That is a classifier issue, not your bug.
- If the classifier returns the right verdict but the page does not show it, the AI's code has a rendering bug. That IS your bug.
- If the PDF lands on disk but the database entry never appears, the AI's code has a storage bug. That IS your bug.

**Your deliverable:** The completed validation matrix, plus a diagnosis note for any failure that explains whether it was a spec bug or an implementation bug.

---

## What You Submit

| Item | Description and Format |
|------|-----------|
| **Boxology diagrams** (Phase 1) | Two diagrams: the contribute page data flow, and the classifier's internal steps |
| **Gap statement** (Phase 1) | One paragraph: what exists, what the classifier does, what is missing |
| **Classifier Integration Contract** (Phase 2) | Your spec with inputs, outputs, storage, and success conditions |
| **Working code** (Phase 3) | The fixed contribute page, endpoint, and storage logic |
| **Verification log** (Phase 3) | The questions you asked your AI, which ones surfaced problems, how you fixed them |
| **Validation matrix** (Phase 4) | Test results for all four (or more) test cases |
| **Storage proof** (Phase 4) | Terminal output showing the PDF exists and the DB entries are correct |
| **Diagnosis notes** (Phase 4) | For any failure: spec bug or implementation bug? |

---

## Files You Must Submit

Your submission must include a **file manifest** that lists every file you changed or created with a one-line description. The instructor will diff your repo against the upstream to verify.

These are the minimum expected files; your list may include more:

| File | Change Type | What It Does |
|------|------------|-------------|
| `ka_contribute_public.html` | Modified | Form now posts to a real endpoint; results section sits below the form |
| Backend endpoint file (e.g., added to `ka_article_endpoints.py` or a new file) | Modified or New | Receives the form submission, runs the `atlas_shared` classifier, returns a JSON result |
| `data/storage/` or `data/pnu_articles/` | New files | Stored PDFs for accepted and edge-case papers |
| Database (e.g., `data/ka_auth.db` or `pipeline_lifecycle_full.db`) | Modified | New rows for submitted papers |

**How to generate your manifest:**
```bash
cd Knowledge_Atlas
git diff --name-only HEAD    # files you changed
git status --short           # new files
```

Include the output of both commands in your submission.

---

## Grading

| Criterion | What we check |
|-----------|--------------|
| **Diagnosis** | Your boxology diagrams are accurate; your gap statement is correct |
| **Spec quality** | Your contract is complete, specific, and testable |
| **Verification questions** | You asked probing questions that caught real problems in the AI's code |
| **Validation** | At least three of four test papers produce correct results and storage |
| **Diagnosis of failures** | You correctly identified whether each failure was a spec bug or an implementation bug |
| **File manifest** | Your manifest is complete and matches your actual changes |
---

# Task 2: Gap Targeting & Query Generation

**Track:** Article Finder
**What you build:** A gap extractor that reads the Article Eater's 166 PNU templates, finds the knowledge gaps inside them, scores those gaps by Value of Information (VOI — a measure of how much filling the gap would change the system's beliefs), and writes targeted search queries in two formats: Google AI Citation (natural language) and Google Scholar Boolean.
**Core lesson:** Before you search for anything, you have to know *what* you are looking for and *why*. VOI scoring tells you which gaps matter most. Query design decides whether you find relevant papers or noise.

---

## Setup

You should already have the four repositories from Task 1:
- `Knowledge_Atlas` — the site (with your fixed contribute page)
- `Article_Finder` — the discovery pipeline
- `Article_Eater` — the extraction engine (it holds both the gap data and the VOI functions)
- `atlas_shared` — the shared classifier (installed via `pip install -e .`)

---

## Phase 1: Understand the Gap Data and the VOI System

Before you build anything, you need to understand the raw material — what a PNU template looks like, what VOI measures, and what the corpus already contains. Skip this phase and your queries will hunt for papers we already have.

### 1A. Understand the PNU templates

The Article Eater holds 166 PNU (Plausible Neural Underpinning) templates. Each template describes a mechanism chain — how an environmental feature (say, ceiling height) produces a psychological outcome (say, creativity) through a series of neural processes. Every step in that chain has a **confidence score**. A low-confidence step is a **knowledge gap**: a place in the chain where the literature has not yet pinned down the mechanism.

Pick three templates from `Article_Eater/data/templates/` and ask your AI:

> *"These are PNU templates from the Knowledge Atlas. Walk me through one template completely: what does each step in the `mechanism_chain` represent, what does `confidence` mean for each step, and what does a low-confidence step (< 0.6) tell us about what is missing from the research corpus?"*

> *"Now look at all three templates and identify: which steps have confidence below 0.6? For each gap, tell me what specific study would fill it."*

### 1B. Understand the VOI scoring system

Value of Information is the lever you use to rank gaps. The Article Eater already supplies a `VOICalculator` for this; you will call it. Ask your AI:

> *"Read `Article_Eater/src/services/voi_search.py`. Find `VOICalculator` and its `calculate_voi()` method. What inputs does it take? What does the combined VOI score mean? When would a gap get a HIGH score vs. a LOW score?"*

**What you should learn:** A gap that sits at a hub in the belief network — high centrality, many downstream beliefs that depend on it — with confidence near 0.4 scores far higher in VOI than an isolated gap with confidence 0.45. VOI answers the question: "how much would knowing this change our predictions?"

### 1C. Know what is already in the corpus

Before you generate a single search query, find out what we already have. Searching for papers we already own wastes API credits and pollutes the funnel.

The lifecycle database tracks every PDF in the system.

**Primary source:** `pipeline_lifecycle_full.db`, table `pdf_corpus_inventory`

This table lists every known PDF and its state:
- Whether it is in `CURRENT_GOLD` (fully processed and validated)
- Whether it is admitted but not yet gold
- Whether it is staged only
- Whether it is registry-backed

**Easiest readable version:** `pdf_corpus_inventory/latest.csv`

The summary report is at `pdf_corpus_inventory/latest.md`.

Ask your AI:

> *"Read `pdf_corpus_inventory/latest.csv`. How many papers are in CURRENT_GOLD? What topics do they cover? This tells me what we already have — I should NOT generate search queries for papers that are already in the corpus."*

If you also need to catch the same paper appearing under different filenames or DOIs, use the companion table:

**Dedupe source:** `pipeline_lifecycle_full.db`, table `pdf_identity_inventory`
**CSV:** `pdf_identity_inventory/latest.csv`

### 1D. Understand the two query types

You will write queries in two formats, and they answer different questions. Read `160sp/ka_google_search_guide.html` for the full tutorial, then ask your AI:

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

The differences in plain terms:
- **AI Citation** uses full sentences with theory names and mechanism descriptions. Google's AI handles synonyms and intent for you.
- **Boolean** uses exact keywords joined by AND/OR with quotes around phrases. Add `-review` to exclude review articles when you want primary research. Use `intitle:` to require that a term appear in the title.

### 1E. Get a boxology diagram of the full pipeline

> *"Draw a box-and-arrow diagram of this complete pipeline (Tasks 2 and 3 combined):*
> 1. *Read PNU templates → extract gaps with confidence < 0.5*
> 2. *Score gaps using VOICalculator → sort by priority*
> 3. *Generate search queries (AI Citation + Boolean)*
> 4. *Execute searches via SerpAPI → get titles, snippets, DOIs*
> 5. *Collect full abstracts via Semantic Scholar / CrossRef / PubMed / OpenAlex*
> 6. *Triage abstracts through classifier + VOI scoring*
> 7. *Classify papers: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT*
> 8. *Display PRISMA funnel on dashboard"*

**Your deliverable:** The boxology diagram, plus a list of five specific gaps with their confidence scores.

---

## Phase 2: Build the Gap Extractor

The gap extractor turns 166 templates into a ranked, machine-readable list of knowledge gaps. It is the input to everything downstream.

### 2A. Write YOUR OWN contract

> **Contract objective:** "I want a program that reads PNU template JSON files and tells me which knowledge gaps are most worth searching for."
> **Contract is with:** The `VOICalculator` in `Article_Eater/src/services/voi_search.py` and the PNU templates in `Article_Eater/data/templates/`.
> **Prompt hint:** *"I need to write a contract for a gap extraction program. The program reads PNU template JSON files, walks their mechanism_chain, and uses VOICalculator.calculate_voi() to score each gap. Help me write the Inputs, Processing, Outputs, and Success Conditions sections."*

Write the contract yourself before you ask any AI to build anything. This is the most important habit in the course: **if you cannot specify what you want, you cannot verify what you got.**

Your contract must have these four sections:

1. **Inputs** — Which files does the program read? In what format?
2. **Processing** — What does the program do, step by step?
3. **Outputs** — What does the program produce? Which fields, in what format?
4. **Success conditions** — How will you know it worked? Be specific. "It works" is not a success condition. "Extracts at least 10 gaps across 166 templates, each with template_id, step_number, confidence < 0.6, and gap_type" IS a success condition.

**Minimum bar** — your contract must cover at least these:
- Reads PNU template JSON files and walks `mechanism_chain`
- Extracts steps whose confidence falls below a threshold you set
- Scores each gap with `VOICalculator.calculate_voi()`
- Writes structured JSON with gap_type, voi_score, and what is missing

### 2B. Write your tests BEFORE you build

A test is a sentence about what the program must do, written before the program exists. Ask your AI:

> *"Given my contract, what are 5 things that could go wrong? For each, write a test I can run to check. For example: 'What if a template has no mechanism_chain field?'"*

Write your tests as a checklist:
- [ ] Handles templates with no low-confidence steps (skips them, does not crash)
- [ ] VOI scores fall between 0 and 1
- [ ] Output JSON is valid and parseable
- [ ] At least 10 gaps found (if fewer, is the threshold wrong?)
- [ ] Gaps sorted by VOI, highest first

### 2C. Delegate to your AI, then validate

Hand the AI your contract and ask it to build a Python script. Then run your tests and interrogate the result:

> *"Show me how you read the mechanism_chain from a template. Which field has the confidence? What threshold do you use?"*

> *"Show me the VOI scores for 3 gaps. Why does one score higher than another?"*

> *"Run the script on 3 templates. Does the output match my contract's output spec? Show me the JSON."*

---

## Phase 3: Generate Search Queries

A ranked gap list is useless without queries to chase the gaps. This phase turns each gap into a matched pair of search queries — one natural-language and one Boolean — ready for Task 3 to execute.

### 3A. Write YOUR OWN query-generator contract

> **Contract objective:** "I want a program that takes my ranked gap list and generates search queries I can use to find papers that fill those gaps."
> **Contract is with:** The `QueryGenerator` in `Article_Eater/src/services/voi_search.py` and the patterns in `ka_google_search_guide.html`.
> **Prompt hint:** *"I need to write a contract for a query generator. It takes a JSON list of knowledge gaps (with VOI scores) and produces two search queries per gap: a Google AI Citation natural-language query and a Google Scholar Boolean query. Help me write the contract."*

Same discipline as Phase 2: **you** write the contract. Cover:
1. **Inputs** — the gap list from Phase 2
2. **Processing** — how queries are generated (refer to `ka_google_search_guide.html`)
3. **Outputs** — what fields each gap carries (both query types plus a gap summary)
4. **Success conditions** — at minimum:
   - At least 10 gaps carry both an AI Citation and a Boolean query
   - AI Citation queries are full sentences that follow the 5-component pattern
   - Boolean queries use `"exact phrases"`, `AND`, `OR`, and `-review`
   - At least three queries have been tested manually in Google and produce relevant first-page results

### 3B. Write your validation tests

> *"What makes a bad Boolean query? Give me 3 examples of common mistakes and how to detect them automatically."*

Your validation checklist:
- [ ] No Boolean query is a bare comma-separated word list (it must contain AND/OR)
- [ ] Every AI Citation query ends with `?` and runs longer than 50 characters
- [ ] Every Boolean query contains at least one `"exact phrase"`
- [ ] At least three queries return relevant results when tested in Google

### 3C. Use the query-generation prompt template

We supply a prompt template designed to produce high-quality queries. See `query_generator_skill.md` in this rubrics folder.

> *Give your AI the prompt template along with three gaps from your extractor. Ask it to generate queries. Then test one AI Citation query in Google by hand — does the first page of results contain relevant papers?*

### 3D. Verification questions

> *"Show me the Boolean query for one gap. Does it use exact-phrase quotes? Does it have OR groups for synonyms? Would Google Scholar parse it correctly?"*

> *"Show me the AI Citation query for the same gap. Does it follow the 5-component pattern? Could a researcher read it as a real research question?"*

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
- [ ] Each gap carries template_id, step number, confidence, gap_type, voi_score

### Step 2: Generate queries for the top 10 gaps

```bash
python3 query_generator.py --gaps gap_results.json
```

Verify:
- [ ] Each gap carries both an AI Citation and a Boolean query
- [ ] AI Citation queries are full sentences, not keyword lists
- [ ] Boolean queries use AND/OR/quotes properly

### Step 3: Manual spot-check

Pick three queries and paste the AI Citation version into Google. For each:

| Gap | Query (first 50 chars) | First-page relevant? | Top result title |
|-----|----------------------|---------------------|-----------------|
| 1 | | Yes / No / Partial | |
| 2 | | | |
| 3 | | | |

### Step 4: Review your query quality

> *Ask your AI: "Review these 10 queries against the patterns in ka_google_search_guide.html. Which queries are strong? Which are weak? How would you improve the weak ones?"*

**Your deliverable:** Gap list, query pairs, the spot-check table, and the AI's review of query quality.

---

## What You Submit

| Item | Description and Format |
|---|---|
| **Gap analysis** (Phase 1) | Boxology diagram plus five gaps with VOI scores |
| **Gap extractor** (Phase 2) | Working script plus contract |
| **Query pairs** (Phase 3) | Ten or more gaps with AI Citation + Boolean queries |
| **Spot-check** (Phase 4) | Manual test of three queries in Google |
| **Query review** (Phase 4) | AI review of query quality |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `gap_extractor.py` | New | Reads templates, extracts gaps, scores them by VOI |
| `query_generator.py` | New | Generates AI Citation + Boolean queries per gap |
| `gap_results.json` | New | Ranked gap list with VOI scores |
| `query_results.json` | New | Query pairs for each gap |

---

## Grading (60 points)

| Criterion | Points | What we check |
|---|---|---|
| **Gap extraction** | 15 | Correctly identifies low-confidence steps from templates |
| **VOI scoring** | 10 | Gaps ranked by VOI; you can explain why one scores higher |
| **AI Citation queries** | 10 | Follow the 5-component pattern, specific enough for retrieval |
| **Boolean queries** | 10 | Proper AND/OR/quotes, not just comma-separated words |
| **Spot-check** | 5 | Three queries tested manually in Google, results reported |
| **Verification questions** | 10 | Caught real problems in the AI's implementation |

---

## A Note About Reuse

The contract → success conditions → test → validate workflow you are practicing here is not a one-off exercise. **You will reuse it directly in Task 3,** where you execute searches and triage results through a PRISMA funnel, and in every later task that touches the corpus. In particular, the PRISMA funnel becomes a recurring deliverable: any time you add papers to the corpus, you must show the funnel as proof that you did so rigorously. Treat this Task 2 contract as a template you will refine, not a throwaway.

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/voi_search.py` | `VOICalculator.calculate_voi()` — scores gaps |
| `src/services/voi_search.py` | `QueryGenerator.generate_queries()` — baseline query generation |
| `src/services/voi_search.py` | `CrossFieldVocabulary.expand_query()` — cross-discipline synonyms |
| `pipeline_lifecycle_full.db` | Table `pdf_corpus_inventory` — every PDF and its state (CURRENT_GOLD, staged, etc.) |
| `pdf_corpus_inventory/latest.csv` | Readable export of the corpus inventory — check what you already have |
| `pdf_identity_inventory/latest.csv` | Dedupe info — catches the same paper under different filenames |
| `course_scaffolding.py probe-collection-pdf` | Foolproof duplicate check — run on any PDF to see if it is already in the corpus |
| `ae_waiting_room_probe.py` | `probe_pdf_against_article_eater()` — the same check, callable from Python |
| `build_pdf_corpus_inventory_surface.py` | Builds the inventory surface from the lifecycle DB |
| `refresh_v7_state_surfaces.py` | Regenerates all state surfaces (run this to get fresh data) |
| `160sp/ka_google_search_guide.html` | Full tutorial on writing AI Citation queries |
| `query_generator_skill.md` | Prompt template for generating queries from gaps |
---

# Task 3: Search Execution & Abstract-First Triage

**Track:** Article Finder
**Prerequisite:** Task 2 (you need your ranked gap list and query pairs)
**What you build:** Run your search queries through SerpAPI (which scrapes Google Scholar), collect each paper's abstract through a fallback chain of free academic APIs, decide at the abstract level whether each paper is worth keeping, and report the whole funnel on a PRISMA-style dashboard.
**Core lesson:** Never download a PDF to decide whether it is relevant. Triage at the cheapest level — abstracts — using free APIs. Then prove the pipeline works with real PRISMA funnel numbers.

---

## What PRISMA Is and Why You Are Building One

PRISMA (**Preferred Reporting Items for Systematic Reviews and Meta-Analyses**) is the gold-standard reporting checklist for systematic literature searches. It forces you to document your funnel transparently — every paper that came in, every paper that fell out, and the reason for each removal:

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

Your dashboard must show these numbers. They are the proof that your pipeline works.

---

## Setup

### Get your SerpAPI key

1. Go to [serpapi.com](https://serpapi.com) and sign up (free plan).
2. The free plan gives you **250 searches per month** for non-commercial use.
3. After email and phone verification, copy your API key from the dashboard.
4. Store it as an environment variable: `export SERPAPI_KEY=your_key_here`

> **Budget your searches.** At 250 per month, you have enough for roughly 10–15 gaps × 2 queries each, plus retries. Do not waste credits on test queries — debug your Boolean syntax in Google Scholar manually first.

### Verify your Task 2 outputs

You need these files from Task 2:
- `gap_results.json` — ranked gaps with VOI scores
- `query_results.json` — AI Citation + Boolean query pairs per gap

---

## Phase 1: Understand the Search & Triage Architecture

Four pieces have to fit together: SerpAPI to find papers, an abstract fallback chain to enrich them, the triage logic to classify them, and a deduplication check to skip what we already have. This phase walks you through each piece before you start building.

### 1A. Understand SerpAPI

SerpAPI scrapes Google Scholar and returns the results as structured JSON. Ask your AI:

> *"Read the SerpAPI Google Scholar documentation. What fields does it return per result? Does it return full abstracts? What about DOIs?"*

**What you should learn:** Each SerpAPI result gives you:
- `title`, `link`, `snippet` (a 2–3-sentence fragment, NOT the full abstract)
- `publication_info` (authors, venue, year)
- `inline_links.cited_by.total` (citation count)
- Sometimes a `resource.link` (a direct PDF link)
- **It does NOT reliably return DOIs or full abstracts**

So SerpAPI gets you only halfway. You then need a second step that looks each paper up by title or DOI to fetch the full abstract.

### 1B. Understand the abstract fallback chain

The Article Eater ships with working API clients for the major free abstract sources. When SerpAPI hands you a title but no abstract, you try each source in order:

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

Once you have abstracts, you classify each paper into one of five buckets:

| Decision | Criteria | What happens |
|---|---|---|
| **ACCEPT** | On-topic (per the classifier) AND voi_score ≥ 0.5 | Stored in lifecycle DB |
| **EDGE_CASE** | On-topic but voi_score < 0.5, OR a borderline topic match | Stored separately and flagged |
| **REJECT** | Off-topic per the classifier | Logged but not stored |
| **MISSING_ABSTRACT** | No abstract found from any source | Stored with a flag, not triaged |
| **DUPLICATE** | Already in `pdf_corpus_inventory` | Counted in the PRISMA funnel, not re-triaged |

Ask your AI:

> *"Read `Article_Eater/src/cmr/voi_scoring.py`. Find `score_voi()`. What does it score — the abstract text? The finding type? How does it decide between high (0.8+), medium (0.5–0.8), and low (< 0.5)?"*

### 1D. Know what is already in the corpus (deduplication)

Before you triage a paper, check whether it is already in the corpus. You met this probe in Task 1; here it does the same job for a different reason. In Task 1 you used it to stop the contribute page from re-storing a duplicate. In Task 3 you use it to mark search hits as `DUPLICATE` so they show up in the right slot of the PRISMA funnel rather than getting re-processed.

The lifecycle database tracks every PDF in the system.

**Primary source:** `pipeline_lifecycle_full.db`, table `pdf_corpus_inventory`
**Easiest readable version:** `pdf_corpus_inventory/latest.csv`

This table tells you whether a paper sits in `CURRENT_GOLD` (already processed), is admitted, or is staged. If a search result matches a paper already in the inventory, mark it `DUPLICATE` in your PRISMA funnel — it counts as "identified" but is removed at the deduplication stage.

For matching by DOI or title, use the companion table:

**Dedupe source:** `pipeline_lifecycle_full.db`, table `pdf_identity_inventory`
**CSV:** `pdf_identity_inventory/latest.csv`

### Foolproof duplicate check (use this)

If you have a PDF in hand and want to know whether it is already anywhere in the pipeline or corpus, run the probe tool — the same one you used in Task 1:

```bash
python3 /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/scripts/course_scaffolding.py \
  probe-collection-pdf --pdf-path /absolute/path/to/file.pdf
```

**How to read the result:**
- `sha256_exact` or `doi_exact` → **Existing duplicate. Do not re-ingest.**
- `title_fuzzy` or `page_text_match` → Possible duplicate. Inspect by hand before deciding.
- No match → New paper, safe to triage and store.

If you are calling this from inside Article Finder code rather than from the shell, use `probe_pdf_against_article_eater(...)` in `ae_waiting_room_probe.py`. The test that proves this works is `test_cataloger_skips_article_eater_duplicate_before_db_insert` in `test_import.py`.

To refresh the inventory tables before you start:
```bash
python refresh_v7_state_surfaces.py
```

---

## Phase 2: Build the Search Runner

The search runner is the first executable stage of the Task 3 pipeline. It takes the query pairs from Task 2 and turns them into raw SerpAPI results.

### 2A. Write YOUR OWN search-runner contract

> **Contract objective:** "I want a program that takes my search queries and runs them against Google Scholar via SerpAPI, collecting structured results."
> **Contract is with:** The SerpAPI `google_scholar` engine and your query pairs from Task 2.
> **Prompt hint:** *"I need a contract for a search runner that sends Boolean queries to SerpAPI's Google Scholar endpoint, extracts DOIs from result URLs, de-duplicates by title, and records null results. Help me write Inputs, Processing, Outputs, and Success Conditions."*

Same discipline as Task 2: **you** write the contract, with Inputs, Processing, Outputs, and Success Conditions.

**Minimum bar** your contract must cover:
- Takes the query pairs from Task 2 as input
- Sends Boolean queries to SerpAPI's `google_scholar` engine
- Extracts a DOI from each result URL where possible
- De-duplicates by title
- Records null results (gap searched, zero papers found)
- Tracks API credit usage

### 2B. Write your tests BEFORE you build

Your test checklist:
- [ ] SerpAPI call uses `engine: google_scholar` (not regular Google)
- [ ] Each search costs exactly one credit (verify in the SerpAPI dashboard)
- [ ] Total searches stay under 250
- [ ] Zero-result searches are recorded, not skipped
- [ ] Output JSON is valid and parseable
- [ ] DOI extraction regex works on three sample URLs

### 2C. Build and validate

Ask your AI to build it. The SerpAPI call should look like this:
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

Then run your tests and interrogate the result:

> *"Show me the exact SerpAPI call. What engine are you using? What parameters?"*

> *"How many API credits does each search cost? How many searches will my pipeline run total? Will I stay under 250?"*

---

## Phase 3: Collect Abstracts

SerpAPI hands you titles and snippets. To triage, you need full abstracts. This phase walks each result through the fallback chain until a real abstract appears — or until every source comes up empty and you tag the paper MISSING_ABSTRACT.

### 3A. Write YOUR OWN abstract-collector contract

> **Contract objective:** "I want a program that takes SerpAPI results (which have snippets, not abstracts) and finds the full abstract for each paper from free academic APIs."
> **Contract is with:** The `SemanticScholarClient`, `CrossRefClient`, `PubMedClient` in `Article_Eater/src/services/paper_fetcher.py`, and the OpenAlex API.
> **Prompt hint:** *"I need a contract for an abstract collector. It takes search results with DOIs and tries to find full abstracts from Semantic Scholar, CrossRef, PubMed, and OpenAlex in fallback order. Papers with no abstract from any source get tagged MISSING_ABSTRACT. Help me write the contract."*

**Minimum bar** your contract must cover:
- Takes SerpAPI results as input (with DOIs where available)
- Tries multiple abstract sources in fallback order (S2 → CrossRef → PubMed → OpenAlex)
- For papers without DOIs, falls back to title-based search
- Tags papers with no abstract as `MISSING_ABSTRACT` (does not silently drop them)
- Records which source supplied the abstract
- Respects rate limits (Semantic Scholar: ≤ 20 req/min without an API key)

**Success conditions you must define:**
- What abstract hit rate is acceptable? (Aim for ≥ 70 percent on papers with DOIs.)
- What counts as a "found" abstract versus a snippet?
- How do you handle ambiguous title matches?

### 3B. Write your tests BEFORE you build

- [ ] Fallback chain actually tries multiple sources, not just Semantic Scholar
- [ ] Rate-limiting delays are present (look for `time.sleep` or `_RateLimiter`)
- [ ] MISSING_ABSTRACT count is tracked and reported
- [ ] Each paper's `abstract_source` field is set correctly
- [ ] Output includes `study_type` from `estimate_study_type()`

### 3C. Build and validate

> *"Show me the fallback chain. If Semantic Scholar has no abstract for a DOI, what is the next source you try?"*

> *"How do you handle rate limits? Do you add delays between API calls?"*

> *"For papers without DOIs, how do you search by title? What happens if the title match is ambiguous?"*

---

## Phase 4: Triage Abstracts

With abstracts in hand, the pipeline can finally make decisions. Triage is the choke point: it converts a long list of candidate papers into a short list of papers worth downloading.

### 4A. Write YOUR OWN triage contract

> **Contract objective:** "I want a program that reads each paper's abstract and decides: is this paper worth downloading?"
> **Contract is with:** The `atlas_shared` classifier (from Task 1) and `score_voi()` from `Article_Eater/src/cmr/voi_scoring.py`.
> **Prompt hint:** *"I need a contract for an abstract triage module. It runs each abstract through the atlas_shared topic classifier, then scores it with score_voi(). Output is a 4-way classification: ACCEPT, EDGE_CASE, REJECT, or MISSING_ABSTRACT, each with a human-readable reason. Help me write the contract."*

**Minimum bar** your contract must cover:
- Runs each abstract through the `atlas_shared` classifier (topic matching)
- Scores each abstract with `score_voi()` from `cmr/voi_scoring.py`
- Produces a four-way classification: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT
- Attaches a human-readable `triage_reason` to every decision
- Stores ACCEPT papers in the lifecycle DB; stores EDGE_CASE separately

**Success conditions you must define:**
- What is the minimum number of papers triaged?
- What classifier confidence threshold separates on-topic from off-topic?
- What VOI threshold separates ACCEPT from EDGE_CASE?

### 4B. Write your tests BEFORE you build

- [ ] Every triaged paper carries a `triage_decision` field
- [ ] Every triaged paper carries a `triage_reason` (never empty)
- [ ] ACCEPT papers appear in the database
- [ ] EDGE_CASE papers are stored but flagged
- [ ] REJECT papers are logged, not silently dropped
- [ ] MISSING_ABSTRACT papers skip triage rather than getting scored as REJECT

---

## Phase 5: Build the PRISMA Dashboard

The dashboard is the public face of your pipeline. It collects every count along the funnel and shows them in one place, so a reader can see — at a glance — how many papers entered, how many fell out at each stage, and why.

### 5A. Dashboard requirements

Build a web page (`ka_topic_proposer.html` or similar) that shows:

1. **Gap Summary** — how many gaps were identified, top five by VOI
2. **Search Summary** — how many queries ran, how many results came back
3. **Abstract Collection** — how many abstracts were found vs. tagged MISSING_ABSTRACT
4. **Triage Results** — ACCEPT / EDGE_CASE / REJECT counts
5. **PRISMA Funnel** — the complete funnel with real numbers
6. **Null Results** — gaps for which no papers were found

Data must persist after a page refresh (use a JSON file, localStorage, or an API endpoint).

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

Pick ONE paper that made it through the entire pipeline and trace its journey:

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

For high-VOI gaps that returned zero search results, write up each one:

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

| Item | Description and Format |
|---|---|
| **Search results** | Raw SerpAPI results as JSON |
| **Abstract collection** | Papers with abstracts plus source attribution |
| **Triage results** | ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT decisions |
| **PRISMA funnel** | Completed funnel table with real numbers |
| **Dashboard** | Working web page showing pipeline results |
| **End-to-end trace** | One paper traced from gap → SerpAPI → abstract → triage → store |
| **Null result report** | Gaps for which no papers were found |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `search_runner.py` | New | Calls SerpAPI with Boolean queries |
| `abstract_collector.py` | New | Collects abstracts via the fallback chain |
| `abstract_triage.py` | New | Runs the classifier + VOI on abstracts |
| `search_results.json` | New | Raw SerpAPI results |
| `triage_results.json` | New | Triage decisions with reasons |
| `ka_topic_proposer.html` | New | PRISMA dashboard |
| Database | Modified | New entries for ACCEPT papers |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **SerpAPI integration** | 10 | Successfully queried Google Scholar, got results back |
| **Abstract collection** | 15 | Fallback chain works; ≥ 70 percent abstract hit rate on DOI papers |
| **Abstract triage** | 15 | Classifier + VOI yield defensible ACCEPT/EDGE_CASE/REJECT decisions |
| **PRISMA funnel** | 10 | Dashboard shows real numbers at every stage |
| **End-to-end trace** | 10 | One paper fully traced through the pipeline |
| **Null results + MISSING_ABSTRACT** | 5 | Documented, not treated as failures |
| **Verification questions** | 10 | Caught real problems in the AI's implementation |

---

## A Note About Reuse

The PRISMA funnel you just built is not a one-off deliverable. **Every future task that adds papers to the corpus will require the same funnel,** updated with new numbers. Design your dashboard with that in mind — when the next task runs new searches, the same page should refresh with new counts rather than be rebuilt from scratch. Treat the PRISMA dashboard as durable infrastructure for the rest of the course, not a deliverable you ship and forget.

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/paper_fetcher.py` | `SemanticScholarClient.search()` + `fetch_by_doi()` |
| `src/services/paper_fetcher.py` | `CrossRefClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PubMedClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PaperFetcher.search()` — unified multi-source search |
| `src/services/paper_fetcher.py` | `estimate_study_type()` — auto-derives study type from abstract |
| `src/services/paper_fetcher.py` | `UnpaywallClient` — checks open-access availability |
| `src/cmr/voi_scoring.py` | `score_voi()` — scores findings by information value |
| `src/services/discovery_funnel.py` | `classify_closure()` — FULL/PARTIAL/NONE/NEGATIVE |
| `pipeline_lifecycle_full.db` | Table `pdf_corpus_inventory` — every PDF and its state |
| `pdf_corpus_inventory/latest.csv` | Readable export — check what is already in the corpus |
| `pdf_identity_inventory/latest.csv` | Dedupe info — catches the same paper under different filenames |
| `course_scaffolding.py probe-collection-pdf` | Foolproof duplicate check — run on any PDF to see if it is already in the corpus |
| `ae_waiting_room_probe.py` | `probe_pdf_against_article_eater()` — the same check, callable from Python |
| `refresh_v7_state_surfaces.py` | Regenerates all state surfaces (run before starting) |
| `atlas_shared` | Topic classifier (from Task 1) |
