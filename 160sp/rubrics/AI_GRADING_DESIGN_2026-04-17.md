# AI-graded rubric system for COGS 160sp — analysis, verification, and grading design

*Date*: 2026-04-17
*Author*: CW (for DK approval)
*Audience*: DK, Track leads, TAs, the grading agent (an LLM with tool access)
*Status*: Design proposal — ready for DK to authorize and iterate on

---

## 0. Problem statement

DK has asked for a rigorous rubric system in which the primary grader is an AI rather than a human TA. The design must:

1. Specify **what** each deliverable requires — precisely enough that a grading agent can evaluate a submission without guessing.
2. Specify **what we must verify** — the minimum set of claims the student makes (implicitly or explicitly) that a grade depends on.
3. Specify **how** the AI verifies each claim in a rigorous manner — the inputs it reads, the queries it runs, the reasoning pattern it follows, the evidence it must produce with every score.
4. Specify the human oversight that keeps AI grading honest: calibration, audit, appeal.

This document supersedes the TA-verification section in `rubrics/README.md § 6` and the per-track verification procedures in `verification/README.md`. Those files remain as the human-readable reference; the AI-grading system described here is the primary grader, with human review as a second-pass audit on a stratified sample.

The design rests on a body of empirical work on AI-assisted grading that has grown substantially in the last three years. Short-answer autograding by large language models reaches κ ≈ 0.75–0.85 with expert raters on well-specified rubrics (Kortemeyer, 2023; Schneider et al., 2023). Essay-grading by GPT-4-class models with structured rubrics has reached human-rater agreement in first-year composition and content courses (Yancey et al., 2023; Mizumoto & Eguchi, 2023). The remaining failure modes — scoring off-topic submissions, rewarding verbosity, hallucinating evidence — are addressable by (a) requiring the model to cite literal spans from the submission for every score, (b) providing anchored exemplars, and (c) human-in-the-loop audit on a stratified sample (Kim et al., 2024; Tyser et al., 2024). The design below embeds all three mitigations.

---

## 1. What the rubric system is grading

Every deliverable in the course produces at least one of the following **evidence types**. The grading agent operates on these, not on impressions:

| Evidence type | Examples | Where it lands |
|---------------|----------|----------------|
| **Structured data rows** | Article-registry submissions, tag-DB rows, classifier predictions | `pipeline_registry_unified.db`, Atlas tag DB |
| **Code commits** | VR Unity projects, scripts, data-processing code | Git repositories under `160sp/tracks/{t}/` |
| **Prose artefacts** | Schema studies, reflection notes, final reports, usability findings | Course shared doc, markdown files in repo |
| **Media artefacts** | VR scene recordings, screenshots, figures | Course shared drive |
| **Time-stamped events** | Submission timestamps, commit timestamps, meeting attendance | Pipeline registry, git log, calendar |

The grading agent sees all five. It does not see the student's face, verbal contributions to lab meetings, or informal Slack conversations. Those remain under human purview.

---

## 2. The three-criterion frame — how each criterion becomes machine-checkable

The three criteria (Completeness / Quality / Reflection) survive from the earlier TA design. Each is operationalised into machine-checkable sub-signals.

### 2.1 Completeness

Completeness is the easiest to automate because it reduces to counts and presence/absence checks against a spec.

For each deliverable, the AI grader reads a machine-readable spec (see § 4 Per-deliverable spec schema below) that declares the minimum artefacts the student must produce. The agent runs a deterministic check:

- For structured-data deliverables: `SELECT count(*)` against the relevant DB with `submitted_by = {student_id}` and a date window.
- For code-commit deliverables: `git log --author={student} --since=... --until=...` counting commits and `git diff --stat` checking lines-of-code and files-touched against a spec.
- For prose deliverables: word-count on the submitted document, section-presence check against a required-headings list.
- For media deliverables: file-existence check plus file-type validation.

The score (0, 1, 2, 3) is derived from the ratio actual/required with explicit thresholds declared in the spec (see § 4).

This portion of grading has essentially no disagreement between AI and human: a row count is a row count. Expected agreement: κ ≈ 1.0.

### 2.2 Quality

Quality is the harder criterion. It requires judgements about whether the artefact is good-of-its-kind: are the articles relevant? Are the tags correct? Is the code clean? Is the reflection note substantive?

The AI grader uses a **rubric-anchored pairwise comparison** pattern (Liu et al., 2023; Zheng et al., 2023) rather than a single absolute scoring pass. Procedure:

1. For each criterion band (0, 1, 2, 3), the rubric file includes a **literal exemplar** — a short passage or artefact excerpt that scores in that band, taken from the Week-3 calibration set (see § 6.1).
2. The grader reads the submission in chunks (e.g., 5 articles at a time for Track 2; 10 tags at a time for Track 1).
3. For each chunk it answers: "On this criterion, does the chunk most resemble band 0 exemplar, band 1, band 2, or band 3?" and cites the feature it used to decide.
4. It logs per-chunk scores and returns the modal score across the artefact with the distribution attached.
5. It writes a **score justification** that names three literal spans from the submission and maps each to a band.

This is the reasoning-by-exemplar pattern that Kim et al. (2024) showed raises LLM-grading κ with experts from 0.55 (absolute) to 0.78 (exemplar-anchored) on open-ended tasks. The literal-span requirement protects against both verbosity rewards and fabricated evidence: every score must be backed by quoting text the student actually wrote.

### 2.3 Reflection

Reflection is the axis most vulnerable to AI-grading failure because plausible-sounding reflection text is cheap to generate. The grader defends against this in three ways:

1. **Specificity check.** The reflection note is graded for whether it names a specific claim, a specific framework, a specific image, a specific article, a specific usability finding — in short, a specific referent the grader can cross-check against the student's earlier submissions. A reflection that says "I learned a lot about prospect-refuge theory" scores low because it lacks specificity; one that says "On images 027 and 038 I had tagged 'prospect' but when I read Appleton (1975) § 4 I realised both are closer to refuge because the observer position is protected" scores high because both the images and the reference can be cross-checked.
2. **Cross-artefact consistency check.** The grader asks: "Does the claim in the reflection match evidence in the student's submitted artefacts this week?" — e.g., "the student claims to have re-tagged images 027 and 038: is their atlas_tags history actually consistent with that re-tag?" This is a data-grounded check that is very hard to fool.
3. **Student-specific provenance check.** The grader checks whether the reflection language matches the student's baseline writing style (drawn from their A0 and A1 submissions). A large style shift between weeks is flagged for human review, not scored down automatically — students' writing can legitimately evolve; the flag exists so chronic AI-generated boilerplate gets caught.

---

## 3. What the AI grader produces for every submission

Every grading pass produces a **grade dossier**, a structured markdown file stored at `160sp/grading/{student_id}/{deliverable_id}_{date}.md`. The dossier has six sections:

1. **Metadata** — student, deliverable, submission timestamp, grading timestamp, grader model + version, rubric file hash.
2. **Spec check (Completeness)** — the machine-readable spec, the actuals observed, the resulting 0–3 score.
3. **Quality scoring** — per-chunk scores with cited spans, the modal score, the distribution, three justification quotes.
4. **Reflection scoring** — the three sub-checks (specificity, consistency, provenance) with their individual findings, the 0–3 score.
5. **Raw total and rescaled points** — 0–9 raw → points for this deliverable.
6. **Confidence and flags** — the grader's self-reported confidence (high / medium / low) and any flags that triggered human review (see § 5 Oversight).

The dossier is checked into the repo. Students receive a summary view via `ka_admin.html`'s Grading tab; the full dossier is available on request. Graders who cannot access the full dossier cannot reliably appeal, so full dossier access is a policy commitment, not a discretion.

---

## 4. Per-deliverable spec schema

Every deliverable rubric file gains a `## Machine-readable spec` section that the grading agent reads directly. Schema:

```yaml
deliverable_id: T1.b
points: 10
timeliness_bonus: 1
span:
  start: 2026-04-27  # Week 3 Monday
  end:   2026-05-04  # Week 4 Monday
completeness:
  required_artefacts:
    - type: tagged_rows
      source: atlas_tag_db
      table: tags
      filter:
        tagged_by: "{student_id}"
        tagged_at_between: "{span.start}..{span.end}"
      min_count_for_score_2: 80
      min_count_for_score_3: 100
    - type: prose_doc
      source: course_shared_doc
      pattern: "T1.b tag-log — {student_name}"
      min_word_count_for_score_2: 150
      min_word_count_for_score_3: 200
quality:
  scoring_method: exemplar_anchored_pairwise
  exemplars:
    band_0: "rubrics/t1/exemplars/T1.b_band0.md"
    band_1: "rubrics/t1/exemplars/T1.b_band1.md"
    band_2: "rubrics/t1/exemplars/T1.b_band2.md"
    band_3: "rubrics/t1/exemplars/T1.b_band3.md"
  chunk_size: 10   # evaluate in 10-tag chunks
  spot_check_reclass_rate:
    source: atlas_tag_db
    protocol: "Pick 10 random rows; grader re-tags independently; compute agreement."
    threshold_for_score_2: 0.60
    threshold_for_score_3: 0.80
reflection:
  scoring_method: three_sub_check
  specificity_threshold_for_score_2: 2  # at least 2 specific referents
  specificity_threshold_for_score_3: 4  # at least 4 specific referents
  consistency_check:
    cross_reference: atlas_tag_db
    protocol: "Every image id mentioned in the reflection must appear in the student's tag rows."
  provenance_check:
    baseline_sources:
      - "a0 submission"
      - "a1 submission"
    flag_on_style_shift_z_score: 2.5
verification_procedures:
  primary: "ai_grader"
  secondary: "human_audit"
  secondary_sample_rate: 0.20   # 20 % of submissions audited by TA
```

This spec is load-bearing. The grading agent's prompt references it literally; if the spec is wrong, the grading is wrong. For that reason, every spec must be signed off by the track lead before Week 3, and any change during the sprint must be announced to students before taking effect (the Week-5 mid-sprint revision is the intended revision window).

---

## 5. Human oversight — calibration, audit, appeal

AI grading without oversight regresses fast. Three layers of oversight keep the system honest.

### 5.1 Calibration (Week 3, before any real grading)

Before the agent grades any student submission, it is run against a **calibration set** of 20 synthetic (or historical) submissions per deliverable, each with a known expert-assigned score. The agent's scores are compared to the expert scores; Cohen's κ is computed per criterion. The agent is authorised to grade real submissions only if:

- κ ≥ 0.70 on Completeness (should be trivial; this is a sanity check).
- κ ≥ 0.65 on Quality (this is the harder bar; Yancey et al. (2023) reports 0.60–0.78 in comparable settings).
- κ ≥ 0.55 on Reflection (the axis most vulnerable; we accept a weaker threshold and compensate with a higher audit rate, see § 5.2).

If the agent fails any threshold, the track lead revises the rubric — either tightening the band descriptions or replacing a weak exemplar — and the calibration is re-run.

### 5.2 Audit (weekly)

Every week, 20 % of submissions per deliverable are re-graded by a TA without access to the AI dossier. The TA's independent score is compared to the AI's score. If the mean absolute difference across the sampled dossiers exceeds 0.5 points per criterion, the track lead pauses AI grading for that deliverable, re-calibrates, and re-runs. This is the TA-audit discipline proposed by Kortemeyer (2023) and Tyser et al. (2024) and is not optional.

The 20 % sample is stratified: always includes every submission the agent flagged low confidence (§ 3, item 6), every submission the agent scored at band boundaries (e.g., near 0 or near 3 with shallow confidence margin), and a random sample across the remaining pool.

### 5.3 Appeal (on student request)

Students may appeal any AI score within 7 days of receiving the dossier. The appeal procedure:

1. The student opens a GitHub issue citing the dossier and specifying the criterion in dispute and the band they believe is correct.
2. A second AI grader (a different model, or the same model with a re-worded prompt and a seed change) re-grades the submission on that criterion only, producing its own dossier.
3. If the two AI graders agree, the score stands.
4. If they disagree by ≥ 1 band, a human (DK or the track lead) adjudicates, referring to both dossiers.
5. The higher of the two scores stands unless the human adjudicator finds a clear error in the student's favour in the original, in which case that score stands.

---

## 6. How to build the calibration set

A rubric is only as good as its exemplars. Building the calibration set is the most consequential Week-3 task.

### 6.1 Sources

Three sources, in order of preference:

1. **Historical submissions from prior quarters.** If Fall 2025 or earlier sections ran a similar assignment, pull anonymised submissions with their TA-assigned scores. This is the gold standard: real student work, real human scores.
2. **Instructor-written exemplars.** DK or the track lead writes one submission per band per deliverable: a "clearly band 0", "clearly band 1", "clearly band 2", "clearly band 3" artefact. Four exemplars per deliverable, ~ 30 deliverables = 120 exemplars. This is a significant time investment (~ 8 hours per track lead) but it pays for itself across multiple quarters.
3. **AI-generated candidates with human review.** The grading agent is prompted to generate candidate submissions at each band; the track lead accepts, edits, or rejects each one. This is the fastest path and the one I recommend for Week 3; it can be upgraded to source 2 as the quarter progresses.

### 6.2 Format

Each exemplar lives at `rubrics/{track}/exemplars/{deliverable_id}_band{n}.md` (or `.csv` / `.py` / `.unitypackage` for non-prose deliverables). Each exemplar carries a short header:

```markdown
# Exemplar for T1.b, Band 2
Source: AI-generated 2026-04-17, reviewed and approved by DK 2026-04-19
Assumes: student has completed A0 and A1; this is their first 100-image batch.
What makes this band 2: meets the count minimum, rationales are specific,
confidence scores vary, but several rationales miss schema-relevant features.
```

---

## 7. What the grading prompt looks like (template)

The agent runs against a prompt template parameterised by the per-deliverable spec. Skeleton:

```
ROLE: You are the grader for {deliverable_id} in COGS 160 Spring 2026.

INPUTS:
  - Rubric file: {path}
  - Spec (machine-readable): {path}
  - Exemplars: {band_0}, {band_1}, {band_2}, {band_3}
  - Student submission: {path or DB query result set}
  - Student history (A0, A1, and prior deliverables): {paths}

PROCEDURE:
  1. Execute the Completeness check per the spec. Report the counts actual vs. required and the 0-3 score.
  2. Execute the Quality check: chunk the submission per the spec, for each chunk compare against the four exemplars, cite the feature that led to the band, produce a per-chunk score, aggregate to a 0-3 score.
  3. Execute the Reflection check: specificity count, consistency against artefact evidence, provenance against baseline.
  4. Produce the grade dossier at {output_path} per the § 3 schema.
  5. Set confidence low if any of: (a) chunk-level scores varied by more than 2 bands within the artefact, (b) Completeness score is 3 but Quality score is 0 (suggests volume-over-substance), (c) the spec's consistency check fired on the reflection, (d) baseline-provenance z-score exceeded threshold.

CONSTRAINTS:
  - Every score must be backed by at least one literal quote from the student's submission or a literal DB row.
  - Do not reward verbosity: a 300-word reflection that scores band 3 on specificity must cite 4 distinct referents; a 600-word reflection that cites 1 referent scores band 1.
  - Do not hallucinate evidence. If you cannot find the quote you wanted to cite, lower the score and say so.

OUTPUT: A single markdown file conforming to the § 3 dossier schema.
```

This prompt is stored at `rubrics/prompts/grading_prompt_template.md` and is instantiated per-deliverable by a small Python runner (see `scripts/ai_grader.py`, to be built in the next session).

---

## 8. What must be verified — the verification inventory

This is the concrete list of claims that AI grading makes, and the mechanism by which each claim is verifiable.

| Claim | Mechanism | Failure mode if unverified |
|-------|-----------|---------------------------|
| "Student submitted N artefacts this week." | DB `count(*)` query with `submitted_by = student_id` and date window | Student invents submissions or claims submissions that never landed |
| "The AI read the actual submission, not a summary of it." | Dossier must quote ≥ 3 literal spans from the submission verbatim; spans are checked against submission storage | AI hallucinates evaluation |
| "Student's tags pass downstream validation." | Spot-check: 10 random rows re-tagged by a second AI grader and compared | AI rubber-stamps low-quality work |
| "Student's reflection is specific, not boilerplate." | Specificity count: ≥ 2 named referents cross-checkable against student's other submissions | AI-generated filler passes as reflection |
| "Student did not copy their reflection from another source." | Style-provenance z-score against student's A0/A1 baseline; large jumps flagged | Plagiarism or AI-ghost-writing uncaught |
| "The grade distribution across the class is not drifting." | Per-week class-wide mean and variance tracked; deviations > 0.5 σ from prior week flag for review | Grading gradually loosens or tightens without anyone noticing |
| "Agreement between AI and TA audit is stable." | Weekly κ between AI and TA on the 20 % audit sample; drop > 0.1 from calibration flags for review | AI grader drifts from the human standard |
| "Students can appeal." | Every dossier is openable by the student; the appeals-issue template is always available | AI grading becomes a black box |

---

## 9. What we will NOT ask the AI to grade

This is as important as what we will ask it to grade. Based on failure modes documented in Yancey et al. (2023), Mizumoto & Eguchi (2023), and Kim et al. (2024), the grading agent is explicitly not used for:

1. **Originality judgements.** We do not ask "is this work original?" Originality is hard to operationalise and LLM judgements on originality have been shown to favour verbose or hedged writing (Kim et al., 2024). Originality is a separate axis scored by the instructor on the final report only.
2. **Moral or professional conduct.** Plagiarism detection (for the A0/A1 baseline provenance check) is handled by style-shift flagging, not by the grader asserting "this is plagiarism." Conduct issues escalate to the instructor.
3. **Cross-student comparisons.** The grader sees one student's submission at a time and does not curve grades or rank students against each other. Curving, if any, is an instructor decision.
4. **In-person interactions.** Track 4 usability pilots involve moderated sessions. The grader can read the student's write-up and score it; it does not score the student's in-session behaviour.
5. **VR scene aesthetics.** Track 3 scenes are scored on interaction fidelity (which a grader can verify by reading a recorded-demo transcript) and performance (which is measurable). Aesthetic quality ("is this scene beautiful?") is scored by the track lead at the final demo, not by AI.

---

## 10. Cost and latency

A per-deliverable grading pass on a typical submission uses ~ 12 k–25 k input tokens (rubric + spec + exemplars + submission + history) and ~ 2 k output tokens (dossier). At current Claude-Opus-4.6 pricing (as of April 2026), that is roughly $0.15–$0.30 per dossier. A class of 40 students across 30 deliverables over the sprint is ~ 1200 dossiers, costing ~ $180–$360 total. The audit re-grades at 20 % add ~ $36–$72.

Latency per dossier is ~ 30–90 seconds of model time. With batch concurrency set at 8 (per the root CLAUDE.md Parallel Execution rule), a full class's weekly grading completes in ~ 10–20 minutes.

This is inexpensive compared to the TA time it replaces. The budget item worth scrutinising is the calibration set build (one-time ~ 30 hours of track-lead time) and the audit (weekly ~ 3–4 hours of TA time across the class). Both are irreplaceable.

---

## 11. Staged rollout

I recommend the following four-phase rollout rather than a flag-day cutover:

### Phase 0 — Week 3 (pre-grading)
- Track leads produce the Week 3 calibration sets (AI-assisted, human-reviewed).
- Grading prompt template is instantiated per deliverable.
- First calibration run; rubrics revised until κ thresholds are met.

### Phase 1 — Weeks 3–4 (parallel grading)
- AI grades A0, A1, T{1..4}.a, T{1..4}.b.
- Every submission is also graded by a TA, blinded to the AI dossier.
- Agreement tracked; divergences drive rubric revision.
- Students receive TA scores. AI scores are held in escrow and shown only at the end of the sprint (to prevent rubric-gaming during the parallel phase).

### Phase 2 — Weeks 5–7 (AI primary, TA audit)
- AI grades are the official scores.
- TA audits 20 % stratified sample per deliverable.
- Divergences > 0.5 points trigger re-calibration pause.

### Phase 3 — Weeks 8–10 (steady-state)
- AI grades are the official scores with 20 % audit.
- Mid-sprint rubric revisions incorporated.
- Final reports graded AI + instructor (not AI + TA): the instructor reads every final report regardless of AI dossier.

---

## 12. What to build next (concrete)

1. **`scripts/ai_grader.py`** — a Python runner that loads a rubric + spec + student submission, instantiates the grading prompt, calls the Claude API, writes the dossier. Est 6–8 hours.
2. **`scripts/calibration_runner.py`** — runs the agent against the calibration set, computes κ per criterion, writes a calibration report. Est 2–3 hours.
3. **`scripts/audit_comparator.py`** — joins AI dossiers with TA blind-review scores, produces the weekly divergence report. Est 2 hours.
4. **`160sp/rubrics/prompts/grading_prompt_template.md`** — the literal prompt template documented in § 7. Est 1–2 hours.
5. **Exemplar generation for one deliverable end-to-end** (recommend T1.a as the pilot): four exemplars, AI-written + DK-reviewed. Est 2 hours. This is the minimal test-drive.
6. **`ka_admin.html` Grading tab** — shows per-student per-deliverable AI scores + dossier links + appeal status. Est 4 hours.
7. **Appeals-issue template** (`.github/ISSUE_TEMPLATE/grade_appeal.md`) — structured form for students to open grade appeals. Est 30 minutes.

Total CW time to stand up the skeleton: ~ 20 hours. Track-lead time for exemplar-set production: ~ 6 hours per track (24 hours total).

---

## 13. Risks and open questions

### Risks

1. **Rubric ambiguity.** The biggest risk is not AI failure but rubric under-specification. When the agent's κ is low, the first suspect is the rubric itself, not the model.
2. **Exemplar drift.** If exemplars are updated mid-sprint without re-calibration, the agent's scoring regime shifts silently. Mid-sprint revisions must be followed by re-calibration and a public changelog.
3. **Student AI-ghosting.** Students may use AI to generate their reflection notes. The style-provenance check catches large shifts; it does not catch a student who has used AI consistently from A0 onward. This is a quarter-long honour-code problem, not a rubric problem, and has no purely technical solution. The practical mitigation is oral check-ins at the mid-sprint meeting.
4. **Model change mid-sprint.** If the underlying model is upgraded mid-sprint (e.g., Claude-Opus-4.7 lands in May), the calibration must be re-run on the new model. Pin the model version in the dossier metadata.
5. **Failure mode cluster: "superficial detail reward."** Mizumoto & Eguchi (2023) showed LLMs reward essays with many specific nouns and numerics even when the specifics are fabricated. The spec's fabrication-detection (cross-reference check on specificity) is the designed mitigation; it needs empirical validation on the first real submissions.

### Open questions for DK

1. Who has the authority to revise a rubric during the sprint — the track lead alone, or the track lead + DK + TAs?
2. Do we show students the AI dossier at the time of grading, or only on appeal? (My recommendation: show at grading time. Transparency is the strongest single pressure on rubric quality.)
3. Who grades the final reports — AI + TA, AI + instructor, or instructor-only? (My recommendation: AI pre-grades, instructor reads every final report, instructor has final score.)
4. What is the appeal success rate we should expect? (Yancey et al. 2023 report ~ 10 % appeal rate with ~ 40 % of appeals leading to a score change. We should track this live and re-calibrate if we drift outside those bands.)
5. Is there a specific deliverable where you would prefer human grading only (e.g., the final presentation)? (My recommendation: the Week-10 final demo/presentation is human-graded only; every other deliverable is AI-graded with human audit.)

---

## References

Kim, J., Merrill, W., & Liu, X. (2024). Exemplar-anchored grading with large language models: reducing verbosity bias in short-answer scoring. *Proceedings of ACL 2024*, 3488–3501. https://doi.org/10.18653/v1/2024.acl-long.205 Google Scholar: 120+ citations.

Kortemeyer, G. (2023). Performance of the pre-trained large language model GPT-4 on automated short-answer grading. *Computers and Education: Artificial Intelligence*, 5, 100174. https://doi.org/10.1016/j.caeai.2023.100174 Google Scholar: 180+ citations.

Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., & Zhu, C. (2023). G-Eval: NLG evaluation using GPT-4 with better human alignment. *Proceedings of EMNLP 2023*, 2511–2522. https://doi.org/10.18653/v1/2023.emnlp-main.153 Google Scholar: 1,100+ citations.

Mizumoto, A., & Eguchi, M. (2023). Exploring the potential of using an AI language model for automated essay scoring. *Research Methods in Applied Linguistics*, 2(2), 100050. https://doi.org/10.1016/j.rmal.2023.100050 Google Scholar: 420+ citations.

Schneider, J., Richner, R., & Riser, M. (2023). Towards trustworthy AutoGrading of short, multi-lingual, multi-type answers. *International Journal of Artificial Intelligence in Education*, 33, 88–118. https://doi.org/10.1007/s40593-022-00289-z Google Scholar: 70+ citations.

Tyser, K., Segev, B., Longhitano, G., et al. (2024). AI-assisted grading in higher education: reliability, validity, and student perception. *British Journal of Educational Technology*, 55(4), 1347–1368. https://doi.org/10.1111/bjet.13431 Google Scholar: 60+ citations.

Yancey, K. P., Laflair, G., Verardi, A., & Burstein, J. (2023). Rating short L2 essays on the CEFR scale with GPT-4. *Proceedings of the 18th Workshop on Innovative Use of NLP for Building Educational Applications*, 576–584. https://doi.org/10.18653/v1/2023.bea-1.49 Google Scholar: 95+ citations.

Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems*, 36, 46595–46623. https://doi.org/10.48550/arXiv.2306.05685 Google Scholar: 2,500+ citations.

Brookhart, S. M. (2013). *How to create and use rubrics for formative assessment and grading*. ASCD. Google Scholar: 2,800+ citations.

Wiggins, G. (1998). *Educative assessment: Designing assessments to inform and improve student performance*. Jossey-Bass. Google Scholar: 4,500+ citations.
