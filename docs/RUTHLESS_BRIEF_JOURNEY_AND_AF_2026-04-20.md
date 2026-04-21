# Ruthless-review fix brief — Journey pages, AF problems, navbar (2026-04-20 PM)

*Date*: 2026-04-20 PM
*Requested by*: DK
*Executors*: Codex and AG, working in parallel on disjoint probes
*Target*: the local working tree of `/Users/davidusa/REPOS/Knowledge_Atlas` at its current tip — every fix below lands before the pending commit
*Expected output*: a status note at `docs/RUTHLESS_FIX_STATUS_2026-04-20_PM.md` plus one commit per probe (attributed to whoever did the work), followed by **CLEAN** so DK can run the local commit, GitHub push, staging pull, and production promote

## Why this exists

Two independent review agents (a code reviewer and a usability-heuristic reviewer in the Nielsen 1994 tradition) walked this afternoon's changes — the fifteen regenerated journey pages, the three new Article Finder problem specs, the left-hand sidebar with twisties, the navbar triangle-glyph + regime-tag removal, the Track 2 hub Region 4.5, and the home-page sub-nav Journeys link. Between them they surfaced **five P0 blockers** (one of which is a dead link on the home page — DK will click it from the nav and see nothing happen; that alone makes today's commit non-shippable) and **eight P1 fixes** that should land before DK commits. The P2s are flagged for a later pass. The fixes are mechanical and self-contained; the reason a ruthless prompt exists rather than CW just landing them is to keep labour divided between Codex and AG and to preserve the audit trail.

## Division of labour

To minimise merge conflict Codex and AG work on disjoint files where possible.

- **Codex** takes HTML / JS / link-integrity fixes: probes P0-1, P0-2, P0-3, P0-4, P0-5, P1-8, P1-9, P1-11, P1-12, and the P2 items.
- **AG** takes CSS + copy fixes: probes P1-6, P1-7, P1-10, P1-13.

Each agent lands its own commits attributed to itself (`--author="Codex <codex@openai.com>"` / `--author="AG <ag@google.com>"`). Each probe is its own commit with subject `fix(journeys): P{level}-{N} — {short subject}`. Body of each commit: a one-paragraph explanation of the bug, the fix, and a link to this brief.

The P2 items are optional. Do them if you have time after the P0s and P1s clear; otherwise skip and note them as deferred in the status file.

---

## P0 blockers (commit is unshippable until all five land)

### P0-1 — Dead "Journeys" link on home page sub-nav

**File**: `ka_home.html` around line 200
**Bug**: the new `<a href="ka_journeys.html" class="sep" ...>◯ Journeys — harder pages</a>` uses class `sep`, but `.subnav a.sep { pointer-events: none; }` at line 68 of the same file disables click handling on anything carrying that class. DK clicks the nav link from the home page → nothing happens.
**Fix**: remove `class="sep"` from the link and replace with a new class `class="branch"` that styles the border-top divider exactly as `.sep` did but without the `pointer-events:none`. Update the `.subnav` CSS to add `.subnav a.branch { border-top:1px dashed #E0D8CC; margin-top:8px; padding-top:10px; }`.
**Verify**: click the link in a real browser; the journeys index opens.
**Owner**: Codex.

### P0-2 — Duplicate `class` attribute on sidebar index anchor

**File**: `ka_journey_surface.js` line 81 (the `parts.push` for the `side-index` anchor).
**Bug**: current code emits `<a class="side-index" href="ka_journeys.html"${currentSlug === "__index__" ? ' class="current"' : ""}>` — two `class` attributes on one element. Browsers keep only the first, so the `.side-index.current` style never applies; the index anchor never highlights on the index page.
**Fix**: interpolate into the single `class` attribute: `<a class="side-index${currentSlug === '__index__' ? ' current' : ''}" href="ka_journeys.html">…`.
**Verify**: open `ka_journeys.html` and confirm the sidebar "↺ Index" row renders with the `.side-index.current` background tint.
**Owner**: Codex.

### P0-3 — Stale "12 surfaces" count in the sidebar label

**File**: `ka_journey_surface.js` around line 80 — the sidebar index anchor text.
**Bug**: label reads `↺ Index · all 12 surfaces` but the journey index now lists fifteen (12 complicated + 3 AF). The discrepancy is immediately visible from the sidebar vs the body of `ka_journeys.html` (which says "all fifteen").
**Fix**: compute the count dynamically — `const total = GROUPS.reduce((n, g) => n + g.slugs.length, 0);` — and emit `↺ Index · all ${total} surfaces`. This prevents the count from going stale as groups grow.
**Verify**: reload any journey page; sidebar says `all 15 surfaces`.
**Owner**: Codex.

### P0-4 — `aria-expanded` mismatch on the index page

**File**: `ka_journey_surface.js` around lines 85-89 in `renderJourneySidebar`.
**Bug**: on the index page, every group is opened visually (because `currentSlug === "__index__"` forces `openCls = " open"`) but the loop still emits `aria-expanded="${gi === activeGroupIdx}"`. On the index page, `activeGroupIdx` is `-1`, so every button announces `aria-expanded="false"` while the group body is visible. Screen readers announce "collapsed" on groups that are plainly open.
**Fix**: compute `const isOpen = gi === activeGroupIdx || currentSlug === "__index__";` once, then use that for both `const openCls = isOpen ? " open" : "";` and `aria-expanded="${isOpen}"`.
**Verify**: open `ka_journeys.html` and inspect the DOM; every `<button class="side-head">` under an open group has `aria-expanded="true"`.
**Owner**: Codex.

### P0-5 — Dangling `track2_hub.html` link in Track 2 hub

**File**: `160sp/ka_track2_hub.html` line 28 (inside the top banner's "primary student roadmap" sentence).
**Bug**: the link targets `track2_hub.html` without the `ka_` prefix — the file does not exist; clicking it 404s. Students entering the Track 2 hub see a broken roadmap link on first contact.
**Fix**: either (a) remove the hyperlink and leave the sentence as plain text, (b) point it at `ka_track2_overview.html` if that file exists, or (c) ask DK for the intended target. Recommend (a) as the safest zero-ambiguity fix.
**Verify**: `curl -o /dev/null -w "%{http_code}"` on the resolved URL returns 200 or the link is gone.
**Owner**: Codex.

---

## P1 fixes (land before commit unless DK approves deferral)

### P1-6 — Status-pill colours fail WCAG AA contrast

**File**: `ka_journey_page.css` around lines 135-136.
**Bug**: `.status-pill.naive { background: #D15A73; color: #fff; }` yields ~3.3:1 contrast and `.status-pill.prototype { background: #E8872A; color: #fff; }` yields ~2.9:1 — both fail the 4.5:1 bar for small text. Violates the DK-mandated WCAG AA rule in `~/REPOS/CLAUDE.md`.
**Fix**: deepen the pill hues: `.status-pill.naive { background: #B23550; color: #fff; }` and `.status-pill.prototype { background: #9a5010; color: #fff; }`. Apply the same two-colour change to the corresponding sidebar `.side-status.naive` / `.side-status.prototype` rules and to the `.status.naive` / `.status.prototype` rules on the index page (`ka_journeys.html` lines 49-52).
**Verify**: drop both colour pairs into a WCAG contrast calculator and confirm they clear 4.5:1 on the white background.
**Owner**: AG.

### P1-7 — Sidebar active-group not visibly distinct from closed groups

**File**: `ka_journey_page.css` around the `.j-sidebar .side-group` rules.
**Bug**: at 260 px the only visual cue distinguishing the open (currently-viewed) group from a closed one is the twisty rotation, which is tiny. A first-time user has to recall which twisty corresponds to their current page.
**Fix**: add `.j-sidebar .side-group.open > button.side-head { background: #F9F5EE; border-radius: 4px; }`. Also bump `font-weight: 800` on the `side-head` of the group whose `currentSlug` is inside — either by adding a `current-group` class to the group in the JS or by a CSS `:has()` selector if targeting modern browsers is acceptable. Simpler: have the JS add `side-group-current` on the group containing `currentSlug`, then style `.side-group-current > button.side-head { font-weight: 800; color: #4A3A8E; }`.
**Verify**: open any journey page; the current group's header reads as clearly distinct from its peers at a glance.
**Owner**: AG (CSS) + Codex (JS class-addition).

### P1-8 — AF sidebar group's "different genre" is under-signalled

**File**: `ka_journey_page.css` — the `.j-sidebar .side-group.side-accent-af` rules.
**Bug**: the `· AF` badge is present but the group header text at 0.82rem in `#9a5010` on white reads as subtle; a first-time visitor does not read "different kind of page" at a glance.
**Fix**: add `background: #FEF3E2; border-left: 3px solid #E8872A; padding-left: 7px;` to `.j-sidebar .side-group.side-accent-af > button.side-head`. Keep the badge.
**Verify**: the AF group header visually reads as a distinct band relative to the five complicated-surface group headers.
**Owner**: Codex.

### P1-9 — Sidebar overflow without a collapse-all affordance

**File**: `ka_journey_surface.js` (the `renderJourneySidebar` function) and `ka_journey_page.css`.
**Bug**: on the index page all six groups auto-expand. At 260 px that's 15 links + 6 group heads; on a 14-inch laptop this overflows the sticky sidebar's `max-height: calc(100vh - 40px)` and forces the sidebar into internal scroll. The scroll is functional but a collapse-all affordance would let the user control the dense view.
**Fix**: before the GROUPS loop in `renderJourneySidebar`, emit a small `<button class="side-toggle-all">Collapse all</button>` that toggles `open` on every `.side-group`. Style: `.j-sidebar .side-toggle-all { width: 100%; background: transparent; border: 0; padding: 4px 8px; font-size: 0.72rem; color: #6B53B8; cursor: pointer; text-align: right; }`. Also change the index-page default so only the first group and the AF group auto-open (`const autoOpenGroups = new Set([0, GROUPS.length - 1]);` and open iff `gi in autoOpenGroups || gi === activeGroupIdx`).
**Verify**: load the index page on a 14-inch viewport; no internal scroll in the sidebar at first paint.
**Owner**: Codex.

### P1-10 — "Evidence density and gaps" — shorten the opaque Layer F label

**File**: `ka_journey_surface.js` line 45 (the fourth GROUPS entry).
**Bug**: label `Where the evidence is dense — or absent` is evocative but opaque at a glance — first-time users do not know what a "meta-front" is and the descriptive sentence only appears on the index page, not in the sidebar.
**Fix**: change the label to `Evidence density and gaps`. Leave the index-page card-header copy as-is (the longer phrasing can keep its poetic form where there's room for the gloss).
**Verify**: sidebar reads cleanly on every journey page.
**Owner**: AG.

### P1-11 — Naive-section visual overload on journey pages

**File**: `ka_journey_page.css` in the section-accent rules.
**Bug**: the "naive solution" section already carries an amber `.j-naive` block plus an amber `.j-naive-label` pill. The section-accent left bar (`body.j-section:nth-of-type(6)::before { background: #E8872A }`) adds a third amber element to the same card, producing visual noise. Section accents are helpful on every other section but redundant here.
**Fix**: add `.j-section:has(.j-naive)::before { display: none; }` to suppress the left-accent bar on the naive section only. Fallback for older browsers without `:has()`: add a class `j-section-naive` to the naive section in the template (`gen_journey_pages.py`) and style `.j-section-naive::before { display: none; }`.
**Verify**: on `ka_journey_theory.html` (a convenient test target), the naive section reads with only the `.j-naive` amber block + `naive` badge, not with the left-accent bar also.
**Owner**: Codex (template tweak) + AG (CSS).

### P1-12 — AF pages' critique prompt is ill-posed

**File**: `scripts/gen_journey_pages.py` — the `TEMPLATE` string, specifically the `<p>` introducing the critique form.
**Bug**: current critique lede reads "For each user type below, write one to three sentences: what in the naive solution works for that user, what fails, and what one thing a redesign should change first." For AF pages the naive solution is "no implementation yet," so asking what "works" is ill-posed — students will write empty or generic responses. The three critique textareas inherit the same problem.
**Fix**: detect the `group` in the template and emit a different lede + placeholder when `group == "af"`:
- AF lede: "For each user type below, write one to three sentences: what the spec above gets right for that user, what it misses, and what one thing should be decided before build starts."
- AF textarea placeholder: "What the spec gets right for this user, what it misses, and one decision that should be made before build."

Keep the complicated-surface lede + placeholder unchanged for the other twelve pages. Then re-run `python3 scripts/gen_journey_pages.py` and confirm `git diff` shows only the three AF HTML files changed (plus the template source).
**Verify**: open `ka_journey_af_references.html` and confirm the critique lede matches the AF variant; open `ka_journey_en.html` and confirm it still matches the complicated-surface variant.
**Owner**: Codex.

### P1-13 — Stale duplicate `160sp/ka_canonical_navbar.js`

**File**: `160sp/ka_canonical_navbar.js` (the stale copy).
**Bug**: this file is a copy of the canonical navbar from before today's regime-tag removal. It still renders `Research Atlas` / `COGS 160 Spring` in its `buildBrand()`. No HTML currently loads this copy (all 160sp pages use `../ka_canonical_navbar.js`), so it is dormant. But leaving it in the tree invites a future drive-by `<script src="ka_canonical_navbar.js">` that will silently re-introduce the tag, defeating DK's removal request.
**Fix**: delete `160sp/ka_canonical_navbar.js`. Before deleting, grep the whole repo for `160sp/ka_canonical_navbar.js` and `src="ka_canonical_navbar.js"` inside 160sp/* files to confirm zero references. If any reference exists, repoint it to `../ka_canonical_navbar.js` and then delete.
**Verify**: `grep -r 'ka_canonical_navbar.js' 160sp/` returns only references ending in `../ka_canonical_navbar.js` (relative-up to root).
**Owner**: AG.

---

## P2 follow-ups (do if time permits; otherwise defer)

### P2-14 — Navbar triangle readability

**File**: `ka_canonical_navbar.js` the `mark` SVG in `buildBrand()`.
**Action**: drop the two inner diagonals (the `<line>` elements from apex to each base corner), keep the outer polygon + three vertex circles. At 22 px the diagonals read as decoration rather than brand structure; removing them raises silhouette legibility.
**Owner**: Codex.

### P2-15 — Keyboard shortcut for sibling jump

**Files**: `ka_journey_surface.js` plus a small keyboard-listener.
**Action**: bind `ArrowLeft` / `ArrowRight` to cycle through `SIBLINGS` when the focus is not in an input or textarea; update the `location.href` to the prev/next sibling.
**Owner**: Codex.

### P2-16 — Index hero prose is long for first-paint

**File**: `ka_journeys.html`.
**Action**: demote the second hero paragraph ("Every linked page on this index follows the same scaffold…") into a collapsible `<details>` labelled "How these pages are structured" below the card grid.
**Owner**: AG.

### P2-17 — Status-pill vocabulary overloading

**Files**: `ka_journeys.html`, `ka_journey_surface.js` GROUPS table.
**Action**: rename the three AF pages' status from `absent` to `spec-only`, and add a `.status.spec-only` CSS rule with a neutral-grey palette. Keeps the complicated-surface `absent` pill as meaning "the page does not yet exist" and distinguishes the AF-side "the functionality does not yet exist" case.
**Owner**: AG.

### P2-18 — `.sep` class misnamed on home sub-nav

**File**: `ka_home.html`.
**Action**: rename the new `.branch` class (landed in P0-1) so the name matches its role — a navigational branch link rather than a visual separator. (This may already be covered by P0-1 if the fix adds the correctly-named new class; confirm on review.)
**Owner**: Codex.

---

## How to land fixes

Each probe is its own commit. Use `--author="Codex <codex@openai.com>"` or `--author="AG <ag@google.com>"` as appropriate. Commit subjects lead with `fix(journeys): P{level}-{N} — {short subject}`. Batch related CSS tweaks if and only if they touch the same rule block.

When all P0 and P1 probes are green, write `docs/RUTHLESS_FIX_STATUS_2026-04-20_PM.md` with: probe-by-probe verdicts, commit hashes, P2 deferrals if any. Verdict: **CLEAN** / **CLEANED (N fixes)** / **BLOCKED (reason)**.

## Completion criteria

- Every P0 probe lands a commit.
- Every P1 probe lands a commit (or is explicitly deferred by DK in the status file).
- `git status` is clean on the working tree.
- A manual 10-minute walk through `ka_home.html` → `ka_journeys.html` → one complicated-surface page → one AF page → back to the Track 2 hub confirms zero dead links, no duplicate classes in the sidebar markup, AF group visually distinct, active-group header clearly highlighted.
- Post `CLEAN` to DK. DK runs `git commit`, `git push origin master`, then asks Codex to `git pull` on staging and to run the Phase 7 symlink flip described in `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md` to promote to production.

## References

Nielsen, J. (1994). Enhancing the explanatory power of usability heuristics. In *CHI '94 Proceedings* (pp. 152–158). https://doi.org/10.1145/191666.191729 — the heuristic framework the usability audit used; H1 Visibility of system status drives the aria-expanded fix, H4 Consistency drives the count-label fix, H5 Error prevention drives the dead-link and 404 fixes, H8 Aesthetic and minimalist design drives the AF critique-prompt rewrite. Google cites ≈ 2,400.

Web Content Accessibility Guidelines (WCAG) 2.1, §1.4.3 Contrast (Minimum). https://www.w3.org/TR/WCAG21/ — the 4.5:1 contrast bar the status-pill fix must clear.
