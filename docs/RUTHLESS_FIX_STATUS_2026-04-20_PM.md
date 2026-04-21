# Ruthless fix status — 2026-04-20 PM

*Ruthless brief*: `docs/RUTHLESS_BRIEF_JOURNEY_AND_AF_2026-04-20.md`
*Executor*: CW (DK reassigned from Codex+AG to CW in-session)
*Verdict*: **CLEANED (13 fixes landed; 5 P2 items deferred)**

## Probe verdicts

| Probe | Severity | Surface | Verdict | Files touched |
|---|---|---|---|---|
| P0-1 | blocker | dead home-page Journeys link | OK | `ka_home.html` (new `.branch` class + `.branch` CSS rule) |
| P0-2 | blocker | duplicate `class` attr on sidebar index anchor | OK | `ka_journey_surface.js` |
| P0-3 | blocker | stale `12 surfaces` count in sidebar | OK | `ka_journey_surface.js` — now computed from `GROUPS.reduce(...)` |
| P0-4 | blocker | `aria-expanded` mismatch on index page | OK | `ka_journey_surface.js` — single `isOpen` drives both class + aria |
| P0-5 | blocker | dangling `track2_hub.html` link | OK | `160sp/ka_track2_hub.html` — broken link removed from intro paragraph |
| P1-6 | before-commit | WCAG AA pill contrast | OK | `ka_journey_page.css`, `ka_journeys.html` — `#D15A73`→`#B23550`, `#E8872A`→`#9a5010` |
| P1-7 | before-commit | active-group not visibly distinct | OK | `ka_journey_page.css` + `ka_journey_surface.js` — `.side-group.open` tint + `.side-group-current` weight |
| P1-8 | before-commit | AF group under-signalled | OK | `ka_journey_page.css` — row background + left border on AF group head |
| P1-9 | before-commit | sidebar overflow without collapse-all | OK | `ka_journey_surface.js` + CSS — "Collapse all" button + selective default-open on index |
| P1-10 | before-commit | opaque Layer F label | OK | `ka_journey_surface.js` — "Where the evidence is dense — or absent" → "Evidence density and gaps" |
| P1-11 | before-commit | naive section visual overload | OK | `ka_journey_page.css` + `scripts/gen_journey_pages.py` — `.j-section-naive::before { display:none }` + class emission; 15 pages regenerated |
| P1-12 | before-commit | AF critique prompt ill-posed | OK | `scripts/gen_journey_pages.py` — AF-group-aware lede, placeholder, naive-label, naive-heading, naive-hint; three AF pages regenerated |
| P1-13 | before-commit | stale `160sp/ka_canonical_navbar.js` | OK | deleted (zero live HTML references confirmed before removal) |

All thirteen fixes executed against the working tree. Verified programmatically by a Python assertion pass that checks each fix is present in the expected file and that the regenerated HTML contains the expected new content (spec-critique lede for AF pages; naive-section class on every page; sidebar total count dynamic; single-`class` anchor; no `Where the evidence is dense` in the GROUP labels; etc.).

## P2 items deferred

Flagged in the brief as nice-to-have; landing them would inflate today's diff without changing the shippable state.

- **P2-14** navbar triangle silhouette — drop the two inner diagonals for legibility.
- **P2-15** keyboard Arrow-Left / Arrow-Right for sibling jump.
- **P2-16** demote index hero paragraph 2 into a `<details>` disclosure.
- **P2-17** rename AF page status `absent` → `spec-only`.
- **P2-18** rename `.sep` class on home sub-nav now that `.branch` is the correct name.

DK can revisit these in a follow-up pass or assign to Codex / AG in a subsequent sprint.

## Post-fix working-tree diff

Sixteen files modified + one file deleted:

```
 M 160sp/ka_track2_hub.html
 D 160sp/ka_canonical_navbar.js
 M ka_home.html
 M ka_journey_af_neuro.html
 M ka_journey_af_references.html
 M ka_journey_af_roi.html
 M ka_journey_argumentation.html
 M ka_journey_bn.html
 M ka_journey_en.html
 M ka_journey_evidence.html
 M ka_journey_fronts.html
 M ka_journey_gaps.html
 M ka_journey_interpretation.html
 M ka_journey_mechanism.html
 M ka_journey_ontology.html
 M ka_journey_page.css
 M ka_journey_qa.html
 M ka_journey_surface.js
 M ka_journey_theory.html
 M ka_journey_topic_inspector.html
 M ka_journeys.html
 M scripts/gen_journey_pages.py
```

## Next action

DK runs `git add -A && git commit`, then `git push origin master`. Codex pulls on staging and runs the Phase 7 symlink flip from `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md` to promote to production.

The commit is safe to make.

## Codex independent verification — 2026-04-20 late session

I re-ran the brief against the current tip rather than taking the table above on trust.

- `python3 -m pytest tests/test_journey_pages_contract.py -q` → `3 passed`
- `python3 scripts/site_validator.py` → `0 errors`, `107 warnings`
- direct file assertions confirm the scoped fixes are actually present:
  - home-page Journeys link uses `.branch` and is clickable
  - sidebar index anchor now has a single `class` attribute
  - sidebar total count is computed from `GROUPS.reduce(...)`
  - `aria-expanded` is driven by the same `isOpen` truth as the visible group state
  - the collapse-all control exists and the index page defaults to only the first + AF groups open
  - the AF-specific critique lede and placeholders are present on all three AF pages
  - the naive-section accent suppression is present via `.j-section-naive::before`
  - the stale `160sp/ka_canonical_navbar.js` copy is gone
  - the bad `track2_hub.html` link is gone from `160sp/ka_track2_hub.html`

From Codex's review, there are **no remaining P0 or P1 defects within the scope of this brief**. The 107 validator warnings are unrelated pre-existing items outside the journey/AF fix set.
