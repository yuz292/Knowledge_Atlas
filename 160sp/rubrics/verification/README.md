# Verification procedures — TA audit guide

*Last updated: 2026-04-17*
*Primary grader*: AI (see `../AI_GRADING_DESIGN_2026-04-17.md`)
*This document's role*: procedures for the human TA audit that shadows the AI grader

---

## 1. What the TA is and is not doing

The AI grades every submission. The TA **audits a stratified 20 % sample** per deliverable. The TA is not the primary grader; the TA's work is the second pass that keeps the AI honest.

Specifically, the TA's weekly responsibilities are:

1. Pull the audit sample for each deliverable from `scripts/audit_comparator.py` (stratified across flagged-low-confidence dossiers, band-boundary dossiers, and random).
2. Re-grade each audit-sample submission **without reading the AI dossier** (blinded review). Record scores on the three criteria.
3. After re-grading, unblind: read the AI dossier and note any disagreement ≥ 1 band on any criterion.
4. For each disagreement, write a one-paragraph explanation: was the AI wrong, was the TA wrong, or was the rubric ambiguous?
5. Submit the audit report to the track lead by end-of-week.

If mean absolute disagreement between AI and TA across the audit sample exceeds 0.5 points per criterion for any deliverable, the track lead pauses AI grading for that deliverable until the rubric or exemplars are revised.

---

## 2. Procedures per track

### 2.1 Track 1 — Image tagging

**What to check, blinded:**

1. Open the student's tag rows for the deliverable in the Atlas tag DB:
   ```sql
   SELECT image_id, tag, confidence, rationale, tagged_at
   FROM tags
   WHERE tagged_by = '{student_id}'
     AND tagged_at BETWEEN '{span.start}' AND '{span.end}'
   ORDER BY tagged_at;
   ```
2. Completeness: does the row count meet the spec's minimum for band 2? For band 3?
3. Quality: independently re-tag 10 random rows without looking at the student's tag. Compare. Compute agreement rate.
4. Reflection: open the tag-log entry in the shared doc. Score against the Reflection band in the rubric.
5. Inter-rater kappa check (T1.c only): confirm the student's submitted kappa computation matches what you get when you recompute from the two taggers' row histories.

**Time per submission**: 15–20 minutes (the spot-check re-tagging dominates).

### 2.2 Track 2 — Article finder

**What to check, blinded:**

1. Open the student's registry rows:
   ```sql
   SELECT article_id, title, doi, evidentiary_tag, relevance_flag, submitted_at
   FROM pipeline_registry_unified
   WHERE submitted_by = '{student_id}'
     AND submitted_at BETWEEN '{span.start}' AND '{span.end}';
   ```
2. Completeness: row count against the spec minimum.
3. Quality: pick 5 random rows, open the PDFs, and independently assess whether each article is relevant to the student's declared sub-topic. Compute agreement rate with the student's self-assessment.
4. VOI-banding sanity (T2.c and later): confirm the student's VOI band for each of 5 random articles against your own judgement using the VOI rubric at `rubrics/voi_banding.md`.
5. Reflection: open the student's weekly log; score against the Reflection band.

**Time per submission**: 20–25 minutes (depends on how many PDFs you open).

### 2.3 Track 3 — VR

**What to check, blinded:**

1. Check out the student's branch / commit:
   ```bash
   cd 160sp/tracks/t3/{student_id} && git log --author={student} --since={span.start} --until={span.end}
   ```
2. Completeness: commit count, files-touched count, presence of required scene files.
3. Quality: open the Unity project, run the scene, note interaction fidelity against the deliverable spec. For T3.d (performance pass), run the profiler and record frame time.
4. Reflection: open the student's dev-log markdown file; score against Reflection band.

**Time per submission**: 25–30 minutes (Unity loading dominates).

### 2.4 Track 4 — UX research

**What to check, blinded:**

1. Open the student's findings document in the shared repo.
2. Completeness: count of findings against the spec minimum; presence of severity ratings; presence of recommendation paragraphs.
3. Quality: pick 3 findings; independently attempt the scenario on the live site; confirm the friction point exists and its severity rating is defensible.
4. Reflection: score against the Reflection band.

**Time per submission**: 20–30 minutes (the independent scenario run dominates).

### 2.5 A0 and A1 common

Follow the Track 2 procedure (articles land in the registry). A0 is a simple count check; A1 adds the schema-study prose check from the rubric.

---

## 3. Disagreement triage

After unblinding and comparing your score to the AI dossier, for each ≥ 1-band disagreement:

1. **Read the AI dossier's cited evidence.** Did the AI quote the right span? Did it interpret it correctly?
2. **Re-read the student's submission against the AI's band argument.** If the AI's band is defensible, that is a TA calibration issue (you may be scoring too strict or too loose).
3. **Re-read the rubric band language.** If the language is ambiguous and both bands are defensible, that is a rubric problem.
4. **Write one paragraph** in the weekly audit report: student ID, deliverable, criterion, your score, AI score, your explanation.

The track lead reads these paragraphs at the weekly sync. Ambiguous-rubric cases drive rubric revisions at the Week-5 mid-sprint checkpoint.

---

## 4. Audit-sample stratification

The 20 % audit sample is not random. It is stratified to maximise the chance of catching AI errors.

| Stratum | Share of sample | Why |
|---------|----------------|-----|
| AI-flagged low confidence | 100 % of flagged | The AI itself reported low confidence; a human should check |
| Band-boundary (score 1 or 2 with shallow margin) | ~ 40 % of remaining sample | Band boundaries are where AI error is most consequential |
| Random | ~ 60 % of remaining sample | Keeps the system honest against silent drift |

`scripts/audit_comparator.py` produces this sample automatically each week.

---

## 5. Escalation

If during audit you discover:

- A pattern of AI error affecting 3+ students on the same deliverable → escalate to the track lead immediately (do not wait for end-of-week).
- A suspected case of plagiarism or academic-integrity violation → escalate to the instructor (DK) directly, not through the normal audit report.
- A rubric ambiguity that makes fair scoring impossible → flag for the Week-5 mid-sprint revision and note in the weekly report.

---

## 6. Why audit matters

AI grading without human audit regresses. The specific failure modes documented in the literature (Kim et al., 2024; Tyser et al., 2024) include:

- **Verbosity reward**: AI gives high Quality scores to long, hedged writing even when substantively thin.
- **Specificity hallucination**: AI accepts fabricated-but-specific-sounding claims because they look like evidence.
- **Drift**: AI's scoring gradually loosens or tightens without anyone noticing, because the class's submissions drift and the AI drifts with them.

The 20 % audit catches all three before they damage grades. The audit is therefore a load-bearing component of the grading system, not an optional extra.
