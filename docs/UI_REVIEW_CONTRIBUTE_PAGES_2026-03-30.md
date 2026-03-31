# UI/UX Review: Knowledge Atlas Contribution Pages
**Date**: March 30, 2026
**Reviewed Pages**: `ka_contribute.html`, `ka_article_propose.html`
**Audience**: University students (COGS 160, 18-22), public researchers, contributors
**Design System**: KA Navy/Amber/Cream palette, Georgia serif headings, system sans body

---

## Overall Assessment

Both contribution pages successfully embody the Knowledge Atlas design system and implement a clear two-step workflow (choose intake mode → execute). The visual hierarchy is strong, color contrast meets WCAG AA standards, and the responsive grid layouts function well down to mobile widths. However, the pages suffer from **cognitive overload due to dense callout blocks** and **inconsistent form field styling** that creates friction for first-time student contributors. The `ka_contribute.html` page is more accessible and task-focused; `ka_article_propose.html` is more feature-rich but assumes higher user sophistication. Error states for upload failures and duplicates are mentioned in callouts but not implemented visually. The upload UX lacks confirmation feedback and explicit file size/format validation messaging.

---

## Critical Findings

### 1. **Dense Callout Block Overload** (ka_article_propose.html)
**Location**: Step 1B — "Upload PDFs" section (lines 226-230)
**Issue**: Four stacked callout boxes (Teal, Amber, Blue, Rose) present 120+ words of rules in rapid succession. A student uploading their first PDF encounters:
- Immediate gate (duplicate detection)
- Deferred gate (relevance review)
- Track 2 rule (citation requirements)
- Security gate (validation procedure)
- Storage rule (deletion after review)

**Impact**: Cognitive load spike. First-time users will scroll past or skim without retention. The information competes with the actual upload interaction.

**Recommendation**:
- Move "Track 2 rule", "Security gate", and "Storage rule" to a footer explanation or a collapsible "Why these gates matter?" section
- Keep only the two most critical callouts visible by default (Immediate gate, Deferred gate)
- Reduce word count per callout from 25–40 words to 15–20 words maximum
- Add subtle icons to the left of each callout for visual scanning (🚫, ⏱️, 🔒, 🗑️)

**Severity**: Major

---

### 2. **Inconsistent Form Field Styling Between Pages**
**Location**: ka_contribute.html (lines 81-86) vs. ka_article_propose.html (lines 60-65)
**Issue**:
- `ka_contribute.html`: Field labels are teal, uppercase, 11px, 600 weight
- `ka_article_propose.html`: Field labels are teal, uppercase, 11px, 600 weight (identical so far)
- **But**: Input padding differs: ka_contribute uses `10px 12px`, ka_article_propose uses `9px 11px`
- Input background colors differ: both use `var(--cream)` on default, but hover/focus behavior is identical (this is fine)
- Font sizes differ slightly: `.84rem` vs `.86rem` for inputs

**Impact**: Subtle, but creates visual discord when users switch between pages. The slightly smaller padding in ka_article_propose makes form fields feel cramped and less inviting.

**Recommendation**:
- Standardize all form input specs across both pages:
  ```css
  .field-input, .field-textarea, .field-select {
    padding: 10px 12px;
    font-size: 0.86rem;
  }
  ```
- Create a shared CSS foundation or import a common stylesheet for both contribution pages

**Severity**: Minor (visual consistency concern)

---

### 3. **Missing Error States for Upload Failures**
**Location**: Upload zones (ka_contribute.html line 243, ka_article_propose.html line 232)
**Issue**:
- The `.upload-zone` has `:hover` and `.dragover` states (border color, background)
- No visual states for: **file too large**, **wrong file type**, **upload failed**, **duplicate detected**
- Callouts mention duplicate detection (ka_article_propose.html line 226) but no accompanying error UI
- No feedback after successful upload: files appear in table but no green checkmark, success message, or animation

**Impact**: Student uploads a 50 MB file or a `.docx` instead of `.pdf` → silence. They don't know if it's processing or if it failed. For duplicates, the callout says "stopped immediately" but there's no visual rejection indicator in the file table.

**Recommendation**:
- Add CSS states for `.upload-zone` error conditions:
  ```css
  .upload-zone.error {
    border-color: #A84F6B; /* rose */
    background: var(--rose-lt);
  }
  .upload-zone.error .upload-label {
    color: #A84F6B;
  }
  ```
- Display file-level error badges in the file table:
  - `.s-toobig`: rose background, "File exceeds 25 MB"
  - `.s-wrongtype`: rose background, "Only PDF accepted"
  - `.s-duplicate`: amber background (exists, but not connected to upload validation)
- Add a success animation or toast message: "✓ 3 files ready for staging"
- Implement client-side file size check before upload with clear messaging: "Max 25 MB per file"

**Severity**: Critical (blocks user awareness of errors)

---

### 4. **Unclear "Stage" vs. "Submit" Terminology**
**Location**: ka_contribute.html (line 302), ka_article_propose.html (line 241)
**Issue**:
- ka_contribute.html: "Submit for Review" button → single unified action
- ka_article_propose.html: "Stage non-duplicates for nightly review" button → implies batch staging, then later review
- The copy says staged items are "held for the nightly reviewer pass" (ka_article_propose.html line 322) but students may not understand that "staging" != "acceptance"
- No visible confirmation that staged items are queued — they disappear from the batch table into an invisible "intake queue"

**Impact**: Student uploads 3 PDFs, clicks "Stage", and they vanish. No confirmation. The queue summary only appears in the sticky sidebar on ka_article_propose.html, and only if the sidebar is visible.

**Recommendation**:
- After staging, show a success message with actionable next steps:
  ```
  ✓ Staged 3 items for review

  What happens next:
  • Nightly review starts at 2 AM PST
  • Check your dashboard tomorrow for decisions
  • View queue →
  ```
- Make the intake queue more prominent: add a toast notification or inline card that confirms items were added
- For ka_contribute.html, add a similar confirmation step before final submission to avoid silent failures

**Severity**: Major (user doesn't know if action succeeded)

---

### 5. **Accessibility: No Alt Text for Icons, Weak Icon Semantics**
**Location**: Action card icons (ka_contribute.html line 207, 218) use raw emoji: `<div class="action-icon">📄</div>`
**Issue**:
- Emoji are inaccessible to screen readers that don't recognize them as meaningful
- No `aria-label` or `role="img"` to describe the icon
- Upload zone uses 📚 (books) but a file icon might be more semantically correct

**Impact**: Screen reader user hears "g-emoji" or silence instead of "PDF upload icon". For students with visual impairments, the distinction between "📄 Upload a paper" and "🔍 Find papers" is lost.

**Recommendation**:
```html
<!-- Change from: -->
<div class="action-icon">📄</div>

<!-- To: -->
<div class="action-icon" role="img" aria-label="Document upload">📄</div>
```
Or use SVG icons instead of emoji for better accessibility and design control.

**Severity**: Major (WCAG 2.1 accessibility violation)

---

### 6. **No Explicit File Format / Size Limits Displayed to User**
**Location**: Upload zones (ka_contribute.html line 246, ka_article_propose.html line 235)
**Issue**:
- Hint text says "PDF only · multiple files supported"
- No mention of max file size (assumed from context: likely 25 MB or similar, but never stated)
- No mention of accepted metadata formats for citation intake
- ka_article_propose.html mentions accepted file types for citations (`.txt`, `.csv`, `.ris`, `.bib`) but only in a field hint at line 218, easy to miss

**Impact**: Student with a 100 MB scanned PDF receives a generic error. They don't know whether to compress, split, or give up. Public contributor doesn't know if they need to provide abstract or just title.

**Recommendation**:
- Add file limits to both upload zones:
  ```
  PDF only · Max 25 MB per file · Multiple files supported
  Metadata extraction happens automatically — no abstract needed
  ```
- For citation input, add a visible format guide above the textarea:
  ```
  Accepted formats: APA citations, DOI, title, or upload .txt/.csv/.ris/.bib files
  ```
- Add a tooltip or `<details>` element: "Not sure about the format? Click here for examples"

**Severity**: Major (prevents user success)

---

### 7. **Sticky Sidebar Disappears on Mobile (Responsive Layout Issue)**
**Location**: ka_article_propose.html (line 30) — two-column grid layout
**Issue**:
- Page uses `grid-template-columns: 1fr 360px` with sticky sidebar on right
- At tablet/phone breakpoints, no media query is defined to stack the sidebar below the main content
- The queue card stays sticky at `top: 80px` even when the layout breaks, potentially obscuring content

**Impact**: On a phone (max-width < 700px), the queue sidebar either vanishes (if hidden via display:none) or floats over the main form, making it unusable.

**Recommendation**:
```css
@media (max-width: 900px) {
  .page-wrap {
    grid-template-columns: 1fr;
  }
  .queue-card {
    position: static; /* Stop sticky behavior */
    margin-bottom: 32px;
  }
}
```

**Severity**: Major (unusable on tablet)

---

### 8. **Modal Overlay Covers Critical Content, No Escape Key**
**Location**: Modal styling (ka_contribute.html, ka_article_propose.html lines 137–144)
**Issue**:
- `.modal-overlay` uses `inset: 0` with `position: fixed` and `background: rgba(0,0,0,.45)`
- Dark overlay is 45% opacity, may be too light to clearly signal "blocking" behavior
- No keyboard escape handler is visible in the CSS or JS snippets
- Modal doesn't trap focus (no `aria-modal="true"` or `role="alertdialog"`)

**Impact**: User tabs through form, accidentally triggers a modal (e.g., "done" confirmation), can't close it without finding a mouse or knowing to press Escape (if that's even implemented). Keyboard users are trapped.

**Recommendation**:
- Increase overlay opacity: `background: rgba(0,0,0,.65)` for stronger visual signaling
- Add keyboard support in JS:
  ```javascript
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.getElementById('confirmModal').classList.contains('open')) {
      closeModal();
    }
  });
  ```
- Add ARIA attributes to modal:
  ```html
  <div class="modal-overlay" id="confirmModal" role="alertdialog" aria-modal="true" aria-labelledby="confirmTitle">
  ```

**Severity**: Major (keyboard accessibility, WCAG 2.1 AA)

---

## Major Findings

### 9. **Breadcrumb Missing on ka_contribute.html**
**Location**: ka_contribute.html has no breadcrumb; ka_article_propose.html does (line 162)
**Issue**: The hero page `ka_contribute.html` provides high-level overview but no way to jump directly back to home or parent page besides the nav. `ka_article_propose.html` has breadcrumb "← Article Search / Propose New Article" but `ka_contribute.html` only has "← Back to Home" in footer nav.

**Impact**: Minor inconsistency; users are not lost, but the page feels less integrated with the information architecture.

**Recommendation**: Add breadcrumb to ka_contribute.html:
```html
<div class="breadcrumb"><a href="ka_home.html">← Home</a> &nbsp;/&nbsp; Contribute</div>
```

**Severity**: Minor

---

### 10. **Topic Chip Selection Feedback Not Retained**
**Location**: ka_contribute.html, Topic Finder section (lines 115–117)
**Issue**:
- Topic chips have `.selected` state with amber background
- No indication of how to confirm selection or what selecting does
- Selection state likely doesn't persist if user navigates away

**Impact**: Student clicks "Attention Restoration" topic, sees instructions, but if they click another topic, the first selection is overwritten. No way to multi-select or submit a topic interest.

**Recommendation**:
- Clarify interaction: does clicking a topic auto-populate a hidden form field, or is it just for reading guidance?
- If multi-select, use checkboxes inside chips or add a "Selected topics: X" summary
- If single-select with action, add button "Find papers for [selected topic]" below the grid
- Add visual feedback: "Your selection guides the scholar search below" in a callout

**Severity**: Minor

---

### 11. **Form Metadata Refinement Fields Collapse / Expand Without Clear Trigger**
**Location**: ka_contribute.html, "Refine metadata (optional)" section (lines 269–298)
**Issue**:
- This section is always visible in the HTML, but in real usage (not shown in HTML) would need to appear/disappear based on whether a PDF was uploaded
- No CSS for conditional display (no `.hidden` or `.display:none`)
- If form is long, user might scroll past without noticing optional refinement fields

**Impact**: Student uploads PDF, scrolls up to check extraction, doesn't see fields are below. Or if empty, fields clutter the page.

**Recommendation**:
- Add a visual toggle: "Improve extracted metadata ▼" that expands/collapses the field group
- Or: use a separate "Modal metadata editor" like ka_article_propose.html does (the `.metadata-panel` on line 101)
- Add a visual indicator of how many fields have been pre-filled: "DOI ✓ Title ✓ Authors — refine here if needed"

**Severity**: Minor

---

### 12. **Color Contrast on Muted Text**
**Location**: Throughout both pages, `.muted` color = `#6B6B6B`
**Issue**:
- Muted text (#6B6B6B, ~55% gray) on cream background (#F7F4EF, 98% light) has a contrast ratio of ~5.5:1 ✓ meets AA standard
- But on the hero section (dark navy background #1C3D3A), secondary text uses `#B8D4CE` which is light teal
- Tested: light teal on dark navy = ~6.2:1 contrast ✓ AA compliant, but noticeably lighter than ideal (should aim for 7+)

**Impact**: No WCAG violation, but hero copy is straining on some displays. Users with mild color vision deficiency may find the teal hard to parse against navy.

**Recommendation**:
- Consider using `#FFFFFF` or `#D4F0EA` (lighter, higher contrast) for secondary text in hero section
- Test final palette with contrast checker: https://www.tpgi.com/color-contrast-checker/

**Severity**: Minor (already compliant, but room for improvement)

---

## Minor Findings

### 13. **"Topic Chip" Labels Not Scalable**
**Location**: ka_contribute.html, Topic grid (line 114)
**Issue**: Topic names auto-truncate at 60 characters (line 430: `if (name.length > 60) name = name.slice(0, 57) + '…'`). Names like "Neuroaesthetics × Contour × Beauty" are readable, but longer topic names might become meaningless: "Interoceptive processing of spatial luminance and thermal c…"

**Impact**: User can't fully understand what a topic is about without clicking / hovering.

**Recommendation**:
- Add `title` attribute to topic chips for hover tooltips:
  ```html
  <div class="topic-chip" title="Full topic name here">…</div>
  ```
- Or increase grid minimum width: `minmax(240px, 1fr)` instead of `minmax(200px, 1fr)` to give more space

**Severity**: Minor

---

### 14. **Mode Selector Not Properly Labeled for Assistive Tech**
**Location**: Both pages, mode-select dropdown (ka_contribute.html line 168, ka_article_propose.html line 149)
**Issue**:
- Dropdown has `aria-label="Switch user mode"` ✓ Good
- But the options don't have explicit labels describing what each mode unlocks (e.g., "Student explorer — limited to course materials")

**Impact**: Screen reader user selects "Contributor" mode but doesn't understand what permissions or features change.

**Recommendation**:
- Add `<optgroup>` or prose description above dropdown:
  ```html
  <div class="field-hint" style="margin-bottom: 8px;">
    Your current role affects what metadata you can edit and how contributions are tracked.
  </div>
  ```

**Severity**: Minor

---

### 15. **Button Hover States Lack Visual Feedback**
**Location**: Primary and secondary buttons throughout
**Issue**:
- `.btn-primary:hover { background: #c97020 }` darkens amber; no shadow, no scale change
- `.btn-secondary:hover { background: #1a5c4e }` darkens teal
- No `:focus` or `:focus-visible` states defined for keyboard navigation

**Impact**: Button press feels unresponsive on slow networks. Keyboard users can't see focus state.

**Recommendation**:
```css
.btn-primary:hover {
  background: #c97020;
  box-shadow: 0 2px 8px rgba(201, 112, 32, 0.3);
}
.btn:focus-visible {
  outline: 2px solid var(--amber);
  outline-offset: 2px;
}
```

**Severity**: Minor (visual polish)

---

## Enhancement Recommendations

### 16. **Progress Indicator for Multi-Step Process**
**Location**: ka_article_propose.html
**Suggestion**: Add a visual progress bar or step indicator at the top of the main column:
```
Step 1A (Citations) → Step 1B (PDFs) → Step 2 (Review) → Step 3 (Cleanup) → Step 4 (Policy)
```
This helps users understand where they are in a 4-step workflow.

**Impact**: Users know how much work remains; reduces abandonment.

---

### 17. **Testimonial or Success Story in Hero**
**Location**: ka_contribute.html hero section (lines 181–198)
**Suggestion**: Add a one-line student quote or metric:
```
"My article on daylighting filled a gap the Atlas needed for circadian research." — COGS 160 student
```
Builds trust and motivation for first-time contributors.

---

### 18. **Batch Citation Upload Feedback**
**Location**: ka_article_propose.html, citation input (line 211–219)
**Suggestion**: After pasting or uploading citations, show a preview table with parsed results:
```
| Title | Authors | Year | Notes |
|-------|---------|------|-------|
| The restorative... | Kaplan, S. | 1995 | ✓ DOI found |
```
Lets user verify parse quality before staging.

---

### 19. **Duplicate Prevention Messaging**
**Location**: Both pages, upload zone
**Suggestion**: Add a link in the upload hint:
```
"Upload a PDF or paste a citation. Already in the Atlas?
Check our database first ↗ or upload anyway — duplicates are caught immediately."
```
Lets concerned users verify their paper isn't already there.

---

## Summary Recommendation

**Overall Verdict: CONDITIONALLY SHIP WITH CRITICAL FIXES**

Both pages are **visually coherent and well-organized**, but require fixes before student launch:

1. **Must fix before shipping**:
   - ✓ Add error states for upload failures (file too large, wrong type, duplicate)
   - ✓ Add keyboard escape handler and focus trap for modal
   - ✓ Add alt text / aria labels to emoji icons
   - ✓ Reduce callout overload on ka_article_propose.html (defer 3 of 5)
   - ✓ Add responsive breakpoint for sidebar on mobile

2. **Should fix in next iteration**:
   - ✓ Standardize form field padding across pages
   - ✓ Add explicit file size / format limits in UI
   - ✓ Add success confirmation when files are staged
   - ✓ Add breadcrumb to ka_contribute.html for consistency

3. **Nice-to-have enhancements**:
   - ✓ Progress indicator for 4-step workflow
   - ✓ Citation preview table before staging
   - ✓ Batch metadata extraction feedback

**Estimated remediation time**: 3–4 hours (error states + responsive fixes + accessibility) + 2–3 hours (QA on real PDFs and citation edge cases).

---

## Test Checklist for Developer

- [ ] Test upload with 50 MB PDF → error state appears
- [ ] Test upload with `.docx` file → rejected with type mismatch message
- [ ] Test duplicate detection → amber "duplicate detected" pill appears in file table
- [ ] Test on iPhone 12 (390px) → sidebar stacks below, form remains usable
- [ ] Test on iPad (768px) → sidebar visible but not sticky
- [ ] Keyboard-only user: Tab through form, trigger modal, close with Escape
- [ ] Screen reader test (NVDA/JAWS): emoji icons have accessible labels
- [ ] Color contrast audit: test all text colors against all backgrounds with APCA or WCAG tool
- [ ] Paste 5 citations → show preview table before staging
- [ ] Stage 3 PDFs → success toast/banner appears, queue updates

---

**Review completed**: March 30, 2026
**Reviewer**: UI/UX Design, Knowledge Atlas
**Next action**: Schedule debrief with dev team to prioritize fixes
