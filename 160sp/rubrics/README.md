# 160sp Rubrics — canonical framework

*Last updated: 2026-04-17*
*Authority: Professor David Kirsh (instructor of record)*
*Maintainer: CW (Claude Code) with track-lead approvals at Week 3 planning meeting*

---

## 1. What this directory is

`160sp/rubrics/` holds every scoring instrument the course uses. Each rubric is a Markdown file with a fixed schema so that a TA, the instructor, or a future Claude session can apply them consistently. This is the single authoritative source; anything outside this directory that claims to grade student work (old pages on the site, loose prose in assignment descriptions, informal notes) is superseded by the file here.

The directory exists for three reasons:

1. **Students must know what they are being graded on.** Before a student submits an artefact, they should be able to open the rubric and see the exact criteria.
2. **TAs must grade consistently across sections and across weeks.** Two graders looking at the same submission should not arrive at wildly different scores.
3. **The instructor must be able to audit grade decisions.** Disputes, grade appeals, and retrospective analysis all require a written standard that both sides can point to.

The rubric system is deliberately simple. A full criterion-reference assessment programme (Brookhart, 2013; Wiggins, 1998) would take longer than a quarter to build. This is what can land in one sprint and be improved over the Fall 2026 cycle.

---

## 2. Class-level point allocation (100 points total)

**Decision 2026-04-17** (DK): points are distributed across the whole class, not per track.

| Component | Points | Notes |
|-----------|-------:|-------|
| A0 — first common assignment | 5 | Orientation, environment, first 5 articles |
| A1 — second common assignment | 5 | Schema-study + 15 articles + first reflection |
| Track work (one of T1/T2/T3/T4) | 75 | Each track allocates its 75 points across 6–9 deliverables by hardness |
| Work on 160F — Fall-2026 contribution | 15 | Documentation / site PR / transfer packet / scaffolding artefact |
| **Total** | **100** | |

The track breakdown (how the 75 points distribute within each track) is in each track's own README; see `t1/README.md`, `t2/README.md`, `t3/README.md`, `t4/README.md`.

Two invariants that every track allocation must respect:

- **Hardness-weighted.** A harder deliverable gets more points. A 1-week observational task should not be worth the same as a 2-week classifier-fine-tuning arc.
- **Multi-week allowed.** Deliverables may span more than one week. The rubric file names are anchored to the deliverable (T1.a, T1.b, …), not to the week number.

---

## 3. The three-criterion rubric (applied to every deliverable)

Every deliverable — from A0 through the Week-10 final — uses the same three-criterion scoring frame. Only the point scale changes.

### 3.1 The three criteria

| Criterion | 0 (unacceptable) | 1 (marginal) | 2 (good) | 3 (excellent) |
|-----------|------------------|--------------|----------|---------------|
| **Completeness** — did the student produce the expected artefact? | Missing or severely incomplete | < half of expected quantity or major gaps | Meets minimum spec | Exceeds spec with demonstrable extras |
| **Quality** — does the artefact meet the track's quality bar? | Requires full redo | Significant TA corrections needed | Clean after minor polish | Publication-quality as submitted |
| **Reflection** — does the student demonstrate understanding of why this matters? | No evidence of reflection | Surface-level comment | Clear articulation of one aspect | Integrated view across the week's work |

Raw score range: 0–9 across the three criteria.

### 3.2 Rescaling raw score to the deliverable's point value

Each deliverable has a point value set by the track allocation table (e.g. T1.a = 5 points, T1.e = 15 points). The rescaling is:

> **points_awarded = round(raw_score × deliverable_points ÷ 9)**

A timeliness bonus of 0 or 1 point may be folded in for larger deliverables (≥ 10 points). See § 5 (Timeliness) below.

### 3.3 Why three criteria, not more

We tested the idea of four or five criteria during the scaffold pass (adding Originality and Communication as separate axes). The case for three:

- Three criteria fit on one line in a grading sheet, keeping grading from becoming bureaucratic overhead.
- Quality already absorbs Originality and Communication for most deliverables; when Originality or Communication are load-bearing (e.g. Track 4's redesign proposal, Track 3's final demo), the per-deliverable rubric spells that out explicitly under Quality.
- Reflection is preserved as a separate axis because without it the track becomes a box-ticking exercise, and the instructor has explicit pedagogical commitments (Kirsh, 2013; Kirsh & Maglio, 1994) to externalising-cognition habits that depend on students writing, not just producing.

The criterion set is open to revision at the Week-5 mid-sprint checkpoint if an axis turns out to be systematically under- or over-used by graders.

---

## 4. Filing conventions

| Path | Contents |
|------|----------|
| `rubrics/README.md` | This file (canonical framework) |
| `rubrics/common/a0.md`, `common/a1.md` | The two common assignments |
| `rubrics/t1/README.md` | T1 track-level allocation + deliverable list |
| `rubrics/t1/T1.a_schema_study.md` | One file per deliverable |
| `rubrics/t1/T1.b_tag_100.md` | etc. |
| `rubrics/f160/README.md` | Work-on-160F rubric |
| `rubrics/verification/README.md` | TA verification procedures |
| `rubrics/verification/t1_kappa_protocol.md` | Specific verification procedures referenced from track rubrics |
| `rubrics/grading_sheet_template.md` | Per-student grading sheet specification |

### Naming rule

Deliverable rubric files use the pattern `{track_id}.{letter}_{short_slug}.md`. Example: `T1.c_interrater_kappa.md`. Short slug is 2–4 words, underscore-separated, no spaces. Two-digit week numbers never appear in filenames because deliverables can span weeks.

### Header block (required on every deliverable rubric)

```markdown
# {Track_id}.{letter} — {full deliverable name}

**Track**: {Track number and name}
**Span**: {Week range or "single week"}
**Hardness**: {Easy / Medium / Medium-hard / Hard}
**Points**: {integer}
**Verification**: {Automated / Manual checklist / Inter-rater — reference the procedure file}
**Rubric authored**: {date}
**Rubric approved**: {date or "pending Week-3 planning meeting"}
```

---

## 5. Timeliness

For deliverables worth 10 or more points, one point of the total is reserved for on-time submission. The rescaling is:

> **if late submission: points_awarded = round(raw × (deliverable_points − 1) ÷ 9)**
> **if on-time: points_awarded = round(raw × (deliverable_points − 1) ÷ 9) + 1**

For deliverables worth fewer than 10 points, there is no timeliness bonus; late-submission policy reduces to a simple − 1 penalty on the rescaled score (floored at 0).

Late submissions are permanently flagged in the grading sheet with the submission timestamp and the number of days late. Students with chronic lateness are flagged to the instructor at the Week-5 mid-sprint checkpoint.

---

## 6. Verification — AI grader as primary, human audit as second pass

The primary grader is an AI (Claude Opus 4.6 in default configuration). The full design — what the AI checks, how it does it rigorously, how we keep it honest — is in `AI_GRADING_DESIGN_2026-04-17.md`. This section summarises.

| Layer | Role | Coverage |
|-------|------|----------|
| **AI grading** (primary) | Scores every submission on every deliverable using the three-criterion frame, produces a dossier with cited evidence | 100 % of submissions |
| **TA audit** (second pass) | Independently re-grades a stratified 20 % sample per deliverable; divergences > 0.5 points trigger re-calibration | 20 % stratified |
| **Instructor review** | Reads every final report and adjudicates appeals | Final reports (100 %) + appeals |

Every deliverable rubric file includes a **machine-readable spec** section (see `AI_GRADING_DESIGN_2026-04-17.md` § 4) that the agent reads directly; that is where required counts, exemplar paths, and consistency checks live. Every grading pass produces a **grade dossier** stored at `160sp/grading/{student_id}/{deliverable_id}_{date}.md` with six sections (metadata, completeness, quality, reflection, total, confidence + flags).

Three checks embedded in every dossier protect against AI failure modes identified in the literature (Kim et al., 2024; Mizumoto & Eguchi, 2023):

- **Literal-span citation.** Every score must be backed by at least one literal quote from the submission or literal DB row. No score without evidence.
- **Cross-artefact consistency.** Reflection claims must match evidence in the student's other submissions that week. If the student claims to have re-tagged image 027, the atlas_tags history is checked.
- **Provenance.** Reflection style is checked against the student's A0/A1 baseline; large shifts flag for human review (they do not automatically score down, because legitimate writing evolution is possible).

Appeals route to a second grading pass (different model or different seed); if the two AI graders disagree by ≥ 1 band, a human adjudicates.

---

## 7. Dispute resolution

If a student challenges a grade, the procedure is:

1. The student opens an issue on the course GitHub repo (private to instructor + student, not public) within 7 days of receiving the grade.
2. The student states the criterion (Completeness / Quality / Reflection) they challenge and the score they believe is warranted, citing the rubric language.
3. The grader responds in the issue with the specific evidence that led to the score.
4. If unresolved, the instructor re-grades from scratch without seeing the original TA score and the higher of the two scores stands, unless the re-grade surfaces a clear grading error in the student's favour in the original (in which case the higher score stands automatically).

This rubric-anchored procedure is adapted from the grading-appeal practice at Carnegie Mellon's Eberly Center and is standard in criterion-referenced assessment (Brookhart, 2013).

---

## 8. Mid-sprint revision

At the Week-5 mid-sprint checkpoint, the TA team and the instructor review:

- Which criteria are producing disagreement between graders (the Quality axis is the usual offender).
- Which deliverables are under- or over-weighted (students who finished in half the expected time, or students who could not finish at all).
- Whether the 3-criterion frame should expand to 4 for any deliverable (Track 4's redesign proposal is the likely candidate, adding Communication).

Any revisions are committed to this directory with a dated header and the pre-revision version is preserved in `rubrics/archive/YYYY-MM-DD/`.

---

## References

Brookhart, S. M. (2013). *How to create and use rubrics for formative assessment and grading*. ASCD. Google Scholar: 2,800+ citations.

Kirsh, D. (2013). Embodied cognition and the magical future of interaction design. *ACM Transactions on Computer-Human Interaction*, 20(1), Article 3. https://doi.org/10.1145/2442106.2442109 Google Scholar: 500+ citations.

Kirsh, D., & Maglio, P. (1994). On distinguishing epistemic from pragmatic action. *Cognitive Science*, 18(4), 513–549. https://doi.org/10.1207/s15516709cog1804_1 Google Scholar: 2,300+ citations.

Wiggins, G. (1998). *Educative assessment: Designing assessments to inform and improve student performance*. Jossey-Bass. Google Scholar: 4,500+ citations.
