# Runtime smoke suite — 2026-04-20

This is the server-runnable deployment gate for the public Knowledge Atlas site.

It is deliberately narrower than a full browser QA pass and deliberately broader than a static validator. It checks three things in one run:

1. the public shells actually load through the live web server
2. the live payload files are reachable and shaped correctly
3. the authenticated and admin flows still work against the deployed services

Optionally, from a checkout, it also runs the local static validator.

## Primary command

From any Knowledge Atlas checkout:

```bash
bash scripts/run_site_runtime_smoke.sh staging
```

or

```bash
bash scripts/run_site_runtime_smoke.sh production
```

That wrapper writes timestamped reports to:

```text
docs/runtime_smoke_reports/
```

and refreshes:

```text
docs/runtime_smoke_reports/latest_staging.md
docs/runtime_smoke_reports/latest_staging.json
docs/runtime_smoke_reports/latest_production.md
docs/runtime_smoke_reports/latest_production.json
```

## Direct Python form

```bash
python3 scripts/site_runtime_smoke.py --profile staging --repo-root .
```

Useful flags:

- `--base-url https://xrlab.ucsd.edu/staging_KA`
- `--student-email ...`
- `--student-password ...`
- `--admin-token ...`
- `--reset-email ...`
- `--fail-on-skip`
- `--no-site-validator`
- `--md-out path.md`
- `--json-out path.json`

## Default profiles

### `staging`

Defaults:

- base URL: `https://xrlab.ucsd.edu/staging_KA`
- student: `jpark@ucsd.edu`
- password: `StagingPass2026`
- expected track: `track4`
- expected question: `Q01`
- admin token: from `KA_SMOKE_ADMIN_TOKEN` or `KA_SMOKE_STAGING_ADMIN_TOKEN`, falling back to the current staging placeholder token if that is what the server is using

### `production`

Defaults:

- base URL: `https://xrlab.ucsd.edu/ka`
- reset email: `dkirsh@ucsd.edu`

Production does **not** assume a seeded student account. If you want the student-login checks on production, pass those values explicitly or through environment variables.

## Environment variables

General:

- `KA_SMOKE_BASE_URL`
- `KA_SMOKE_RESET_EMAIL`
- `KA_SMOKE_ADMIN_TOKEN`

Staging-specific:

- `KA_SMOKE_STAGING_BASE_URL`
- `KA_SMOKE_STAGING_RESET_EMAIL`
- `KA_SMOKE_STAGING_STUDENT_EMAIL`
- `KA_SMOKE_STAGING_STUDENT_PASSWORD`
- `KA_SMOKE_STAGING_ADMIN_TOKEN`
- `KA_SMOKE_STAGING_EXPECTED_TRACK`
- `KA_SMOKE_STAGING_EXPECTED_QUESTION_ID`

Production-specific:

- `KA_SMOKE_PRODUCTION_BASE_URL`
- `KA_SMOKE_PRODUCTION_RESET_EMAIL`
- `KA_SMOKE_PRODUCTION_STUDENT_EMAIL`
- `KA_SMOKE_PRODUCTION_STUDENT_PASSWORD`
- `KA_SMOKE_PRODUCTION_ADMIN_TOKEN`
- `KA_SMOKE_PRODUCTION_EXPECTED_TRACK`
- `KA_SMOKE_PRODUCTION_EXPECTED_QUESTION_ID`

## What it checks

Public shells:

- home
- login
- forgot-password
- user home
- topic facet view
- article view
- journeys index
- theory explorer
- mechanism journey
- admin page shell
- Track 2 hub

Payloads:

- `data/ka_payloads/topic_crosswalk.json`
- `data/ka_payloads/article_details.json`

Authenticated flows:

- `/health`
- `/auth/forgot-password`
- `/auth/login`
- `/auth/me`
- `/api/assignments`

Admin flows:

- `/api/admin/class/health`
- `/api/admin/class/roster`
- `/api/admin/class/grading`

Local checkout validation:

- `python3 scripts/site_validator.py --json`

## Exit rule

The suite exits non-zero if any check fails.

If you also want skipped checks to fail the run, pass:

```bash
--fail-on-skip
```

That is appropriate for a staging-to-production gate.
