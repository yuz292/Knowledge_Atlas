# Ruthless Prompt — Site And Payload Validation (2026-04-22)

You are not here to be reassuring. You are here to discover whether the
Knowledge Atlas site is actually fit to trust.

## Mission

Test the current checkout and the currently served site as if you expect to find
deception, drift, stale assets, broken auth state, or hollow payload claims.

Do **not** stop at HTTP 200.

## Required standards

Treat each of these as a separate claim to verify:

- the public shells render
- the auth state changes visibly after login and logout
- A0 renders the assigned question and the Question 2 pool
- forgot-password is honest
- reset-password rejects invalid tokens honestly
- the public payloads actually exist and have the shape they claim
- the served tree matches the checked-out tree

## Command sequence

From the relevant checkout, run:

```bash
bash scripts/run_ruthless_validation_cycle.sh staging
```

and, after staging is clean:

```bash
bash scripts/run_ruthless_validation_cycle.sh production
```

If the run should exercise forgot-password in a browser, set a safe reset-email
target first, for example:

```bash
KA_BROWSER_SMOKE_RESET_EMAIL=jpark@ucsd.edu bash scripts/run_ruthless_validation_cycle.sh staging
```

For production, do **not** set a real reset email unless you intentionally want
to test that path and invalidate earlier links.

## What must be exercised

### Local contract layer

- `tests/test_site_runtime_smoke.py`
- `tests/test_payload_soft_rebuild_contract.py`

### Runtime layer

- home shell
- login shell
- forgot-password shell
- reset-password shell
- user-home shell
- A0 shell
- topic facet shell
- article page shell
- journeys shell
- theory explorer shell
- mechanism journey shell
- admin shell
- navbar/CSS/favicon assets
- `topic_crosswalk.json`
- `article_details.json`
- `paper_pnus.json`
- `theories.json`
- `mechanisms.json`
- auth health
- student login
- `auth/me`
- assignments
- A0 question assignment
- A0 Question 2 topic pool
- admin health, roster, grading when token is available

### Browser layer

- anonymous navbar
- anonymous A0 overlay
- admin anonymous gate
- invalid reset-token handling
- forgot-password browser flow when configured
- login redirect
- cross-tab navbar refresh after login
- cross-tab navbar refresh after logout
- A0 visible state after login
- A0 visible reset after logout

## Interpretation rules

- A 200 with the wrong DOM markers is a failure.
- A 200 with the wrong JSON shape is a failure.
- A payload that exists but overclaims its semantics is a failure.
- A skip is acceptable only if the missing credential or reset target is
  explicitly named.
- Do not claim “all green” if protected checks were skipped.

## Specific honesty constraint for the soft rebuild

The current soft rebuild legitimately exposes:

- paper-level PNU summaries
- a descriptive theory index
- a flattened mechanism inventory

It does **not** yet justify claims about:

- paper-grounded mechanism chains
- populated theory-mechanism packets
- prediction-bearing theory exports

If any UI or report implies otherwise, call it out plainly.

## Deliverable

Return:

1. a one-line verdict for staging or production
2. every failing or skipped check
3. the likely root cause of each failure
4. whether the defect is code, payload, deployment, permissions, or cache
5. whether production promotion is justified
