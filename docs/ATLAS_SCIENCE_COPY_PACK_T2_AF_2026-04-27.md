# ATLAS Science-Writing Copy Pack — Track 2 (Article Finder)

**Date**: 2026-04-27
**Author**: K-ATLAS Science-Writing Agent
**Pages covered**: `t2_intro.html`, `t2_task2.html`, `t2_task3.html`
**Downstream consumer**: GUI Agent v3 (or CW) for HTML rewrite
**Source recon**: `/Users/davidusa/REPOS/Knowledge_Atlas/docs/AF_PIPELINE_RECON_2026-04-27.md`

This pack carries three new substantive specifications into the Track 2 page copy: (A) the `article_references` table as the candidate buffer between harvest and acquisition; (B) the three-stage triage protocol — metadata-only, then abstract-and-citations, then PDF-only-after-triage; (C) the four-scraper layer — SerpAPI, `scholarly`, `paper-scraper`, and `scidownl` — placed by stage and policy rather than treated as interchangeable. Each page is delivered as the canonical 13-item copy pack. Page purpose is preserved: `t2_intro` overviews the track, `t2_task2` stays gap-targeting and query-generation, `t2_task3` stays search-execution and triage.

---

## §1. `t2_intro.html` — Track Overview Copy Pack

### 1. One-sentence purpose line

Build a PRISMA-defensible discovery pipeline that harvests candidate references from review papers and search engines, triages them in three stages before downloading anything, and writes every decision into the article lifecycle database.

### 2. Short intro (2–3 sentences)

Track 2 is the Article Finder track. You build the inflow side of the Knowledge Atlas — the system that turns knowledge gaps into search queries, runs those queries through a coordinated set of four scrapers, and triages each candidate at the abstract level before any PDF is downloaded. Every candidate, accepted or rejected, lands as a row in the `article_references` table so the pipeline can be audited, deduplicated, and reproduced.

### 3. Expanded explainer (1–2 paragraphs)

The Atlas needs steady, defensible inflow. Researchers working on environment-and-cognition need to know which questions the literature has answered, which it has only half-answered, and which it has not yet asked. Without a disciplined discovery pipeline the Atlas drifts on whatever its contributors happened to read this week, and without an audit trail the pipeline cannot be defended in a PRISMA report. Track 2 builds both the pipeline and the audit trail end-to-end across three tasks.

The pipeline has a specific shape that this track teaches. Candidate references arrive from two channels: review papers already in our corpus that cite other work (harvested by an existing Article Eater script), and search engines that respond to the queries you write (SerpAPI for paid Google Scholar, `scholarly` as a free fallback, and `paper-scraper` for preprints). Every candidate is written to the `article_references` table, then walked through three triage stages — metadata-only screening on title and venue, then abstract collection and classifier scoring, then PDF retrieval only after a paper has cleared abstract triage. PDF acquisition prefers Unpaywall and OpenAlex; `scidownl` is treated as a last-resort source that requires a UCSD library policy check before use. By the end of the track, your pipeline produces a PRISMA funnel reconstructed directly from the lifecycle database.

### 4. Section labels

- Hero: `Track 2: Article Finder`
- `What you'll build`
- `How the pipeline is organised` (NEW — this is where the four-scraper layer and the three-stage triage funnel are introduced at overview level)
- `Where harvested references live: the article_references table` (NEW)
- `The three tasks`
- `Repos you'll need`
- `How submission works for Track 2`

### 5. Primary CTA wording

`Start with Task 1 →` (label below the three task cards), with secondary CTA `Read the pipeline reconnaissance` linking to `docs/AF_PIPELINE_RECON_2026-04-27.md` for students who want the architecture before the rubric.

### 6. Example questions (4–6)

These are the questions the track teaches a student to answer.

1. Which low-confidence steps in the PNU mechanism chains have the highest Value of Information, and what queries would close them?
2. For a given gap, what candidate references already exist in the reference lists of review papers we already own, and which of those do we not yet have the PDF for?
3. Of the 250 candidate references our search returned this month, how many were rejected at metadata-only triage, how many at abstract triage, and how many reached PDF retrieval?
4. When SerpAPI's free quota is exhausted, what does the `scholarly` fallback recover, and at what reliability cost?
5. For a candidate paper that no open-access source can deliver, what is the policy-correct next step before invoking `scidownl`?
6. How does a single candidate reference move through `article_references` from `triage_stage = 'metadata_only'` to `triage_stage = 'acquired'`, and what audit rows does that journey leave behind?

### 7. Warnings / caveats (2–3, epistemic)

1. **PDF download is not a triage tool.** Downloading a PDF before you have read the abstract is a budget leak and a PRISMA-defensibility leak. The three-stage funnel exists so that PDFs are fetched only for candidates that have cleared abstract triage.
2. **`scidownl` is not a default scraper.** It pulls from Sci-Hub mirrors and sits inside an unresolved UCSD library and copyright question. It must be opt-in via a config flag, last-resort in the source cascade, and logged as `pdf_acquisition_last_source = 'scidownl'`. Treat its use as a decision your PI signs off on, not a default behaviour of your pipeline.
3. **Free-floating outputs do not count.** A reference list extracted into a JSON file that never joins back to the lifecycle database is invisible to the rest of the pipeline. Every harvested candidate must land as an `article_references` row; otherwise the next harvester will rediscover it, the PRISMA dashboard cannot count it, and your work is unverifiable.

### 8. Empty-state text

> No tasks started yet. Track 2 begins with Task 1 (fix the contribute page); Task 2 (gap targeting and query generation) and Task 3 (search execution and triage) build on it. Begin with Task 1 to set up your repos and your branch.

### 9. Loading-state text

> Loading Track 2 overview…

### 10. Error-state text

> The Track 2 overview did not load. The page is static; if you see this, refresh the page or pull the latest commit on `Knowledge_Atlas/main`. If the issue persists, the file `160sp/t2_intro.html` may be missing from your local checkout.

### 11. Tooltip / helper text candidates

- **PRISMA**: Preferred Reporting Items for Systematic Reviews and Meta-Analyses — the reporting checklist that makes a search auditable: every paper that came in, every paper that fell out, and the reason for each removal.
- **Article lifecycle DB**: `pipeline_lifecycle_full.db`. The single source of truth for the state of every paper in the system. Tracks acquired papers in `papers`, harvested-but-not-yet-acquired references in `article_references`, and every state transition in `lifecycle_transitions`.
- **`article_references` table**: The candidate buffer. Every reference the system *knows about* but does not yet have a PDF for. Rows are linked back to the review they were harvested from (`discovered_from_paper_id`) and forward to the acquired paper, if and when it arrives (`acquired_paper_id`).
- **Three-stage triage**: A funnel that screens candidates cheapest-first — title and venue, then abstract and classifier, then PDF retrieval. PDFs are fetched only for candidates that survive the first two stages.
- **VOI (Value of Information)**: A score, computed by `VOICalculator`, that estimates how much filling a particular knowledge gap would change the rest of the belief network. High-VOI gaps sit at hubs with many downstream dependencies.

### 12. Beginner variant (key labels and intros)

- Hero sub: *Build the part of the Knowledge Atlas that finds new papers — write search queries, run them, and decide which results are worth keeping. Every step is logged in a database so a reader can check your work later.*
- `What you'll build` first sentence: *You'll build a small pipeline that takes the gaps in our knowledge of how environments shape minds, turns each gap into a query, runs the query through Google Scholar and a few other sources, and decides — at the abstract level — whether each paper is worth downloading.*
- `Where harvested references live` first sentence: *Every candidate paper your pipeline finds gets recorded in a table called `article_references`. Think of it as the holding area: papers you've heard of but don't yet have the PDF for live there until you decide what to do with them.*

### 13. Expert variant (denser, more precise)

- Hero sub: *PRISMA-defensible inflow pipeline. Two harvest channels (review-PDF reference extraction, four-scraper search), single candidate buffer (`article_references`), three-stage triage funnel (metadata-only → abstract+classifier → PDF retrieval), Unpaywall-first acquisition cascade with `scidownl` gated behind a UCSD policy flag.*
- `What you'll build` first sentence: *You build, in three tasks, a contract-driven discovery pipeline whose state is fully reconstructible from the lifecycle DB: gap extraction over PNU mechanism chains with VOI scoring, paired AI-Citation/Boolean query generation, multi-scraper candidate harvest, and a three-stage abstract-first triage funnel that writes every decision into `article_references` and `lifecycle_transitions`.*
- `Where harvested references live` first sentence: *The `article_references` table is the candidate buffer between harvest and acquisition; rows carry `discovered_via` provenance, `triage_stage` and `triage_decision` state, classifier and VOI scores, and forward links into `papers` once acquisition completes.*

---

## §2. `t2_task2.html` — Gap Targeting & Query Generation Copy Pack

### 1. One-sentence purpose line

Build a gap extractor and a query generator whose output feeds the four-scraper search layer in Task 3, and prototype the queries against the 46 review-PDF references the Article Eater has already harvested for you.

### 2. Short intro (2–3 sentences)

Task 2 is where you decide *what* the pipeline will look for. You walk the PNU mechanism chains for low-confidence steps, score the resulting gaps with `VOICalculator`, and translate each high-VOI gap into a paired natural-language and Boolean query. You do not yet run any external search — Task 2 ends just before SerpAPI — but everything you write here becomes the input to Task 3's four-scraper search layer.

### 3. Expanded explainer (1–2 paragraphs)

A search pipeline is only as good as the gaps it targets. Before any query is sent, this task forces you to read the data carefully — which steps in the mechanism chains are weak, which are weak in ways that matter, and which gaps the literature is already converging on. The `VOICalculator` does the formal scoring; your job is to ground it in real templates, ask the AI to walk you through the chain, and produce a ranked gap list whose top entries are defensible to a researcher who reviews them. Skip this discipline and your queries will hunt for papers we already have, or for gaps the field has already closed.

You will also prototype your queries against real harvested data before they ever touch a search API. The Article Eater has already extracted reference lists from 46 review PDFs in its neuro-key collection; the harvest sits at `/Users/davidusa/REPOS/_Collecting Articles/Neuro key articles/_atlas_inventory/latest_neuro_review_reference_harvest.json` and contains a dictionary of DOIs and their co-citation counts across reviews. Treat this as a free corpus for query validation: a well-targeted query should retrieve titles whose DOIs already appear in this harvest, because high co-citation count is a proxy for high VOI by construction. The queries you finalise in this task feed directly into Task 3's `search_runner.py`, which routes them to SerpAPI first, `scholarly` if the SerpAPI quota is exhausted, and `paper-scraper` for the preprint channel; every result those scrapers return will be written as a row in `article_references`.

### 4. Section labels

- Hero: `Gap Targeting & Query Generation`
- `Setup`
- `Phase 1: Understand the gap data and the VOI system`
- `Phase 2: Build the gap extractor`
- `Phase 3: Generate search queries — and prototype them against real data` (REVISED label)
- `Phase 4: Prove it works`
- `Where your queries go next: the four-scraper layer in Task 3` (NEW — short forward-pointer section)
- `What you submit`
- `Files you must change or create`
- `Grading (60 points)`
- `A note about reuse`
- `Existing code you should know about`
- `Submit Task 2 on GitHub`

### 5. Primary CTA wording

`Start Phase 1 →`. Secondary CTAs in the new forward-pointer section: `Browse the harvested neuro-review references (JSON)` and `Read the Task 3 scraper map` linking ahead to the t2_task3 scraper section.

### 6. Example questions (4–6)

1. Which three PNU templates have the highest aggregate VOI across their low-confidence steps, and which one step in each is the single highest-VOI gap?
2. For a given gap, what is the matched pair of an AI-Citation question (full sentence with theory name and mechanism) and a Boolean Google Scholar query (exact phrases joined by AND/OR with `-review` to exclude reviews)?
3. Does my Boolean query, when checked against the harvested neuro-review reference DOIs, retrieve any titles whose DOIs already appear in `latest_neuro_review_reference_harvest.json`? If yes, my query is at least pointed at the right neighbourhood of the literature; if no, my query may be too narrow or aimed at the wrong sub-field.
4. Which of my high-VOI gaps map onto DOIs that the harvest shows are highly co-cited (e.g., `10.3389/fnhum.2017.00477` with cite-count 7), suggesting the field is converging on those mechanisms?
5. Which gaps does the harvest *not* speak to at all — that is, no review in our collection cites a paper on this mechanism — and what does that imply for the kind of search Task 3 will need to run?
6. For one gap, write the AI-Citation query, the Boolean query, and a one-sentence prediction of which scraper in Task 3's layer (SerpAPI, `scholarly`, or `paper-scraper`) will be most productive on this query, and why.

### 7. Warnings / caveats (2–3, epistemic)

1. **A gap list with no provenance is useless.** Every gap you extract must carry its `template_id`, the step number in the mechanism chain, the original confidence score, and the VOI score. A flat list of phrases tells the next stage of the pipeline nothing about why a gap matters.
2. **Boolean queries are brittle.** A bare comma-separated word list is not a Boolean query; it is a keyword soup that Google Scholar will interpret unpredictably. Every Boolean query must contain at least one quoted exact phrase and at least one `AND`/`OR` join. If you cannot read your own query aloud and explain why each clause is there, neither can the AI you handed the contract to.
3. **Prototyping against the harvest is necessary but not sufficient.** The 46-review harvest is a real corpus and a useful sanity check, but it is biased toward the sub-fields those reviews cover. A query that retrieves zero hits in the harvest may still be a good query for a genuinely under-covered gap; do not over-fit your queries to what the harvest already knows.

### 8. Empty-state text

> No gap list yet. Run `gap_extractor.py --templates Article_Eater/data/templates/` to extract low-confidence steps from the PNU templates and produce `gap_results.json`.

### 9. Loading-state text

> Walking 166 PNU templates and scoring each low-confidence step with `VOICalculator`. This usually finishes in under a minute on a laptop.

### 10. Error-state text

> Gap extraction failed. The most common causes are: the templates directory cannot be found (check the `--templates` path), `VOICalculator` cannot be imported (check that you ran `pip install -e .` in `atlas_shared` and that `Article_Eater` is on your `PYTHONPATH`), or a template has no `mechanism_chain` field (your extractor should skip rather than crash). The error message above is the AI's; read it before retrying.

### 11. Tooltip / helper text candidates

- **PNU template**: Plausible Neural Underpinning template. A JSON file describing one mechanism chain — how an environmental feature (e.g., ceiling height) produces a psychological outcome (e.g., creativity) through a series of neural processes. Each step carries its own confidence score.
- **`mechanism_chain`**: The ordered list of steps inside a PNU template. Walk this list to find low-confidence steps, which are the gaps you target.
- **`VOICalculator.calculate_voi()`**: The function that scores a gap on Value of Information. High-VOI gaps sit at hubs with many downstream dependencies; low-VOI gaps are isolated.
- **AI-Citation query**: A natural-language search query — a full sentence with theory names and mechanism descriptions, written for Google's AI overview to handle synonyms and intent.
- **Boolean query**: A structured search query — exact phrases in quotes, joined by `AND` and `OR`, with `-review` to exclude reviews and `intitle:` to require a term in the title. This is what Task 3 sends to SerpAPI.
- **`latest_neuro_review_reference_harvest.json`**: A dictionary `{doi: cite_count}` of the references the Article Eater has already extracted from 46 review PDFs. Useful as a free corpus to prototype your queries against.

### 12. Beginner variant

- Hero sub: *Read the templates, find the steps where the science is weak, score them by how much they matter, and write search queries to find papers that would fill them.*
- Phase-1 first sentence: *A PNU template is a JSON file that describes how something in the environment — say, ceiling height — affects something in the mind — say, creativity — through a chain of brain steps. Some steps in the chain are well understood; others are not. The poorly-understood steps are your knowledge gaps.*
- New forward-pointer first sentence: *The queries you write in this task don't run yet. Task 3 will take them and feed them to a set of four search tools — one paid (SerpAPI), three free (`scholarly`, `paper-scraper`, and a PDF-fetcher called `scidownl` you'll learn about later).*

### 13. Expert variant

- Hero sub: *Gap extraction over PNU mechanism chains; VOI scoring with `VOICalculator`; paired AI-Citation/Boolean query generation; prototype validation against the 46-review neuro-key reference harvest.*
- Phase-1 first sentence: *Walk each PNU `mechanism_chain` for steps with `confidence < 0.6`; pass each candidate to `VOICalculator.calculate_voi()` to obtain a centrality-weighted information value; rank descending and dedupe against `pdf_corpus_inventory` to avoid re-targeting acquired evidence.*
- New forward-pointer first sentence: *Your `query_results.json` is the input to Task 3's `search_runner.py`, which dispatches each query to SerpAPI's `google_scholar` engine first, falls back to `scholarly` when the 250/month SerpAPI quota is exhausted, and routes preprint-eligible queries to `paper-scraper`'s arXiv/bioRxiv/medRxiv/chemRxiv backends; all returned candidates land as `article_references` rows with `discovered_via` set to the corresponding scraper tag.*

---

## §3. `t2_task3.html` — Search Execution & Triage Copy Pack

### 1. One-sentence purpose line

Run the four-scraper search layer, write every candidate into `article_references`, walk each row through the three-stage triage funnel, and acquire PDFs only for candidates that have cleared abstract triage — never before.

### 2. Short intro (2–3 sentences)

Task 3 is where the discipline is enforced. Four scrapers — SerpAPI, `scholarly`, `paper-scraper`, and (for PDF retrieval only, last resort) `scidownl` — produce candidates that all land in the same `article_references` table. Each candidate is then walked through three triage stages: metadata-only screening, abstract collection and classifier scoring, and only then PDF retrieval. The PRISMA funnel that proves your pipeline works is reconstructed directly from `article_references` and `lifecycle_transitions` — no spreadsheets, no parallel state, no free-floating JSON.

### 3. Expanded explainer (1–2 paragraphs)

The pipeline you build in this task has one cardinal rule: never download a PDF to decide whether you want the paper. The three-stage triage funnel exists to enforce that rule cheaply and defensibly. Stage 1 is metadata-only: a candidate enters `article_references` with `triage_stage = 'metadata_only'`, gets its title and venue passed through the `atlas_shared` classifier, and is rejected immediately if the classifier confidence falls below threshold. Stage 2 runs the abstract fallback chain (Semantic Scholar → CrossRef → PubMed → OpenAlex), scores the abstract with `score_voi()`, and assigns `triage_decision` = `ACCEPT`, `EDGE_CASE`, `REJECT`, or `MISSING_ABSTRACT`. Stage 3 — PDF retrieval — runs only for `ACCEPT` rows and only via the source cascade (Unpaywall, then OpenAlex OA, then `scidownl` when the policy flag is set). Each transition is mirrored in `lifecycle_transitions` so the PRISMA dashboard reconstructs the funnel from audit history rather than from current state alone.

The four scrapers are not interchangeable. SerpAPI is the paid Google Scholar channel — fast, reliable, but capped at 250 free credits per month. `scholarly` is the free Google Scholar channel — same source, no cost, but rate-limited and prone to CAPTCHA blocks; treat it as the quota-exhausted fallback, and document its results as best-effort. `paper-scraper` reaches preprint servers (arXiv, bioRxiv, medRxiv, chemRxiv) that Google Scholar covers unevenly; it is the right scraper for high-VOI gaps where the literature is moving fast or the mechanism is too new to be indexed widely. `scidownl` is none of these — it is a PDF acquisition tool of last resort that proxies to Sci-Hub mirrors. UCSD library policy on Sci-Hub is unresolved, so `scidownl` must be opt-in via a config flag (`enable_paid_or_grey_sources`), called only after Unpaywall and OpenAlex have both failed for an `ACCEPT` row, and logged as `pdf_acquisition_last_source = 'scidownl'`. Discuss with your instructor before you turn the flag on; do not make the decision unilaterally.

### 4. Section labels

- Hero: `Search Execution & Three-Stage Triage`
- `What PRISMA is and why you are building one`
- `Setup`
- `Phase 1: Understand the search and triage architecture`
- `Phase 2: Wire the four scrapers into the search runner` (REVISED label)
- `Phase 3: The article_references table — every candidate, one row` (NEW phase, short)
- `Phase 4: Three-stage triage — metadata, abstract, PDF` (REVISED — replaces the previous Phase 3+4)
- `Phase 5: PDF acquisition cascade and the scidownl policy gate` (NEW)
- `Phase 6: Build the PRISMA dashboard from article_references`
- `Phase 7: Prove it works (end-to-end trace, null results, MISSING_ABSTRACT)`
- `What you submit`
- `Files you must change or create`
- `Grading (75 points)`
- `A note about reuse`
- `Existing code you should know about`
- `Submit Task 3 on GitHub`

### 5. Primary CTA wording

`Run the search runner →` next to the Phase 2 code block. Secondary CTAs: `View the article_references DDL` (links to the recon doc, §3), `Open the SerpAPI dashboard`, and `Read the scidownl policy gate` (anchors into Phase 5).

### 6. Example questions (4–6)

1. For a given Boolean query, how many candidates does SerpAPI return; how many of those are duplicates against `pdf_corpus_inventory` (caught at Stage 1); how many survive metadata-only triage; how many reach abstract triage; how many are marked `ACCEPT`; and how many of those `ACCEPT` rows actually have a PDF after the Stage-3 cascade runs?
2. When SerpAPI's monthly quota is exhausted mid-run, what does my pipeline do — does it fall back to `scholarly` automatically, does it queue the remaining queries for next month, and what does the PRISMA dashboard show for the dropped queries?
3. For a high-VOI preprint-era gap (e.g., a 2024–2026 mechanism not yet in published reviews), does `paper-scraper` retrieve candidates that SerpAPI misses? If yes, what `discovered_via` distribution does my `article_references` table show for that gap?
4. For one `ACCEPT` row whose PDF Unpaywall and OpenAlex both fail to deliver, what does the `pdf_acquisition_attempts` count look like, what is the `pdf_acquisition_last_source`, and have I confirmed with my instructor whether `scidownl` is permitted for this paper before invoking it?
5. Reconstruct the PRISMA funnel for this run with one SQL query: `SELECT triage_stage, triage_decision, COUNT(*) FROM article_references GROUP BY 1, 2`. Do the counts match what my dashboard reports?
6. For one paper that made it from gap to acquired PDF, trace its row in `article_references`: `discovered_via`, `discovered_from_paper_id` or `discovered_query`, the `triage_stage` transitions, the `voi_score` and `classifier_score`, the `pdf_acquisition_last_source`, and the linked `acquired_paper_id` in `papers`.

### 7. Warnings / caveats (2–3, epistemic)

1. **Never download a PDF before triaging the candidate at the abstract level.** This is the rule the three-stage funnel exists to enforce. If your code calls `pdf_downloader` on a candidate whose `triage_stage` is anything other than `'pdf_retrieved'` (set after `triage_decision = 'ACCEPT'`), it has bypassed the funnel. The funnel state machine in `triage/funnel_state.py` is what stops this; do not write a parallel acquisition path that skips it.
2. **`scidownl` is not a default scraper. It is a last-resort PDF source with an unresolved policy question.** It pulls from Sci-Hub mirrors. UCSD library policy on Sci-Hub use is not settled, and the legal status varies by jurisdiction. Treat `scidownl` as opt-in via a config flag, last in the source cascade after Unpaywall and OpenAlex, logged on every use, and discussed with your instructor before the flag is turned on. The flag should default to `false`. The right phrase for your contract is: *"If `enable_paid_or_grey_sources` is True, attempt scidownl as the final source; log every attempt; require the UCSD library policy check to be present in `policy_clearance.json` before the call."* Do not bypass this.
3. **`scholarly` is brittle. Document its limits.** It scrapes Google Scholar HTML, which is not a stable contract; rate limits, CAPTCHA challenges, and silent IP blocks are routine. Use it as a quota-exhausted fallback, mark its rows with `discovered_via = 'scholarly_search'` so a reader can audit which candidates came from a brittle source, and do not present `scholarly` results as having the same reliability as SerpAPI results.

### 8. Empty-state text

> No candidates yet. Run `python3 cli/main.py search-runner --queries query_results.json` to dispatch the queries from Task 2 to the scraper layer. Candidates will appear in `article_references` as they are harvested and immediately enter Stage 1 triage.

### 9. Loading-state text

> Dispatching queries to the scraper layer (SerpAPI primary, `scholarly` fallback, `paper-scraper` for preprint-eligible queries). Each candidate enters `article_references` with `triage_stage = 'metadata_only'` as it is harvested.

### 10. Error-state text

> The pipeline failed. Common causes, in rough order of likelihood:
>
> - **`SERPAPI_KEY` missing or invalid** — check `echo $SERPAPI_KEY` and that the key is still active on the SerpAPI dashboard.
> - **SerpAPI quota exhausted** — your pipeline should fall back to `scholarly`; if it does not, check the fallback handler in `search/serpapi_scholar.py`.
> - **Lifecycle DB locked** — another process is writing to `pipeline_lifecycle_full.db`; close other shells, then retry.
> - **`article_references` table missing** — run the migration: the DDL is in `scripts/coordination/lifecycle/schema.sql` (see the recon doc, §3); apply with `python3 scripts/coordination/lifecycle/apply_migrations.py`.
> - **`scidownl` invoked without policy clearance** — by design. The pipeline aborts on `scidownl` calls when `policy_clearance.json` is absent. Talk to your instructor before clearing this.

### 11. Tooltip / helper text candidates

- **`article_references`**: The candidate buffer. One row per known-about reference, whether or not we have its PDF. Carries `discovered_via`, `triage_stage`, `triage_decision`, `voi_score`, and forward links into `papers` once acquired.
- **`triage_stage`**: Where this candidate sits in the funnel — `metadata_only`, `abstract_collected`, `pdf_retrieved`, `rejected_at_metadata`, `rejected_at_abstract`, `duplicate`, `missing_abstract`, or `acquired`.
- **`discovered_via`**: Which scraper or harvester told us about this reference — `serpapi_scholar`, `scholarly_search`, `paperscraper_search`, `review_pdf_extract`, `openalex_expansion`, `crossref_search`, or `student_upload`.
- **SerpAPI**: Paid Google Scholar scraper. Free tier: 250 credits/month. Returns title, link, snippet, publication info — *not* full abstracts and *not* reliably DOIs. Each call costs one credit.
- **`scholarly`**: Free Python package that scrapes Google Scholar HTML. Same source as SerpAPI, but rate-limited and CAPTCHA-prone. Use as quota-exhausted fallback.
- **`paper-scraper`** (also written `paperscraper`): Free preprint-server scraper covering arXiv, bioRxiv, medRxiv, and chemRxiv. The right tool for high-VOI gaps where the literature is moving fast.
- **`scidownl`**: PDF downloader that proxies to Sci-Hub mirrors. Last-resort source for `ACCEPT` candidates whose PDFs Unpaywall and OpenAlex cannot deliver. Opt-in via config flag; requires a UCSD library policy clearance file before use; logged on every call.
- **PDF acquisition cascade**: The Stage-3 source order — Unpaywall first, OpenAlex OA URL second, `scidownl` (if policy-cleared) third. Each attempt is recorded in `pdf_acquisition_attempts` and `pdf_acquisition_last_source`.
- **`v_acquisition_queue`**: A view over `article_references` showing every `ACCEPT` row that does not yet have a PDF, sorted by VOI descending. The PDF-retrieval worker reads from this view.

### 12. Beginner variant

- Hero sub: *Run your queries through four search tools, save every result in a database table, decide which ones to keep using just the title and abstract, and only then download the PDFs you actually want. The dashboard at the end shows how many papers came in and how many fell out at each step.*
- Phase 5 (the scidownl policy gate) first sentence: *`scidownl` is a tool that downloads PDFs from a website called Sci-Hub. UCSD's library hasn't decided whether students should use Sci-Hub for coursework, so for now this tool is off by default — you have to ask your instructor before turning it on, and your code has to log every time it's used.*
- Three-stage triage first sentence: *The pipeline screens candidates in three rounds, cheapest first. Round 1 looks at just the title and the journal name. Round 2 fetches the abstract and runs it through a topic classifier. Round 3 — and only round 3 — actually downloads the PDF.*

### 13. Expert variant

- Hero sub: *Coordinated four-scraper harvest layer (SerpAPI / `scholarly` / `paper-scraper` / `scidownl`); single candidate buffer in `article_references`; three-stage abstract-first triage funnel with atomic `triage_stage` transitions logged in `lifecycle_transitions`; Unpaywall-first acquisition cascade with `scidownl` gated behind UCSD policy clearance; PRISMA dashboard reconstructed directly from `article_references` group-counts.*
- Phase 5 first sentence: *`scidownl` invocation is conditional on (i) `enable_paid_or_grey_sources` set in config, (ii) presence of `policy_clearance.json` countersigned by the instructor, (iii) prior failure of Unpaywall and OpenAlex OA for the same `reference_id`, and (iv) `triage_decision = 'ACCEPT'` on the row; every call writes `pdf_acquisition_last_source = 'scidownl'` and an audit row to `lifecycle_transitions`.*
- Three-stage triage first sentence: *Stage 1 (`metadata_triage.py`): classifier on title+venue, reject below threshold (suggested 0.20). Stage 2 (`abstract_triage.py`): four-source abstract fallback chain, `score_voi()` on abstract, four-way decision (`ACCEPT` / `EDGE_CASE` / `REJECT` / `MISSING_ABSTRACT`). Stage 3 (`pdf_downloader.py`, extended): runs only for `ACCEPT` rows pulled from `v_acquisition_queue`, walks the source cascade, and updates `acquired_paper_id` on success.*

---

## Closing notes for the next agent

The HTML rewrite that follows this copy pack should:

1. Add the four-scraper layer and the three-stage triage funnel into `t2_intro.html`'s overview narrative without lengthening the page beyond about 50% of its current size — these are framing additions, not new tasks.
2. Extend `t2_task2.html` with one new short forward-pointer section (`Where your queries go next`) and a new sub-step in Phase 3 for prototyping queries against `latest_neuro_review_reference_harvest.json`. The page's centre of gravity must remain on gap targeting and query generation; do not let the scraper layer pull this page into Task 3 territory.
3. Restructure `t2_task3.html` around the seven-phase outline above. The biggest changes are: (a) Phase 2 explicitly wires four scrapers, not one; (b) a new Phase 3 introduces the `article_references` table and its DDL excerpt; (c) Phase 4 makes the three triage stages explicit and atomic; (d) a new Phase 5 introduces the PDF acquisition cascade and the `scidownl` policy gate as a first-class topic, not a footnote; (e) the existing PRISMA dashboard phase becomes Phase 6 and is rewritten to read counts from `article_references` directly.
4. Preserve every existing rubric, grading table, file-manifest table, and GitHub submission section verbatim unless the new content forces a count change. Where it does (for example, Task 3 grading should now include rows for "article_references wiring" and "scidownl policy gate handled correctly"), surface the change clearly.

The substantive material (DDL, funnel diagram, scraper map, AE script provenance) lives in `/Users/davidusa/REPOS/Knowledge_Atlas/docs/AF_PIPELINE_RECON_2026-04-27.md`. This copy pack is the science-writing layer over that material; the next agent should consult both.
