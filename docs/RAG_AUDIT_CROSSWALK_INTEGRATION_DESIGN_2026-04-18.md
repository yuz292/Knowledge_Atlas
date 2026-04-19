# RAG-audit integration with Codex's topic crosswalk — design only

*Date*: 2026-04-18
*Author*: CW (design only; not implemented per DK 2026-04-18: hold on implementation until Codex finishes the topics work)
*Depends on*: `data/ka_payloads/topic_crosswalk.json` (Codex, in progress); `ka_article_endpoints.py classify_single_paper` endpoint (Codex, landed `f87c2c9`); `scripts/rag_harvest.py`, `scripts/rag_classify_check.py` (CW, landed `7eb912b`); `160sp/rubrics/t2/T2.d.2_rag_audit.md` (CW, landed `94becac` + §11 in `7eb912b`).
*Scope*: specifies the three-way integration across Codex's classifier, Codex's crosswalk, and CW's RAG harvest plumbing. Does not implement it.

---

## 1. What changes in the RAG-audit workflow, in one paragraph

Codex's `classify_single_paper` endpoint turns `rag_classify_check.py` from an audit of *papers already in our corpus* into an audit of *whatever the RAG returns*, because any RAG-returned paper that is not yet in `pipeline_registry_unified.db` can now be classified on demand. Codex's `topic_crosswalk.json` adds a second upgrade on top: instead of comparing a RAG's claim against raw `(topic_category, topic_subcategory)` columns, we compare it against a *defended topic bundle* with a known outcome cluster, known architectural family, known theory set, known paper list, and an explicit `evidence_status`. The student's disagreement report moves from "the RAG said X, our classifier said Y" to "the RAG said X, our defended bundle B says Y, and these are the specific papers / theories / measures B was constructed from". That is a stronger pedagogical artefact and a stronger training signal for the next classifier revision.

## 2. The three-way integration

The RAG audit pipeline becomes a sequence of four stages per student query:

1. **Harvest** (existing, unchanged). `scripts/rag_harvest.py` queries each service listed in `data/rag_services.yaml`; each adapter returns a normalised JSON with a paper list plus per-paper RAG claims.

2. **Resolve or classify** (new step, replaces the DOI-lookup-or-unknown dichotomy). For every harvested paper:
   - DOI is in our corpus (`papers.doi` match): read its pre-computed `topic_category`, `topic_subcategory`, `canonical_article_type`.
   - DOI is not in our corpus: POST `{title, abstract}` to `ka_article_endpoints.classify_single_paper`; receive the same fields as live output.
   - POST fails or abstract is empty: mark the row `classifier_error` and move on (do not fabricate a label).

3. **Bundle lookup** (new step, uses crosswalk). Using the paper's classified `(iv_root, dv_focus)` pair, look up the matching crosswalk row. This yields the defended `topic_id`, `topic_label`, `theories`, `fronts`, `paper_ids`, `common_measures`, and — critically — `evidence_status` and `outcome_term_match_status`. These last two fields tell us whether the disagreement is worth reporting: a disagreement against an `unresolved` row is less interesting than one against a `defended` row.

4. **Disagreement tagging** (extended). The existing `agreement_flag` (`agree` / `service_disagreement` / `our_disagreement` / `unknown_to_us` / `mixed`) remains. Three new flags are added:
   - `agree_with_defended_bundle` — RAG and our classifier both land the paper in the same defended crosswalk row.
   - `agree_with_mixed_bundle` — same, but the bundle's `evidence_status` is `mixed` (weaker signal).
   - `our_disagreement_with_defended_bundle` — RAG returned a paper our classifier placed in a different cell from the one the RAG implied; and the RAG's implied cell is a defended crosswalk row. This is the most pedagogically rich disagreement type: a defended bundle missed something a RAG caught, or the RAG overclaims against a surface our classifier judges defended.

## 3. The new `classifier_check.csv` schema

Current columns (from the landed rubric in `94becac`):

```
doi, title, services_returning_it,
service_claimed_relevance, service_claimed_verdict,
our_paper_id, our_topic_category, our_topic_subcategory,
our_canonical_article_type, our_canonical_primary_topic,
our_classification_confidence, agreement_flag
```

Added columns after integration:

```
classified_live          (bool)    — was this paper classified on-demand via the endpoint?
live_classification_latency_ms (int)— endpoint round-trip; for cost tracking
crosswalk_topic_id        (text)   — the defended bundle, if any
crosswalk_evidence_status (text)   — 'defended'|'mixed'|'working'|null
crosswalk_outcome_match   (text)   — 'exact_term_id'|'override'|'unresolved'|null
crosswalk_theories        (json)   — theories attached to the bundle
crosswalk_fronts          (json)   — fronts attached to the bundle
```

These are fields the student's `disagreement_report.md` can cite directly: "service X returned paper P; our live classifier placed P in the defended bundle B = `luminous__affect_negative_stress`; the paper's abstract matches B's theory set (SRT, ART) and the service's claimed relevance of 0.91 is consistent; we agree. But service Y returned paper Q with a claimed 'supports' verdict, and our classifier placed Q in the `mixed` bundle `material__affect_preference`; the service's implied bundle would have been `material__affect_negative_stress`, which IS a defended bundle, and neither Q's method nor its measure (from the bundle's `common_measures`) appears in Q's text — the service is overreaching."

## 4. The fallback contract (DK's robustness requirement)

DK's explicit requirement: "the fallback is utterly robust and completely implemented." The fallback path fires in three scenarios:

1. The Knowledge Atlas backend is not running (HTTP connection refused).
2. The backend is running but the `classify_single_paper` endpoint returns 4xx/5xx or times out.
3. The backend is running but the paper cannot be classified (empty abstract, corrupted JSON, classifier internal error).

In all three cases, `rag_classify_check.py` falls back to an **in-process classifier call** by `import`ing `atlas_shared.classifier_system.AdaptiveClassifierSubsystem` and invoking `.classify_article(title, abstract)` locally. This is the same code path Codex's endpoint wraps, so the result shape is identical and downstream code does not need to branch on "was this HTTP or in-process?" The CSV records which path was used in a new `classified_via` column (`http` | `in_process` | `none`), so a run with systematic HTTP failures is diagnosable without re-running.

Robustness checklist:

- **Timeout**: every HTTP call has a 10-second timeout; no request blocks the classifier loop indefinitely.
- **Retries**: one retry on 5xx (backends can hiccup during deploys); no retry on 4xx (a 4xx means the request is malformed and retrying won't help).
- **Batch limit**: no more than 20 simultaneous in-flight HTTP calls (respects the backend's session limits).
- **In-process warm-up cost**: the `AdaptiveClassifierSubsystem` takes ~ 2–5 seconds to initialise on first call; the fallback caches the instance as a module-level singleton so subsequent calls are fast.
- **Both paths logged**: every classification writes a line to `160sp/tracks/t2/{student_id}/T2.d.2/classify.log` with the path taken, the DOI, the latency, and the resulting labels. This log is part of the audit trail and is referenced from the student's disagreement report.

## 5. What still needs DK input before implementation

1. **Services list** — still needed for the adapters. The harvest skeleton is in place but every service adapter is a stub until DK names the real list.
2. **Backend URL** — where does `ka_article_endpoints` live when running? Local dev at `http://localhost:8000`, production at `https://xrlab.ucsd.edu`, or another host? This determines the default URL for the HTTP path of the fallback.
3. **Option A point allocation** — absorb T2.e into T2.d.2? Still pending.

## 6. What I will *not* do until Codex finishes topics

Per DK's instruction ("make your plans but not yet implement them until you can see what codex does and whether it requires you to alter yr plans"):

1. No code changes to `scripts/rag_classify_check.py` yet.
2. No extension of `classifier_check.csv` yet.
3. No production use of `topic_crosswalk.json` — I have read it (102 rows, 18 outcomes, 9 families, consistent with the audit) and designed against it, but will not wire the lookup until Codex has published the canonical builder and the payload has stabilised.
4. No new service adapters for `rag_harvest.py` — the stubs remain stubs until the services list is confirmed.

## 7. What I will do when Codex's topic work is stable

In order:

1. Read Codex's canonical builder (`scripts/build_ka_adapter_payloads.py`) and confirm the payload shape I designed against matches the shipped payload.
2. Extend `classifier_check.csv` with the 7 new columns listed in §3.
3. Write the fallback-with-in-process path in `rag_classify_check.py`, covering all three failure scenarios from §4.
4. Update `T2.d.2_rag_audit.md` §11 to reference the defended-bundle-level disagreement flags.
5. Regression-test the whole pipeline with `--dry-run` data, confirming the CSV has the new columns populated and the fallback path fires correctly when the backend is explicitly killed.
6. Write a second exemplar pass for T2.d.2 bands that reflects the richer data surface (the current exemplars in `t2/exemplars/T2.d.2_band{0..3}.md` do not exist yet and will need authoring regardless).

Total time when unblocked: ~ 3–4 hours.

## 8. Risks and open questions

1. **Endpoint availability in student environments.** Students will run `rag_harvest.py` + `rag_classify_check.py` on their own machines for T2.d.2. They need either (a) a live KA backend at a URL they can reach or (b) `atlas_shared` installed locally so the fallback path works. Option (b) needs a dependency pinning sprint. Worth flagging before the cohort starts.
2. **Crosswalk drift during the sprint.** Codex's builder regenerates the crosswalk payload from multiple sources. If the crosswalk changes mid-sprint (e.g., a topic is reassigned to a different outcome cluster), dossiers that cite a specific bundle may become stale. Mitigation: dossiers include `crosswalk_version` in their metadata, and re-grading after a crosswalk regeneration is explicit.
3. **Classifier-endpoint cost.** The in-process fallback is free; HTTP calls to a production server that runs `atlas_shared` are free (DK's infra). But if a student queries an RAG that returns 200 papers, and 150 of them are not in our corpus, that is 150 classifier calls. The backend should be sized for this load or the batch path should throttle. A 150-paper run at ~ 0.5 seconds per paper = 75 seconds end-to-end, which is acceptable but needs a progress indicator in the student-facing runner.

## 9. References

Roberts, J. C. (2007). State of the art: Coordinated and multiple views in exploratory visualization. *CMV 2007 Proceedings*, 61–71. https://doi.org/10.1109/CMV.2007.20 (Google Scholar: 920+) — for the three-way integration pattern.

Shneiderman, B., &amp; Plaisant, C. (2016). *Designing the user interface: Strategies for effective human-computer interaction* (6th ed.). Pearson. (Google Scholar: 18,000+) — on direct-manipulation patterns, relevant for the student-facing runner's error-reporting surface.

Wang, S., Scells, H., Koopman, B., &amp; Zuccon, G. (2024). Can ChatGPT write a good Boolean query for systematic review literature search? *British Medical Journal*, 385, q1018. https://doi.org/10.1136/bmj.q1018 (Google Scholar: 95+) — on the RAG-service failure modes the audit is designed to surface.
