# Knowledge Atlas User Journey Audit — Documentation Index

**Audit Date**: 2026-04-01  
**Auditor**: Claude Code  
**Scope**: All 112 HTML pages

---

## Documents in This Audit

### 1. **USER_JOURNEY_AUDIT_2026-04-01.md** (PRIMARY DOCUMENT)
**Length**: ~12KB | **Read Time**: 10-15 minutes

The comprehensive audit report. Contains:
- Executive summary with headline findings
- Detailed journey maps for all 5 user types
- Assessment of each journey (complete/broken status)
- List of 10 highest-priority broken CTAs
- Inventory of 20+ orphan pages
- Methodology notes

**Who should read**: Product managers, design leads, QA testers, developers implementing fixes

**Key Finding**: Only 22% of journeys (2 of 9) are complete. Most workflows have missing CTAs.

---

### 2. **JOURNEY_QUICK_REFERENCE.md**
**Length**: ~2KB | **Read Time**: 3-5 minutes

One-page cheat sheet. Contains:
- All journeys summarized in visual format
- Critical breaks highlighted
- List of problems by page
- Working journeys (don't touch these)

**Who should read**: Anyone needing a quick status check; useful for daily standups

---

### 3. **JOURNEY_FIX_ROADMAP.md** (IMPLEMENTATION GUIDE)
**Length**: ~12KB | **Read Time**: 15-20 minutes

Technical implementation guide for developers. Contains:
- All 10 broken CTAs with exact locations
- HTML code snippets showing the fix
- Severity levels and impact assessment
- Phase-by-phase implementation plan
- Pre/post-implementation testing checklist

**Who should read**: Developers implementing fixes; QA writing test plans

**How to Use**: 
1. Pick a phase (1-4)
2. Find the issue number
3. Copy the HTML code snippet
4. Paste into the specified file location
5. Test according to checklist

---

## Quick Statistics

| Metric | Value |
|--------|-------|
| Total HTML Pages | 112 |
| User Types Identified | 5 |
| Major Journeys Mapped | 9 |
| Complete Journeys | 2 (22%) |
| Broken Journeys | 7 (78%) |
| Missing CTAs | 12 |
| Critical Issues | 3 |
| High Priority Issues | 4 |
| Medium Priority Issues | 3 |
| Orphan Pages | 20+ |

---

## Top 3 Critical Issues

1. **Article Finder Track is Broken** (blocks student submissions)
   - Students complete assignment but can't reach collection page
   - Collection page exists but has no "Submit" CTA
   - Impact: Students stuck after collecting articles

2. **Hypothesis Building Incomplete** (blocks learning path)
   - No link from hypothesis builder to warrant reference
   - Students can't learn warrant types in context
   - Impact: Students frustrated during hypothesis formation

3. **Course Setup Disconnected** (blocks instructor workflow)
   - Instructors can't navigate: setup → schedule → prep checklist
   - CTAs missing at multiple steps
   - Impact: Instructors must manually find each page

---

## How to Use This Audit

### For Prioritization & Planning
1. Read JOURNEY_QUICK_REFERENCE.md (3 min)
2. Review critical issues above
3. Look at Phase 1 in JOURNEY_FIX_ROADMAP.md

### For Implementation
1. Review USER_JOURNEY_AUDIT_2026-04-01.md — understand the journeys
2. Use JOURNEY_FIX_ROADMAP.md — step-by-step implementation
3. Follow the testing checklist at bottom of roadmap doc

### For QA/Testing
1. Use JOURNEY_QUICK_REFERENCE.md to understand all journeys
2. Cross-reference JOURNEY_FIX_ROADMAP.md for fixes
3. Use testing checklist to validate each fix
4. Test full journeys end-to-end after all fixes

### For Design/Product Review
1. Start with Executive Summary in USER_JOURNEY_AUDIT_2026-04-01.md
2. Review "Orphan Pages" section
3. Review "Critical Findings" table
4. Discuss Phase 1-4 prioritization with team

---

## Key Findings Summary

### What's Working Well ✓
- **Onboarding Journey**: Home → Register → Login → Workspace (clear and complete)
- **Instructor Approval**: Simple and functional
- **All pages exist**: No 404 errors; all links point to existing pages

### What's Broken ✗
- **Course Track**: Students get stuck after collecting articles
- **Research Workflows**: Missing CTAs between evidence, warrants, annotations
- **Hypothesis Formation**: No reference to warrant types
- **Instructor Setup**: Disconnected from schedule and prep pages

### What's Missing
- 12 CTAs across 9 journeys
- Clear pathways for researchers
- Navigation between instructor management pages
- Definition of "Theory Explorer" and "Practitioner" user types

---

## Implementation Timeline Estimate

| Phase | Issues | Effort | Time |
|-------|--------|--------|------|
| Phase 1 (Critical) | 2 | High | 2-4 hours |
| Phase 2 (Learning) | 4 | Medium | 3-5 hours |
| Phase 3 (Course) | 2 | Low | 1-2 hours |
| Phase 4 (Polish) | 3 | Low | 1-2 hours |
| **Testing** | — | High | 4-6 hours |
| **TOTAL** | **10** | — | **11-19 hours** |

---

## Next Steps

1. **Week 1**: Implement Phase 1 (critical path)
   - Unblock Article Finder students
   - Test end-to-end

2. **Week 2**: Implement Phases 2-3 (learning + course)
   - Add researcher workflow CTAs
   - Connect instructor setup pages

3. **Week 3**: Phase 4 (polish) + comprehensive testing
   - Clarify remaining ambiguous journeys
   - Full regression testing on all 9 journeys

4. **Post-Implementation**: Monitor and iterate
   - Gather user feedback on fixed journeys
   - Test with real students/researchers
   - Update documentation

---

## Questions?

Refer to:
- **"Why is this journey broken?"** → USER_JOURNEY_AUDIT_2026-04-01.md (detailed explanation)
- **"How do I fix issue #3?"** → JOURNEY_FIX_ROADMAP.md (code snippet + test steps)
- **"What's the overall status?"** → JOURNEY_QUICK_REFERENCE.md (one-page summary)

---

## Document Maintenance

These documents should be updated:
- After each phase of implementation (mark issues as "FIXED")
- After testing discovers new journey issues
- When new user types are added to the mode selector
- When new pages are added to the site

Last Updated: 2026-04-01
