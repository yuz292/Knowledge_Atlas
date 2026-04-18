# Work on 160F (Fall-2026 contribution) — 15 points

*Last updated: 2026-04-17*

## What this is

DK's requirement that every Spring student leaves an artefact the Fall 2026 cohort can actually use. This is not a reporting requirement; it is an integration requirement. The measure is whether something shipped that the Fall instructor or a Fall student would pick up on their own.

Each Spring student picks one of four contribution tracks at the Week 3 planning meeting and delivers across Weeks 5–10.

## The four contribution tracks (student picks one)

| Track | Description | Primary deliverable |
|-------|-------------|---------------------|
| **F160.a — Documentation** | Write up one workflow (pipeline, tagging, VR build, research protocol) in Fall-ready form | A markdown doc in `160sp/fall_handoff/workflows/{topic}.md` |
| **F160.b — Site improvement** | Land one reviewed PR on K-Atlas (bug fix, accessibility repair, feature) | Merged PR referenced by PR number in the grading sheet |
| **F160.c — Transfer packet** | Write the Week-0 onboarding packet the Fall cohort will read first | A markdown doc at `160sp/fall_handoff/onboarding/FALL_WEEK_0.md` |
| **F160.d — Scaffolding artefact** | Build one piece of infrastructure (template, rubric draft, sample dataset, tutorial) for the Fall instructor | One or more files in `160sp/fall_handoff/scaffolding/{artefact}/` |

## Three-part scoring (5 + 5 + 5 = 15 points)

### 1. Shipment (5 points)

Was the artefact submitted by the Week-10 deadline and does it meet the structural minimum for its track?

Machine-checkable:

```yaml
f160_shipment:
  required_artefact: "{per track above}"
  deadline: 2026-06-15
  min_word_count_or_file_count:
    F160.a: "2000-word workflow doc"
    F160.b: "1 merged PR, non-trivial diff"
    F160.c: "2500-word onboarding packet"
    F160.d: "one file + README"
```

- **0** — Not submitted or well below the minimum.
- **1** — Submitted but thin; major structural gaps.
- **2** — Submitted, meets minimum, clean.
- **3** — Submitted, exceeds minimum, clean, with a second-student review noted.

Rescaled to 5 points: 0 → 0; 3 → 5; linear interpolation.

### 2. Usability by a Fall student or instructor (5 points)

At the Week-10 review, the track lead (or DK) evaluates whether a Fall student or instructor who has never seen the artefact could actually use it.

Machine-checkable: AI grader reads the artefact as a Fall-student persona and scores whether the artefact is self-explanatory. Instructor audit at Week 10 confirms or overrides.

- **0** — Unreadable or full of unexplained internal jargon.
- **1** — Readable but requires significant external context.
- **2** — Readable and usable with one or two clarifying questions to the original author.
- **3** — Self-contained; a reader with no prior contact can pick it up.

Rescaled to 5 points.

### 3. Integration (5 points)

Was the artefact actually merged into the Fall-2026 repository / site / process by Week 10?

Machine-checkable: a link or PR number is supplied; the AI grader verifies the link resolves and the target actually contains the artefact.

- **0** — Not merged; lives only in the student's personal branch.
- **1** — Merged to a branch, not to main; or merged to main but not linked from any active page.
- **2** — Merged to main and linked from at least one page the Fall cohort will see.
- **3** — Merged, linked, and cited by at least one other student's work.

Rescaled to 5 points.

## Machine-readable spec

```yaml
deliverable_id: F160
points: 15
subcomponents:
  - id: F160.shipment
    points: 5
    scoring: three_point_rescale_to_5
  - id: F160.usability
    points: 5
    scoring: three_point_rescale_to_5
    grader: "ai + instructor audit"
  - id: F160.integration
    points: 5
    scoring: three_point_rescale_to_5
    protocol: "Verify link/PR resolves; verify referent contains artefact; count inbound links."
span:
  start: 2026-05-11  # Week 5
  end:   2026-06-15  # Week 10
track_choice_deadline: 2026-04-27  # Week 3
instructor_review: true  # DK reviews every F160 submission at Week 10
```

## Why this exists

The course runs every year; every Spring cohort leaves the Fall cohort a partly-rebuilt foundation. Without an explicit Fall-handoff requirement, the Spring work decays: students graduate, tribal knowledge leaves the lab, and the Fall section re-learns what the Spring section already knew. This 15 % commitment forces the decay to land as a written-up artefact instead.

## Common failure modes

1. **"Documentation" that is a weekly log with a title change.** F160.a requires a workflow write-up: how to do the thing, not what I did this week. The usability criterion catches this at Week 10.
2. **PRs that the student never pushed to main.** F160.b requires a merged PR, not a draft PR. The integration criterion catches this.
3. **Scaffolding artefacts no one knows exists.** F160.d requires an inbound link from at least one place a Fall student will look. The integration criterion catches this.

The three scoring parts (shipment / usability / integration) are designed to catch each failure mode explicitly.
