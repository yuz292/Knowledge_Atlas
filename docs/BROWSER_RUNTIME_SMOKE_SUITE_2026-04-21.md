# Browser Runtime Smoke Suite

Date: 2026-04-21

## Purpose

`site_runtime_smoke.py` proves that the server, assets, payloads, and API routes answer sensibly.

`browser_runtime_smoke.py` proves something stricter:

- a previously opened page updates its visible auth state after login;
- A0 renders its assigned-question DOM after login, not merely the JSON endpoint;
- previously opened pages return to an anonymous state after logout;
- the canonical navbar and page-specific shells agree about the user's state.

## Why This Exists

Recent failures were not failures of simple reachability. They were failures of **truthfulness in the browser**:

- login succeeded but the banner remained anonymous;
- A0 endpoints worked but the page showed no assignment;
- old tabs remained stale until hard refresh.

This suite is intended to catch exactly those cases.

## Commands

From the repo root:

```bash
bash scripts/run_browser_runtime_smoke.sh staging
bash scripts/run_browser_runtime_smoke.sh production
```

Direct invocation:

```bash
python3 scripts/browser_runtime_smoke.py --profile staging
python3 scripts/browser_runtime_smoke.py --profile production
```

## Credential Inputs

The wrapper reads `.smoke.env` if present.

Useful variables:

```bash
KA_BROWSER_SMOKE_STAGING_STUDENT_EMAIL=...
KA_BROWSER_SMOKE_STAGING_STUDENT_PASSWORD=...
KA_BROWSER_SMOKE_PRODUCTION_STUDENT_EMAIL=...
KA_BROWSER_SMOKE_PRODUCTION_STUDENT_PASSWORD=...
```

If these are absent, the suite falls back to the current smoke students.

## Current Checks

1. anonymous home navbar shows `Log in` and `Register`
2. anonymous A0 page shows the login overlay
3. login succeeds through the real browser flow
4. a previously opened home page refreshes to signed-in state without manual hard reload
5. a previously opened user-home page refreshes to signed-in top-bar state
6. a previously opened A0 page renders Question 1 and Question 2 choices after login
7. logout succeeds through the canonical navbar
8. previously opened user-home and A0 pages return to anonymous state after logout

## Limits

- This suite requires Playwright and a Chromium browser install.
- It is currently aimed at the highest-value auth and A0 flows, not every page on the site.
- It complements, rather than replaces, the HTTP/runtime smoke.
