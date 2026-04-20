# Snapshot Notice — `ka_live_snapshot/`

**Status:** FROZEN HISTORICAL MIRROR. Do **not** treat as a source of truth for
current site state, nav structure, file contracts, or link targets.

**Captured:** on or before 2026-04-11. The raw VM dump is now treated as an
operator-local artefact and is not kept in git.

## Why this directory exists

`ka_live_snapshot/` was cloned from the production VM (`/var/www/xrlab/ka/`) so
that a local Cowork session could diff against what is actually deployed. Once
captured, it was never updated. The live repo root has advanced since then —
navbars, intake pages, portal sub-navs, and critique endpoints have all
changed.

## Do not grep here for current state

Grep / ripgrep tooling will happily return matches from this directory that
look current but are weeks stale. Known stale strings include (but are not
limited to):

- `ka_track_signup.html` (replaced with `ka_student_profile.html` in the class
  navbar)
- the amber gradient `#E8872A → #C96F1E` (replaced with the darker AA-contrast
  pair `#B45F14 → #8E4A10`)
- references to `ka_search.html` (renamed to `ka_article_search.html`)
- Track 2 student-facing links that still point to `ka_article_propose.html`
  (Track 2 students now land on `ka_track2_intake.html`)
- `docs/SITEMAP.md` sitemap links (replaced with `ka_sitemap.html`)

When auditing current site state, restrict searches to the repo root and
`160sp/` while excluding `ka_live_snapshot/`, `archive/`, and the
operator-local `ka_server_snapshot.*` files. Example:

```sh
rg --glob '!ka_live_snapshot/**' --glob '!archive/**' \
   --glob '!*ka_server_snapshot*' "pattern"
```

## When to refresh this snapshot

When the next production deploy happens, refresh by re-running
`scripts/pull_full_server.sh` (or the equivalent) into a *new* dated directory
(e.g. `ka_live_snapshot_2026-MM-DD/`) rather than overwriting this one, and
update this notice to point to the new directory as the current mirror.
