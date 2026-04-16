# Codex Site Navigation Audit And Deploy Notes

Date: 2026-04-16
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`

## What was checked

I audited the active student-facing site graph starting from these current entry points:

- `160sp/ka_student_setup.html`
- `160sp/ka_student_profile.html`
- `160sp/ka_track1_tagging.html`
- `160sp/ka_track1_setup.html`
- `160sp/ka_track2_pipeline.html`
- `160sp/ka_track2_setup.html`
- `160sp/ka_track2_intake.html`
- `160sp/ka_track3_hub.html`
- `160sp/ka_track3_team_hub.html`
- `160sp/ka_track3_setup.html`
- `160sp/ka_track3_today.html`
- `160sp/ka_track3_resources.html`
- `160sp/ka_track3_vr.html`
- `160sp/ka_track4_ux.html`
- `160sp/ka_track4_setup.html`
- `160sp/ka_track4_hub.html`
- `ka_sitemap.html`
- `ka_theory.html`

The crawl followed internal HTML links only. It ignored external URLs and old archive material.

## Result

`ACTIVE_BROKEN_LINKS = 0`

For the audited active site pages, internal file navigation is currently clean.

## Track 3 naming state

Track 3 is now internally coherent:

- `160sp/ka_track3_hub.html` is the canonical student roadmap page.
- `160sp/ka_track3_team_hub.html` is the explicit team-coordination page.
- `160sp/track3_hub.html` remains only as a compatibility redirect shim to the canonical roadmap.
- Track 3 week pages, setup, today, resources, student profile, and cross-track nav now point to the canonical Track 3 names.

## Merge state

The in-progress merge was blocking deploy readiness. That merge has now been resolved and committed locally before the follow-up navigation fixes.

## What was repaired in this pass

- Removed the stale unresolved merge marker from `160sp/ka_track1_setup.html`.
- Normalized Track 3 roadmap vs team-hub naming.
- Updated Track 3 navigation targets across the 160sp pages that referenced the old names.
- Repaired stale sitemap links for week agenda pages.
- Repaired the stale sitemap link to the nonexistent `fall160_schedule.html`.
- Replaced the broken `ka_theory.html` link to `160sp/TASKS.md` with a valid course roadmap link.

## Remaining consistency debt

The site now navigates cleanly, but naming is still not fully uniform across all tracks.

The main remaining structural inconsistency is:

- Track 2 still uses `track2_hub.html` as the student roadmap page while `ka_track2_hub.html` is a different manifest/resource page.
- Track 4 still uses `track4_hub.html` as the student roadmap page while `ka_track4_hub.html` is a different team-hub page.

If the goal is full site-wide naming consistency, the next normalization pass should mirror what was just done for Track 3:

1. Promote the student roadmap page to the `ka_trackN_hub.html` name.
2. Rename the current secondary hub to an explicit role name such as `ka_trackN_team_hub.html` or `ka_trackN_manifest_hub.html`.
3. Leave the old `trackN_hub.html` path behind as a redirect shim.

That is not required for the site to function now, but it is required for a perfectly uniform naming scheme.

## Deploy recommendation

Given the recent divergence between local and server website trees, and given that the server holds live user/auth/article state, the safer web deploy method is:

1. Push the local repo state to GitHub.
2. Back up the server website tree and server databases.
3. Deploy only the changed web files to the live tree via `scp` or `rsync`, rather than doing a blind `git pull`, unless the server repo is already confirmed clean and on the intended branch.

Why `scp` / `rsync` is safer here:

- It updates only the known page assets.
- It avoids surprising server-side merge state.
- It leaves the existing databases and runtime files untouched.
- It is easier to roll back by restoring the previous copied files or the backup directory.

## Deployment preconditions

Before deploy, verify on the server:

- the live web root path
- whether the server repo has local edits
- whether the auth server or other backend process needs restart
- where the live DB files are, so they are excluded from any file copy

## Recommended immediate next move

1. Commit the current post-merge navigation fixes and this note.
2. Push to GitHub.
3. Prepare an explicit changed-files deployment bundle.
4. Copy that bundle to the server with backup-first procedure.
