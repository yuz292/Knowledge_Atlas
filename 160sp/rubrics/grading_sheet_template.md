# Grading sheet — per-student per-deliverable

*Last updated: 2026-04-17*
*Target implementation*: Excel (`.xlsx`) generated from this spec, with auto-summing totals; the present document is the schema that `scripts/ai_grader.py` writes to after each grading pass

---

## Sheet structure

One workbook per cohort (`grading_sheet_cogs160sp_2026.xlsx`). The workbook has the following worksheets:

| Sheet | Purpose |
|-------|---------|
| `Roster` | One row per student: id, name, track, pair (for T1.c / T4.e) |
| `Common` | A0 + A1 scores per student |
| `Track_T1` | Per-student × per-deliverable grid for T1.a through T1.g |
| `Track_T2` | Per-student × per-deliverable grid for T2.a through T2.g |
| `Track_T3` | Same for T3 |
| `Track_T4` | Same for T4 |
| `F160` | Per-student Work-on-160F scores (shipment / usability / integration) |
| `Totals` | Computed per-student course total (5 + 5 + 75 + 15 = 100) |
| `Audit` | TA-audit reconciliation (AI score vs. TA blind-review score per audited deliverable) |

---

## Per-deliverable column block

Each deliverable in a track sheet has this column block:

| Column | Type | Source |
|--------|------|--------|
| `{deliverable}_completeness_raw` | 0–3 | AI dossier |
| `{deliverable}_quality_raw` | 0–3 | AI dossier |
| `{deliverable}_reflection_raw` | 0–3 | AI dossier |
| `{deliverable}_timeliness_bonus` | 0 or 1 | Submission timestamp + deadline |
| `{deliverable}_late_penalty` | integer ≤ 0 | Deadline compare |
| `{deliverable}_points` | formula | `round(raw_sum × (max_points − bonus) / 9) + timeliness_bonus + late_penalty`, floored at 0 |
| `{deliverable}_confidence` | high/medium/low | AI dossier |
| `{deliverable}_dossier_link` | URL | Path to dossier MD |
| `{deliverable}_audit_flag` | boolean | TRUE if audited |
| `{deliverable}_audit_ta_score` | integer | TA blind review (if audited) |
| `{deliverable}_audit_disagreement` | integer | `abs(points − audit_ta_score × max_points/9)` |

---

## Totals sheet formulas

Cell `Totals!B{row}` computes total for student id in row:

```
= SUMIFS(Common!C:C, Common!A:A, A{row})       # A0 + A1
+ IF(track = "T1", SUM(Track_T1!{student_points_columns}))
+ ...
+ F160!B{row} + F160!C{row} + F160!D{row}       # 5 + 5 + 5
```

The totals sheet caps at 100; any formula error (e.g., missing deliverable) reports `#VERIFY` rather than a silent NA, because a silent missing row propagates into the term grade unnoticed.

---

## Student-facing view (ka_admin.html Grading tab)

The student-facing view in `ka_admin.html`'s Grading tab shows:

- Student name and current total / 100.
- Per-deliverable row with: title, span, points earned / max, dossier link, appeal status.
- A per-criterion breakdown on hover (completeness / quality / reflection bands).
- A "course-total-to-date" number that updates after each grading pass.

Permissions:

- **Student**: sees own row only.
- **Track lead**: sees all students in the track.
- **TA**: sees all students, audit flag column visible.
- **Admin (DK)**: sees everything, plus the Audit sheet.

---

## Why markdown and not direct `.xlsx`

The spec lives here as markdown so that it can be version-controlled alongside the rubrics. A small `scripts/render_grading_sheet.py` script generates the `.xlsx` from this spec in a follow-on session using the `xlsx` skill. That separation keeps the authoritative spec in diff-able plain text and makes the Excel file a pure build artefact.
