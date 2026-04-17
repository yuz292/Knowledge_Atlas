# K-ATLAS site defects — fix plan and prevention strategy

**Date**: 2026-04-16
**Author**: CW (on behalf of DK)
**Source**: `__fixing the website.docx` (uploaded 2026-04-16)
**Status**: Plan — awaiting approval to execute Phase 2 onward

---

## 1. Defects observed (from the uploaded document)

| # | Page | Defect class |
|---|------|--------------|
| 1 | `160sp/collect-articles-upload.html` | Wrong nav regime; personalization without login |
| 2 | `ka_topics.html`                     | Old nav; no login/register/user-type in right slot |
| 3 | `ka_evidence.html`                   | Broken banner and navigation |
| 4 | `ka_gaps.html`                       | Broken banner and navigation |
| 5 | `ka_articles.html`                   | Old nav; no right-hand controls; "insanely complex" |
| 6 | `ka_contribute.html`                 | Stale nav, stale data |
| 7 | `ka_forgot_password.html`            | Backend — email send doesn't work |
| 8 | (several other public pages)         | "Stale nav, stale data, too complex" |

---

## 2. Root-cause diagnosis — six defect classes

1. **Inline-navbar drift.** Pages carry hand-written `<nav>` blocks that were
   copies of the canonical nav at the time and have silently drifted since.
   This is the anti-pattern called out explicitly in `KA_STYLE_GUIDE.md §5a`
   ("Do not build custom inline navbars").
2. **Wrong nav regime.** Class (`160sp`) nav appearing on general pages, or
   global nav on class pages. The regime detection rule is implicit in
   path-prefix, not declared per page.
3. **Missing right-hand controls.** Public, non-class pages lack the
   login / register / user-type picker in the right-hand slot.
4. **Personalisation without auth.** Pages render user-specific content
   without first checking the session state.
5. **Broken backend actions.** UI elements (forgot-password form) exist but
   their server-side wire is missing or misconfigured.
6. **Stale data and over-complex layout.** Cards carry numbers that were
   correct months ago; page hierarchy has accreted without simplification.

---

## 3. Why the agents missed this (the honest answer)

Three mutually reinforcing failures:

**(a) Source-only review.** Both the website-design agent and the usability
agent reviewed source code or prose descriptions, not rendered pages. Source
can contain a nav tag and still render the wrong thing — because the inline
markup is stale, because the page moved regimes without the nav being
updated, or because the right-hand slot is conditionally rendered and the
conditional is broken. A reviewer who never loads the page in a browser
cannot see any of these.

**(b) No canonical contract to check against.** KA_STYLE_GUIDE names the
canonical pattern but does not *enforce* it. A rigorous source review would
still have nothing to diff against.

**(c) No differential / visual regression test.** Without baseline
screenshots, every one of these defects is a silent regression —
indistinguishable from "working" until a human loads the page and looks.

**The user's closing question answers itself.** *Yes*, taking an image of
each page and using it to determine what is wrong is exactly the right
mechanism. It is the core of the prevention strategy below.

---

## 4. Fix plan — four phases

### Phase 1 — Immediate (today)

| Action | Owner | Status |
|--------|-------|--------|
| Add Tanishq Rathore (`trathore@ucsd.edu`) as admin, role = instructor | CW | **Done** (in `ka_admin.html` ADMINS list) |
| Save this plan doc to the workspace | CW | **Done** |
| Request mount of site-root (parent of `160sp/`) so fixes can proceed | DK | Pending |
| Clarify: "add the class csv" — which CSV, to where, for what purpose? | DK | Pending |

### Phase 2 — Batch-fix the named defects

For each of the seven named pages, apply the same patch:

1. Remove the inline `<nav>...</nav>` block.
2. Add `<script src="ka_canonical_navbar.js" defer></script>` to `<head>`.
3. Add `<body data-ka-regime="global">` (or `"160sp"` where appropriate).
4. Add `<div id="ka-navbar-slot"></div>` and `<div id="ka-breadcrumb-slot"></div>`
   where the navbar should render.
5. Verify in a screenshot that the right-hand slot shows
   login / register / user-type picker for a logged-out visitor on global pages.
6. For `ka_articles.html`: scope a simplification pass (separate design review
   with the usability agent, screenshot-based).
7. For `ka_forgot_password.html`: the form renders fine — the defect is
   server-side. Wire the SMTP endpoint; add a one-off integration test that
   submits the form and asserts an email was sent.
8. For `collect-articles-upload.html`: add the auth check *before*
   rendering any personalised block. Unauthenticated visitors see a prompt
   to sign in, not a populated view.

### Phase 3 — Site-wide crawl and fix

Build `scripts/site_validator.py` that walks every `.html` file in the site
root and `160sp/` and reports:

- Presence of inline `<nav>` outside the canonical slot
- Missing `ka_canonical_navbar.js`
- Missing `data-ka-regime` on `<body>`
- Regime mismatch between declared value and URL path
- Missing right-hand nav slot for non-`160sp` pages
- Broken internal links (href to nonexistent file)
- Missing referenced images (src to nonexistent file)
- Orphan pages (not linked from any nav or index)
- Stale `data-ka-last-verified` (older than N days)

Output a Markdown defect report. Fix everything it flags, in one sweep.

### Phase 4 — Prevention systems (install once, prevent permanently)

Seven layers, detailed in §5 below.

---

## 5. Prevention strategy — seven layers

### 5.1 Single-source navbar
Every page includes `ka_canonical_navbar.js`. Nobody ships inline navs.
The linter in §5.3 rejects pages that carry an inline `<nav>` outside the
canonical slot. The canonical script detects regime from
`<body data-ka-regime>` and auth state from the session, then renders the
correct nav.

### 5.2 Page-contract metadata
Every page declares its contract in the `<body>` tag:

```html
<body
  data-ka-regime="global"                           <!-- or "160sp" -->
  data-ka-user-types="visitor,researcher,practitioner,contributor"
  data-ka-last-verified="2026-04-16"
  data-ka-owner="dkirsh">
```

The validator enforces:
- Regime matches the URL path (`/ka/foo.html` → `global`; `/ka/160sp/*` → `160sp`).
- User-types listed are a subset of the canonical set.
- Last-verified date is within threshold (default 90 days for static content,
  14 days for stats / data cards).

### 5.3 Pre-deploy validator as a CI gate
`scripts/site_validator.py` runs on every commit. Any failure blocks the
deploy. Rules listed in Phase 3 above.

### 5.4 Visual regression testing
Headless Chromium loads each page at three viewports (1440×900, 768×1024,
390×844) in three auth states (logged-out, logged-in as 160 Student,
impersonating as admin). Each rendered page is screenshotted and diffed
against a baseline committed to the repo.

Recommended tool: **BackstopJS** (open-source, configured via a single
`backstop.json`, produces HTML diff reports, plays well with CI). Playwright
or Puppeteer can do this directly if we prefer to own less surface area.

Any diff > 0.1% requires human approval before the new baseline is accepted.

### 5.5 Agent prompt rewrite
Both the website-design agent and the usability agent receive **screenshots
as primary evidence**, not source diffs. Their checklist, enforced by the
prompt:

- Does the rendered navbar match the canonical for this page's regime?
- Does the right-hand slot show the correct controls for the declared
  regime and auth state?
- Is any data card labelled with a `data-verified` date older than N days?
- Is the page's user-type declaration consistent with what the rendered
  content assumes the viewer to be?
- Run through one impersonation pass per declared user-type and confirm no
  dead ends or access errors.

Reject any PR where the agent cannot quote the exact screenshot it based its
approval on.

### 5.6 Canonical nav contract doc
A one-page authoritative reference, `docs/KA_NAV_CONTRACT.md`, that names:

- The two regimes (Global K-ATLAS, COGS 160 Spring) and their visual identity.
- The slots in the navbar: brand · left items · right items · user-type picker.
- The rules for each auth state (logged-out, logged-in student, admin,
  admin-impersonating).
- The regime detection rule (URL path prefix plus `data-ka-regime` override).
- The list of legitimate right-hand controls: **login / register / user-type
  picker / account menu**, and which appear in which state.

Every agent reads this before touching any page.

### 5.7 Staleness markers on data cards
Each card or panel that shows numbers, stats, or time-sensitive content
carries `data-verified="YYYY-MM-DD"`. The admin Site-Health tab surfaces the
N oldest; the validator flags anything beyond the per-card-type threshold.

---

## 6. The inventory / sitemap task you asked for

You asked for an HTML inventory, a sitemap, a list of orphans, and the top
5 usability problems. I can produce all of this, but I need to read the
site-root HTML files (the parent of `160sp/`), which I don't currently have
mounted. I have `160sp/` but not `ka_home.html`, `ka_topics.html`,
`ka_evidence.html`, `ka_gaps.html`, `ka_articles.html`, `ka_contribute.html`,
or `ka_forgot_password.html`.

**To proceed**: select the parent folder (the `ka/` site root) using
the file-picker, and I'll run the full inventory in the next pass.

---

## 7. Open questions for DK

1. **"Add the class csv"** — did you mean:
   (a) the CSV *upload feature* (already in `ka_admin.html` as "Upload roster CSV")
   (b) actually load a specific roster you have on hand — please attach it
   (c) add a *template* CSV as a download link so students/admins can see the format
2. **Simplifying `ka_articles.html`** — do you want this scoped as a
   separate design review (with before/after wireframes), or should I just
   propose a cut and show you the result?
3. **BackstopJS vs Playwright** for visual regression — do you have a
   preference, or shall I pick? (I lean BackstopJS for lower operational
   cost on a static site.)
4. **Email send for `ka_forgot_password.html`** — is there an SMTP endpoint
   I should wire against, or do I design the stub assuming a future backend?

---

## 8. References

Fowler, M. (2006). *Continuous integration*. https://martinfowler.com/articles/continuousIntegration.html. Google Scholar citations ≈ 2,100.

Humble, J., & Farley, D. (2010). *Continuous delivery: Reliable software releases through build, test, and deployment automation*. Addison-Wesley. Google Scholar citations ≈ 4,600.

Nielsen, J. (1994). *Usability engineering*. Morgan Kaufmann. Google Scholar citations ≈ 27,000.

Nielsen, J., & Molich, R. (1990). Heuristic evaluation of user interfaces. In *Proceedings of CHI '90* (pp. 249–256). ACM. https://doi.org/10.1145/97243.97281. Google Scholar citations ≈ 8,000. *(The foundational argument for evaluating the rendered interface, not the source.)*

Rosenzweig, E. (2015). *Successful user experience: Strategies and roadmaps*. Morgan Kaufmann. Google Scholar citations ≈ 70.

Shneiderman, B., Plaisant, C., Cohen, M., Jacobs, S., Elmqvist, N., & Diakopoulos, N. (2016). *Designing the user interface* (6th ed.). Pearson. Google Scholar citations ≈ 23,000.
