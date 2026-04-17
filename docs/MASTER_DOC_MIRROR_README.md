# Master-doc mirror — read this before editing

**File**: `docs/MASTER_DOC_CMR_ASSEMBLED.md`
**Mirror refresh date**: 2026-04-17
**Source**: `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/MASTER_DOC_CMR_ASSEMBLED.md`
**Purpose**: Track-context reference for COGS 160 students and instructors,
kept in-repo so 160sp pages can link to it without cross-repo navigation.

## Authority

The copy in **this** repo is a **mirror**, not the source of truth. The
Article Eater repo holds the authoritative version. Edits should be made
in the AE repo and then propagated here via the procedure below. Edits made
directly to this mirror will be overwritten on the next sync.

## What to read first for each track

| Track | Start at section | Why |
|-------|------------------|-----|
| Track 1 · Image Tagger | §121.5 (Pipeline Architecture) + §122.4 (Mechanism Profiles) | How tagged images become evidence anchors |
| Track 2 · Article Finder | §121.4 (Research Queue) + §122.1–§122.3 (PNU overview + selection tree) | Where the articles go after intake |
| Track 3 · VR | §122.4 + §122.8 (Temporal Dynamics) | Which mechanisms to instrument in the VR scene |
| Track 4 · UX | §122.6 (12 SC-PNU prose conditions) + §122.13 (2026-04-17 revision) | What readers will actually see; usability target |

Section numbers refer to the markdown TOC at the top of the master doc.

## Section reconciliation notes (as of 2026-04-17)

Two §122.11 headings existed in the authoritative doc before the 2026-04-17
refresh. The second one (the revision block from this session) was
renumbered to **§122.13** on append. The duplicate that remains is not a
bug — it reflects two phases of the same project folded into one document.
If you see `§122.11 Current Status and Coverage` and you're looking for the
2026-04-17 additions, scroll past it to `§122.13`.

## How to refresh this mirror

Run this from the repo root on the Mac:

```bash
cp /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/MASTER_DOC_CMR_ASSEMBLED.md \
   docs/MASTER_DOC_CMR_ASSEMBLED.md
```

Then update the "Mirror refresh date" at the top of *this* file and commit
both. Do not edit the mirrored `MASTER_DOC_CMR_ASSEMBLED.md` directly.

## If the authoritative doc has moved

The Article Eater repo is, by convention, at
`~/REPOS/Article_Eater_PostQuinean_v1_recovery/`. Per root-level
`CLAUDE.md`, `Article_Eater_PostQuinean_v1/` (without the `_recovery`
suffix) is **deprecated** and must not be used as a source. Always verify
the path before syncing.

## Companion artefacts

- `data/ka_payloads/pnus.json` — machine-readable PNU manifest generated
  from the master doc's referenced mechanism index. Refreshed weekly and
  on demand via the admin page.
- `ka_neural.html` — public-facing page that consumes `pnus.json`.
- `docs/SSH_SETUP_FOR_PNU_REFRESH.md` — the admin-page-to-Mac refresh
  procedure and security model.
