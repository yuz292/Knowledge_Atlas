# K-ATLAS site — text-level defect catalogue
**Date**: 2026-04-16
**Source**: HTML fetched from `xrlab.ucsd.edu/ka/*` (production)
**Author**: CW for DK
**Companion**: `SITE_DEFECTS_PLAN_2026-04-16.md`

---

## 0. Headline finding (not in the original plan)

The production site is running **three incompatible navbar systems
simultaneously**, and no single one of them is complete. Every defect
on your list is downstream of this.

| System | Name | Used by | Has mode switching? | Has login / register? |
|--------|------|---------|:-:|:-:|
| **A** | `ka_canonical_navbar.js` | `160sp/ka_track1_hub.html`, a handful of track hubs | via body attrs | No (student profile only) |
| **B** | `ka_shell.js` → `window.KA_SHELL.initShell()` | `ka_topics.html`, `ka_evidence.html`, `ka_gaps.html`, `ka_articles.html`, `ka_contribute.html` | **Yes** (mode-pill + mode-select) | **No** |
| **C** | Bespoke inline `<nav>` | `ka_home.html`, `ka_forgot_password.html`, `160sp/collect-articles-upload.html` | Varies (tabs on home) | **Yes on ka_home only** |

`KA_STYLE_GUIDE.md §5a` names System A as canonical. The most important
pages on the site do not use it. The most featureful system (B) has no
login/register controls. The only nav with login/register (C) is
hand-rolled per-page and drifts. **There is, today, no single navbar
implementation that satisfies the union of required features.**

---

## 1. Per-page findings

### 1.1 `ka_topics.html`

- **Nav system**: B (`KA_SHELL.initShell`, target `.nav-left ul`)
- **Nav items**: Explore · Topic Map · Evidence · Gaps · Articles · Contribute
- **Right slot**: mode-pill + mode-select (`id="topics-mode-select"`)
- **No login/register controls**
- **No `data-ka-regime` / `data-ka-active` / `data-ka-crumbs`** on `<body>`
- **No reference** to `ka_canonical_navbar.js` or `ka_user_type.js`
- No `data-verified` timestamps on any card

### 1.2 `ka_evidence.html`

- **Nav system**: B (`ka_shell.initShell()`), plus the `<nav>` items are also hardcoded inline — **both** are present
- **Nav items**: Knowledge Atlas (brand) · Explore · Topic Map · Evidence · Gaps · Articles · Contribute
- **Right slot**: "RESEARCHER" mode pill + `#evidence-mode-select`
- **No login/register**
- **No `data-ka-*`** attributes
- Conditional content (`evidence-intro-researcher`, `evidence-intro-student`) referenced but **markup missing from payload** — explains the user's "broken banner" complaint
- Fallback dataset hardcoded with years 1997–2019 (static)

### 1.3 `ka_gaps.html`

- **Nav system**: B (`KA_SHELL.initShell`, target `.nav-links`, mode `researcher`)
- **Nav items**: same Explore/Topic Map/Evidence/Gaps/Articles/Contribute
- **Right slot**: mode pill (green `#4A8C6E`) + mode-select
- **No login/register**
- **"Back to My ATLAS"** footer link to `ka_user_home.html` with no session check
- **Broken fallback**: no error boundary for missing `ka_gaps.json` payload

### 1.4 `ka_articles.html`

- **Nav system**: B (`KA_SHELL.initShell`, target `.nav-center`)
- **Nav items**: Explore · Evidence · Gaps · Articles · Contribute · **Course** (→ `160sp/ka_student_setup.html`) &nbsp; *(different from 1.1–1.3: "Topic Map" missing; "Course" added)*
- **Right slot**: mode-select (`Contributor`) + mode-pill + **user avatar** (initials)
- **No login/register**
- **Eight major widgets** on the page (sidebar progress, search+filters, results, reference panel, relevance rating, quality assessment, evidence classification, submission) — confirms the "insanely complicated" complaint
- No reference to `ka_canonical_navbar.js`

### 1.5 `ka_contribute.html`

- **Nav system**: B (`KA_SHELL.initShell`, target `.nav-links`)
- **Nav items**: Knowledge Atlas · Explore · Topic Map · Evidence · Gaps · Articles · Contribute
- **Right slot**: mode-pill + mode-select
- **No login/register**
- Hero stats (Topics / Articles / Open Gaps) computed from a three-row fallback dataset: Neuroaesthetics, Attention Restoration, Stress Recovery — **the stale/seed data you flagged**
- Token check via `localStorage.getItem('ka_access_token')` — no visible session UI

### 1.6 `ka_forgot_password.html`

- **Nav system**: C (inline `<nav>` with `.wordmark` + `.nav-back` only)
- **Nav items**: wordmark + a single "back" link
- **Form**: email-only, `POST ${API}/auth/forgot-password`
- **Backend**: expects `ka_auth_server.py` on **localhost:8765** — that's a development-only server. The email error message is explicit: *"Could not reach the auth server. Is ka_auth_server.py running on port 8765?"*
- **This is why email doesn't work in production**: there is no production SMTP endpoint; the form is hard-wired to a local dev server that isn't running on `xrlab.ucsd.edu`
- No reference to `ka_canonical_navbar.js` or `ka_user_type.js`

### 1.7 `160sp/collect-articles-upload.html`

- **Nav system**: C (inline `.ka-nav`), styled as the class (160sp) nav
- **Nav items**: wordmark · Explore · Evidence · Gaps · Articles · Contribute · Course · 160 Syllabus
- **Right slot**: user avatar + "Signed in as — [Sign out]"; **login/register not rendered in any branch**
- **Personalization renders before auth completes**: `getUserDisplayName()` and `getUser()` read `localStorage` and paint the hero immediately; the 401 response from `/api/student/assignments` later toggles the login overlay
- Explicit style-guide violation: the comment in the page reads *"Top bar (legacy, hidden — replaced by ka-nav)"*, confirming this file knowingly went its own way

### 1.8 `ka_home.html` (not on your list, but critical context)

- **Nav system**: C (inline static `<nav>`)
- **Nav items**: wordmark · 160 Student · Researcher · Contributor · Practitioner · Theorist · About
- **Right slot**: **`btn-login` + `btn-register-nav` (orange)** — the only production page that actually shows login/register
- **No `data-ka-*` attributes**
- Mode switching via JavaScript that *reorders* nav elements (brittle)

---

## 2. Five root-cause observations

1. **No single canonical navbar.** Three systems. Each was once called
   "canonical" by some author. The style guide names the one almost nobody
   uses.
2. **Login/register exists in exactly one place** (`ka_home.html`) and
   that place isn't shared by any other page. Every other public page has
   no auth affordance.
3. **Mode switching and auth are in different systems.** No navbar offers
   both simultaneously. Users changing mode can't log in; users logging in
   can't change mode on the same chrome.
4. **Data freshness is invisible.** Zero pages carry `data-verified`
   timestamps. "Stale" is an adjective, not a check.
5. **Auth is client-first.** At least two pages render personalised
   content from `localStorage` before the server has validated the token.
   A stale or forged localStorage entry paints a personalised page for
   whomever looks.

---

## 3. Corrected fix plan

The original plan said "adopt the canonical navbar everywhere." Given the
findings above, the fix is bigger and must be sequenced differently.

### Phase 2a — Decide the winner

**Pick System B (`ka_shell.js` / `KA_SHELL.initShell`) as the new
canonical.** Reasons: it is already on five of six global pages; it owns
mode switching (the most complex feature); it is the only one with
per-page configuration. Retain the `ka_shell.js` name or rename to
`ka_canonical_navbar.js` for continuity with the style guide — either
works, but choose once and never rename again.

### Phase 2b — Extend the winner

Add to `ka_shell.js`:
- Right-slot `btn-login` / `btn-register-nav` when `getUser()` returns
  null (lifted from `ka_home.html`).
- Right-slot `account-menu` with `Sign out` and `Switch user type` when
  `getUser()` returns a session.
- `data-ka-regime` detection: if the page path starts with `/160sp/`,
  render the class nav; otherwise global.
- Single source of truth for nav items per regime, declared at the top
  of the file.

### Phase 2c — Migrate

Seven pages need `ka_shell.js` wired in and their inline navs deleted:
`ka_home.html`, `ka_topics.html`, `ka_evidence.html`, `ka_gaps.html`,
`ka_articles.html`, `ka_contribute.html`, `160sp/collect-articles-upload.html`.
(`ka_forgot_password.html` is a different problem — Phase 2d.)

### Phase 2d — Fix forgot-password

The hard-coded `localhost:8765` endpoint is the root cause. Either:
- Stand up the auth server on production (same host as `xrlab.ucsd.edu`,
  reverse-proxied to `/api/auth/*`), or
- Replace the dev call with a call to an institutional SMTP relay
  (UCSD ITS provides this).

### Phase 2e — Gate personalisation

Every page that reads `localStorage` to render a hero must first await
the `/api/me` response. Three-line change per page; mechanical.

### Phase 2f — Staleness markers

Add `data-verified="YYYY-MM-DD"` to every hero stat, data card, and
"seed" panel. Add a `/admin/stale` report that lists everything past
threshold.

---

## 4. What I still need

- **Parent folder mounted** — so I can apply the patches to `ka_home.html`,
  `ka_topics.html`, etc.
- **Chrome extension signed in** — so I can run the visual regression
  pass and produce screenshots for the catalogue above. Today the
  extension is unreachable.
- **Auth-server decision** — reverse-proxy the existing Python server, or
  switch to institutional SMTP. Affects Phase 2d design.
