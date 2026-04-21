#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
exec "$REPO/scripts/run_site_runtime_smoke.sh" staging "$@"
if [[ "$roster_rc" == "0" && "$roster_code" == "200" && "$roster_body" == *'jpark@ucsd.edu'* ]]; then
  record_result "Admin roster data" "PASS" "HTTP 200; roster includes seeded student jpark@ucsd.edu"
else
  record_result "Admin roster data" "FAIL" "rc=$roster_rc; HTTP $roster_code; body excerpt: ${roster_body:0:180}"
fi

timestamp="$(date '+%Y-%m-%d %H:%M %Z')"
cat >"$OUTPUT_PATH" <<EOF
# Staging Functional Smoke Matrix — 2026-04-20

- Base URL: \`$BASE_URL\`
- Transport: public HTTP routes exercised from \`$SSH_HOST\` via \`curl\`
- Run time: $timestamp
- Student account tested: \`$STUDENT_EMAIL\`

## Summary

- Passed: **$PASS_COUNT**
- Failed: **$FAIL_COUNT**
- Verdict: **$( [[ "$FAIL_COUNT" -eq 0 ]] && echo "PASS" || echo "NEEDS ATTENTION" )**

## Results

| Check | Result | Detail |
|---|---|---|
$(printf '%b' "$RESULT_ROWS")

## Notes

- This is an HTTP/action smoke matrix, not a full browser-behaviour audit.
- The checks pull live triggers where that is feasible quickly: password-reset, login, \`/auth/me\`, assignments, admin health, and roster.
- Client-side rendering pages such as the article and topic views are checked at the page-shell level plus their required payload assets, but not with a full interactive browser in this run.
EOF

printf 'Wrote %s\n' "$OUTPUT_PATH"
printf 'Passed: %s\nFailed: %s\n' "$PASS_COUNT" "$FAIL_COUNT"
