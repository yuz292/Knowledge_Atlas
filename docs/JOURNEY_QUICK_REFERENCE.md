# Knowledge Atlas — Journey Quick Reference
**Generated**: 2026-04-01

## At a Glance

- **5 User Types** identified in mode selector
- **9 Major Journeys** mapped
- **2 Complete** (onboarding, instructor approval)
- **7 Broken** with 12 critical CTA gaps
- **112 Pages** total

---

## All Journeys at a Glance

```
STUDENT EXPLORER (3 journeys)
  ✓ First-Time Entry (home → register → login → workspace)
  ✗ Explore Topics & Articles (1 CTA broken)
  ✗ Hypothesis Building (1 CTA missing)

RESEARCHER (2 journeys)
  ✗ Deep Evidence Exploration (1 CTA missing)
  ✗ Research Data Analysis (2 CTAs missing/broken)

CONTRIBUTOR (2 journeys)
  ✗ Propose & Submit Article (1 CTA weak)
  ✗ Course Track (2 CTAs broken)

INSTRUCTOR (2 journeys)
  ✓ Review & Approve Submissions
  ✗ Manage Course Setup (2 CTAs missing)

THEORY EXPLORER — Not mapped (no journeys found)
PRACTITIONER — Not mapped (no journeys found)
```

---

## Critical Breaks (Highest Priority)

### Course Track is Broken (2 Steps)
```
ka_article_finder_assignment.html
  ✗ Missing → ka_collect_articles.html
ka_collect_articles.html
  ✗ Missing → ka_approve.html
```
**Impact**: Students complete assignment but don't know how to submit.

### Hypothesis Building is Incomplete
```
ka_hypothesis_builder.html
  ✗ Missing → ka_warrants.html
```
**Impact**: Students can't navigate from hypothesis builder to warrant reference.

### Evidence Exploration Incomplete
```
ka_evidence.html
  ✗ Missing → ka_warrants.html
```
**Impact**: Researchers can't learn warrant types from evidence page.

---

## Pages with Most Problems

| Page | Issues | Needs |
|------|--------|-------|
| `160sp/ka_article_finder_assignment.html` | No exit CTA | → ka_collect_articles.html |
| `160sp/ka_collect_articles.html` | No submission CTA | → ka_approve.html |
| `ka_hypothesis_builder.html` | No warrant link | → ka_warrants.html |
| `ka_evidence.html` | No warrant link | → ka_warrants.html |
| `160sp/ka_student_setup.html` | No schedule link | → ka_schedule.html |
| `160sp/ka_schedule.html` | No prep link | → instructor_prep.html |

---

## Pages with No Journey (Orphans)

- ka_my_work.html
- ka_question_maker.html
- ka_workflow_hub.html
- ka_gaps.html
- ka_contribute.html
- ka_forgot_password.html
- ka_reset_password.html
- ka_neuro_grounding_demo.html
- ka_neuro_perspective.html
- All Designing_Experiments/* pages
- All 160sp/week*_agenda.html pages

---

## Working Journeys (Don't Change)

1. **Student Entry**: home → register → login → workspace ✓
2. **Instructor Review**: approve dashboard → review page ✓

Both are clear and functional.

---

## What's Next?

1. Add 2 CTAs to break Article Finder bottleneck
2. Add 3 CTAs to enable research workflows
3. Audit orphan pages for integration
4. Test all journeys end-to-end
