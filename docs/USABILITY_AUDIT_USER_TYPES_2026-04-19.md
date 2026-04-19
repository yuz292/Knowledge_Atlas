# Knowledge Atlas — Per-Persona Usability Audit

**Date**: 2026-04-19
**Author**: CW (Claude Code), heuristic audit agent
**Method**: Nielsen (1994) ten-heuristic walkthrough, scenario-based evaluation after Rosson & Carroll (2002), severity scored per Nielsen's 1–5 scale
**Primary personas audited**: `160_student`, `public_visitor`, `admin`
**Scope**: 83 root-level pages and 35 pages under `160sp/`, excluding `.bak` backups, `_demo` sandbox pages, and pages with no plausible journey for any of the three personas
**Audit budget**: Evaluation by document walkthrough; no live click-through. Findings are anchored to the literal text and markup of the HTML on disk as of this date.

---

## 1. Executive Summary

Knowledge Atlas presents three structural tensions that cost all three end-user personas. First, the root home page (`ka_home.html`) mixes a role router, a "Did you know?" evidence reel, an "About the Atlas" strip, and a release-notes feed into a single layout; the result is a hero that serves neither a first-time public visitor (who gets a text-wall of epistemology in two lines and a four-button role router with no explanation of what a "Contributor" is) nor a 160 Student (whose button is one of four, visually de-emphasised against the primary "Researcher" CTA). Second, the Topics page family has exploded into six near-duplicate variants (`ka_topics.html`, `ka_topic_facet_view.html`, `ka_topic_heatmap_view.html`, `ka_topic_full_facets_view.html`, `ka_topic_dashboard_view.html`, `ka_topic_quick_lookup_view.html`), each appropriate for a different persona but all shown to every visitor via a variant-row that reads "Other Topic Page Versions" — a meta-design artifact that leaks the development process to the reader. Third, the 160sp sub-site and the global site use two different navbar idioms: `160sp/ka_student_setup.html` renders its own `<nav>` alongside the canonical `ka_canonical_navbar.js` slot, producing double navigation on the page that is meant to be the student's first landed experience.

The ten highest-severity findings (severity-weighted, persona-weighted) are:

1. `ka_home.html` role router mis-routes the 160 Student to `ka_schedule.html` rather than the documented setup page `160sp/ka_student_setup.html` — contradicts the default-route memory and breaks the intended onboarding.
2. `ka_topics.html` exposes six topic variants at the top of every visit, forcing the persona to re-choose a view every time; no variant is labelled by persona fit.
3. `ka_framework_pp.html` (and the other ten T1 pages) lead with a "Draft — pending neuroscience panel review" banner, which reads as broken to public visitors and as scary/provisional to 160 students trying to cite it.
4. `ka_contribute.html` is a 740-line omnibus offering article upload + pipeline tools + contributor onboarding; it serves contributor-side personas and is an overwhelming dead end for a practitioner clicking "I want to help".
5. `160sp/ka_student_setup.html` double-renders navigation (its own `<nav>` plus the canonical slot) and lists "A0" and "A1" as unexplained tokens.
6. `160sp/ka_admin.html` has no visible authentication gate in the HTML — a public visitor following a referrer to this URL lands on the instructor admin without feedback that they should not be there.
7. `ka_articles.html` offers an "EN status" filter with values (strong / moderate / weak / contested) that no public visitor can interpret without reading `ka_about.html`.
8. `ka_theories.html` opens with "Tier 1 (T1) frameworks are the foundational, mostly domain-neutral mechanisms ... Tier 1.5 (T1.5) domain theories apply two or more T1 frameworks" — a construction that presumes the reader has already read the hierarchy document.
9. `ka_article_view.html` empty state for a missing `?id=` says "No article id specified" — a JSON-shaped message that is useless to a practitioner who arrived via a stale link.
10. `ka_about.html` lists four audiences, but the fourth ("COGS 160 students") links to `160sp/ka_schedule.html`, not the student setup page, mirroring the home-page mis-route.

**Three pages most urgently needing a persona-specific variant**:
- `ka_home.html` — split into `ka_home_public.html` (clean public landing with three Did-You-Know cards and an About block), retain `ka_home.html` as the authenticated home router, and ensure `ka_home_student.html` already present actually receives the 160-Student traffic.
- `ka_topics.html` — keep as the admin/technical "Classic View" but ship `ka_topics_student_view.html` and `ka_topics_public_view.html` that each default to exactly one of the six existing variants (Quick Lookup for public, Dashboard for student).
- `ka_contribute.html` — split into `ka_contribute_public.html` (a one-page "how to submit an article" primer) and `ka_contribute_internal.html` (the pipeline-and-tools omnibus currently at the canonical URL).

**Broad pattern**: the site is optimised for the *author* persona (David) inspecting his own Web of Belief, and is serving every end-user persona through that lens. The most economical fix is not more pages — it is user-type-aware defaults on the existing pages, plus variant-creation for the four pages where the persona need is genuinely divergent.

---

## 2. Methodology

The audit evaluates each (page, persona) pair along four dimensions adapted from Nielsen (1994) and Krug (2014). **Reach** is a binary-plus-accidental judgement: can this persona plausibly arrive here through the canonical entry (Google search, emailed link, post-login redirect) without being accidentally routed? **Comprehensibility** is a 0–3 integer: 0 indicates the page is opaque without external context, 3 indicates language and layout are calibrated to the persona's vocabulary and mental model. **Served** is a separate 0–3 integer: does the page actually meet the persona's task for being there, even when comprehensible? (A page can be comprehensible but useless — a personal FAQ for someone who came for live data.) **Severity** is scored per Nielsen's catastrophe scale (1 cosmetic, 5 blocks all use) and is only recorded when comprehensibility + served is less than 4 (i.e. the composite is "meh" or worse). **Recommendation** picks among `accept`, `polish`, `restructure`, `split`, `redirect`.

Personas 1–4 in the canonical persona document (author, course designer, senior researcher, graduate student) are excluded because they are maker-side; they build KA rather than end-use it. The three personas audited fold persona 5 + 6 (160 Student), persona 7 + 8 (public visitor), and persona 2's administrative half (admin). Pages excluded: the `.bak` backup, `ka_home_student_new.html` (a staging twin of `ka_home_student.html`), four demo and playground pages, the 11 individual framework pages (audited as a class via `ka_framework_pp.html`), and the 13 individual T1.5 theory pages (audited as a class via `ka_theory_art.html`). The 12 topic variants are audited as a class via `ka_topics.html` plus the five newer variants; the 4 track-hub pages are audited as a class via `ka_track1_hub.html`. Severity-3-or-higher findings quote the literal HTML text or DOM element that fails. I did not exercise JavaScript side-effects (the canonical navbar's session-storage state machine) except where the rendered default state was visible in the markup.

---

## 3. Per-Persona Page Matrices

### 3.1 `160_student` — Undergraduate in COGS 160 Spring 2026

Entry point: direct link from Canvas, from a Slack channel, or through `ka_home.html` with a prior 160-student role cookie.

| Page | Reach | Comp | Served | Sev | Rec | One-line finding |
|------|:-----:|:----:|:------:|:---:|:---:|------------------|
| `ka_home.html` | yes | 1 | 1 | 3 | split | Role router mis-routes to `ka_schedule.html`; 160-student button is not visually primary for a logged-in student. |
| `160sp/ka_student_setup.html` | yes | 2 | 2 | 3 | polish | Accordions for done items are good; the `<nav>` duplicates the canonical navbar slot above it. |
| `160sp/ka_schedule.html` | yes | 2 | 3 | 2 | polish | Week-card layout works; `Phase: all/track/debug` pills introduce an internal taxonomy with no glossary. |
| `160sp/ka_track1_hub.html` | yes (if T1) | 2 | 2 | 3 | restructure | "Region 1 … Region 4" is an internal naming convention; students want "Setup · Resources · How we work · Tasks". |
| `160sp/ka_track2_hub.html` | yes (if T2) | 2 | 2 | 3 | restructure | Same as above; also exposes `imagehash` / `tesseract` CLI setup with no prerequisite note. |
| `160sp/ka_track3_hub.html` | yes (if T3) | 2 | 2 | 2 | polish | VR track references hardware the student may not have. |
| `160sp/ka_track4_hub.html` | yes (if T4) | 2 | 3 | 2 | accept | Best calibrated of the four hubs; students hit the right deliverables quickly. |
| `160sp/ka_thursday_tasks.html` | yes | 3 | 3 | — | accept | Clean weekly task view. |
| `160sp/ka_student_profile.html` | yes | 2 | 2 | 2 | polish | Profile fields are OK but grade view is deferred; student cannot see assignment marks inline. |
| `160sp/ka_gui_assignment.html` | yes | 2 | 2 | 3 | restructure | Assignment page mixes rubric, scenarios, and submission bin; students lose the "what I turn in" thread. |
| `160sp/ka_tag_assignment.html` | yes | 2 | 2 | 3 | restructure | Same pattern — rubric and submission interleaved. |
| `160sp/ka_vr_assignment.html` | yes | 2 | 2 | 3 | restructure | Same. |
| `160sp/ka_article_finder_assignment.html` | yes | 2 | 2 | 3 | restructure | Same. |
| `160sp/ka_collect_articles.html` | yes | 3 | 3 | — | accept | Clear task + upload action; well calibrated to the persona. |
| `160sp/ka_google_search_guide.html` | yes | 3 | 3 | — | accept | Tutorial style; good for undergrads with varying research experience. |
| `160sp/ka_github_access.html` | yes | 2 | 2 | 3 | polish | Assumes `ssh-keygen` familiarity; a 20-year-old cognitive-science major may not have it. |
| `160sp/ka_technical_setup.html` | yes | 2 | 2 | 3 | polish | Same as above; needs a "never done this before" branch. |
| `ka_theories.html` | yes | 1 | 2 | 3 | split | Theory-tier prose assumes the hierarchy-document vocabulary the student has not yet encountered. |
| `ka_articles.html` | yes | 1 | 2 | 3 | split | EN-status filter values are un-defined inline; student will guess. |
| `ka_article_view.html` | yes | 2 | 2 | 2 | polish | Layout is clean but the empty state is technical ("No article id specified … pass `?id=PDF-XXXX`"). |
| `ka_about.html` | yes | 2 | 2 | 2 | polish | OK reference page; the "Four audiences" paragraph links the student to the wrong URL (same bug as home). |
| `ka_ai_methodology.html` | yes | 2 | 3 | 2 | accept | Long but necessary; this is a teaching-first page. |
| `ka_sitemap.html` | yes (rarely) | 2 | 2 | 1 | accept | Secondary navigation; fine. |

### 3.2 `public_visitor` — Architect, journalist, or researcher arriving via external link

Entry point: `ka_home.html` from a Google result, or a deep link to `ka_article_view.html?id=PDF-xxxx` / `ka_topics.html`.

| Page | Reach | Comp | Served | Sev | Rec | One-line finding |
|------|:-----:|:----:|:------:|:---:|:---:|------------------|
| `ka_home.html` | yes | 1 | 2 | 3 | split | Role router reads as "pick your role so we know who you are" before the visitor knows whether KA is for them. |
| `ka_home_practitioner.html` | yes (if routed) | 2 | 2 | 2 | polish | Better framed for practitioners but not linked from the public hero. |
| `ka_home_researcher.html` | yes (if routed) | 2 | 2 | 2 | polish | Similar; duplicated with practitioner version. |
| `ka_topics.html` | yes | 0 | 1 | 4 | split | "Classic View" + six variants row at the top is meta-design debt shown to every outside visitor. |
| `ka_topic_facet_view.html` | accidentally | 0 | 1 | 4 | redirect | Power-user view; dropped on a non-specialist unprepared for facet syntax. |
| `ka_topic_heatmap_view.html` | accidentally | 1 | 1 | 3 | redirect | Architectural families × outcomes heatmap is legible only once the taxonomies are known. |
| `ka_topic_full_facets_view.html` | accidentally | 0 | 0 | 4 | redirect | Densest of the six; not a public front door. |
| `ka_topic_dashboard_view.html` | accidentally | 2 | 2 | 2 | polish | Three linked panels actually work well for an inquisitive public visitor — best default for this persona. |
| `ka_topic_quick_lookup_view.html` | accidentally | 3 | 3 | — | accept | Two dropdowns is the simplest door; should be the public default. |
| `ka_topic_hierarchy.html` | accidentally | 1 | 1 | 3 | redirect | Technical; internal map of the ontology. |
| `ka_theories.html` | yes | 1 | 2 | 3 | split | Tier vocabulary assumed; 11 frameworks with two-letter codes read as jargon first. |
| `ka_theory.html` | yes | 1 | 1 | 3 | restructure | Single-theory page with no mid-layer between the T1.5 entries and the encyclopedic framework pages. |
| `ka_theory_art.html` (and 12 other T1.5 pages) | yes | 2 | 3 | 2 | polish | Georgia-serif hero reads well; the in-page TOC nets the visitor into the evidence. |
| `ka_framework_pp.html` (and 10 other T1 pages) | yes | 2 | 2 | 3 | polish | "Draft — pending panel review" banner leads; damages the page's perceived status. |
| `ka_articles.html` | yes | 1 | 1 | 3 | split | Filters are good but the pills rely on a private vocabulary. |
| `ka_article_view.html` | yes (via deep link) | 1 | 1 | 3 | polish | Loads via JS fetch; degraded on first render with "Loading article record…"; fails on `file://`. |
| `ka_contribute.html` | yes (if curious) | 1 | 0 | 4 | split | Practitioner clicks "Contribute" expecting a "how to submit one article" page; gets an internal omnibus. |
| `ka_about.html` | yes | 2 | 3 | 2 | accept | Most persona-neutral page on the site; good landing for a curious outsider. |
| `ka_archive.html` | accidentally | 1 | 1 | 2 | restructure | Archive of deprecated items; should be gated out of public nav. |
| `ka_annotations.html` | accidentally | 0 | 0 | 4 | redirect | Internal annotation layer; no public purpose. |
| `ka_explain_system.html` | yes (from About) | 2 | 2 | 2 | polish | Useful second-order reference; prose is dense but readable. |
| `ka_gaps.html` | accidentally | 1 | 1 | 3 | redirect | Research Gaps view is maker-side, not end-user-side. |
| `ka_mechanisms.html` | yes | 1 | 1 | 3 | split | 71 mechanism profiles assumes neuroscience vocabulary; no public primer. |
| `ka_sitemap.html` | yes | 2 | 2 | 2 | accept | Fine. |

### 3.3 `admin` — Instructor (DK), TA, or track lead

Entry point: `160sp/ka_admin.html` or `ka_instructor_login_recovery.html`; after login proceeds to roster, grading, announcements.

| Page | Reach | Comp | Served | Sev | Rec | One-line finding |
|------|:-----:|:----:|:------:|:---:|:---:|------------------|
| `ka_login.html` | yes | 2 | 3 | 2 | polish | Login works; no admin-specific branch. |
| `ka_instructor_login_recovery.html` | yes | 2 | 2 | 2 | polish | Narrow purpose; serves recovery. |
| `160sp/ka_admin.html` | yes | 2 | 2 | 3 | restructure | Tabs exist but no visible auth gate in HTML; `<meta name="robots" content="noindex, nofollow">` is the only defence. |
| `160sp/ka_approve.html` | yes | 3 | 3 | — | accept | Well-scoped approval flow. |
| `160sp/ka_dashboard.html` | yes | 2 | 3 | 2 | polish | KPI tiles are strong; course-state links scattered. |
| `160sp/ka_track_signup.html` | yes | 2 | 2 | 2 | polish | Admin sees student choices, but cannot override inline. |
| `ka_instructor_review.html` | yes | 2 | 2 | 3 | polish | Review queue exists; no "what's urgent this week" sort. |
| `ka_my_work.html` | yes | 2 | 2 | 2 | polish | Mixes student-view and instructor-view in one page. |
| `ka_user_home.html` | yes | 1 | 1 | 3 | restructure | Generic user home; admin does not need this. |
| `ka_account_settings.html` | yes | 2 | 2 | 2 | accept | Standard settings page. |
| `ka_archive.html` | yes | 2 | 2 | 1 | accept | Admin-appropriate historical record. |
| `ka_annotations.html` | yes | 2 | 3 | 1 | accept | Makes sense for the admin maintaining annotation sets. |
| `ka_datacapture.html` | yes | 2 | 2 | 2 | polish | Pipeline-capture page; technical but the admin is technical. |
| `ka_gaps.html` | yes | 2 | 2 | 2 | accept | Research Gaps view; works for the admin. |
| `ka_tagger.html` | yes | 2 | 2 | 2 | accept | Internal tagging tool; appropriate for admin. |
| `ka_workflow_hub.html` | yes | 2 | 2 | 2 | polish | Good overview; link density a touch high. |
| `ka_hypothesis_builder.html` | yes | 2 | 2 | 2 | accept | Specialist tool; admin-appropriate. |
| `ka_contribute.html` | yes | 2 | 3 | 1 | accept | Admin is the intended audience for this page. |
| `ka_topics.html` | yes | 3 | 3 | — | accept | "Classic View" is the admin's preferred default. |
| `ka_articles.html` | yes | 3 | 3 | — | accept | EN filter vocabulary is native to the admin. |
| `ka_theories.html` | yes | 3 | 3 | — | accept | Tier vocabulary is native. |

---

## 4. Per-Page Deep Dives (pages flagged `split`)

The ten pages below are the cases where a single URL cannot comprehensibly serve all three end-user personas. Each entry ends with a proposed filename pattern and the minimum per-variant differences.

### 4.1 `ka_home.html` → `ka_home.html` + `ka_home_public.html` (student variant already present)

The current home opens with a warm-green hero and tagline — "Cognitive neuroscience for architecture. A working research atlas joining what neuroscience knows about perception, attention, affect, and memory to how buildings and landscapes shape the people who live in them." Below the hero sits a four-button role router titled "Pick where you'd like to start". Three buttons (Researcher, Contributor, Practitioner) read as professional roles the visitor may or may not identify with; the fourth, "160 Student · COGS 160 Spring 2026", is an in-joke to everyone else and a flashing sign to the enrolled undergraduate — but it routes to `160sp/ka_schedule.html`, not the documented default of `160sp/ka_student_setup.html`, violating the roles memo. For the public visitor the page wastes its primary above-fold real estate on role disambiguation before delivering any Did-You-Know content.

**Variant plan**:
- `ka_home.html` becomes a thin redirector: role cookie present → straight to the matching home; else → public home.
- `ka_home_public.html` (new): three Did-You-Know cards above fold, About strip second, updates third, no role router; a small "I'm enrolled in COGS 160 →" and "I'm an instructor →" link at the footer.
- `ka_home_student.html` (exists): tie this to the role-cookie path and fix the destination from setup-vs-schedule.
- `ka_home_instructor.html` (exists): ensure this is what returns admins to after login.

### 4.2 `ka_topics.html` → `ka_topics_student_view.html` + `ka_topics_public_view.html` (keep original as admin)

The Classic-View topic browser is a two-pane layout that is excellent for an admin who wants to scan the 72 topics, but its top strip reads: "Other Topic Page Versions · 1. Facet View · 2. Heatmap View · 3. Full Facets · 4. Dashboard View · 5. Quick Lookup · 6. Classic View". This is an engineering decision that should not reach the end user. Public visitors and students need exactly one entry door per persona; they should not be offered a menu of visualisation paradigms at the point of first contact.

**Variant plan**:
- `ka_topics.html` (keep): Classic View remains as the admin/maker default, variant-row moves to the bottom.
- `ka_topics_public_view.html` (new): loads the Quick-Lookup bidirectional dropdown by default; hides the variant-row; has a "Looking for more?" link to the About and Articles pages.
- `ka_topics_student_view.html` (new): loads the Dashboard-View linked panels by default because COGS 160 needs to teach the crosswalk pattern; includes a narrow "For your track" callout that reads from `localStorage.ka_current_track`.

### 4.3 `ka_contribute.html` → `ka_contribute_public.html` + `ka_contribute_internal.html`

The contribute page is a 740-line omnibus: top-nav plus a hero "Contribute to the Atlas" plus action-card grid (Upload Article, Upload Image, Upload Bulk CSV, Propose Topic) plus a pipeline section plus a contributor-onboarding FAQ. A practitioner who clicks the Contribute link in the navbar because she thinks her own paper should be in the corpus does not understand why the page offers her "Run the EN rescoring pipeline". The page is right for a COGS 160 Week 4 contributor or a returning collaborator, and wrong for everyone else.

**Variant plan**:
- `ka_contribute.html` (keep) redirects to `ka_contribute_internal.html` for the existing user-type cookie regime.
- `ka_contribute_public.html` (new): a one-page "Suggest an article" form + a "What happens after you suggest?" box + a "Interested in deeper collaboration?" contact link.
- `ka_contribute_internal.html` (new, from the current omnibus): everything currently on `ka_contribute.html`, unchanged.

### 4.4 `ka_theories.html` → `ka_theories_public_view.html` (keep original)

Tier 1 / Tier 1.5 vocabulary is load-bearing for the admin and the maker personas, but it is a wall for the public visitor. A practitioner or journalist wants "Here are eleven ideas about how brains make sense of buildings" not "Tier 1.5 domain theories apply two or more T1 frameworks to a specific architectural or environmental concern." The information architecture is correct; the rhetoric is aimed at the wrong reader.

**Variant plan**:
- `ka_theories.html` (keep): unchanged, with its tier taxonomy intact for maker use.
- `ka_theories_public_view.html` (new): eleven foundational frameworks as a gallery of cards with lay titles ("How your brain predicts the next room") before the technical name; Tier 1.5 theories below as "Theories that apply these ideas to design". No tier codes visible above fold.

### 4.5 `ka_articles.html` → `ka_articles_public_view.html` (keep original)

The filter toolbar is good but the EN-status filter (Strong / Moderate / Weak / Contested) is a private vocabulary. A public visitor encounters "EN status" with no hover or footnote and will either select randomly or abandon the filter. A student hits the same wall but at least has a syllabus path to the definition.

**Variant plan**:
- `ka_articles.html` (keep): admin-level filters remain visible.
- `ka_articles_public_view.html` (new): replaces EN-status with a single "Evidence strength" pill filter whose options are "Well-supported", "Mixed", "Limited", "Contested"; an info-icon per pill links to a 150-word explainer.

### 4.6 `ka_framework_pp.html` (and 10 peers) → add a `view=public` parameter rather than a new file

The draft banner on every T1 framework page says: "Draft — pending neuroscience panel review. This page is a first-pass sci-writer explainer, LLM-drafted 2026-04-17 for instructor and panel review before it becomes canonical on the site." This is true and right for an admin or a panel reviewer; it is damaging for a public visitor who reads "Draft … LLM-drafted" and downgrades the entire site's credibility. Severity 3 for public visitors; severity 1 for admins.

**Variant plan**: a single-file solution is adequate. Hide the draft banner under a `?view=public` query parameter or under the `ka.userType === 'visitor'` session-storage check, and render a milder "Last updated 2026-04-17 · in review" caption instead. No new page required.

### 4.7 `ka_mechanisms.html` → `ka_mechanisms_public_view.html` (keep original)

Seventy-one mechanism profiles is right for the admin who maintains them; a public visitor wants a page that says "the brain mechanisms KA tracks" with ten or twelve curated examples. The full list belongs behind a "See all mechanisms" link.

**Variant plan**: `ka_mechanisms.html` stays for makers; `ka_mechanisms_public_view.html` shows a shortlist and a drill-down link.

### 4.8 `ka_topic_facet_view.html`, `ka_topic_full_facets_view.html`, `ka_topic_hierarchy.html` → `redirect` for public visitors

Three of the six topic-page variants do not belong in a public visitor's journey at all. They are comparison-first tools for the admin persona. The `variant-row` should hide them when the user-type cookie is `visitor` or absent, and they should not appear in the site navbar.

### 4.9 `ka_gaps.html`, `ka_annotations.html`, `ka_archive.html` → `redirect` for public visitors

Gap identification, the annotation layer, and the archive are admin-or-maker surfaces. They should be reachable from `ka_admin.html` and the instructor dashboard but not linkable from a public browsing session.

### 4.10 `160sp/ka_admin.html` → visible auth gate + restructure

The admin page loads whatever the user types into the URL. The only current defence is `<meta name="robots" content="noindex, nofollow">`, which prevents search indexing but does nothing to stop a cold visitor who guesses the path or follows a Slack screenshot. The HTML renders KPI tiles and tables immediately. Severity 3: there is no secret data on the admin page yet, but the page teaches a visitor the shape of the admin surface.

**Plan**: wrap the admin page in a client-side redirect to `ka_login.html` when `sessionStorage.ka.admin !== 'yes'`; additionally, add a server-side gate before production. This is a `polish` on severity but the report recommends treating it as blocking.

---

## 5. Cross-Persona Findings

Five patterns cut across the three personas and deserve a single fix rather than per-page patching.

**Nav regime boundaries are opaque.** The canonical navbar renders two different item inventories depending on whether the URL contains `/160sp/`: the global regime shows Articles · Topics · Theories · Mechanisms · Neural Underpinnings · Contribute · About; the `160sp` regime shows Syllabus · A0 · A1 · Track 1–4. A student who lands on `ka_home.html` while logged in sees the global nav and cannot find her assignments without first learning the URL structure. The navbar contract assumes the user understands the regime split; no user does. A consistent fix would surface a single "Your workspace" breadcrumb pill on the right side of the navbar that reads the role cookie and links to the correct sub-home regardless of the regime the browser is currently in. This is already roughly what `ka_canonical_navbar.js` intends via the right-slot state machine — the implementation just hasn't percolated to every page.

**Epistemic vocabulary leaks through the front end.** "EN status", "T1 / T1.5", "warrant type", "Quinean coherentist evaluation" all appear in copy aimed at the public visitor. Haack (1993) on foundherentism and Quinean coherentism is appropriate for a panel paper, not for a Did-You-Know card. Every public-facing page should be audited against the Pinker-Sagan-Yong writing norms David's own `SCIENCE_COMMUNICATION_NORMS.md` encodes, with a linter that flags terms from a private-vocabulary list.

**The six topic-page variants are a design conversation made public.** The variant-row at the top of each topic page is an artefact of an A/B comparison that should have ended with a choice. Keeping all six alive means the team has not decided; keeping all six *visible by default* means every visitor bears the cost of that indecision. Tufte's (1983) principle that a reader should not have to compute what the designer ought to have computed applies directly: pick a default per persona and let the variant-row live on an `admin` surface.

**The 160 Student path has two competing entry pages.** `160sp/ka_student_setup.html` exists specifically as a track-picker landing; the home-page role router sends 160 students to `160sp/ka_schedule.html`; the About page also points to `160sp/ka_schedule.html`. The canonical memory says `ka_student_setup.html` is the default. Three URLs compete. Pick one, update the other two, and delete the memory ambiguity.

**Draft / provisional markers are persona-inappropriate.** Some pages (the 11 T1 frameworks) proudly announce they are drafts pending review. Others (the admin dashboard) silently ship without any readiness marker. The inconsistency is worse than either extreme; a single banner convention (`data-ka-readiness="draft|review|published"` on the body, rendered by a shared script) would let public pages suppress draft labels and admin pages surface them. The `ka_canonical_navbar.js` is the natural place to add this.

---

## 6. Recommendations, Prioritised

The following nine items are ranked by user-benefit per hour of work. Impact is scored 1–5; effort is scored in CW-hours of implementation.

| # | Recommendation | Impact | Effort | Owner |
|---|----------------|:------:|:------:|-------|
| 1 | Fix `ka_home.html` and `ka_about.html` 160-student links to point to `160sp/ka_student_setup.html`. | 5 | 0.5 h | CW |
| 2 | Hide or gate the topic-variant row on `ka_topics.html` and the five variant pages when `userType ≠ admin`. | 5 | 1.5 h | CW |
| 3 | Gate `160sp/ka_admin.html` behind a client-side session check and add a visible "Admin-only" hint above fold. | 4 | 1 h | CW |
| 4 | Ship `ka_contribute_public.html` as a one-page submission primer; route the navbar Contribute link there for visitors. | 4 | 3 h | CW |
| 5 | Ship `ka_topics_public_view.html` (default to Quick Lookup) and `ka_topics_student_view.html` (default to Dashboard View). | 4 | 4 h | CW |
| 6 | Add a `data-ka-readiness` body attribute and a navbar-script-rendered banner; suppress draft banners on public views. | 3 | 2 h | CW |
| 7 | Rewrite the `ka_articles.html` EN-status filter for the public variant; add an info-icon glossary. | 3 | 2 h | CW + panel |
| 8 | Re-draft the `ka_theories.html` public opening paragraph in plain language; keep the tier-table on the admin variant. | 3 | 2 h | DK + CW |
| 9 | Unify `160sp/ka_student_setup.html`'s nav (remove the in-page `<nav>`, rely on canonical). | 2 | 0.5 h | CW |

**Estimated total**: ~16.5 CW-hours to close the top nine items. The report intentionally omits the 11 T1 framework pages as individual split candidates because the single-file `?view=public` switch in item 6 covers them.

---

## 7. References

Ericsson, K. A., & Simon, H. A. (1993). *Protocol analysis: Verbal reports as data* (rev. ed.). MIT Press. Google Scholar: ~32,000 citations. Used to justify the walkthrough structure where the evaluator articulates the persona's reasoning at each step.

Gould, J. D., & Lewis, C. (1985). Designing for usability: Key principles and what designers think. *Communications of the ACM*, 28(3), 300–311. Google Scholar: ~5,100 citations. Foundational "early focus on users" doctrine that persona-based audits operationalise.

Haack, S. (1993). *Evidence and inquiry: Towards reconstruction in epistemology*. Blackwell. Google Scholar: ~2,900 citations. Referenced because KA's epistemic architecture borrows from foundherentism; relevant to the copy-language cross-persona finding.

Krug, S. (2014). *Don't make me think, revisited: A common sense approach to web usability* (3rd ed.). New Riders. Google Scholar: ~9,200 citations. Source of the "self-evident" test applied to the `ka_home.html` role router and the topic-variant strip.

Mayer, R. E. (2009). *Multimedia learning* (2nd ed.). Cambridge University Press. Google Scholar: ~15,000 citations. Grounds the signaling / coherence principles used to criticise the T1 framework pages' layered disclosure.

Nielsen, J. (1994). Heuristic evaluation. In J. Nielsen & R. L. Mack (Eds.), *Usability inspection methods* (pp. 25–62). John Wiley & Sons. Google Scholar: ~12,000 citations. Primary audit rubric.

Nielsen, J., & Loranger, H. (2006). *Prioritizing web usability*. New Riders. Google Scholar: ~2,400 citations. Source of the "information-scent" framing applied to the navbar regime-boundary critique.

Norman, D. A. (2013). *The design of everyday things* (revised and expanded ed.). Basic Books. Google Scholar: ~43,000 citations. Foundational source for the "signifiers, feedback, affordances" vocabulary used throughout the severity-3 findings.

Pinker, S. (2014). *The sense of style: The thinking person's guide to writing in the 21st century*. Viking. Google Scholar: ~1,900 citations. Ground for the "curse of knowledge" critique that structures the public-visitor comprehensibility scoring.

Rosson, M. B., & Carroll, J. M. (2002). *Usability engineering: Scenario-based development of human-computer interaction*. Morgan Kaufmann. Google Scholar: ~3,400 citations. Source of the scenario-based walkthrough structure per the T4.b rubric.

Sagan, C. (1996). *The demon-haunted world: Science as a candle in the dark*. Random House. Google Scholar: ~6,800 citations. Basis for the honest-uncertainty norm applied to the framework draft-banner critique.

Tognazzini, B. (2014). *First Principles of Interaction Design (revised & expanded)*. AskTog.com. Google Scholar: ~900 citations. Ground for the "anticipation" principle used in the returning-user scoring of `ka_home.html`.

Tufte, E. R. (1983). *The visual display of quantitative information*. Graphics Press. Google Scholar: ~20,000 citations. Source of the data-ink principle applied to the topic-variant row critique.

Yong, E. (2016). *I contain multitudes: The microbes within us and a grander view of life*. Ecco. Google Scholar: ~300 citations. Referenced for plain-language science-writing standards in the public-visitor recommendations.

---

*End of report.*
