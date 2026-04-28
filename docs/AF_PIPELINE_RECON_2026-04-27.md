# AF Pipeline Reconnaissance Report

**Date:** 2026-04-27
**Author:** CW reconnaissance agent
**Purpose:** Provide CW the precise material needed to update `t2_intro.html`, `t2_task2.html`, and `t2_task3.html` with: (a) a concrete article-reference harvesting story, (b) a database wiring plan, (c) a triage protocol, and (d) the four-scraper integration map.
**Scope:** Reports findings only. CW writes the page updates; this document does not.

---

## §1. Current Track 2 Spec — What Is There, What Is Missing

### What Is Already Specified

The three Track 2 pages already cover a coherent gap-driven discovery pipeline at moderate fidelity.

**`t2_intro.html`** establishes the throughline: PRISMA-compliant discovery, contract-first delegation to AI, four repos (Knowledge_Atlas, Article_Finder, Article_Eater, atlas_shared), three tasks worth 75 / 60 / 75 points, and a single git branch per student.

**`t2_task2.html`** specifies a four-phase sequence:
1. Read PNU templates and learn `VOICalculator`.
2. Build a gap extractor (`gap_extractor.py`) that walks `mechanism_chain` and ranks low-confidence steps.
3. Build a query generator (`query_generator.py`) that emits paired Google-AI-Citation and Google-Scholar-Boolean queries.
4. Spot-check three queries by hand in Google.
The page already references `pipeline_lifecycle_full.db` for corpus deduplication via `pdf_corpus_inventory` and `pdf_identity_inventory` surfaces, and points students to existing helpers (`probe-collection-pdf`, `ae_waiting_room_probe.py`, `refresh_v7_state_surfaces.py`).

**`t2_task3.html`** specifies six phases: SerpAPI search runner, abstract collector with a four-step fallback chain (Semantic Scholar → CrossRef → PubMed → OpenAlex), a four-bucket triage (ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT) tied to the `atlas_shared` classifier and `score_voi()`, a PRISMA dashboard, and an end-to-end trace deliverable.

### What Is Missing or Under-Specified

The three pages do **not** currently cover four specific things that this reconnaissance is meant to backfill.

1. **No story for "where references come from."** The pages assume search starts from queries, then collects abstracts. They do not name the *other* harvesting channel: pulling reference lists out of review papers already in CURRENT_GOLD. AE already has a working harvester for this (`extract_neuro_key_review_references.py`) and a working ranking step (`build_neuro_review_acquisition_queue.py`); these belong in the Track 2 story.
2. **No `article_references` table.** The pages describe writing to "Database / lifecycle DB" without specifying *what* table holds harvested but not-yet-acquired references. The lifecycle DB schema currently has `papers`, `paper_metadata`, `page_processing_log`, `snip_registry`, `mathpix_cost_ledger`, `lifecycle_transitions`, `decisions` — there is no table for *candidate* references. Students will end up creating ad-hoc JSON files that never join back to the corpus.
3. **No scraper map.** The pages name SerpAPI for the Google Scholar query channel and the four metadata APIs for abstract collection, but never mention the four scrapers David asked about (SerpAPI, `scholarly`, `paper-scraper`, `scidownl`) as a coordinated set, nor the pipeline stages where each plugs in.
4. **No abstract-first triage protocol.** Task 3 implies abstract-first triage but does not state it as a rule. A clear three-stage funnel — metadata-only triage → abstract-and-citations triage → PDF retrieval only after triage — would make the pipeline cheaper to operate and easier to defend in PRISMA reporting.

---

## §2. AF Pipeline Architecture — Entry Points and Integration Points

The active codebase lives at `/Users/davidusa/REPOS/Article_Finder_v3_2_3/`. The relevant top-level packages:

```
Article_Finder_v3_2_3/
├── cli/main.py              # Single CLI entry point; subcommands wire each subsystem
├── config/                  # YAML config + loader
├── core/                    # Database wrapper (uses pdf_lifecycle.db)
├── ingest/                  # ALL inflow paths
│   ├── smart_importer.py    # CSV/Excel/RIS reference import
│   ├── citation_parser.py   # APA/MLA/Chicago/Vancouver string parser
│   ├── pdf_downloader.py    # Unpaywall-driven PDF acquisition
│   ├── doi_resolver.py      # OpenAlex / CrossRef DOI lookup
│   ├── pdf_cataloger.py     # Catalogs PDFs from a directory
│   ├── pdf_watcher.py       # Inbox-folder polling
│   ├── enricher.py          # Bulk metadata enrichment
│   ├── abstract_fetcher.py  # Queue-based abstract fetch
│   └── zotero_bridge.py     # Zotero local read + import/export
├── search/
│   ├── discovery_orchestrator.py   # Master loop (import → classify → expand → acquire → AE → feedback)
│   ├── bibliographer.py            # Taxonomy-driven systematic discovery
│   ├── citation_network.py         # OpenAlex forward/backward citation fetch
│   ├── bounded_expander.py         # Citation-graph expansion with VOI filter
│   ├── expansion_scorer.py
│   ├── deduplicator.py             # PDFMatcher
│   ├── ae_feedback.py              # Read AE outputs to find new gaps
│   ├── gap_analyzer.py             # Identify under-covered cells
│   └── execution_logger.py
├── triage/                  # Embedding-based triage + scoring
├── knowledge/               # Semantic search, claim graph, query engine
├── eater_interface/         # job_bundle, invoker, output_parser — handoff to AE
└── ui/                      # Streamlit app + pages
```

### Entry Points

The single CLI entry is `cli/main.py`. The relevant subcommands for Track 2:

| Subcommand | Function | Relevance to Track 2 |
|------------|----------|----------------------|
| `import <file>` | `cmd_import` | Imports a CSV / Excel / RIS list of references — the existing path for "reference harvest into AF" |
| `import-pdfs <dir>` | `cmd_import_pdfs` | Catalogs a directory of PDFs (used by Task 1) |
| `inbox` | `cmd_inbox` | Watches the inbox directory (Task 1 contribute-page backend) |
| `enrich` | `cmd_enrich` | Adds metadata + abstracts from OpenAlex / CrossRef |
| `abstracts` | `cmd_abstracts` | Queue-based abstract fetch (the chain Task 3 will call) |
| `expand` | `cmd_expand` | Citation-network expansion via OpenAlex (the *existing* reference-harvesting path) |
| `discover` | `cmd_discover` | Full pipeline loop |
| `bibliographer` | `cmd_bibliographer` | Systematic taxonomy-driven discovery |
| `download` | `cmd_download` | PDF acquisition via Unpaywall |
| `build-jobs` | `cmd_build_jobs` | Hand off to Article Eater |

### Where New Candidate-Harvesting Code Plugs In

The code that AF students will write in Task 2/Task 3 is *not* a parallel pipeline; it plugs into the existing one at three points.

1. **Reference harvest in →** new module `ingest/reference_harvester.py`, called as a new subcommand `cli/main.py harvest-references`. This module does for *review PDFs already in CURRENT_GOLD* what `smart_importer.py` does for *uploaded CSVs*: extract candidate references, normalize DOIs, and write them into the database. The model already exists in AE at `scripts/coordination/extract_neuro_key_review_references.py` — the AF version should mirror its logic (tail-page extraction with `pdfplumber`, header detection for "References" / "Bibliography" / "Literature Cited", entry segmentation, DOI regex, year regex).
2. **Search-driven candidate harvest →** the existing `search/discovery_orchestrator.py` already orchestrates SerpAPI-style search through `bibliographer.py`. Track 2's `search_runner.py` is a simplified, student-built version targeted at SerpAPI Google Scholar specifically; it writes into the same candidate-reference table.
3. **Triage gate →** the existing `triage/` package already has `embeddings.py` and a hierarchical scorer. Task 3's `abstract_triage.py` is the per-record decision step that pulls candidate references off the candidate table, decides ACCEPT/EDGE_CASE/REJECT, and, only for ACCEPT, releases them to `pdf_downloader.py`.

The `discover` command in `cli/main.py` is the integration test surface: after a student wires reference-harvest + search-runner + abstract-collector + triage, `python3 cli/main.py discover --import-file gap_results.json` should walk the whole loop end-to-end.

---

## §3. Lifecycle DB — Existing Schema and Proposed `article_references` Table

### Existing Tables (in `scripts/coordination/lifecycle/schema.sql`)

| Table | Primary Key | Purpose |
|-------|-------------|---------|
| `schema_version` | `version` | Migration audit |
| `papers` | `paper_id` (e.g. `PDF-0736`) | One row per acquired PDF, keyed by SHA-256, with timestamp flags for every preprocessing stage |
| `paper_metadata` | `paper_id` | DOI, title, abstract, authors, year, venue, OpenAlex/S2 IDs, Zotero linkage |
| `page_processing_log` | `(paper_id, page_number, tool, processed_at)` | Every page × tool × run |
| `snip_registry` | `snip_id` | Cropped figures/tables/equations |
| `mathpix_cost_ledger` | `id` | Mathpix billing per call |
| `lifecycle_transitions` | `id` | Audit trail of stage changes |
| `decisions` | `decision_id` | Sprint decisions per CLAUDE.md |
| `v_pipeline_state` (view) | — | Computed current stage per paper |

**Critical gap:** there is no table for *references that are known about but not yet acquired*. Currently a harvested DOI either becomes a `papers` row (only after the PDF arrives and a SHA-256 is computed) or it sits in an ad-hoc JSON file outside the DB. This forces every harvester to re-deduplicate on its own and prevents any single query like "which DOIs do we want but not yet have."

### Proposed `article_references` Table (DDL)

This table is the candidate buffer between *harvesting* and *acquisition*. It should be added to `scripts/coordination/lifecycle/schema.sql` with a migration row.

```sql
-- -----------------------------------------------------------------------------
-- article_references: candidate references discovered by harvesting (review-PDF
-- reference lists, SerpAPI search hits, citation-network expansion). Each row
-- is a *known about* paper that may or may not be in the corpus. When/if the
-- PDF lands, the row is linked to `papers` via `acquired_paper_id`.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS article_references (
    reference_id        TEXT PRIMARY KEY,           -- 'REF-2026-04-27-000123', generated
    -- Identity
    doi                 TEXT,                       -- normalized lowercase, no URL prefix
    title_raw           TEXT,                       -- as harvested
    title_normalized    TEXT,                       -- whitespace-collapsed, lowercased, for fuzzy match
    first_author_surname TEXT,
    publication_year    INTEGER,
    venue               TEXT,
    -- Provenance: who told us about this reference?
    discovered_via      TEXT NOT NULL,              -- 'review_pdf_extract' | 'serpapi_scholar' |
                                                    -- 'scholarly_search' | 'paperscraper_search' |
                                                    -- 'openalex_expansion' | 'student_upload' |
                                                    -- 'crossref_search'
    discovered_from_paper_id TEXT REFERENCES papers(paper_id),
                                                    -- if discovered by harvesting an already-owned PDF
    discovered_query    TEXT,                       -- the search query, if applicable
    discovery_run_id    TEXT,                       -- groups co-discovered references
    -- The raw evidence (harvester output); store small snippets here, not full PDFs
    raw_citation        TEXT,                       -- the messy reference-list line as captured
    snippet             TEXT,                       -- search snippet or abstract fragment
    -- Triage state — three-stage funnel; see §5
    triage_stage        TEXT NOT NULL DEFAULT 'metadata_only',
                                                    -- 'metadata_only' | 'abstract_collected' |
                                                    -- 'pdf_retrieved' | 'rejected_at_metadata' |
                                                    -- 'rejected_at_abstract' | 'duplicate' |
                                                    -- 'missing_abstract' | 'acquired'
    triage_decision     TEXT,                       -- 'ACCEPT' | 'EDGE_CASE' | 'REJECT' |
                                                    -- 'MISSING_ABSTRACT' | 'DUPLICATE' | NULL
    triage_reason       TEXT,                       -- human-readable
    voi_score           REAL,                       -- from VOICalculator at harvest time
    classifier_score    REAL,                       -- atlas_shared classifier confidence
    classifier_label    TEXT,                       -- on-topic facet / node
    abstract_text       TEXT,                       -- when fetched
    abstract_source     TEXT,                       -- 'semantic_scholar' | 'crossref' | 'pubmed' | 'openalex' | NULL
    -- Acquisition link
    acquired_paper_id   TEXT REFERENCES papers(paper_id),
                                                    -- non-NULL once the PDF arrives in `papers`
    pdf_acquisition_attempts INTEGER DEFAULT 0,
    pdf_acquisition_last_source TEXT,               -- 'unpaywall' | 'scidownl' | 'openalex_oa' | NULL
    -- Lifecycle timestamps
    discovered_at       TEXT NOT NULL,              -- ISO 8601
    triaged_at          TEXT,
    abstract_fetched_at TEXT,
    pdf_attempted_at    TEXT,
    acquired_at         TEXT,
    -- Free-form
    notes               TEXT
);

CREATE INDEX IF NOT EXISTS idx_article_references_doi
    ON article_references(doi)
    WHERE doi IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_article_references_title_norm
    ON article_references(title_normalized);
CREATE INDEX IF NOT EXISTS idx_article_references_triage
    ON article_references(triage_stage, triage_decision);
CREATE INDEX IF NOT EXISTS idx_article_references_discovered_from
    ON article_references(discovered_from_paper_id);
CREATE INDEX IF NOT EXISTS idx_article_references_acquired
    ON article_references(acquired_paper_id);

-- Convenience: every reference that we want but do not yet have a PDF for.
CREATE VIEW IF NOT EXISTS v_acquisition_queue AS
SELECT reference_id, doi, title_raw, first_author_surname, publication_year,
       voi_score, classifier_score, triage_stage, discovered_via, discovered_at
FROM article_references
WHERE triage_decision = 'ACCEPT'
  AND acquired_paper_id IS NULL
ORDER BY voi_score DESC NULLS LAST, discovered_at ASC;
```

### How the Table Joins to the Article Lifecycle DB

* **One-way link to `papers`:** `discovered_from_paper_id` (reference was harvested out of an already-owned PDF) and `acquired_paper_id` (reference *became* a paper row).
* **DOI matching:** harvesters MUST call `normalize_doi()` (the function already exists in `build_neuro_review_acquisition_queue.py`) before insert; duplicates by DOI should `UPDATE … SET discovered_via = discovered_via || ', ' || NEW.discovered_via` rather than insert again.
* **Title fuzzy matching:** the existing `pdf_identity_inventory` surface holds normalized titles for the corpus; new harvesters compare `title_normalized` against it before insert and set `triage_stage = 'duplicate'` immediately if a fuzzy match scores above the existing identity-table threshold.
* **PRISMA reporting:** the funnel counts in Task 3's dashboard come from `SELECT triage_stage, triage_decision, COUNT(*) FROM article_references GROUP BY 1, 2`. No separate "PRISMA state" table is needed.

---

## §4. Reference Extraction in V7 — What Already Exists, What AF Should Consume

### What V7 Produces (Today)

The V7 extraction pipeline in `Article_Eater_PostQuinean_v1_recovery/` does **not** currently produce a structured reference list per paper. The verification outputs at `data/verification_runs/codex_local_gold_outputs/chunk009_validation.json` (and its peers) carry only `paper_id`, `findings`, and an `ok` flag. The supervalidation files are similarly thin. V7's reference-aware artifacts live elsewhere.

### What V7 *Does* Produce That AF Should Consume

Two coordination scripts already do real reference work and should be the foundation Track 2 students build on, not reinvent:

1. **`scripts/coordination/extract_neuro_key_review_references.py`** — for each review-kind PDF in the inventory it opens with `pdfplumber`, takes the last 8 pages or 40 KB of text, locates a "References" / "Bibliography" / "Literature Cited" / "Reference List" header, segments candidate entries by author-initial-pattern or `[N]` markers, and parses each entry for a year (regex `\b(19|20)\d{2}\b`) and a DOI (regex `\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b`). Output is a JSON harvest at `_atlas_inventory/latest_neuro_review_reference_harvest.json` that already aggregates "top cited DOIs" across review papers.
2. **`scripts/coordination/build_neuro_review_acquisition_queue.py`** — reads that harvest, applies a strict DOI normalizer (rejects generic suffixes, requires a digit in the suffix), filters out DOIs already in CURRENT_GOLD, and produces a ranked queue with priority labels HIGH / MEDIUM / LOW based on co-citation count and family breadth.

The `_atlas_inventory/latest_neuro_review_reference_harvest.json` file as of 2026-04-26 covers 46 review PDFs and yields a dict of `{doi: cite_count}` — for example `10.1038/s41583-022-00512-y: 4`, `10.1073/pnas.1301227110: 4`, `10.3389/fnhum.2017.00477: 7`. This is real, working harvested data.

### How AF Students Should Consume It

The Track 2 spec should be explicit:

* **Do not write a new reference-list parser.** Import the AE script's logic (or call it as a subprocess on demand) and write the parsed candidates into `article_references`.
* **The `discovered_via` column should be `'review_pdf_extract'`** for every row that originated from this path, and `discovered_from_paper_id` should hold the AE `paper_id` of the review.
* **The student-built `gap_extractor.py` (Task 2) should *also* read the harvest file** and use it as a source of "questions the literature is already trying to answer" — gaps with high reference-co-occurrence are higher-VOI by construction (they are mechanism nodes the field is converging on).
* **Reference-list harvest is one of two harvesters Task 3 students wire up.** The other is the SerpAPI search runner. Both write into the same `article_references` table; both go through the same triage funnel. This unifies the PRISMA accounting.

### What AF Adds That V7 Doesn't

The AE harvester stops at "list of plausible DOIs." AF adds: (a) DOI/title resolution against OpenAlex/CrossRef to fill in `title_normalized`, year, and venue; (b) abstract collection via the four-source fallback chain; (c) classifier + VOI triage; (d) PDF acquisition via Unpaywall and (when needed) `scidownl`. None of those steps exist in the AE harvester scripts and none should be added there — they are AF's job.

---

## §5. Triage Protocol — Three-Stage Funnel and Where the Four Scrapers Plug In

### The Funnel

```
       HARVEST                           STAGE 1: METADATA-ONLY TRIAGE
  ┌──────────────────┐                  ┌────────────────────────────┐
  │ Review-PDF       │                  │ For each candidate:        │
  │  extractor       │                  │  • dedupe vs. corpus       │
  │ (AE script)      │  ──── DOI/title  │  • CrossRef metadata pull  │
  │                  │       only       │  • classifier on title +   │
  │ SerpAPI Scholar  │ ────────────────►│     venue                  │
  │  search runner   │                  │  • cheap VOI proxy         │
  │                  │                  │  • REJECT obvious off-topic│
  │ scholarly        │                  └────────────┬───────────────┘
  │  search runner   │                               │
  │                  │                               ▼
  │ paper-scraper    │                  STAGE 2: ABSTRACT + CITATIONS TRIAGE
  │  search runner   │                  ┌────────────────────────────┐
  └──────────────────┘                  │ For each survivor:         │
                                        │  • abstract chain          │
                                        │     S2 → CrossRef → PubMed │
                                        │     → OpenAlex             │
                                        │  • atlas_shared classifier │
                                        │     on abstract            │
                                        │  • full VOI score          │
                                        │  • ACCEPT / EDGE_CASE /    │
                                        │     REJECT / MISSING_ABS   │
                                        └────────────┬───────────────┘
                                                     │ (only ACCEPT)
                                                     ▼
                                        STAGE 3: PDF RETRIEVAL
                                        ┌────────────────────────────┐
                                        │ Try in order:              │
                                        │  1. Unpaywall              │
                                        │  2. OpenAlex OA URL        │
                                        │  3. scidownl (last resort) │
                                        │  → store in `papers`       │
                                        │  → set acquired_paper_id   │
                                        └────────────────────────────┘
```

### Why Three Stages, Not Two

The current Task 3 spec implicitly conflates "decide if we want the paper" with "fetch its abstract." Splitting them out gives three benefits:

1. **Cheaper rejection.** Title + venue + classifier already kills 30-50% of search noise without spending a Semantic Scholar request, an OpenAlex polite-pool slot, or a SerpAPI credit on abstract collection.
2. **PRISMA defensibility.** Each stage is a separate funnel level with its own count. The PRISMA dashboard can show "rejected at metadata: N" and "rejected at abstract: M" rather than collapsing both into one "screened out" bin.
3. **Scraper budget protection.** PDF retrieval (especially via `scidownl`, which proxies to Sci-Hub mirrors) is the politically and ethically loaded step. Forbidding it before triage ACCEPT is the right policy default.

### Where the Four Scrapers Plug In

| Scraper | Stage | Purpose | Notes |
|---------|-------|---------|-------|
| **SerpAPI** (`google_scholar` engine) | Harvest | Generates candidate references from gap-driven Boolean queries | Already in Task 3 spec. Costs ~1 credit per query, free 250/month. Returns title, link, snippet — *not* full abstract or DOI reliably. Writes rows with `discovered_via = 'serpapi_scholar'`. |
| **`scholarly`** (Python pkg, scrapes Google Scholar HTML) | Harvest (free fallback) | Same purpose as SerpAPI but free; rate-limited and prone to CAPTCHA blocks | Use as fallback when SerpAPI quota exhausted. Brittle; document as best-effort. Writes `discovered_via = 'scholarly_search'`. |
| **`paper-scraper`** (a.k.a. `paperscraper`, scrapes arXiv / bioRxiv / medRxiv / chemRxiv / PubMed) | Harvest (preprint channel) | Generates candidate references from preprint servers — captures unpublished work and recent posts not yet indexed by Scholar | Free. Best for high-VOI gaps where the literature is moving fast. Writes `discovered_via = 'paperscraper_search'` with venue tag. |
| **`scidownl`** (PDF downloader via Sci-Hub mirrors) | **Stage 3 only**, last-resort | Acquires PDFs after triage ACCEPT when Unpaywall and OpenAlex OA both fail | Ethically and legally fraught — must be last-resort, must be logged with `pdf_acquisition_last_source = 'scidownl'`, must be opt-in via config flag (`enable_paid_or_grey_sources`). Document limits to students explicitly. |

### Concrete Placement in the AF Codebase

* `search/serpapi_scholar.py` — new module, called from a new `search_runner.py` CLI command. Writes to `article_references`.
* `search/scholarly_scraper.py` — new module, parallel structure, used as quota-exhausted fallback.
* `search/preprint_harvester.py` — wraps `paperscraper`. New module.
* `ingest/pdf_downloader.py` — *extend* the existing module to add a `scidownl` source class behind a feature flag. Do not write a parallel downloader.
* `triage/metadata_triage.py` — new module for Stage 1 (the cheap classifier pass).
* `triage/abstract_triage.py` — the module Task 3 already names; this is Stage 2.
* `triage/funnel_state.py` — small helper that walks an `article_references` row through the stages and updates `triage_stage` atomically.

### Triage Rule (Recommendation in One Paragraph)

A candidate enters `article_references` with `triage_stage = 'metadata_only'`. Stage 1 runs immediately at ingest: title + venue go through the `atlas_shared` classifier; if classifier confidence is below a threshold (suggested: 0.20) the row is set to `triage_stage = 'rejected_at_metadata'` and never enriched further. Survivors move to Stage 2 in a separate batch job: the four-source abstract chain is called, then `score_voi()` runs on the abstract; rows with classifier on-topic AND VOI ≥ 0.5 become `triage_decision = 'ACCEPT'` and `triage_stage = 'pdf_retrieved'` *only after* Stage 3 completes. PDF retrieval is a separate worker that reads the `v_acquisition_queue` view and calls the source cascade. Each transition is mirrored in `lifecycle_transitions` so the PRISMA funnel reconstructs from audit history rather than from current state alone.

---

## End of Reconnaissance

The four pieces CW asked for are now grounded in concrete file paths and existing code: (a) AE's `extract_neuro_key_review_references.py` is the reference-harvesting prior art, (b) the `article_references` table DDL above is the wiring, (c) the three-stage funnel is the triage rule, (d) the four scrapers plug in at the harvest stage (SerpAPI / `scholarly` / `paper-scraper`) and the acquisition stage (`scidownl`) with the existing AF modules as their integration points. CW has what is needed to write t2_intro / t2_task2 / t2_task3 updates without further reconnaissance.
