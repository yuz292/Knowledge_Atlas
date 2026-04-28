# Knowledge Atlas Ruthless Site Audit

Date: 2026-04-27
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Scope: navbar consistency on non-160sp pages, link integrity across the static tree (excluding `ka_live_snapshot/`, `Older Repos etc/`, `Patches_etc/`, `node_modules/`, `.git/`), and backend hookup (front-end → server) coverage

## What "ruthless" means here

Ruthless is not hostile. It means:
- separate structural failures (the navbar is missing on a real user-facing page) from cosmetic ones (an invalid `data-ka-regime` value that the JS still falls back from correctly)
- count the failures that compound (one stale skip-link in a partial that ships into 5 pages = 1 fix, not 5)
- judge the system as a system: a navbar shim that auto-hides legacy `<body><nav>` chrome is doing real work, but a page that has no `<body>` at all defeats the shim
- give the punch list in priority order so the next worker can cut the highest-leverage failure first

## Current site inventory

| Surface | HTML pages | Has canonical navbar? |
|---|---|---|
| Root (`*.html`) | 107 | 105 / 107 (98%) |
| `160sp/` (course regime) | 245 | (out of scope per brief) |
| `Designing_Experiments/` | 51 | (legacy, out of scope) |
| `ka_live_snapshot/` | (frozen mirror) | (skipped) |

Front-end → server map: 36 unique `/api/*` or `/auth/*` endpoints called from the front-end, 34 of them implemented in this repo across 5 server processes.

## Highest-level finding

**The site has converged on the canonical navbar to a degree the prior audit did not see.** 105 of 107 root pages now include `ka_canonical_navbar.js`, 104 declare a valid `data-ka-regime`, and the script's `retireLegacyTopNavs()` shim is doing the visible work of suppressing the older inline `<body><nav>` blocks so the chrome appears identical across pages it has never been hand-edited into. This is a quietly large architectural win since the March 24 audit, which still treated the system as "a federation of strong-but-disconnected pages."

The system is now blocked instead by a small number of high-impact regressions: one root page (`ka_tagger.html`) is a structural HTML fragment with no `<head>` or `<body>` and therefore renders without any chrome at all; one (`ka_search.html`) was forgotten by the migration and still uses its own non-canonical top-nav; an entire subtree (`160sp/track4/*.html`) was authored at one directory depth and committed at a deeper one, breaking ~55 navbar/footer hrefs per page; and the headline "Grader" pill in the canonical navbar dispatches admins to a tab that fails ungracefully when the optional autograder server is not running.

The data layer is in much better shape than the front-end debugging would suggest: 34 of 36 referenced endpoints are implemented in `ka_auth_server.py` (port 8765), `scripts/ka_class_api.py` (port 8080), `scripts/ka_admin_refresh_endpoint.py`, and `160sp/grader_page/server.py` (port 5050). The rest are documentation strings inside `ka_demo_wiring.js`'s "Coming Soon" modal payloads, which is intentional and not a bug.

## Strongest current assets

1. The canonical navbar has actually landed. 105/107 root pages include it; the JS's auto-detection of regime, auto-injection of styles and skip-link, and auto-suppression of legacy `<body><nav>` siblings means new pages get correct chrome by adding one `<script>` tag.
2. The endpoint surface is mostly real, not stubbed. Most of what looked from the front-end like "stub admin endpoints" or "fictional auth" turned out to live in `ka_auth_server.py` plus its included routers (`ka_article_endpoints.py`, `ka_critique_endpoints.py`). The "stub" mental model from previous reviews is out of date.
3. Static asset references (`<script src>`, `<link href>` on local CSS/JS) all resolve in the root, `160sp/`, and `Designing_Experiments/` directories — no missing JS files, no broken stylesheet references in the audited tree.
4. The `ka_archive.html` regime-tag deviation is contained: an invalid `data-ka-regime="archive"` value falls through the JS guard and the URL-based inference correctly classifies it as `global`. The wrong value never reaches user-visible chrome.

## Audit 1 — Global-navbar consistency on non-160sp pages

**Sample**: 107 root `*.html` files. Inputs: `<script src="ka_canonical_navbar.js" defer></script>`, wordmark target (should be `ka_home.html`), `data-ka-regime` declaration.

### BLOCKER

**1. `ka_tagger.html` is an HTML fragment, not a page.** The file (440 lines) begins on line 1 with `<a href="ka_tagger.html" class="sidebar-nav-item active">Tag Images</a>` and has no `<!DOCTYPE>`, `<html>`, `<head>`, or opening `<body>` — only the closing `</body></html>` on lines 439–440. As a result it cannot render the canonical navbar (no `<body>` to mount into), it cannot be read by browsers as standards-mode HTML, and the entire page that the previous audit called out as "a real page that needs to be brought into the main mental model" is currently shipping as a partial that browsers interpret in quirks mode. This is the worst defect in the whole site.

**2. `ka_search.html` was missed by the navbar migration.** It is a structurally complete page but uses its own non-canonical `<nav class="top-nav">` (lines 174–186) and does not include `ka_canonical_navbar.js`. Wordmark target `ka_home.html` is correct, but the nav-center links are a hand-written legacy list (`Explore | Evidence | Gaps | Articles | Contribute | Search | Site map`) that diverges from the canonical regime items (`Articles | Topics | Theories | Mechanisms | Neural Underpinnings | Contribute | About`). Every other root page in this regime has been updated; this one was not. It is also the page the canonical navbar's `⌕ Search` link sends users to, so the discontinuity is high-visibility.

### SHOULD-FIX

**3. `ka_archive.html` declares an invalid regime.** `<body data-ka-regime="archive">` is not a value the JS knows; it falls back to URL inference (root → `global`), so the chrome does render correctly, but the explicit value misleads any future maintainer reading the page. Either remove the attribute or change to `data-ka-regime="global"`.

**4. Root login/register inline navs target the wrong home.** `ka_login.html` line 365 has `<a href="160sp/ka_schedule.html" class="nav-brand">` and `ka_register.html` line 571 has `<a href="ka_home.html" class="nav-brand">`. The canonical navbar's `retireLegacyTopNavs()` correctly identifies these as legacy `<body><nav>` siblings and hides them at runtime, so the user-visible chrome is fine. But `ka_login.html`'s legacy wordmark pointing into `160sp/ka_schedule.html` (a course-internal page) is the only remaining trace of the pre-March re-skinning where login was a course-only feature, and it should be deleted to prevent it from ever resurfacing if the JS hide-shim is bypassed.

**5. `ka_demo.html` legacy wordmark href is `"#"`** (line 332). Same hide-shim story as #4 — the user never sees it — but the dead link should be cleaned.

### MINOR

**6. Six pages have leftover `<a class="wordmark">` elements** (`ka_demo.html`, `ka_demo_v04.html`, `ka_instructor_review.html`, `ka_search.html`, `ka_user_home.html`, plus `fall160_schedule.html`'s `<nav class="top-nav" style="display:none">`). All except `ka_search.html` are statically hidden either by `display:none` or by the runtime shim. They are dead code; sweep when convenient.

**7. The 160sp/journey-page exemption is correctly noted in the JS comment** (line 357 of `ka_canonical_navbar.js`). Confirmed against `160sp/t1_intro.html`: it uses an inline `<nav class="top-nav">` from `_track_pages_shared.css` and links the wordmark to `../ka_home.html`. That is the documented exception. Listing it here only so it does not get lumped with the genuine deviations above.

## Audit 2 — Link integrity

**Crawl**: 265 HTML files (root + `160sp/` + `Designing_Experiments/`), 4,029 internal links (after filtering out 45 JS-template-literal pseudo-hrefs like `${h}`, `' + esc(item.image_url) + '`). 75 broken internal links found, concentrated in 3 files.

### BLOCKER

**8. `160sp/track4/*.html` was authored one directory shallower than committed.** Three files — `journey_q29_art_affect_confound.html`, `answer_shape_catalogue.html`, `chinn_brewer_response_widget.html` — each carry 18–19 broken hrefs in their inline top-nav, breadcrumb, and footer. Every link is the same family of mistake: from `160sp/track4/foo.html` they reference `../ka_home.html` (resolves to `160sp/ka_home.html`, missing) when they should reference `../../ka_home.html`; and they reference `../160sp/ka_schedule.html` (resolves to `160sp/160sp/ka_schedule.html`, missing) when they should reference `../ka_schedule.html`. This is one mechanical fix per file (sed across 8 distinct hrefs), but until it ships, every navbar item, every breadcrumb crumb, and every footer link on these three pages 404s. Cumulative count: 55 of 75 broken links in the entire site come from these three pages alone.

### SHOULD-FIX

**9. Five `160sp/ka_track*_hub.html` pages have a stale inline skip-link to `#main`** (line 13 of each), but their main element is `<main id="ka-main">`. The canonical navbar injects its own working skip-link to `#ka-main` ahead of the inline one, so the bug only fires for the rare case of a screen-reader user activating the second (inline) skip link. Fix is one global sed: `href="#main"` → `href="#ka-main"` in those five files. Affected: `ka_track1_hub.html`, `ka_track3_resources.html`, `ka_track3_team_hub.html`, `ka_track4_hub.html`, `ka_track4_persona_panel.html`.

**10. `Designing_Experiments/{hypothesis_builder,experiment_wizard}.html` link to anchors that no longer exist on `theory_and_experiment_design.html`.** Five broken anchor links across two pages: `#theories`, `#taxonomy`, `#critical`. The target page now uses `#tab-theories`, `#panel-theories`, `#tab-taxonomy`, `#tab-critical`. Either rename the target anchors back to the simpler form or update the source links. Low traffic on the legacy DE pages but visible to anyone clicking from the wizard into theory documentation.

### MINOR

**11. `160sp/article_finder_assignment_v1_archive.html`** has 5 broken hrefs in a `<nav class="header-nav" style="display:none">` block (lines 226–229 and 481): `student-assignment.html`, `teach-google-search.html`, `image-tagger-assignment.html`, `login.html`. The nav is hidden by inline style and the file name carries `_archive`, so this is dead code in a deliberately-archived page. No action required unless someone removes the `display:none`.

**12. `Designing_Experiments/docs/student_tracks/vr_wk{04,05}_production*.html`** carry 5 broken `#resources` self-anchors. Self-references inside legacy course material; cosmetic.

## Audit 3 — Backend hookup

**Sweep**: 36 unique endpoint references in front-end HTML + JS, against the 5 server processes documented in this repo.

### Server inventory (current)

| Server | Port | Endpoints | Run command |
|---|---|---|---|
| `ka_auth_server.py` | 8765 | `/auth/*`, `/api/articles/*`, `/api/student/*`, `/api/critique/*`, `/api/assignments`, `/api/questions` | `uvicorn ka_auth_server:app --port 8765` |
| `scripts/ka_class_api.py` | 8080 | `/api/admin/class/*` (8 endpoints, X-Admin-Token gated) | `uvicorn scripts.ka_class_api:app --port 8080` |
| `scripts/ka_admin_refresh_endpoint.py` | 8781 | `/api/admin/refresh-pnus`, `/api/admin/refresh-pnus/health` | (FastAPI, separate) |
| `160sp/grader_page/server.py` | 5050 | `/api/grade`, `/api/roster`, `/api/review`, `/api/results/<id>`, `/api/task-info/<track>/<task>`, `/api/export/grades` | `python3 160sp/grader_page/server.py` |
| `scripts/ka_sso_stub.py` | (stub) | `/auth/sso/callback`, `/auth/signout`, `/api/admin/whoami` | Stub only |

### Coverage

| Status | Count | Notes |
|---|---|---|
| IMPLEMENTED | 34 | All `/auth/*`, `/api/articles/*`, `/api/student/*`, `/api/critique/*`, `/api/assignments`, `/api/admin/refresh-pnus`, `/api/grade`, `/api/roster`, `/api/review` |
| STUB | 2 | `/api/admin/class` (referenced as base only in `ka_admin.html` shim — sub-paths are implemented in `ka_class_api.py`); `/api/tag-browser` (Designing_Experiments demo route, no Python backing here) |
| DOC-ONLY | 16 | `/api/v1/*` references inside `ka_demo_wiring.js`'s "Coming Soon" modal `data-cs-source` strings — these are documentation labels, never fetched |

The "many endpoints are stubs" suspicion the brief raised against `ka_admin.html` is largely false: every `kaApiGet('/grading')`, `kaApiGet('/calibration')`, etc. resolves to `/api/admin/class/grading`, `/api/admin/class/calibration` etc. once the `KA_CLASS_API_BASE` prefix is applied, and all 8 of those are implemented in `scripts/ka_class_api.py`. The shim's silent fallback to `DEMO_*` constants when the server is unreachable is by design (per the comment at `ka_admin.html:1295`).

### BLOCKER

**13. The Grader pill in the canonical navbar fails ungracefully.** `ka_canonical_navbar.js:424` renders `<a class="ka-pill ka-pill-admin" href="http://localhost:5050/" target="_blank" rel="noopener" title="...">🎓 Grader</a>` for every admin session. When the optional autograder server is not running (which is the default — the instructor must launch it manually), clicking the pill opens a new browser tab that immediately shows the browser's "could not connect" error page. There is no client-side preflight check, no fallback message in the original tab, no styling to indicate "server may not be available." The `title` attribute warns "instructor must run server.py first" but only on hover. This is the highest-visibility surface in the canonical navbar (it is the only orange admin pill alongside the Admin link itself), and its primary failure mode is a confusing browser error.

### SHOULD-FIX

**14. `KA_API`/`KA_AUTH_API` resolve to empty string when `__KA_CONFIG__` is unset.** Every call site uses the pattern `const KA_API = window.__KA_CONFIG__?.apiBase ?? '';`. When the static site is served without `ka_config.js` having been loaded (or when `__KA_CONFIG__.apiBase` is undefined), the base resolves to `''` and `fetch('/auth/login')` issues a same-origin POST. On a static-file server (Python `http.server`, `live-server`, GitHub Pages, etc.) this returns 405 or 404 with no useful diagnostic. Either bake a sensible default like `'http://localhost:8765'` for dev mode, or surface an in-page banner when the auth/api server is unreachable.

**15. `/api/tag-browser` referenced from `Designing_Experiments/docs/student_tracks/image_tag_visualizer.html`** has no Python backing in this repo — it is documentation showing a Flask route the student is asked to build. Acceptable for a course exercise, but easy to mistake for a missing endpoint. Add a comment in the calling code clarifying intent.

### MINOR

**16. `scripts/ka_sso_stub.py`** is documented as "stub" in its own filename. Nothing in the front-end currently calls `/auth/sso/callback` or `/api/admin/whoami`, so it is currently dead code inside the repo. Keep, but mark as not-in-use.

## What should not be done

1. Do not "fix" the `track4/` pages by editing each broken href manually. The pattern is `../ka_home.html` → `../../ka_home.html` and `../160sp/X.html` → `../X.html`; one sed pass per file.
2. Do not delete `ka_search.html`'s legacy `top-nav` until the canonical script has been added; otherwise the page renders chrome-less for the gap.
3. Do not rebuild `ka_tagger.html` from scratch. Its body content is intact — it is missing only the wrapping shell. Patch the shell back in (`<!DOCTYPE>`, `<html>`, `<head>` with title and meta, `<body data-ka-regime="global" data-ka-active="contribute">`) and the canonical navbar will mount as it does on every other page.
4. Do not assume the demo `/api/v1/*` strings in `ka_demo_wiring.js` are real endpoint references the next time someone audits. They are intentional documentation in "Coming Soon" modals.

## Triaged top-10 punch list

| # | Severity | Action | Where |
|---|---|---|---|
| 1 | BLOCKER | Repair `ka_tagger.html`: prepend `<!DOCTYPE html><html lang="en"><head><meta>...<title>...<script src="ka_canonical_navbar.js" defer></script></head><body data-ka-regime="global" data-ka-active="contribute">` | `/Users/davidusa/REPOS/Knowledge_Atlas/ka_tagger.html` |
| 2 | BLOCKER | Add canonical navbar to `ka_search.html`; remove its inline `<nav class="top-nav">`; declare `<body data-ka-regime="global" data-ka-active="search">` | `/Users/davidusa/REPOS/Knowledge_Atlas/ka_search.html` lines 1, 174–186 |
| 3 | BLOCKER | Sed-fix the `track4/` subtree's relative paths (`../` → `../../` for root targets; `../160sp/` → `../`) | `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/track4/{journey_q29_art_affect_confound,answer_shape_catalogue,chinn_brewer_response_widget}.html` (~55 hrefs total) |
| 4 | BLOCKER | Make the Grader pill graceful: either (a) ping `http://localhost:5050/health` on hover and grey out if unreachable, or (b) route through an interstitial admin page that shows server status before opening | `/Users/davidusa/REPOS/Knowledge_Atlas/ka_canonical_navbar.js` lines 421–426 |
| 5 | SHOULD-FIX | Replace `href="#main"` with `href="#ka-main"` in 5 track-hub pages | `/Users/davidusa/REPOS/Knowledge_Atlas/160sp/{ka_track1_hub,ka_track3_resources,ka_track3_team_hub,ka_track4_hub,ka_track4_persona_panel}.html` line 13 (mostly) |
| 6 | SHOULD-FIX | Provide a sensible default for `__KA_CONFIG__.apiBase` (e.g. `'http://localhost:8765'`) or show an in-page warning when fetches return 4xx/5xx | `/Users/davidusa/REPOS/Knowledge_Atlas/ka_config.js` (or define one) |
| 7 | SHOULD-FIX | Update `ka_archive.html`'s `data-ka-regime="archive"` to `"global"` | `/Users/davidusa/REPOS/Knowledge_Atlas/ka_archive.html` line 74 |
| 8 | SHOULD-FIX | Reconcile the 5 broken `#theories`, `#taxonomy`, `#critical` anchors in `Designing_Experiments/{hypothesis_builder,experiment_wizard}.html` against the new `#tab-*` / `#panel-*` IDs | `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/{hypothesis_builder.html:797, experiment_wizard.html:1838-1962}` |
| 9 | SHOULD-FIX | Delete the legacy `<nav class="nav-brand">` blocks in `ka_login.html` (line 363) and `ka_register.html` (line 569). The runtime shim hides them but they are zombie chrome that will resurface if the shim is ever bypassed | `/Users/davidusa/REPOS/Knowledge_Atlas/ka_login.html`, `/Users/davidusa/REPOS/Knowledge_Atlas/ka_register.html` |
| 10 | MINOR | Sweep dead `<a class="wordmark">` blocks from `ka_demo.html`, `ka_demo_v04.html`, `ka_instructor_review.html`, `ka_user_home.html`, `fall160_schedule.html` | (root pages above) |

## Closing observation

The site has crossed an important threshold. With the canonical navbar landing across 98% of root pages and 34 of 36 endpoint references actually backed by Python code, the current failure mode is no longer "pages drift from each other" (the March 24 finding) but "a small set of edge cases — one structurally broken page, one forgotten migration, one mis-located subtree, and one ungraceful header pill — disproportionately damage the perceived quality." Items 1–4 above, fixed in one sitting, would shift the user's impression of the site from "mostly works but with weird chrome gaps" to "fully unified." Items 5–10 are clean-up that buys insurance against future regressions but does not change today's UX.
