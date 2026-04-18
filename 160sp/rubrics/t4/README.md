# Track 4 — UX Research rubric overview

*Last updated: 2026-04-17*

## Track-level allocation (75 points)

| Deliverable | Span | Hardness | Points | Rubric file |
|-------------|:----:|:--------:|-------:|-------------|
| T4.a Heuristic audit of K-Atlas public site (10 findings) | Weeks 3–4 | Medium | 12 | `T4.a_heuristic_audit.md` |
| T4.b Scenario-based walkthrough on 3 archetype roles | Week 4 | Medium | 10 | `T4.b_scenarios.md` |
| T4.c Moderated usability pilot (n = 5) | Weeks 5–6 | Hard | 15 | `T4.c_usability_pilot.md` |
| T4.d Friction-point severity rubric + prioritised backlog | Week 6 | Medium-hard | 10 | `T4.d_severity_backlog.md` |
| T4.e Reproducibility check — second student confirms 5 findings | Week 7 | Hard | 13 | `T4.e_reproducibility.md` |
| T4.f Redesign proposal for one high-severity finding | Weeks 7–8 | Medium | 10 | `T4.f_redesign.md` |
| T4.g Final report + reflection | Week 8 | Easy | 5 | `T4.g_final_report.md` |
| **Total** | | | **75** | |

## Primary signals the AI grader reads

- Structured markdown findings documents in `160sp/tracks/t4/{student_id}/findings/`, one file per finding with a fixed schema (see `T4.a` spec).
- Screenshots and screen-recordings referenced from findings files.
- Survey CSVs and interview notes for T4.c.
- Severity-rating CSVs for T4.d.
- Second-rater confirmation files for T4.e.

## Track-specific conventions

- **Every finding is a structured document.** A "finding" is not free prose; it is a markdown file with: title, scenario, observed behaviour, expected behaviour, impact, severity (1–5 per Nielsen's scale), screenshot, recommendation. The AI grader reads the schema fields directly.
- **Reproducibility is graded.** T4.e requires a second student to independently land on five of the student's findings given the same scenarios. Partial-credit if 3–4/5; below 3 caps the finding set at band 1.
- **Usability pilot ethics.** T4.c uses the same class-protocol as T3.e: consent form, anonymised data, n = 5 from the student's social network outside the class.
