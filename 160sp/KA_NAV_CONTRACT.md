# K-ATLAS Navigation Contract
**Date**: 2026-04-16
**Status**: Canonical — all agents (CW, AG, Codex) and human contributors must follow this
**Authority**: Supersedes the navbar sections of KA_STYLE_GUIDE.md §5a for actual site behaviour. The style-guide palette (§2–§8) remains canonical.
**Implementation**: `ka_canonical_navbar.js` + `ka_user_type.js`

---

## 1. One canonical. Two regimes. No exceptions.

Every page on the site includes `ka_canonical_navbar.js` and declares its
regime on `<body>`. No inline `<nav>` may exist outside the canonical slot.
The pre-deploy validator rejects any page that violates this rule.

## 2. The two regimes

### 2.1 Global (`data-ka-regime="global"`)

Serves all non-class visitors: researchers, practitioners, contributors, visitors.

Left items, in order:
**Articles · Topics · Theories · Mechanisms · Neural Underpinnings**

Pages currently live: `ka_articles.html`, `ka_topics.html`.
Pages needing stubs (as of 2026-04-16): `ka_theories.html`, `ka_mechanisms.html`,
`ka_neural.html`. Until these ship, the nav renders a small `stub` badge next
to the link so the reader knows the destination is a placeholder.

### 2.2 COGS 160 Spring (`data-ka-regime="160sp"`)

Serves enrolled class students and instructors.

Left items, in order:
**Syllabus · A0 · A1 · Track 1 · Track 2 · Track 3 · Track 4**

Paired with the Student Profile pill on the right for signed-in students.

## 3. Right-slot state machine

The right slot is the one place where auth state and presentation mode meet.
It renders one of four compositions, deterministically, from the session.

| Session state | Right-slot composition |
|---------------|-----------------------|
| **Anonymous** (not signed in)                        | `[User-type picker]` `[Log in]` `[Register →]` |
| **Signed in · public user type** (no class)          | `[User-type picker]` `[Account menu]` |
| **Signed in · 160 Student**                          | `[160 Student pill]` `[Account menu]` |
| **Signed in · Admin** (with or without impersonating) | `[★ Admin badge]` `[User-type picker]` `[Account menu]` |

The **user-type picker** exposes:
- Public (no sign-in required): Visitor, Researcher, Practitioner, Contributor
- Gated: 160 Student, Instructor/Admin

An admin who picks a gated role enters *impersonation mode*; `ka_user_type.js`
draws the amber "Viewing as X — Return to admin — Stop impersonating" banner
across the top of every page until the admin exits.

## 4. Per-page declaration

```html
<body
  data-ka-regime="global"                  <!-- or "160sp" -->
  data-ka-active="topics"                  <!-- matches an item id -->
  data-ka-crumbs='[["Home","ka_home.html"],["Topics",""]]'>
```

- `data-ka-regime` is authoritative; the script falls back to the URL path
  (`/160sp/` → `160sp`, else `global`) if absent.
- `data-ka-active` highlights the current item in the navbar.
- `data-ka-crumbs` is a JSON array of `[label, href]` pairs; the last pair
  has an empty href to mark the current page.

## 5. Slots

```html
<div id="ka-navbar-slot"></div>
<div id="ka-breadcrumb-slot"></div>
<!-- page content -->
<script src="ka_canonical_navbar.js" defer></script>
<script src="ka_user_type.js" defer></script>
```

If either slot is missing the script creates it at the top of `<body>`. This
is a convenience; authors should still declare the slots so HTML review can
see them.

## 6. Cross-regime links

Hrefs in `REGIME_ITEMS` are declared **relative to the regime's root**.
The script prefixes automatically:

- A page in `/ka/` linking to a 160sp item → `160sp/ka_schedule.html`
- A page in `/ka/160sp/` linking to a global item → `../ka_topics.html`

Authors should never hand-prefix nav hrefs.

## 7. The three authoritative session keys

Only these three `sessionStorage` keys drive the navbar. Nothing else should:

| Key | Values | Meaning |
|-----|--------|---------|
| `ka.admin` | `"yes"` / unset | The viewer is signed in as an administrator |
| `ka.160.authed` | `"yes"` / unset | The viewer is signed in as a 160 Student |
| `ka.userType` | one of Visitor / Researcher / Practitioner / Contributor / 160-student / Instructor | Current presentation mode |
| `ka.impersonating` | `"yes"` / unset | Admin is viewing the site as another role |
| `ka.adminEmail`, `ka.studentEmail` | email string | Only for display in the account menu |

In production these are backed by a signed session cookie read server-side;
the client-side keys are convenience mirrors.

## 8. Prohibited patterns

The validator rejects any page that:

- Contains an inline `<nav>` outside `#ka-navbar-slot`
- Omits `ka_canonical_navbar.js` from its `<script>` includes
- Lacks `data-ka-regime` on `<body>`
- Declares a regime that contradicts its URL path (exception: `archive`
  regime, which is legitimately orphan — see §8a)
- Declares `data-ka-active` pointing at an id not in `REGIME_ITEMS[regime]`
- References a nav item via a hand-coded href instead of the regime table
- Reads from `localStorage` or `sessionStorage` to render personalised
  content *before* the server has validated the session

### 8a. The `archive` regime

Pages marked `data-ka-regime="archive"` are exempt from the
orphan-page check because they are *intentionally* unreachable from
public surfaces. An archived page is linked only from two
designated places: the Track 4 hub (for UX-research study of prior
design patterns) and the instructor admin console. The validator
enforces the inverse constraint: any page with
`data-ka-regime="archive"` that is linked from a surface other than
those two is a validation error.

The archive index (`ka_archive.html`) enumerates archived pages with
reason, category tag (`archived` / `folded` / `retired` / `useful`),
and links to the live page and any replacement. Archived pages
themselves keep the canonical navbar but are not listed in any
regime's `REGIME_ITEMS` array. When a page is archived, remove its
entry from `REGIME_ITEMS` and add a row to `ka_archive.html`; when a
page is un-archived, do the inverse.

## 9. Updating the item list

Changes to `REGIME_ITEMS` require:
1. A PR that updates `ka_canonical_navbar.js`
2. A matching update to §2 of this document
3. Visual regression baseline regeneration for every page
4. Sign-off from DK (instructor-of-record)

## 10. The style-guide delta

`KA_STYLE_GUIDE.md §5a` names `ka_canonical_navbar.js` as the shared nav
component but defers the item list to §1a/§1b of the same guide. This
contract upgrades that to a *mandatory* single source of truth. §1a and §1b
of the style guide are the aspirational nav we are now implementing; this
document makes them binding.
