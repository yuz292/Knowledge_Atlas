# Science Communication Review: KA Contribute Pages
**Date**: March 30, 2026
**Pages Reviewed**: `ka_contribute.html`, `ka_article_propose.html`
**Audience**: University students (COGS 160), public contributors
**Review Criteria**: Clarity, tone, jargon, redundancy, missing information, action verbs, error handling, label quality, reading level, consistency

---

## Executive Summary

Both pages serve as intake surfaces for research articles but target different user contexts: `ka_contribute.html` is a simplified two-option workflow for broad audiences (public + COGS 160 students), while `ka_article_propose.html` is a detailed four-step workflow for researchers and Track 2 students.

**Overall Assessment**: The writing is **clear and well-structured** but suffers from:
1. **Inconsistent terminology** across the two pages (e.g., "duplicate detection," "intake mode," "metadata extraction")
2. **Jargon without definition** (DOI, APA citation, metadata, extraction, staging, resolution confidence)
3. **Redundant explanations** of the same workflow concepts
4. **Tone mismatch**: ka_contribute.html is friendly and concise; ka_article_propose.html is technical and verbose
5. **Missing guidance** on when to use which page
6. **Inconsistent metaphors**: mixing "pipeline," "extraction," "engine," "intake queue"

The pages are **not failing at their primary job** (guiding users through article submission), but they would benefit from unified terminology, simplified jargon, and clearer role separation.

---

## Page-by-Page Findings

### ka_contribute.html

#### Finding 1: Unclear Primary Action
**Problematic text:**
> "Option A — Submit a Paper"
> "Upload a PDF or paste a citation"

**Issue**: The page has two "options" (A and B), but the action language is asymmetrical. Option A uses imperative "Submit a Paper" while Option B uses "Find Papers We Need." For a student browsing this page, it's unclear whether both are equally important or if one is a prerequisite for the other.

**Suggested revision**:
```
Option A: Contribute a Paper You Already Have
Option B: Discover Papers the Atlas Needs Most
```

This clarifies that A is about *your* discovery; B is about *the system's* needs.

---

#### Finding 2: "Metadata Extraction" Without Definition
**Problematic text:**
> "Drop a PDF below and we handle the rest — metadata extraction, duplicate checking, and staging for review."

**Issue**: The phrase "metadata extraction" appears 4 times on this page. For a 18-22-year-old student, "metadata" may not be obvious. The system extracts author, title, year, DOI—but the term is never defined.

**Suggested revision**:
```
Drop a PDF below and we handle the rest — we automatically pull out the author names,
title, publication year, and DOI. Then we check for duplicates and stage it for review.
```

Or introduce the term once:
```
Drop a PDF and we extract metadata (author names, title, year, DOI) automatically,
then check for duplicates and stage for review.
```

---

#### Finding 3: Inconsistent Status Labels
**Problematic text** (in file table):
```
<span class="status-pill s-ready">READY</span>
<span class="status-pill s-duplicate">DUPLICATE</span>
<span class="status-pill s-staged">STAGED</span>
```

**Issue**: The page shows three status pills but never explains what they mean or when they appear. "STAGED" especially is jargon (borrowed from software development). A student may not understand that "staged" = "ready for nightly reviewer to see."

**Suggested revision**: Add a brief legend below the file table:
```
Status legend:
- READY: This PDF is unique and can be submitted for review
- DUPLICATE: We already have this article in the Atlas
- STAGED: You submitted this; it's in the intake queue waiting for reviewer decision
```

---

#### Finding 4: "Scholar Panel" Guidance Is Buried
**Problematic text**:
> "Search for the theory name combined with one or two constructs. For example: [dynamic example]"

**Issue**: This guidance appears in a panel that only shows *after* clicking a topic chip. A user scrolling the page may never see it. Also, "Search for the theory name combined with one or two constructs" is solid advice, but the phrasing is academic. Undergrads may not think of "theory name" as a searchable term.

**Suggested revision**: Move guidance above the topic grid or add a callout:
```
💡 Tip: Google Scholar works best when you search for a specific theory (e.g., "Attention
Restoration Theory") plus one or two key variables (e.g., "natural environment," "recovery").
Pick a topic below to see example searches.
```

---

#### Finding 5: Missing Workflow Flowchart
**Issue**: The page presents two parallel workflows (Upload PDF vs. Find Papers), but the relationship is unclear. Can you do both in one session? Do you need to complete A before B? Is this a "choose one or the other" scenario?

**Suggested addition**: A brief text summary before the action cards:
```
You have two ways to help build the Atlas:

• If you've already found a paper, upload it (Option A). We handle the rest.
• If you'd rather help fill gaps we've identified, browse our topic list (Option B)
  and use it to guide your search.

You can do both in the same session.
```

---

#### Finding 6: "APA Citation" Assumed to Be Known
**Problematic text**:
> "Paste a full APA citation, a DOI, or a title."

**Issue**: The page assumes students know what "APA citation" means. While COGS 160 students likely have seen APA format, a public contributor may not.

**Suggested revision**:
```
Paste a full citation (APA format), a DOI, or a title. Examples:
• Kaplan, S. (1995). The restorative benefits of nature... Journal of Environmental Psychology...
• 10.1016/0272-4944(95)90001-2
• The restorative benefits of nature
```

---

#### Finding 7: Redundant Explanation of "Why It Matters"
**Problematic text** (end of page):
> "The Atlas is not a bibliography. It is an epistemic engine — and you are one of its sources of fuel."

**Issue**: This is powerful and clarifying, but it comes *after* students have already submitted. The framing ("each article produces dozens of typed propositions") appears at the end, where it should appear at the *beginning* to motivate contribution. Also, the metaphor shift from "biography" to "engine" to "fuel" is jarring in a paragraph meant to inspire.

**Suggested move**: Place a shorter version of this concept in the hero/top section to set context before the action cards.

---

### ka_article_propose.html

#### Finding 8: "Intake Mode" Introduced Without Context
**Problematic text** (early heading):
> "Choose an intake mode"
> "This should become one unified intake surface."

**Issue**: The meta-note "This should become one unified intake surface" appears in the body copy, not in a comment. It signals the page is a work-in-progress and creates confusion about whether the mode choice is temporary or permanent. Also, "intake mode" is not a term students will have heard before.

**Suggested revision**: Remove the meta-note. Rename the section:
```
Step 1: How are you submitting?
Choose whether you have PDFs or just citations ready.
```

---

#### Finding 9: "Staging" Is Used Without Clear Definition
**Problematic text**:
> "Best if you already have PDFs. Duplicate checks happen immediately, but Track 2
> should still attach a usable citation record before staging."

**Issue**: "Staging" appears 8+ times but is never explicitly defined. For a developer, "stage" is clear (prepare for deployment). For a student, it's obscure.

**Suggested revision**: Define it once prominently, then use it consistently:
```
Best if you have PDFs ready. Duplicates are caught immediately. Before you stage
(submit for overnight review), make sure each file has at least author + title or a DOI.
```

---

#### Finding 10: Overly Technical "Security Gate" Callout
**Problematic text**:
> "Security gate: uploaded files are untrusted until validated. The real intake backend
> must verify file type by content, quarantine uploads, hash them, reject encrypted
> or malformed files, and process them in an isolated worker before any promotion
> into the main corpus."

**Issue**: This callout is written for system administrators, not students. The phrase "isolated worker" is backend jargon. A student reading this will be confused about whether *they* need to do something or whether the system handles it.

**Suggested revision**: Either remove it (it's not actionable for the user) or rewrite it:
```
✓ Security: Your uploads are checked for viruses and malicious content before
  being added to the Atlas. If a file is corrupted, you'll be notified.
```

---

#### Finding 11: Conflicting Instructions for Track 2 vs. Public Contributors
**Problematic text** (appears multiple times):
> "Track 2 rule: do not stage an orphan PDF. Before staging, include either a
> pasted APA citation or enough metadata to reconstruct one quickly..."

**Issue**: This page conflates two user types (Track 2 students + public researchers) without clear separation. A public researcher won't know what "Track 2" means. The page should either:
1. Create a clear visual/semantic separation between "Student (Track 2)" instructions and "Public Contributor" instructions, OR
2. Remove Track 2-specific rules and handle them in a separate page.

**Suggested revision**: Add a visual flag at the top of each Track 2 rule:
```
📚 For COGS 160 Track 2 students: Do not stage an orphan PDF. Before submitting,
   include at least author + title or a DOI so we can find the full citation later.
```

---

#### Finding 12: "Resolution Confidence" Is Unexplained
**Problematic text**:
> "resolutionConfidence: 'high' | 'medium' | 'low'"

**Issue**: This term appears in code comments and JavaScript but is never explained to users. What does "high confidence" mean? Should users care about it?

**Suggested revision**: Either remove this detail from user-facing text, or explain it:
```
Confidence level: Whether the system is confident it can find the full citation
from what you provided. High = we have a DOI or exact title match.
Low = we only have partial information.
```

---

#### Finding 13: Inconsistent Field Labels (ka_article_propose vs ka_contribute)
**ka_contribute.html**:
```
Label: "APA citation (one per line)"
Placeholder: "Kaplan, S. (1995)..."
```

**ka_article_propose.html**:
```
Label: "Paste citations, DOI lines, or title lines"
Placeholder: "One citation or DOI per line..."
```

**Issue**: Same functionality, two different label styles. The second is broader (accepts DOI or title alone), but a user might not realize it.

**Suggested revision**: Standardize to:
```
Label: "Paste citations, DOIs, or titles (one per line)"
Hint: "Full APA citation, a DOI (10.xxxx/...), or just a title is acceptable."
```

---

#### Finding 14: "Nightly Review" Process Not Clearly Explained
**Problematic text**:
> "Deferred gate: relevance is reviewed asynchronously in the nightly intake process.
> That means contributors can move quickly, while maintainers make the harder
> inclusion decisions in batch."

**Issue**: The concept is sound (immediate duplicate check + deferred relevance review), but "nightly intake process" is vague. When will the student hear back? What should they do in the meantime?

**Suggested revision**:
```
After you submit, two things happen:
1. Immediate: We check for duplicates (if it's already here, you'll see that right away).
2. Overnight: Our reviewers decide if it's relevant to the Atlas (usually within 24 hours).

You'll see the status in your "Intake Queue" panel.
```

---

#### Finding 15: Missing Jargon: "Constructs" and "Theories"
**Problematic text** (in the topic search):
> "Search for papers related to <strong id="scholarConstructs">—</strong> using one of these tools"

**Issue**: The page assumes students know what a "construct" is in the research sense (e.g., "attention," "stress recovery," "cognitive load"). A freshman may not.

**Suggested addition**: Add a brief tooltip or definitions callout:
```
Looking for constructs? These are the concepts researchers measure—like "attention,"
"visual complexity," "natural light," "recovery time." Theories are bigger frameworks
that explain how constructs relate (e.g., Attention Restoration Theory).
```

---

#### Finding 16: "Identifier" (KA-PROP-XXXX) Not Explained
**Problematic text** (in queue table):
```
<div class="qi-title">KA-PROP-0041: Thermal comfort and cognitive performance...</div>
```

**Issue**: The system assigns each submission a tracking ID, but the format (KA-PROP-XXXX) is never explained. Students may wonder if they need to remember this number.

**Suggested revision**: Add a note in the queue section:
```
Your Intake Queue

Each submission gets a tracking ID (e.g., KA-PROP-0041). Use it to reference your
submission if you contact us with questions.
```

---

#### Finding 17: Unclear File Type Acceptance Language
**Problematic text**:
> "Accepted file types for citation intake: <code>.txt</code>, <code>.csv</code>,
> <code>.ris</code>, and <code>.bib</code>."

**Issue**: This is clear, but the sentence that follows is confusing:
> "In the real backend these would be parsed by the AF importer before de-duplication and staging."

The phrase "AF importer" and "in the real backend" signal this is prototype text, not production guidance. Remove it.

**Suggested revision**: Just state what's accepted:
```
Accepted formats: .txt, .csv, .ris, .bib (BibTeX)

Not sure what format you have? .txt (plain text with one citation per line) always works.
```

---

#### Finding 18: Tone Shift in Callouts
**Problematic text** (multiple callouts):
```
🔵 Immediate gate: duplicate detection happens as soon as the PDF is inspected.
🟠 Deferred gate: relevance is reviewed asynchronously...
🔵 Track 2 rule: do not stage an orphan PDF.
🔴 Storage rule: rejected staged PDFs should be deleted...
```

**Issue**: Four different callout colors (teal, amber, blue, rose) for different rule types, but the categorization is inconsistent. Some are about system behavior (gates), some are about student behavior (rules), some are about storage. No legend explains the color coding.

**Suggested revision**: Either use one color for all procedural rules and explain the color once, or reorganize by category:
```
🔷 What the system does:
- Duplicates are caught immediately.
- Relevance review happens overnight.

📋 What you should do (Track 2):
- Include author + title or DOI before submitting.
```

---

## Consistency Across Pages

### Terminology Inconsistencies

| Concept | ka_contribute.html | ka_article_propose.html | Suggested Standard |
|---------|-------------------|------------------------|-------------------|
| Entry point | "Submit a Paper" | "Propose an Article" | **"Submit an Article"** (shorter, more direct) |
| PDF checking | "duplicate checking" | "duplicate detection" | **"duplicate check"** (noun) or **"we check for duplicates"** (verb) |
| Process | "metadata extraction" | "DOI/title extraction" | **"we extract citation info"** (concrete) |
| Storage | "staging" | "staging for review" / "staged items" | **"submit for review"** (simpler) |
| Processing | "extraction pipeline" | "intake queue" / "extraction queue" | **"review queue"** or **"intake queue"** (pick one) |
| Citation input | "APA citation" | "citation, DOI, or title" | **"citation (APA, DOI, or title)"** |
| System behavior | "nightly — accepted papers enter the extraction pipeline" | "nightly intake process" | **"overnight review; you'll see status updates in your queue"** |
| Metadata fields | "Author Names, Title, Year, DOI" | "First author or author string, Probable title, DOI, Year" | **Standardize labels** (see below) |

---

### Metadata Field Labels (Should Be Identical)

**Current state**: Fields have slightly different labels and placeholders across pages.

| Field | ka_contribute.html | ka_article_propose.html | Suggested Standard |
|-------|-------------------|------------------------|-------------------|
| Authors | "Authors" (placeholder: "Last, F. M., ...") | "First author or author string" | **"Authors"** with hint: "Last, F., Last, F., & Last, F." or just "Last, F." |
| Publication Year | "Year" | "Year" | ✓ **Consistent** |
| Journal | "Journal" | "Journal / venue" | **"Journal or venue"** (include venue for conferences) |
| How to cite | Not present | "Preferred citation / APA line" | **Include on both pages** or clarify when it's needed |

---

## Jargon Assessment & Definitions Needed

| Term | Used in | Clarity | Suggested Action |
|------|---------|---------|-------------------|
| **DOI** | Both pages, multiple times | Low (not defined) | Add definition: "A Digital Object Identifier—a permanent ID for an article, like 10.1234/example" |
| **APA citation** | Both pages | Medium (students likely know, but public contributors may not) | Add example: "Kaplan, S. (1995). Title. Journal, 15(3), 169–182." |
| **Metadata** | Both pages (4+ times) | Low (undefined jargon) | Replace with "citation info" or define once: "metadata = author, title, year, DOI" |
| **Extraction** | Both pages | Low (abstract concept) | Simplify: "we pull out the author, title, and other details automatically" |
| **Staging** | ka_article_propose | Low (software jargon) | Replace: "submit for review" or define: "stage = prepare and submit for overnight review" |
| **Constructs** | ka_article_propose (in scholars panel) | Low (research jargon) | Add tooltip: "Constructs = measurable concepts (e.g., attention, stress, light levels)" |
| **Theories** | ka_article_propose (implicit) | Medium | Define via example: "Attention Restoration Theory explains how nature reduces mental fatigue" |
| **Resolution confidence** | ka_article_propose (code) | N/A (not visible to users) | Remove from user-facing text or explain: "confidence = how certain we are about the citation" |
| **Warrant** | References in hero section (ka_contribute) | Low (epistemic jargon, domain-specific) | Context-dependent; used correctly but may confuse general readers |
| **Nightly intake** | ka_article_propose | Low (temporal + process jargon) | Replace: "overnight review" |

---

## Recommendations: Priority Order

### Critical (Clarity & Safety)

1. **Standardize "Submit" vs. "Propose" language** across both pages.
   → Use "Submit" throughout. It's clearer and shorter.

2. **Define or replace "metadata extraction"** on both pages.
   → Replace with: "we automatically extract the author, title, year, and DOI."

3. **Add a legend for status pills** (READY, DUPLICATE, STAGED) on ka_contribute.html.
   → Show what each status means and when it appears.

4. **Separate Track 2 instructions from public contributor instructions** on ka_article_propose.html.
   → Use visual flags (📚 badge) or a separate section.

### High (Consistency & Tone)

5. **Standardize field labels** (Authors, Journal, Citation) across both pages.
   → Use the same label text and placeholders everywhere.

6. **Replace jargon with concrete language** (staging → submit, extraction → pull out, nightly → overnight).
   → Keep technical jargon out of user instructions.

7. **Add examples for every field that accepts structured input** (citation format, DOI format, author format).
   → Show students exactly what the system wants.

8. **Create a unified "Intake Queue" explanation** on both pages.
   → Explain what "pending," "approved," "rejected," "duplicate" mean.

### Medium (Discoverability)

9. **Move "Why It Matters" section higher** on ka_contribute.html.
   → Motivate contribution before asking for input.

10. **Add a workflow diagram or flowchart** explaining when to use each page.
    → Clarify the relationship between ka_contribute and ka_article_propose.

11. **Document the KA-PROP-XXXX tracking ID format** in the queue section.
    → Explain what it's for and that students don't need to memorize it.

### Low (Polish)

12. Remove prototype/backend notes like "This should become one unified intake surface" and "In the real backend..."
    → These break immersion and create doubt about the system.

13. Standardize callout color meanings or remove color-coding altogether.
    → Use consistent visual hierarchy (one color for critical info, one for tips).

---

## Suggested Unified Jargon Glossary

Create a shared file (e.g., `docs/KA_TERMINOLOGY.md`) with these definitions. Link to it from both pages.

| Term | Definition | Example |
|------|-----------|---------|
| **Article / Paper** | A peer-reviewed research study. The Atlas accepts articles from journals, conferences, and verified preprints. | Kaplan's 1995 study on attention restoration |
| **Citation** | A formatted reference to an article, including author, title, year, and journal. The Atlas uses APA format. | Kaplan, S. (1995). The restorative benefits of nature... |
| **DOI** | Digital Object Identifier. A permanent web address for an article, starting with "10.". | 10.1016/0272-4944(95)90001-2 |
| **Duplicate** | An article the Atlas already contains. Duplicates are blocked immediately. | If you upload a 2nd copy of Kaplan 1995, it's marked as a duplicate. |
| **Intake Queue** | A list of articles you've submitted, showing their review status. | "3 pending, 1 approved, 2 rejected" |
| **Metadata** | Citation information: author, title, year, journal, DOI. | From a PDF, the system auto-extracts title and year. |
| **Status** | The current review stage of your submission. Examples: Pending (waiting for review), Approved (accepted into the Atlas), Rejected (not relevant), Duplicate (already exists). | Your Thermal Comfort submission is "pending" overnight review. |
| **Submit / Stage** | To formally enter an article into the intake queue for review. | Click "Submit for Review" after adding the citation info. |
| **Track 2** | A cohort of COGS 160 students completing a structured article-finding assignment. | COGS 160 Spring 2026 students are in Track 2. |
| **Construct** | A measurable concept or variable in research. Examples: attention, stress, cognitive load, natural light. | The paper measures two constructs: attention restoration and heart rate variability. |
| **Theory** | A framework explaining how constructs relate. | Attention Restoration Theory explains why nature helps people recover from mental fatigue. |

---

## Test Cases for Clarity

To validate improvements, have 2-3 undergraduate readers attempt these tasks:

1. **Upload a PDF**
   → Can they find the upload zone without reading every word?
   → Do they understand what "duplicate" means if one is detected?

2. **Find papers we need**
   → Can they understand the difference between a topic with "3 papers" vs. "8 papers"?
   → Do they know what to search for after selecting a topic?

3. **Submit using a citation instead of a PDF**
   → Can they identify where to paste a citation?
   → Do they understand the difference between ka_contribute and ka_article_propose?

4. **Track their submission**
   → Can they find their intake queue?
   → Do they understand what "pending," "approved," "rejected" mean?

---

## Final Notes

**Tone**: Both pages strike an appropriate balance between professional and approachable. The metaphor of "epistemic engine" is powerful but might be better positioned earlier in the journey.

**Accessibility**: Color alone is used to distinguish status pills (good—the system has fallback text labels), but the callout colors on ka_article_propose are purely decorative and should either be explained or removed.

**Mobile responsiveness**: The CSS uses responsive grids, which is good. No copy changes needed for mobile readability.

