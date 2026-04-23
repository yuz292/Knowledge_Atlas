### CW commit 42d65fc — deployment

- Phase 1 result: PASS
  - `python3 scripts/gen_journey_pages.py` regenerated 15 journey pages with no committed drift.
  - Internal `href` targets in `ka_journey_*.html` resolved cleanly against the filesystem.
  - AF self-link suppression pattern was correct on `ka_journey_af_references.html`, `ka_journey_af_roi.html`, and `ka_journey_af_neuro.html`.
  - Claude's requested `python3 scripts/site_runtime_smoke.py --local` flag does not exist in the current script. Deviation: used the supported command `python3 scripts/site_runtime_smoke.py --profile staging --repo-root /Users/davidusa/REPOS/Knowledge_Atlas`, which passed with `28 pass, 0 fail, 0 skip`.

- Phase 2 result: PASS
  - `git push origin master` reported `Everything up-to-date`.

- Phase 3 Nginx fix: DONE
  - The staging alias had previously been serving HTML but 404ing `.js`, `.css`, and `.ico`.
  - Current staging asset checks now return `200` for `ka_canonical_navbar.js`, `ka_atlas_shell.css`, `ka_journey_page.css`, and `favicon.ico`.

- Phase 3 deploy result: PASS
  - Current staging path in use: `/home/dkirsh/ka-staging-2026-04-20`
  - Current deployment mechanism in use: `bash scripts/server_release_cycle.sh full`
  - Staging smoke at `2026-04-21T17:13:11Z` UTC: `28 pass, 0 fail, 0 skip`

- Phase 4 cut-over: PASS
  - Production path in use: `/var/www/xrlab/ka`
  - Deviation from Claude prompt: current production cut-over is handled by the canonical release script rather than an explicit `/srv/...` symlink flip.
  - Production refresh completed during the release cycle at `2026-04-21T17:13:14Z` UTC.
  - Production smoke at `2026-04-21T17:13:14Z` UTC: `22 pass, 0 fail, 6 skip`
  - Production favicon now returns `200`, and production forgot-password page now points at `/auth/forgot-password` rather than the stale `/api/auth/forgot-password` fallback.

- Any deviations from this prompt and why:
  - Deployed current `master` tip (`59ef0ad`) rather than checking out detached commit `42d65fc`, because `master` already contained `42d65fc` plus necessary hotfixes for staging assets, favicon delivery, and forgot-password routing.
  - Used the current server paths (`/home/dkirsh/ka-staging-2026-04-20` and `/var/www/xrlab/ka`) rather than the older `/srv/...` placeholders in the prompt.
  - The release script performs the production promotion atomically for this environment, so no manual symlink flip was required.

- Ping CW: deployment complete; staging and production are both green on the current master tip.

### CW commit d684010 — deployment

- Phase 1 result (five checks): PASS
  - `python3 scripts/gen_journey_pages.py` rewrote 15 journey pages and `git diff --stat -- ka_journey_*.html` was empty.
  - Internal `href` targets in `ka_journey_*.html` resolved cleanly against the filesystem; no broken local targets were found.
  - AF self-link suppression was correct on `ka_journey_af_references.html`, `ka_journey_af_roi.html`, and `ka_journey_af_neuro.html`.
  - The prompt's `python3 scripts/site_runtime_smoke.py --local` flag no longer exists. Deviation: used the supported equivalent `python3 scripts/site_runtime_smoke.py --profile staging --repo-root /Users/davidusa/REPOS/Knowledge_Atlas --student-email jpark@ucsd.edu --student-password StagingPass2026 --expected-track track4 --expected-question-id Q01 --admin-token STAGING_TOKEN_HERE`, which passed with `30 pass, 0 fail, 1 skip` after rerunning outside the local network sandbox.
  - `grep -oE '[0-9]+ pts &middot;' 160sp/ka_track2_hub.html | sort` returned exactly `10 / 10 / 10 / 13 / 13 / 13 / 6`.

- Phase 2 result: PASS
  - `git push origin master` succeeded.

- Phase 3 Nginx fix: NOT-NEEDED
  - The staging asset-routing fix was already live.
  - External checks returned `200` with correct content types for:
    - `/staging_KA/ka_journeys.html`
    - `/staging_KA/ka_journey_af_references.html`
    - `/staging_KA/ka_canonical_navbar.js`
    - `/staging_KA/ka_journey_page.css`

- Phase 3 deploy result: PASS
  - Current staging path in use: `/home/dkirsh/ka-staging-2026-04-20`
  - Current staging tree was updated to `ada7a8c`.
  - Staging smoke at `2026-04-21T22:54:04Z` UTC: `30 pass, 0 fail, 1 skip`
  - The only skip was `Forgot-password action` because no reset email was configured for this run.

- Phase 4 symlink flip timestamp + PASS/FAIL:
  - Deviation: current production cut-over uses `bash scripts/server_release_cycle.sh promote` into `/var/www/xrlab/ka`, not the older `/srv/...` symlink procedure from the prompt.
  - Production refresh completed immediately before the smoke run at `2026-04-21T22:54:04Z` UTC.
  - Production verification passed:
    - `/ka/ka_journeys.html` -> `200`
    - `/ka/ka_canonical_navbar.js` -> `200`
    - public JS contains `buildBrand`
  - Production smoke at `2026-04-21T22:54:04Z` UTC: `27 pass, 0 fail, 4 skip`

- Any deviations from this prompt and why:
  - The prompt's named deploy tip `d684010` is no longer the branch tip. `master` had already advanced to `ada7a8c`, and that newer commit touched the same Track 2/journey surfaces. I therefore reviewed `42d65fc` and `d684010` as requested, but deployed current `master` rather than regressing the live tree to an older detached commit.
  - The prompt's `--local` smoke command is obsolete; the current smoke script supports `--profile ... --repo-root ...` instead.
  - The prompt's `/srv/...` staging and production placeholders are not current for this environment. The active paths are `/home/dkirsh/ka-staging-2026-04-20` and `/var/www/xrlab/ka`.
  - `docs/STAGING_FUNCTIONAL_SMOKE_MATRIX_2026-04-20.md` is a stale record from the pre-fix staging outage and is not an accurate pre-flight gate now. The current staging smoke plus external curl checks were used instead.

- Ping CW: review and deployment complete; staging and production are green on current master, with only the expected skipped protected checks remaining.

### Codex atlas_shared cleanup — 2026-04-22

- Commits landed:
  - `2cba6b1` `fix(relevance): disambiguate bundle_id when constitutions share a topic`
  - `3cfce93` `fix(intake): downgrade keyword false-positive hits to manual_review`
  - `cc87d91` `refactor(intake): move domain lexicon to data/domain_lexicon.json`
  - `3a07167` `refactor(relevance): move article-type defaults to data/article_type_defaults.json`
  - `c4c936f` `refactor(registry_sink): promote paper_id to top-level RegistryFact field`
  - `8ad63b3` `chore(registry_sink): type-constrain RegistryFact.schema_version as Literal`
  - `bf77f5f` `docs(contract): name paper_id as the canonical article-identity field`
  - `789132a` `chore(util): consolidate duplicate helpers into _util.py`
  - `d2f0191` `chore(api): trim __all__ to ten canonical public-API entry points`
  - `885c873` `chore(package): expose __version__ = 0.2.0`
  - `804e286` `docs(changelog): start CHANGELOG.md with backfilled history through 0.3.0`
  - `cbd323a` `chore(types): satisfy final mypy sweep`

- PR URL:
  - `https://github.com/dkirsh/atlas_shared/pull/1`

- Test baseline before:
  - `25 pass / 0 fail / 0 skip`

- Test baseline after:
  - `33 pass / 0 fail / 0 skip`
  - `mypy src/atlas_shared` -> clean

- Any suggestions written to `docs/ATLAS_SHARED_SUGGESTIONS_2026-04-21.md` as new Codex-review entries:
  - none

- Anything that needed a DK decision and was deferred rather than implemented:
  - none

- Deviation from Claude prompt:
  - one extra content commit, `cbd323a`, was added after the final static sweep exposed real type inconsistencies in `bundle_router.py`, `intake.py`, and `cli_adjudicator.py`. This was done explicitly rather than hidden inside earlier commits.

- Ping CW: atlas_shared cleanup branch is pushed, PR is open, tests are greener than baseline, and the shared article-type / paper-id / bundle-id layer is materially tidier for AF use.
