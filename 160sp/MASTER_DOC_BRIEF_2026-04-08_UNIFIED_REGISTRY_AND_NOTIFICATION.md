# Master Doc Brief: Unified Pipeline Registry and Notification Architecture

**Date**: 2026-04-08
**Section Target**: §122.13 (appended to PART XV: TECHNICAL IMPLEMENTATION)
**Status**: WRITTEN
**Author**: Claude (CW), with classifier inventory contributions from Codex

---

## §122.13: The Unified Pipeline Registry

### Purpose and Rationale

The unified pipeline registry (`data/pipeline_registry_unified.db`) is the canonical per-paper state database for the ATLAS system. It consolidates metadata, extraction status, downstream integration state, and classification results into a single 162-column table covering all 1,428 papers in the corpus.

Prior to its creation (April 7, 2026), paper state was scattered across multiple databases: `ae.db` (extraction metadata), `pipeline_state.db` (stage completion), `web_persistence_v5.db` (beliefs and classifications), `topic_memberships_v1.json` (topic assignments), and various JSONL files. No single query could answer "what is the complete status of paper X?" — one had to join across five or more sources, each with different schemas and paper-ID coverage.

The registry solves this by maintaining a single row per paper with all state fields. It is populated by two complementary mechanisms: backward sync (batch reconciliation from downstream databases) and write-through notification (real-time updates from classifiers and pipeline stages).

### Schema Architecture (162 Columns)

The 162 columns are organized into logical groups:

**Identity and Bibliographic** (15 columns): paper_id, title, doi, authors, year, venue, abstract, apa_citation, citation_count, zotero_folder, original_filename, acquisition_source, acquisition_method, acquisition_date, acquisition_notes

**PDF and Document State** (15 columns): pdf_path, pdf_path_legacy, pdf_path_production, pdf_pages, pdf_source, pdf_size_bytes, pdf_sha256, pdf_readable, total_chars, has_abstract, has_introduction, has_methods, has_results, has_discussion, has_references

**Structural Features** (12 columns): has_figures, figure_count, has_tables, table_count, has_equations, has_stimuli, n_pages_with_statistics, statistics_pages, theory_pages, structure_summary, references_start_page, has_conclusion

**Mathpix and OCR** (7 columns): has_mathpix, mathpix_dir, mathpix_mmd_path, mathpix_html_path, mathpix_lines_json_path, mathpix_pdf_id, mathpix_status

**Page Images and Crops** (6 columns): page_imgs_dir, page_imgs_count, page_imgs_dpi, crops_auto_pass, crops_needs_review, crops_skipped, crops_on_disk

**Science Writer Summary** (8 columns): sw_summary_path, sw_summary_words, sw_summary_source, sw_summary_model, sw_summary_date, sw_summary_accepted, sw_article_html_path, sw_article_md_path

**Extraction** (14 columns): extraction_json_path, extraction_jsonl_path, n_findings, n_theories_identified, detected_family, classification_confidence, last_extractor, last_extraction_date, extraction_method, extraction_engine_version, extraction_model, article_type, document_kind, is_on_domain

**Gold Standard** (10 columns): gold_submitted, gold_submission_date, gold_directory, gold_status, gold_validation_passed, gold_supervalidation_passed, gold_validation_bad_rows, supervalidation_fail_count, gold_attempts_count, gold_accepted_for_rebuild

**PNU (Neural Underpinning)** (6 columns): pnu_json_path, pnu_html_path, pnu_status, pnu_word_count, pnu_mechanism_count, pnu_model, pnu_date

**Downstream Integration** (20 columns): topic_category, topic_subcategory, bn_node_id, bn_node_label, bn_links, bn_export_path, en_node_id, en_warrant_ids, en_warrant_types, en_links, n_beliefs, belief_ids, web_integration_status, n_constraints_from_paper, n_rules_sourced, rule_ids, n_iv_dv_classifications, n_bn_edges, n_tag_assignments, n_annotations

**Classification (New, April 2026)** (14 columns): article_type_current, article_type_confidence, question_filter_enabled, question_best_verdict, question_best_confidence, question_best_question_id, question_best_bundle_id, question_best_edge_case_kind, question_max_novelty_signal, topic_expansion_candidate_count, new_topic_candidate_count, primary_topic_candidate, primary_bundle_candidate, classification_provenance_json

**Pipeline State** (10 columns): current_stage, current_status, completeness_tier, is_blocked, blocked_reason, is_quarantined, quarantine_reason, overall_quality, field_quality_avg, quality_flags

**Metadata** (3 columns): created_at, last_updated, notes

### Corpus Statistics (as of April 8, 2026)

- **Total papers**: 1,428 (1,341 original + 87 reconciled orphans from PDF-1342 through PDF-1445)
- **Papers with extraction data**: 760 (53.2%)
- **Papers with topic classification**: 726 (50.8%)
- **Papers with EN node assignments**: 760 (53.2%)
- **Papers with BN node assignments**: 697 (48.8%)
- **Papers unextracted, awaiting processing**: 668 (all confirmed CNFA-relevant)

---

## §122.14: The Notification Architecture

### The Write-Through Pattern

The notification architecture (defined in `contracts/REGISTRY_NOTIFICATION_CONTRACT_2026-04-08.md`) replaces periodic batch synchronization with event-driven updates. The core principle: every subsystem that modifies paper state calls `notify_registry()` at the point of computation, rather than writing to a local database and relying on a separate batch job to propagate the data.

This pattern has three advantages. First, it eliminates the latency between computation and registry visibility — a classification result is immediately queryable in the registry rather than waiting for the next backward-sync run. Second, it enforces provenance tracking at the point of origin: every update carries a record of which subsystem produced it, when, and whether it was heuristic-only or LLM-adjudicated. Third, it simplifies the overall data flow architecture by replacing N separate sync pathways with a single notification interface.

### The notify_registry() Function

The core function signature:

```python
notify_registry(
    paper_id: str,
    fields: dict[str, Any],          # {column_name: new_value}
    source_subsystem: str,            # dotted path to classifier/module
    source_type: str,                 # heuristic | llm | ag_adjudication | codex_adjudication | manual
    broker_string: str | None = None, # which model/service if AG/LLM was used
    event_stage: str | None = None,   # lifecycle stage this update corresponds to
    details_json: dict | None = None, # extra per-event JSON for lifecycle history
)
```

Each call atomically updates both databases:

1. The `papers` table in `pipeline_registry_unified.db` (current state)
2. The `lifecycle_events` table in `pipeline_lifecycle_full.db` (historical record)

### Classifier Inventory (9 Subsystems)

The ATLAS system has accumulated nine classifiers across three repositories, authored by three different AI workers (Codex, Claude/CW, and AG). All nine are registered in the notification contract and must use `notify_registry()` when they produce a paper-level judgment:

1. **QuestionArticleRelevanceFilter** (Codex, atlas_shared) — question-level relevance with constitutions
2. **HeuristicArticleTypeClassifier** (Codex, atlas_shared) — lightweight portable article type classification
3. **QuestionBundleRouter** (Codex, atlas_shared) — reverse routing to topic bundles
4. **CLI Adjudicators** (Codex, atlas_shared) — multi-AI adjudication (AG, Claude, Codex)
5. **Structural Pre-classifier** (Claude/CW, AE_recovery) — section-heading-based article type
6. **Rule-based PDF Relevance Filter** (Claude/CW, AE_recovery) — 7-step domain relevance
7. **Question-Article Relevance Filter** (Claude/CW, AE_recovery) — wraps atlas_shared
8. **HierarchicalCentroidClassifier** (Codex, Article_Finder) — embedding-based taxonomy
9. **Question Relevance Gate** (Codex, Article_Finder) — question relevance for triage

### Semantic Edge-Case Distinctions

A critical design requirement: the system preserves three distinct edge-case categories that must not be conflated:

- **near_miss**: a paper that narrowly fails current relevance thresholds but could become relevant with minor boundary adjustments
- **topic_expansion_candidate**: a paper that suggests an existing topic boundary is too narrow — the topic itself should grow
- **new_topic_candidate**: a paper that does not fit any existing topic — it may signal an entirely new domain of inquiry

These distinctions are stored as separate fields (`question_best_edge_case_kind`, `topic_expansion_candidate_count`, `new_topic_candidate_count`) and are independently queryable. The intellectual motivation is that uncertainty about classification (near_miss) is categorically different from signals about the classification system's scope (topic expansion and new topics).

---

## §122.15: The Lifecycle Database

The lifecycle database (`data/pipeline_lifecycle_full.db`) provides event-sourced history for every paper. Where the registry stores current state (one row per paper), the lifecycle database stores the full trajectory (multiple events per paper across 26 stages).

**26 Lifecycle Stages**: acquisition → pdf_retrieval → mathpix_ocr → structural_analysis → indexing → relevance_filter → extraction → gold_validation → super_validation → gold_acceptance → rebuild → web_integration → belief_generation → constraint_generation → rule_generation → iv_dv_classification → tag_assignment → annotation → bn_edge_generation → molecule_linkage → qa_reference → interpretation → question_answering → topic_classification → pnu_generation → site_display

**Current Coverage**: 1,428 papers × 26 stages = 37,128 lifecycle events

**Event Detail Storage**: Each lifecycle event has a `details` JSON field that stores classifier-specific output. The notification contract specifies that event-level fields (question_relevance_summary, bundle_routing_result, edge_case_kind, novelty_signal, proposed_topic_labels, etc.) are stored here rather than as hard columns, following the extensibility pattern established in `paper_lifecycle.py`.

---

## Implementation Files

| File | Location | Purpose |
|------|----------|---------|
| `pipeline_registry_unified.db` | `data/` | 162-column per-paper registry (1,428 papers) |
| `pipeline_lifecycle_full.db` | `data/` | Event-sourced lifecycle history (37,128 events) |
| `notify_registry.py` | `src/services/` | Write-through notification module |
| `run_backward_sync.py` | `scripts/sync/` | Batch reconciliation (6 sync pathways) |
| `reconcile_orphan_papers.py` | `scripts/sync/` | Orphan paper ingestion |
| `build_full_lifecycle_db.py` | `scripts/sync/` | Lifecycle DB rebuild |
| `BACKWARD_SYNC_CONTRACT_2026-04-07.md` | `contracts/` | Backward sync contract |
| `REGISTRY_NOTIFICATION_CONTRACT_2026-04-08.md` | `contracts/` | Notification contract |

---

## Querying the Registry

```sql
-- Papers flagged as topic-expansion candidates
SELECT paper_id, primary_topic_candidate, topic_expansion_candidate_count
FROM papers WHERE topic_expansion_candidate_count > 0;

-- Papers flagged as new-topic candidates
SELECT paper_id, new_topic_candidate_count
FROM papers WHERE new_topic_candidate_count > 0;

-- Complete status snapshot for a single paper
SELECT paper_id, title, article_type, current_stage, completeness_tier,
       n_findings, n_beliefs, topic_category, en_node_id, bn_node_id,
       article_type_current, question_best_verdict, primary_topic_candidate
FROM papers WHERE paper_id = 'PDF-0042';

-- Field coverage audit
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN title IS NOT NULL THEN 1 ELSE 0 END) as has_title,
  SUM(CASE WHEN n_findings > 0 THEN 1 ELSE 0 END) as has_findings,
  SUM(CASE WHEN topic_category IS NOT NULL THEN 1 ELSE 0 END) as has_topic
FROM papers;
```

---

*End of brief. This content should be appended to the master document as §122.13–§122.15, following the existing §122.12 (End-to-End Pipeline Integration).*
