# CLAUDE.md — Knowledge_Atlas repo

*Last updated: 2026-04-13*

This file supplements the root `~/REPOS/CLAUDE.md` with guidance specific to
the Knowledge Atlas repo. The root file still applies; this file overrides or
extends it for this project.

---

## Grep/audit exclusion: frozen snapshots and historical reference docs

Several directories and files in this repo are **intentionally frozen**: they
exist to document past state (server snapshots, pre-rename archives, audit
prompts tied to a specific date). Grep and ripgrep will happily return matches
from them that look current but are weeks or months stale.

**When auditing current site state, exclude these paths:**

| Path | What it is | Frozen as of |
|------|------------|--------------|
| `160sp/ka_live_snapshot/` | Mirror of production VM | 2026-04-11 |
| `160sp/ka_server_snapshot.sh` | Pull script (writes operator-local snapshot outside git) | n/a |
| `archive/` (all subdirectories) | Pre-rename / pre-refactor working trees | varies |
| `160sp/CODEX_PREDEPLOY_AUDIT_PROMPT_2026-04-13.md` | Audit contract snapshot | 2026-04-13 |
| Any file matching `SESSION_TRANSFER_DOC_*.md` | Session handoff docs | each dated |
| Any file matching `*_AUDIT_REPORT_*.md` | Historical audit reports | each dated |

### Recommended ripgrep invocation for live-state audits

```sh
rg --glob '!160sp/ka_live_snapshot/**' \
   --glob '!160sp/ka_server_snapshot.*' \
   --glob '!archive/**' \
   --glob '!**/CODEX_PREDEPLOY_AUDIT_PROMPT_*.md' \
   --glob '!**/SESSION_TRANSFER_DOC_*.md' \
   --glob '!**/*_AUDIT_REPORT_*.md' \
   "<pattern>"
```

### Known-stale strings in frozen artifacts

If you encounter these in search results, check the file path first — if it
matches the excluded set above, the match is historical and not a bug:

- `ka_track_signup.html` — superseded by `ka_student_profile.html` in the
  canonical class navbar.
- Amber gradient `#E8872A → #C96F1E` — superseded by `#B45F14 → #8E4A10` for
  WCAG 2.1 AA contrast compliance.
- `ka_search.html` — renamed to `ka_article_search.html`.
- Track 2 student flows linking to `ka_article_propose.html` — Track 2
  students now land on `160sp/ka_track2_intake.html`; the propose page remains
  the public-contributor surface.
- `docs/SITEMAP.md` — replaced with `ka_sitemap.html`.
- `#track-health` anchor — replaced with `#metrics` on the instructor portal.

### When to refresh snapshots

Only refresh `ka_live_snapshot/` and the operator-local `ka_server_snapshot.*` output *after* a
production deploy. Each refresh should create a *new* dated directory
(`ka_live_snapshot_2026-MM-DD/`) rather than overwriting the existing one, and
`SNAPSHOT_NOTICE.md` inside the old directory should be updated to point at
the new current mirror.

---

## Canonical class navbar (160sp pages)

Every page under `160sp/` that is part of the student-facing course flow should
use the canonical navbar:

- Left: Knowledge Atlas logo SVG + wordmark + "COGS 160"
- Center: `160 Syllabus` · `A0` · `A1` · `Track 1` · `Track 2` · `Track 3` · `Track 4`
- Right: `160 Student Profile` (→ `ka_student_profile.html`)

The right-nav slot is **not** a track-signup link and **not** a login link. A
previous iteration used `ka_track_signup.html`; that target has been retired.

---

## API base URL contract

All client-side fetch calls to KA endpoints must read the API base from
`window.__KA_CONFIG__.apiBase` (loaded from `ka_config.js`), not from
`location.origin`. The config script must be loaded before any page-specific
script that makes network calls. See `ka_article_propose.html:735` for the
canonical pattern.

## Authentication header contract

Authenticated endpoints read the identity from
`Authorization: Bearer <localStorage.ka_access_token>`. Pages that make
student-attributed submissions (e.g. `ka_track2_intake.html`,
`ka_article_propose.html`) must attach this header on every fetch; omitting
it causes the backend's `_get_optional_user` to treat the submission as
anonymous.
