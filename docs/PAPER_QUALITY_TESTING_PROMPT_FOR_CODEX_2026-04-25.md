# Paper-Quality Testing Prompt — for Codex (Adversarial Pass)

**Document**: `PAPER_QUALITY_TESTING_PROMPT_FOR_CODEX_2026-04-25.md`
**Target executor**: Codex in terminal, on a fresh checkout of the
three repos *after* the build prompt's twelve commits have landed and
been merged to `master`/`main`.
**Authorising reviewer**: DK, 2026-04-25.
**Companion reading**:
`PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23.md` (the build
prompt this testing pass audits);
`PAPER_QUALITY_PANEL_CONSULTATION_2026-04-23.md` (the methodological
backbone the panel ratified);
`PAPER_QUALITY_SYSTEM_DESIGN_2026-04-23.md` (the ground-truth
specification).

---

## 0. Why this prompt exists

The build prompt itself includes hardening against the failure modes
DK flagged on 2026-04-25: heuristic substitution, parallelisation
that fakes multi-LLM agreement, threshold-gaming on confidences. But
those defences are written into the build process, which means they
can in principle be subverted by code that satisfies the build's own
tests while shipping a degraded extractor. This testing prompt is the
external audit. It runs on a fresh checkout, with no state shared
with the build's processes, and probes the same failure modes from
outside.

The testing pass is a *gate*, not a *suggestion*. Until every probe
in this document passes, the paper-quality layer does not run on real
papers. The build's smoke tests are insufficient on their own. Both
gates must clear.

A second-order purpose: when the layer eventually fails on a real
paper in production, this testing prompt is the first place we look.
The probes should produce diagnostic output rich enough to localise
the failure rather than merely flag it.

---

## 1. Pre-flight

```bash
# Confirm the build has landed on all three repos' protected branches.
cd /Users/davidusa/REPOS/atlas_shared && git checkout master \
    && git pull --ff-only && git log --oneline -5

cd /Users/davidusa/REPOS/Knowledge_Atlas && git checkout main \
    && git pull --ff-only && git log --oneline -5

cd /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery \
    && git checkout <main-branch> && git pull --ff-only \
    && git log --oneline -5

# Create the testing branch in each repo. All testing-pass changes go
# here; if the testing pass surfaces fixes, they ship as fix commits
# on this branch and are merged in a separate PR.
cd /Users/davidusa/REPOS/atlas_shared \
    && git checkout -b paper-quality-testing-2026-04-25
cd /Users/davidusa/REPOS/Knowledge_Atlas \
    && git checkout -b paper-quality-testing-2026-04-25
cd /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery \
    && git checkout -b paper-quality-testing-2026-04-25

# Install the testing dependencies (a small extra set beyond what the
# build needs):
pip3 install --break-system-packages \
    'pytest-recording==0.13.*' \
    'hypothesis==6.*' \
    'tiktoken==0.5.*' \
    'jaccard-distance==0.3.*'
```

The testing prompt assumes the build's own pytest suites pass on the
fresh checkout. If they do not, stop and post the failure to
`COORDINATION.md` under `### CW paper-quality testing — pre-flight
fail` before proceeding.

---

## 2. Probes — the nine adversarial tests

Every probe below produces three outputs: a pass/fail verdict, a
machine-readable diagnostic JSON written to
`reports/paper_quality_testing_<probe_id>_<timestamp>.json`, and a
two-paragraph human-readable summary in
`reports/paper_quality_testing_summary_2026-04-25.md`. Probes run in
order; later probes assume earlier ones passed.

### Probe 1 — Heuristic-detection (LLM-required-fields canary)

**Goal**: confirm Hard Rule 7 — that the seven semantic fields are in
fact extracted by LLM call rather than by regex or keyword match.

**Procedure**: for each of the seven LLM-required fields:

1. Run the extractor on a known-good fixture from the calibration set.
   Record the field's extracted value.
2. Patch `atlas_shared.llm_adapter.call_llm` and the OpenAI-class
   equivalent so that every call raises
   `RuntimeError("LLM disabled for canary test")`.
3. Re-run the extractor on the same fixture.
4. Assert that the extractor either (a) raises the same RuntimeError
   or (b) routes the field to adjudication with confidence 0.0. Any
   other outcome — particularly a successful extraction under patched
   LLMs — is a fail.

**Pass criterion**: all seven fields fail under LLM-disabled mode.

**Diagnostic on failure**: which field succeeded, and the call stack
of the function that produced the value. The stack will localise the
heuristic shortcut.

### Probe 2 — Model-call audit (multi-LLM independence)

**Goal**: confirm Hard Rule 8 — that the Claude-class and OpenAI-class
adapters run as independent processes with no output-sharing.

**Procedure**:

1. Instrument both adapters' `call_llm` entry points to log every
   request to `logs/llm_audit_<timestamp>.jsonl`. Each log line:
   `{paper_id, field, model, prompt_hash, response_hash, ts, pid,
   parent_pid}`.
2. Run the extractor across the 24-fixture set (20 anchor + 4
   adversarial).
3. After the run, parse the audit log and assert:
   (a) every paper produced ≥ N Claude-class calls and ≥ N
   OpenAI-class calls where N = number of LLM-required fields;
   (b) no Claude-class `response_hash` appears as the `prompt_hash`
   or substring-of-`prompt_hash` for any OpenAI-class call on the
   same paper, and vice-versa;
   (c) the `pid` for Claude-class calls and OpenAI-class calls on
   the same paper differ (independent processes).

**Pass criterion**: all three sub-assertions hold across all 24
papers.

**Diagnostic on failure**: which paper, which assertion, and the
offending log lines.

### Probe 3 — Deterministic-output detection

**Goal**: confirm that LLM calls are not being short-circuited by a
deterministic cache or by a regex that returns identical output every
time.

**Procedure**:

1. For each of the seven LLM-required fields, run the extractor three
   times on the same fixture at temperature 0.3 with the audit log
   active.
2. Compute self-consistency variance:
   - For list-valued fields (rhetorical flags, effect sizes,
     sample-composition entries): mean Jaccard similarity across the
     three runs.
   - For numeric fields (effect-size precision, multiple-comparisons
     count): coefficient of variation across the three runs.
   - For categorical fields (construct-validity verdict, document
     type): Krippendorff's alpha across the three runs.
3. Assert that variance falls within the expected envelope per
   field. The envelope is calibrated from the build's Pass 2
   self-consistency report; this probe re-runs and compares.
4. Specifically assert that no LLM-required field has *zero*
   variance across three samples on the calibration set as a whole.
   Zero variance on a field where legitimate paper-to-paper variation
   is documented indicates a deterministic shortcut.

**Pass criterion**: variance envelope respected for every field.

**Diagnostic on failure**: which field, observed variance, expected
envelope.

### Probe 4 — Paper-type variance check

**Goal**: confirm the extractor produces distinct fingerprints across
paper types — a single template would produce convergent fingerprints
that betray the shortcut.

**Procedure**:

1. Run the extractor on the four adversarial fixtures plus four
   normal fixtures spanning lab experiment, field study,
   meta-analysis, and theoretical paper.
2. Compute pairwise fingerprint distance using a domain-aware metric:
   - effect-size structure (count, type, range)
   - sample structure (N, country composition, recruitment)
   - design-type categorical
   - construct-validity narrative semantic distance (cosine over
     embedded text)
3. Assert that fingerprints across paper types cluster appropriately:
   the meta-analysis is closer to the systematic review than to the
   theoretical paper; the lab experiment is closer to the field
   study than to the meta-analysis; etc.

**Pass criterion**: cluster structure matches the panel's expected
typology with ≥ 0.7 silhouette score.

**Diagnostic on failure**: the distance matrix and the offending
clustering.

### Probe 5 — Confidence-distribution audit

**Goal**: confirm Hard Rule 9 — that confidence is not threshold-gamed.

**Procedure**:

1. Across the 24-fixture set, collect every per-field point
   confidence. Bin into 20 bins from 0.0 to 1.0.
2. Assert that the empirical distribution does not have a spike at
   any single bin in the 0.85–0.90 range. A spike is defined as a bin
   count ≥ 1.5× the mean of its two neighbours.
3. Assert that the distribution has a non-zero mass in at least 8 of
   the 20 bins. A field whose confidence lands in fewer than 8 bins
   across 24 papers is suspiciously low-variance.
4. Assert that the per-token logprob mean (Hard Rule 9 part b)
   correlates positively with the point confidence at r ≥ 0.5
   across the 24-fixture set. A confidence value not anchored in
   logprob structure is a fabricated heuristic value.

**Pass criterion**: all four sub-assertions hold.

**Diagnostic on failure**: the histogram and the correlation plot.

### Probe 6 — V7 lifecycle integration

**Goal**: confirm the new pipeline stages 18 and 19 fire correctly
and the auxiliary tables are populated.

**Procedure**:

1. Take a single fresh paper not in the calibration set, drop it
   into the V7 pipeline input box.
2. Watch the lifecycle event stream and assert that events fire for
   every stage 1 through 30 in order, with the new
   `paper_quality_extraction` (stage 18) and
   `paper_quality_finalisation` (stage 19) events present and
   carrying the expected payload schemas.
3. After completion, query `pipeline_lifecycle_full.db` and assert
   the three auxiliary tables (`fingerprint_staging`,
   `quality_adjudication_queue`, `quality_calibration_history`) have
   the expected rows for this paper.
4. Re-apply the migration script
   (`scripts/migrations/2026_04_23_paper_quality.sql`) to a fresh DB
   copy and assert idempotency: row counts unchanged, schema
   unchanged, no errors.

**Pass criterion**: all four sub-assertions hold.

**Diagnostic on failure**: the lifecycle event stream and the SQL
diff.

### Probe 7 — Anchor-set regression

**Goal**: confirm the extractor's outputs on DK's 20-paper anchor set
align with DK's sidecar ratings within an acceptable margin.

**Procedure**:

1. Load DK's anchor-set ratings from
   `atlas_shared/tests/fixtures/paper_quality_calibration/dk_sidecar_ratings.json`.
2. Run the extractor on every anchor-set paper.
3. For each of the four sidecar fields (construct-validity verdict,
   generalisation envelope, methodological severity, theoretical
   importance), compute agreement:
   - Construct-validity verdict (categorical, 5 levels): exact match
     rate; weighted κ allowing one-step ordinal slip.
   - Generalisation envelope (categorical, 4 levels): same.
   - Methodological severity (numeric, 1–5): Spearman ρ; mean
     absolute difference.
   - Theoretical importance (numeric, 1–5): same.
4. Assert that exact-match rate ≥ 60 % for each categorical sidecar
   and that mean absolute difference ≤ 1.0 for each numeric sidecar.
5. Flag any anchor paper where the model verdict differs from DK's by
   more than one ordinal step on any sidecar field; these go into the
   adjudication queue for DK review.

**Pass criterion**: thresholds met across the anchor set.

**Diagnostic on failure**: confusion matrix per sidecar field.

### Probe 8 — Cross-repo dependency test

**Goal**: confirm the dependency on `atlas_shared.paper_quality` is
real and tight, not vestigial.

**Procedure**:

1. Confirm `from atlas_shared.paper_quality import
   PaperQualityFingerprint` succeeds in both Knowledge_Atlas/backend
   and Article_Eater_PostQuinean_v1_recovery's test environments.
2. Make a temporary local commit on `atlas_shared` that renames
   `PaperQualityFingerprint` to `PaperQualityFingerprintV2`.
3. Re-run pytest in Knowledge_Atlas/backend and Article_Eater. Both
   suites must fail on import. If either still passes, the dependency
   is shadowed by a local copy somewhere in the consuming repo, which
   is a violation of the "Do Not Reinvent" contract and a signal that
   `atlas_shared` is not actually the source of truth.
4. Revert the temporary commit; re-run both suites; both must pass.

**Pass criterion**: both consumer repos fail under the renamed import
and pass when restored.

**Diagnostic on failure**: the consumer that did not fail, and the
location of the shadow definition.

### Probe 9 — Adjudication-queue behaviour under load

**Goal**: confirm the adjudication queue handles forced disagreements
and confidence-floor routing correctly under realistic batch input.

**Procedure**:

1. Construct a batch of 50 synthetic papers spanning fingerprint
   profiles: 10 high-confidence-no-disagreement, 10 with one
   forced-disagreement field, 10 with low confidence on construct
   validity, 10 with the OSF-mentioned-but-not-prereg pattern, 10
   theoretical papers.
2. Submit the batch to the V7 pipeline.
3. After the batch completes, query the adjudication queue and
   assert:
   - The 10 high-confidence-no-disagreement papers contribute zero
     items to the queue.
   - The 10 forced-disagreement papers each contribute exactly one
     item (the disagreement field) with both candidate verdicts
     visible.
   - The 10 low-construct-validity papers each contribute exactly
     one item with the source excerpts attached.
   - The 10 OSF-mentioned papers each contribute the
     preregistration-status field with the discussion paragraph
     quoted.
   - The 10 theoretical papers contribute zero items because the
     fields requiring sample-based adjudication are correctly marked
     "skip" with `expected = False`.
4. Adjudicate three items via the admin UI; assert the
   `quality_calibration_history` table records the adjudication with
   the WEIGHTING_FUNCTION_VERSION.

**Pass criterion**: all five queue-shape assertions plus the
adjudication-history assertion hold.

**Diagnostic on failure**: the queue contents and the missing or
extra items.

---

## 3. Success conditions

The testing pass is **green** when:

- All nine probes pass.
- The summary report
  (`reports/paper_quality_testing_summary_2026-04-25.md`) lists every
  probe with verdict and metric.
- A diagnostic JSON exists for every probe (passing probes still log
  metrics, not just verdicts).
- No probe required a build-side fix to pass — i.e. the layer as
  shipped from the build prompt cleared every probe without changes.

The testing pass is **amber** when:

- All probes pass but one or more required a small build-side fix
  shipped as a commit on `paper-quality-testing-2026-04-25`. The fix
  must be reviewable by DK and merged in a separate PR before the
  layer goes live.

The testing pass is **red** when:

- Any probe fails after the build-side fix attempt.
- The diagnostic shows a failure mode this prompt was designed to
  catch (heuristic substitution, multi-LLM faking, threshold gaming,
  paper-type insensitivity).
- The adjudication queue does not behave as Probe 9 specifies.

A red verdict halts the layer indefinitely. The build prompt is
re-opened for revision; DK reviews the failure mode; the build is
re-run.

---

## 4. Non-goals (what this prompt does NOT do)

- **No new feature work.** The testing pass adds no fields, no
  endpoints, no UI components. Anything beyond test code, audit
  instrumentation, and the report files is out of scope.
- **No retrofit on the existing 1 400-paper corpus.** That happens
  separately after both gates clear.
- **No changes to the build prompt.** If a probe surfaces a need to
  change the build prompt's rules, file a `### CW paper-quality
  testing — rule change request` in `COORDINATION.md` and wait for
  DK. Do not edit the build prompt from inside the testing branch.
- **No interpretation-layer integration.** That is a separate build
  pass (PQ-INTERP-001) that ships after the main layer is live.
- **No COGS 160 Fall pedagogical adaptation.** Out of scope; that is
  PQ-160F-001.

---

## 5. Reporting

At the end of the testing pass, post to `COORDINATION.md` under
`### CW paper-quality testing — landed`:

- The probe-by-probe verdict table (probe ID, verdict, metric).
- The summary verdict (green / amber / red) with one-paragraph
  justification.
- The list of any build-side fix commits and their SHAs (amber case
  only).
- The list of any items that landed in the adjudication queue during
  Probe 9 and require DK review.
- Wall-clock time per probe and total wall-clock time.
- Any deviations from this prompt and why.

If the verdict is amber or red, also post the failing probe's
diagnostic JSON path so DK can inspect.

Tag CW on `COORDINATION.md` when done.

---

## 6. Failure handling

If any probe fails in a way that is not a simple test-code fix, stop
and post the failing probe ID, the diagnostic JSON path, and a
one-sentence hypothesis to `COORDINATION.md` under
`### CW paper-quality testing — blocker`. Do not adjust the probe's
pass criterion to make it pass; the criteria are the contract.

If the testing pass discovers that a build-prompt rule is genuinely
unworkable (not merely inconvenient), file the rule-change request
per Section 4 and wait. Do not relax the rule from the testing
branch.

---

## 7. Timeline

The testing pass is a one-day run. Probes 1–5 are roughly one hour
each on the calibration set; Probes 6–9 are between thirty minutes
and two hours each depending on whether the V7 lifecycle DB needs to
be reset between runs. Total wall-clock time should not exceed eight
hours.

If any probe exceeds two hours of wall-clock time, post progress to
`COORDINATION.md` and continue.

---

## 8. After the testing pass

On a green verdict, the paper-quality layer goes live for new papers
the next time the V7 pipeline runs. The retrofit pass on the existing
1 400-paper corpus follows on a schedule DK sets.

On an amber verdict, the build-side fix commits merge first; the
testing pass re-runs (only the affected probes); on the second green,
the layer goes live.

On a red verdict, the layer does not go live. The build prompt is
re-opened, the panel is re-convened if necessary, and the build is
redone.

---

*End of testing prompt. Companion build prompt:
`PAPER_QUALITY_BUILD_PROMPT_FOR_CODEX_2026-04-23.md`. Together they
form the two-gate pattern: build first, test second, both must clear
before real papers see the new layer.*
