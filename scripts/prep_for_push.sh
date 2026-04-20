#!/usr/bin/env bash
# prep_for_push.sh — one command that readies the repo for a staging
# deploy, handling server-side hotfixes automatically rather than asking
# the operator to make a decision.
#
# What it does, in order (all automatic):
#
#   1. Verify the working tree is clean (no uncommitted changes).
#   2. SSH-probe the server to confirm it's reachable.
#   3. Count files on the server so the size of the delta is logged.
#   4. rsync --dry-run to find files that exist on the server but
#      differ from (or are absent from) our local tip.
#   5. If server-only / server-newer files exist:
#        a. Create a named recovery branch `server-recovery-YYYY-MM-DD-HHMM`
#           off the current master tip.
#        b. rsync those specific files from the server onto the recovery
#           branch (never onto master directly).
#        c. Git-add every affected path; commit under "Recovery" author
#           with a summary listing the recovered files.
#        d. Check the branch back out and return to master.
#      This is idempotent: if the branch already exists, the script
#      creates one with a later timestamp.
#   6. Run the site validator; if errors > 0, stop with a clear message.
#   7. Run the end-to-end smoke test against a throwaway DB.
#   8. Print a final PASS / ACTION-REQUIRED summary.
#
# No decisions are required from the operator mid-run. If the script
# prints PASS, the repo is ready for Phase 3 of the deploy plan.
# If it prints ACTION-REQUIRED, the action is named in plain English.
#
# Options:
#   --skip-probe      skip the server probe (local validation + smoke only)
#   --skip-smoke      skip the smoke test
#   --server HOST     override default SSH target
#   --path PATH       override default server path
#
# Defaults assume xrlab:/var/www/ka; change via env or flags.

set -u
set -o pipefail

SERVER="${SERVER:-dkirsh@xrlab.ucsd.edu}"
SERVER_PATH="${SERVER_PATH:-/var/www/ka}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SKIP_PROBE=0
SKIP_SMOKE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-probe) SKIP_PROBE=1; shift ;;
    --skip-smoke) SKIP_SMOKE=1; shift ;;
    --server)     SERVER="$2"; shift 2 ;;
    --path)       SERVER_PATH="$2"; shift 2 ;;
    -h|--help)    sed -n '2,40p' "$0"; exit 0 ;;
    *) echo "unknown flag: $1" >&2; exit 1 ;;
  esac
done

cd "$REPO"

# ── Colours + output helpers ────────────────────────────────────
BOLD="\033[1m"; GREEN="\033[32m"; RED="\033[31m"; YELLOW="\033[33m"; RESET="\033[0m"
step=0
step_header() { step=$((step+1)); printf "\n${BOLD}[Step %d]${RESET} %s\n" "$step" "$1"; }
ok()   { printf "  ${GREEN}✓${RESET} %s\n" "$1"; }
warn() { printf "  ${YELLOW}⚠${RESET} %s\n" "$1"; }
fail() { printf "  ${RED}✗${RESET} ${BOLD}%s${RESET}\n" "$1"; shift; for l in "$@"; do printf "    %s\n" "$l"; done; }

# ── Final verdict accumulator ───────────────────────────────────
ACTION_REQUIRED=0
RECOVERY_BRANCH=""
SUMMARY_LINES=()
add_summary() { SUMMARY_LINES+=("$1"); }

printf "\n${BOLD}Knowledge Atlas — prep for push${RESET}\n"
printf "repo:   %s\n" "$REPO"
printf "server: %s (path %s)\n" "$SERVER" "$SERVER_PATH"
printf "local:  %s\n" "$(git log --oneline -1)"

# ── Step 1: working tree must be clean ──────────────────────────
step_header "Working-tree cleanliness"
if ! git diff --quiet HEAD 2>/dev/null; then
  fail "you have uncommitted changes — commit or stash them before deploying" \
       "run 'git status' to see them, then 'git add' + 'git commit' (or 'git stash') and rerun"
  exit 1
fi
# Allow untracked files but flag them
UNTRACKED_COUNT=$(git status --porcelain | awk '/^\?\?/{c++} END{print c+0}')
if [[ "$UNTRACKED_COUNT" -gt 0 ]]; then
  warn "$UNTRACKED_COUNT untracked file(s) present — they will NOT be deployed"
  git status --short | awk '/^\?\?/{print "    " $0}' | head -5
  add_summary "$UNTRACKED_COUNT untracked files ignored (run 'git status' to see them)"
else
  ok "working tree clean, nothing untracked"
fi

# ── Step 2: server probe ────────────────────────────────────────
if [[ "$SKIP_PROBE" -eq 0 ]]; then
  step_header "Server reachability"
  if ! ssh -o ConnectTimeout=6 -o BatchMode=yes "$SERVER" 'true' 2>/dev/null; then
    fail "SSH to $SERVER failed" \
         "check VPN, check ssh-add -l, check ~/.ssh/config" \
         "rerun with --skip-probe to continue without the server check"
    exit 1
  fi
  ok "SSH reachable"

  if ! ssh "$SERVER" "test -d '$SERVER_PATH'" 2>/dev/null; then
    fail "$SERVER_PATH does not exist on $SERVER" \
         "override with --path /path/to/deploy/root if the layout has changed"
    exit 1
  fi
  ok "$SERVER_PATH exists on $SERVER"

  step_header "Server file counts"
  ssh "$SERVER" "cd '$SERVER_PATH' && \
       total=\$(find . -type f | wc -l); \
       html=\$(find . -type f -name '*.html' | wc -l); \
       echo 'total files: '\$total'; html: '\$html" | sed 's/^/  /'

  # ── Step 3: find server-only / server-newer files ────────────
  step_header "Diffing server vs. local (this may take ~20s)"
  TMP_DIFF="$(mktemp /tmp/ka_prep_diff.XXXXXX)"

  # rsync --dry-run with --itemize-changes; we want files where the
  # server has content we don't (candidates for recovery).
  # Direction FROM server TO local: the ">f" / "cf" lines are things
  # the server has that we'd receive.
  if ! rsync -nirc \
      --exclude='.git/' --exclude='.git' \
      --exclude='data/' --exclude='160sp/grading/' \
      --exclude='*.db' --exclude='*.db-shm' --exclude='*.db-wal' \
      --exclude='__pycache__/' --exclude='*.pyc' \
      --exclude='.DS_Store' --exclude='node_modules/' \
      --exclude='data/ka_payloads/' \
      "$SERVER:$SERVER_PATH/" "$REPO/" \
      > "$TMP_DIFF" 2>/dev/null; then
    warn "rsync dry-run failed; skipping auto-recovery"
    add_summary "rsync dry-run failed — run scripts/probe_server_diff.sh manually to inspect"
  else
    RECEIVE_COUNT=$(awk '/^(>f|cf)/{c++} END{print c+0}' "$TMP_DIFF")
    if [[ "$RECEIVE_COUNT" -eq 0 ]]; then
      ok "no server-side files differ from local (no hotfixes to recover)"
    else
      warn "$RECEIVE_COUNT file(s) on the server differ from local"
      awk '/^(>f|cf)/{print "    " $0}' "$TMP_DIFF" | head -10
      if [[ "$RECEIVE_COUNT" -gt 10 ]]; then
        printf "    ... and %s more\n" $((RECEIVE_COUNT - 10))
      fi

      # ── Step 4: auto-recover hotfixes onto a branch ─────────
      step_header "Recovering server hotfixes onto a named branch"
      RECOVERY_BRANCH="server-recovery-$(date +%Y-%m-%d-%H%M)"
      CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

      # Ensure the branch name is unique even if this runs repeatedly
      while git rev-parse --verify "$RECOVERY_BRANCH" >/dev/null 2>&1; do
        sleep 61   # branches are minute-stamped; wait and retry
        RECOVERY_BRANCH="server-recovery-$(date +%Y-%m-%d-%H%M)"
      done

      if ! git checkout -b "$RECOVERY_BRANCH" 2>/dev/null; then
        fail "could not create branch $RECOVERY_BRANCH"
        exit 1
      fi
      ok "branch created: $RECOVERY_BRANCH"

      # Pull only the files that actually differ; keep other local
      # content untouched. --files-from= is the safest idiom.
      RECOVER_LIST="$(mktemp /tmp/ka_recover_list.XXXXXX)"
      awk '/^(>f|cf)/{print $2}' "$TMP_DIFF" > "$RECOVER_LIST"

      if ! rsync -av --files-from="$RECOVER_LIST" \
            --exclude='data/ka_payloads/' \
            "$SERVER:$SERVER_PATH/" "$REPO/" >/dev/null 2>&1; then
        warn "rsync of $(wc -l < "$RECOVER_LIST") files partially succeeded"
      fi

      # Stage exactly those paths and commit on the recovery branch
      while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        git add -- "$f" 2>/dev/null || true
      done < "$RECOVER_LIST"

      if git diff --cached --quiet; then
        warn "recovery branch has no new content (server content matched local despite rsync diff)"
        git checkout "$CURRENT_BRANCH" >/dev/null 2>&1
        git branch -D "$RECOVERY_BRANCH" >/dev/null 2>&1
        RECOVERY_BRANCH=""
      else
        SHORT_LIST=$(head -5 "$RECOVER_LIST" | tr '\n' ', ' | sed 's/, $//')
        COMMIT_SUBJ="Recovery: server-side hotfixes from $SERVER_PATH ($RECEIVE_COUNT files)"
        git -c user.name="Server Recovery" \
            -c user.email="server-recovery@localhost" \
            commit -m "$COMMIT_SUBJ" \
            -m "Pulled automatically by scripts/prep_for_push.sh from $SERVER:$SERVER_PATH." \
            -m "These files were on the server but not in our git tip. They are captured on this branch so no hotfix is lost during the staging deploy." \
            -m "First 5 recovered paths: $SHORT_LIST (see full list at $RECOVER_LIST during this run)." \
            -m "Review with: git diff master..$RECOVERY_BRANCH" \
            >/dev/null 2>&1

        ok "committed $RECEIVE_COUNT recovered files onto $RECOVERY_BRANCH"
        add_summary "Recovered $RECEIVE_COUNT server hotfixes onto branch $RECOVERY_BRANCH"
        add_summary "  Review with: git diff $CURRENT_BRANCH..$RECOVERY_BRANCH"
        add_summary "  Merge into $CURRENT_BRANCH with: git checkout $CURRENT_BRANCH && git merge $RECOVERY_BRANCH"
      fi

      git checkout "$CURRENT_BRANCH" >/dev/null 2>&1
      ok "returned to $CURRENT_BRANCH"
      ACTION_REQUIRED=1   # DK should review the recovery branch before merging
    fi
  fi
  rm -f "$TMP_DIFF"
else
  step_header "Server probe (skipped per --skip-probe)"
fi

# ── Step 5: site validator ───────────────────────────────────────
step_header "Site validator"
VAL_OUT=$(python3 scripts/site_validator.py 2>&1 | tail -6)
N_ERR=$(echo "$VAL_OUT" | grep -oE "'error': [0-9]+" | grep -oE "[0-9]+" | head -1 || echo 1)
N_WARN=$(echo "$VAL_OUT" | grep -oE "'warn': [0-9]+" | grep -oE "[0-9]+" | head -1 || echo 0)
if [[ "${N_ERR:-1}" == "0" ]]; then
  ok "validator: 0 errors, ${N_WARN:-0} warns"
else
  fail "validator: ${N_ERR:-1} error(s) — deploy blocked"
  echo "$VAL_OUT" | sed 's/^/    /'
  exit 1
fi

# ── Step 6: smoke test ───────────────────────────────────────────
if [[ "$SKIP_SMOKE" -eq 0 ]]; then
  step_header "End-to-end smoke test"
  if bash scripts/smoke_test_e2e.sh >/tmp/ka_smoke.log 2>&1; then
    STAGES=$(grep -c "^ .* ✓" /tmp/ka_smoke.log || echo 0)
    ok "smoke test: all stages green"
  else
    fail "smoke test failed — deploy blocked" \
         "log at /tmp/ka_smoke.log"
    tail -20 /tmp/ka_smoke.log | sed 's/^/    /'
    exit 1
  fi
else
  step_header "Smoke test (skipped per --skip-smoke)"
fi

# ── Step 7: final verdict ────────────────────────────────────────
printf "\n${BOLD}════════════════════════════════════════════════════════════${RESET}\n"
if [[ "$ACTION_REQUIRED" -eq 0 ]]; then
  printf "${BOLD}${GREEN}PASS.${RESET} The repo is ready for Phase 3 of the staging deploy.\n"
  printf "Next step:\n"
  printf "  git push origin master\n"
  printf "  git tag -a v\$(date +%%Y-%%m-%%d)-staging -m 'staging release'\n"
  printf "  git push origin v\$(date +%%Y-%%m-%%d)-staging\n"
else
  printf "${BOLD}${YELLOW}ACTION REQUIRED.${RESET}\n"
  for line in "${SUMMARY_LINES[@]}"; do
    printf "  • %s\n" "$line"
  done
  printf "\nOne thing to decide:\n"
  if [[ -n "$RECOVERY_BRANCH" ]]; then
    printf "  • Do you want to merge %s into master?\n" "$RECOVERY_BRANCH"
    printf "    Review:  git diff master..%s\n" "$RECOVERY_BRANCH"
    printf "    Merge:   git merge %s\n" "$RECOVERY_BRANCH"
    printf "    Discard: git branch -D %s\n" "$RECOVERY_BRANCH"
    printf "\n  After deciding, rerun this script; it will then PASS.\n"
  fi
fi
printf "${BOLD}════════════════════════════════════════════════════════════${RESET}\n\n"
