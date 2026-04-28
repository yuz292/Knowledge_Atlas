# Staging Functional Smoke Matrix — 2026-04-20

- Base URL: `https://xrlab.ucsd.edu/staging_KA`
- Transport: public HTTP routes exercised from `xrlab` via `curl`
- Run time: 2026-04-20 18:21 PDT
- Student account tested: `jpark@ucsd.edu`

## Summary

- Passed: **0**
- Failed: **20**
- Verdict: **NEEDS ATTENTION**

## Results

| Check | Result | Detail |
|---|---|---|
| Home page | FAIL | rc=0; HTTP 000; missing: A Large Knowledge Model social behavior and brains. |
| Journeys index | FAIL | rc=0; HTTP 000; missing: all fifteen Article Finder problems |
| Journey theory page | FAIL | rc=0; HTTP 000; missing: Theory deep-dive Cross-jump |
| Journey AF page | FAIL | rc=0; HTTP 000; missing: what the spec above gets right for that user Article Finder problems |
| Forgot-password page shell | FAIL | rc=0; HTTP 000; missing: Reset your password Back to home Visitor, Researcher, Practitioner, and Contributor roles are public. |
| Login page shell | FAIL | rc=0; HTTP 000; missing: Forgot password Knowledge Atlas |
| User home shell | FAIL | rc=0; HTTP 000; missing: GUI track workbench Theory Explorer |
| Topic facet shell | FAIL | rc=0; HTTP 000; missing: Topic Page (Facet View) data/ka_payloads/topic_crosswalk.json |
| Article page shell | FAIL | rc=0; HTTP 000; missing: Loading article record article_details.json |
| Admin page shell | FAIL | rc=0; HTTP 000; missing: This console lets you run the class roster Sign in with your UCSD instructor account. |
| Track 2 hub | FAIL | rc=0; HTTP 000; missing: Article Finder Unified pipeline reference |
| Crosswalk payload | FAIL | rc=0; HTTP 000; missing: "rows" "outcome_index" |
| Article details payload | FAIL | rc=0; HTTP 000; missing: "details" PDF-0007 |
| Auth health endpoint | FAIL | rc=0; HTTP 000; body excerpt:  |
| Forgot-password action | FAIL | rc=0; HTTP 000; body excerpt:  |
| Student login action | FAIL | rc=0; HTTP 000; body excerpt:  |
| Student auth/me state | FAIL | Skipped because login failed |
| Student assignments state | FAIL | Skipped because login failed |
| Admin class health | FAIL | rc=0; HTTP 000; body excerpt:  |
| Admin roster data | FAIL | rc=0; HTTP 000; body excerpt:  |

## Notes

- This is an HTTP/action smoke matrix, not a full browser-behaviour audit.
- The checks pull live triggers where that is feasible quickly: password-reset, login, `/auth/me`, assignments, admin health, and roster.
- Client-side rendering pages such as the article and topic views are checked at the page-shell level plus their required payload assets, but not with a full interactive browser in this run.
