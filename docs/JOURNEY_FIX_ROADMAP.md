# Knowledge Atlas — Journey Fix Roadmap
**Date**: 2026-04-01

## Overview

This document provides the technical roadmap for fixing all broken CTAs and incomplete journeys in Knowledge Atlas.

---

## PHASE 1: CRITICAL PATH (Blocks Student Submissions)

### Issue 1.1: Article Finder Track — Missing Collection Page Link
**Severity**: CRITICAL
**Affects User Type**: Contributor (160sp students)
**Journey**: Course Track (Article Finder)

**Location**: `160sp/ka_article_finder_assignment.html`
**Problem**: Students complete assignment page but have no CTA to collection page
**Current State**: Page ends without exit CTA
**Fix**: Add button at bottom of page:

```html
<a href="ka_collect_articles.html" class="btn-cta btn-primary"
   style="background:#E8872A;color:#fff;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:700;display:inline-block;margin-top:20px;">
  Next: Collect Articles →
</a>
```

**Test**: User can click through to collection page

---

### Issue 1.2: Collect Articles — Missing Approval Submission CTA
**Severity**: CRITICAL
**Affects User Type**: Contributor (160sp students)
**Journey**: Course Track (Article Finder)

**Location**: `160sp/ka_collect_articles.html`
**Problem**: Students collect articles but don't know how to submit
**Current State**: File shows upload mechanics but no final submission CTA
**Current Link**: Has "Go to Contribute Page" (→ ka_contribute.html) which is wrong path
**Fix**: Add prominent submission button before footer:

```html
<div style="background:#f7f4ef;padding:24px;border-radius:8px;margin:30px 0;text-align:center;">
  <h3 style="font-size:1.1rem;margin-bottom:12px;">Ready to submit?</h3>
  <p style="color:#666;margin-bottom:18px;">Send your collected articles for instructor approval</p>
  <a href="ka_approve.html" class="btn-cta"
     style="background:#E8872A;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:700;display:inline-block;">
    Submit for Approval →
  </a>
</div>
```

**Test**: Student gets to approval flow after collecting articles

---

## PHASE 2: LEARNING PATHWAY (Blocks Research Workflows)

### Issue 2.1: Hypothesis Builder — Missing Warrant Reference Link
**Severity**: HIGH
**Affects User Type**: Student Explorer
**Journey**: Hypothesis Building

**Location**: `ka_hypothesis_builder.html`
**Problem**: Students building hypotheses have no link to warrant types
**Current State**: Form exists but no "Learn about warrants" CTA
**Fix**: Add button in right-side panel or after form explanation:

```html
<div style="background:#e8f0fd;padding:16px;border-radius:8px;margin:20px 0;">
  <h4 style="margin-bottom:10px;color:#1a3a7a;">Understand Warrants</h4>
  <p style="font-size:0.9rem;margin-bottom:12px;color:#333;">
    Not sure what counts as evidence for your hypothesis?
  </p>
  <a href="ka_warrants.html" style="color:#1a56a4;font-weight:700;text-decoration:none;">
    Learn about warrant types →
  </a>
</div>
```

**Test**: Students can navigate from hypothesis form to warrant reference

---

### Issue 2.2: Evidence Page — Missing Warrant Understanding Link
**Severity**: HIGH
**Affects User Type**: Researcher
**Journey**: Deep Evidence Exploration

**Location**: `ka_evidence.html`
**Problem**: Researchers viewing evidence have no path to understand warrant theory
**Current State**: Evidence browser exists but no contextual link to warrants
**Fix**: Add CTA in evidence sidebar or as prominent button:

```html
<!-- Add to evidence view section -->
<div style="padding:16px;background:#f0f7ff;border-left:4px solid #1a56a4;margin:20px 0;">
  <h4 style="margin-bottom:8px;">Understand Evidence Quality</h4>
  <p style="font-size:0.9rem;margin-bottom:12px;">
    Learn how different types of evidence support or challenge claims.
  </p>
  <a href="ka_warrants.html" style="color:#1a56a4;font-weight:700;text-decoration:none;">
    See warrant framework →
  </a>
</div>
```

**Test**: Researchers can navigate from evidence to warrant definitions

---

### Issue 2.3: Data Capture — Missing Methodology Link
**Severity**: MEDIUM
**Affects User Type**: Researcher
**Journey**: Research Data Analysis

**Location**: `ka_datacapture.html`
**Problem**: Form-driven page with no reference to how methodology works
**Current State**: Form for data entry but no learning path
**Fix**: Add info button or link:

```html
<!-- Add to form intro section -->
<p style="color:#666;margin:12px 0;">
  Need to understand how we process this data?
  <a href="ka_ai_methodology.html" style="color:#E8872A;font-weight:700;">
    Read the methodology →
  </a>
</p>
```

**Test**: Users can reference methodology while entering data

---

## PHASE 3: COURSE INFRASTRUCTURE (Enables Instructor Use)

### Issue 3.1: Student Setup — Missing Schedule Link
**Severity**: MEDIUM
**Affects User Type**: Instructor, Student Contributors
**Journey**: Manage Course Setup

**Location**: `160sp/ka_student_setup.html`
**Problem**: Instructors set up course but can't navigate to schedule
**Current State**: Setup page exists but no "View Schedule" CTA
**Fix**: Add button in "next steps" section:

```html
<div style="background:#fff;border:1px solid #ddd;padding:20px;border-radius:8px;margin:30px 0;">
  <h3 style="margin-bottom:12px;">Next Steps</h3>
  <a href="ka_schedule.html" class="btn-cta"
     style="background:#1a56a4;color:#fff;padding:12px 24px;border-radius:6px;text-decoration:none;font-weight:700;display:inline-block;margin-right:12px;">
    View Course Schedule →
  </a>
  <a href="instructor_prep.html" class="btn-cta"
     style="background:#666;color:#fff;padding:12px 24px;border-radius:6px;text-decoration:none;font-weight:700;display:inline-block;">
    Pre-Class Checklist →
  </a>
</div>
```

**Test**: Instructor can navigate from setup to schedule and prep

---

### Issue 3.2: Schedule — Missing Prep Checklist Link
**Severity**: MEDIUM
**Affects User Type**: Instructor
**Journey**: Manage Course Setup

**Location**: `160sp/ka_schedule.html`
**Problem**: Schedule page has no link to instructor prep checklist
**Current State**: Weekly agenda exists but no "go to prep" CTA
**Fix**: Add button in sidebar or top bar:

```html
<!-- Add to top of schedule page before content -->
<div style="background:#fff3cd;padding:12px 16px;border-radius:6px;margin-bottom:20px;text-align:center;">
  <a href="instructor_prep.html" style="color:#856404;font-weight:700;text-decoration:none;">
    View Pre-Class Checklist →
  </a>
</div>
```

**Test**: Instructor can navigate from schedule to prep checklist

---

## PHASE 4: RESEARCH WORKFLOWS (Secondary Improvements)

### Issue 4.1: Sensors — Clarify Data Capture Path
**Severity**: MEDIUM
**Affects User Type**: Researcher
**Journey**: Research Data Analysis

**Location**: `ka_sensors.html`
**Problem**: Sensor catalog exists but path to data entry is unclear
**Current State**: CTA exists but labeled ambiguously
**Fix**: Ensure clear "Capture Data" button points to `ka_datacapture.html`:

```html
<!-- Verify this link exists and is prominent -->
<a href="ka_datacapture.html" class="btn-primary"
   style="background:#E8872A;color:#fff;padding:14px 28px;border-radius:8px;">
  Capture Data with These Sensors →
</a>
```

**Test**: Clear progression from sensor reference to data entry form

---

### Issue 4.2: Article Proposal — Clarify Data Entry Path
**Severity**: MEDIUM
**Affects User Type**: Contributor
**Journey**: Propose & Submit Article

**Location**: `ka_article_propose.html`
**Problem**: Proposal form exists but exit to data capture is weak
**Current State**: May have CTA but not prominent enough
**Fix**: Add prominent "Next step" button:

```html
<!-- After form submission info -->
<div style="margin-top:30px;padding:20px;background:#e3f4ec;border-radius:8px;">
  <h4 style="margin-bottom:10px;color:#1a5c30;">Next: Enter Study Data</h4>
  <p style="font-size:0.9rem;margin-bottom:12px;">
    After proposing an article, enter the study's key metadata.
  </p>
  <a href="ka_datacapture.html" style="color:#1a5c30;font-weight:700;text-decoration:none;">
    Go to Data Capture →
  </a>
</div>
```

**Test**: Clear path from proposal to data entry

---

### Issue 4.3: Topics Page — Clarify Article Search Path
**Severity**: LOW
**Affects User Type**: Student Explorer
**Journey**: Explore Topics & Articles

**Location**: `ka_topics.html`
**Problem**: Journey spec says → ka_articles.html but nav goes to ka_article_search.html
**Current State**: Ambiguity in intended workflow
**Decision Needed**: Which is the intended page?
  - `ka_articles.html` — Article browser/explorer?
  - `ka_article_search.html` — Search-driven discovery?

**Fix**: Once decided, add explicit CTA:

```html
<!-- Option A: If using ka_article_search.html -->
<a href="ka_article_search.html" class="btn-cta" style="...">
  Search Articles →
</a>

<!-- Option B: If using ka_articles.html -->
<a href="ka_articles.html" class="btn-cta" style="...">
  Browse Articles →
</a>
```

**Test**: Consistent navigation from topic to article browsing

---

## IMPLEMENTATION CHECKLIST

### Pre-Implementation
- [ ] Review all proposed button styles against existing design system
- [ ] Verify color palette (`#E8872A`, `#1a56a4`, etc.) matches current site
- [ ] Get design approval for CTA placements
- [ ] Create backup of all files before editing

### Implementation (Per Phase)

**Phase 1** (Critical):
- [ ] Edit `160sp/ka_article_finder_assignment.html` — add collection CTA
- [ ] Edit `160sp/ka_collect_articles.html` — add submission CTA
- [ ] Test article finder workflow end-to-end

**Phase 2** (Learning):
- [ ] Edit `ka_hypothesis_builder.html` — add warrant link
- [ ] Edit `ka_evidence.html` — add warrant link
- [ ] Edit `ka_datacapture.html` — add methodology link
- [ ] Edit `ka_article_propose.html` — add datacapture link
- [ ] Test all research workflows

**Phase 3** (Course):
- [ ] Edit `160sp/ka_student_setup.html` — add schedule/prep CTAs
- [ ] Edit `160sp/ka_schedule.html` — add prep checklist CTA
- [ ] Test instructor workflow

**Phase 4** (Polish):
- [ ] Verify `ka_sensors.html` data capture CTA
- [ ] Clarify topics → articles workflow decision
- [ ] Implement clarified CTA

### Post-Implementation
- [ ] User testing: Have students complete Article Finder track
- [ ] User testing: Have researchers complete evidence workflow
- [ ] Update journey documentation
- [ ] Update site navigation diagram if exists

---

## Testing Checklist

For each fixed journey, verify:

- [ ] All CTAs are visible and not hidden by CSS
- [ ] All links point to correct pages (test hrefs)
- [ ] Button styling is consistent with site design
- [ ] Mobile responsive (test at 375px, 768px, 1024px)
- [ ] Keyboard accessible (Tab through CTAs)
- [ ] Color contrast meets WCAG AA standard
- [ ] Pages load without JavaScript errors

---

## Success Criteria

- **Phase 1**: Students can complete Article Finder track without confusion
- **Phase 2**: Researchers can navigate from evidence to warrants
- **Phase 3**: Instructors can navigate between setup → schedule → prep
- **Phase 4**: All documented journeys have complete CTA chains

**Overall**: All 9 journeys have clear CTAs at every step.
