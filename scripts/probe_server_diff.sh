#!/usr/bin/env bash
# probe_server_diff.sh — read-only reconnaissance of the xrlab production site
# before a staging-then-swap deploy. Tells DK (a) whether the server is
# reachable, (b) which files on the server differ from our GitHub tip,
# and (c) how large the current production tree is.
#
# Safe to run many times; makes no changes anywhere.
#
# Usage:
#   bash scripts/probe_server_diff.sh
#   SERVER=dkirsh@xrlab.ucsd.edu SERVER_PATH=/var/www/ka \
#       bash scripts/probe_server_diff.sh
#
# Exit codes:
#   0  = server reachable, probe produced output
#   1  = could not reach server
#   2  = reachable but the expected path is missing on the server

set -u

SERVER="${SERVER:-dkirsh@xrlab.ucsd.edu}"
SERVER_PATH="${SERVER_PATH:-/var/www/ka}"
LOCAL_REPO="$(cd "$(dirname "$0")/.." && pwd)"

BOLD="\033[1m"; GREEN="\033[32m"; RED="\033[31m"; YELLOW="\033[33m"; RESET="\033[0m"

printf "\n${BOLD}KA production-site probe${RESET}\n"
printf "server:      %s\n" "$SERVER"
printf "server path: %s\n" "$SERVER_PATH"
printf "local repo:  %s\n" "$LOCAL_REPO"
printf "local tip:   %s\n\n" "$(cd "$LOCAL_REPO" && git log --oneline -1)"

# ─── 1. SSH reachability ──────────────────────────────────────────
printf "${BOLD}[1/5]${RESET} Checking SSH reachability...\n"
if ! ssh -o ConnectTimeout=6 -o BatchMode=yes "$SERVER" 'true' 2>/dev/null; then
  printf "  ${RED}✗ SSH to %s failed.${RESET}\n" "$SERVER"
  printf "  Things to check:\n"
  printf "    * Are you on the UCSD VPN?\n"
  printf "    * Is your SSH key loaded? (ssh-add -l)\n"
  printf "    * Does ~/.ssh/config have a Host entry for xrlab?\n"
  exit 1
fi
printf "  ${GREEN}✓ server reachable${RESET}\n\n"

# ─── 2. Path exists on server ─────────────────────────────────────
printf "${BOLD}[2/5]${RESET} Checking server path exists...\n"
if ! ssh "$SERVER" "test -d '$SERVER_PATH'" 2>/dev/null; then
  printf "  ${RED}✗ %s does not exist (or is not a directory) on %s.${RESET}\n" \
         "$SERVER_PATH" "$SERVER"
  printf "  Override with SERVER_PATH=<path> if the deploy root has moved.\n"
  exit 2
fi
printf "  ${GREEN}✓ %s exists${RESET}\n\n" "$SERVER_PATH"

# ─── 3. Count files on server ─────────────────────────────────────
printf "${BOLD}[3/5]${RESET} Counting files in server tree...\n"
COUNTS=$(ssh "$SERVER" "cd '$SERVER_PATH' && \
         echo -n 'total: '; find . -type f | wc -l; \
         echo -n 'html:  '; find . -type f -name '*.html' | wc -l; \
         echo -n 'js:    '; find . -type f -name '*.js' | wc -l; \
         echo -n 'css:   '; find . -type f -name '*.css' | wc -l; \
         echo -n 'json:  '; find . -type f -name '*.json' | wc -l;")
echo "$COUNTS" | sed 's/^/  /'
printf "\n"

# ─── 4. List top-level files (sample) ─────────────────────────────
printf "${BOLD}[4/5]${RESET} Sample of top-level files on server:\n"
ssh "$SERVER" "cd '$SERVER_PATH' && ls ka_*.html 2>/dev/null | head -12" | sed 's/^/  /'
printf "\n"

# ─── 5. Diff against local tip ────────────────────────────────────
printf "${BOLD}[5/5]${RESET} File-by-file diff summary (this may take ~ 15–30s)...\n"
# Use rsync --dry-run --itemize-changes to get a list of files that differ.
# -n dry-run, -i itemize, -c use checksum (not mtime), -r recursive,
# --exclude data/ to avoid diffing payload JSON (often mutated live).
RSYNC_OUT=$(rsync -nirc \
  --exclude='.git/' --exclude='.git' \
  --exclude='data/' --exclude='160sp/grading/' \
  --exclude='*.db' --exclude='*.db-shm' --exclude='*.db-wal' \
  --exclude='__pycache__/' --exclude='*.pyc' \
  --exclude='.DS_Store' --exclude='node_modules/' \
  "$LOCAL_REPO/" "$SERVER:$SERVER_PATH/" 2>/dev/null) || {
    printf "  ${YELLOW}note: rsync dry-run failed; falling back to server-ls only${RESET}\n"
    RSYNC_OUT=""
  }

if [[ -z "$RSYNC_OUT" ]]; then
  printf "  ${YELLOW}no rsync-able diff produced; rely on git log for the delta${RESET}\n"
else
  # Count lines in RSYNC_OUT that start with >f (would send from local to server)
  # and <f (would pull from server to local — indicates server has files we don't)
  SEND_COUNT=$(echo "$RSYNC_OUT" | awk '/^>f/{count++} END{print count+0}')
  DEL_COUNT=$(echo "$RSYNC_OUT" | awk '/^\*deleting/{count++} END{print count+0}')
  NEW_DIR_COUNT=$(echo "$RSYNC_OUT" | awk '/^cd/{count++} END{print count+0}')

  printf "  files local would REPLACE on server: ${BOLD}%s${RESET}\n" "$SEND_COUNT"
  printf "  files local would CREATE on server:  %s\n" "$NEW_DIR_COUNT"
  printf "  files that exist on server but not locally: ${YELLOW}%s${RESET}\n" "$DEL_COUNT"
  printf "\n"
  if [[ "$DEL_COUNT" -gt 0 ]]; then
    printf "  ${YELLOW}⚠ Server has %s files that are not in our local tree.${RESET}\n" "$DEL_COUNT"
    printf "  These may be hotfixes that need to round-trip to git before deploy.\n"
    printf "  Here are the first 20:\n"
    echo "$RSYNC_OUT" | awk '/^\*deleting/ {print "    " $0}' | head -20
    printf "\n  To preserve them, run:\n"
    printf "    rsync -av '$SERVER:$SERVER_PATH/<file>' '$LOCAL_REPO/<file>'\n"
    printf "    git add, commit, push before proceeding with the staging deploy.\n"
  fi
  if [[ "$SEND_COUNT" -gt 500 ]]; then
    printf "\n  ${YELLOW}⚠ %s files would be replaced on the server. That's a big delta —${RESET}\n" "$SEND_COUNT"
    printf "  confirm this matches your expectation before the swap.\n"
  fi
fi

printf "\n"
printf "${BOLD}Probe complete.${RESET}\n"
if [[ "${DEL_COUNT:-0}" -gt 0 ]]; then
  printf "  ${YELLOW}Next step: recover server-only files to local commits.${RESET}\n"
  exit 0
else
  printf "  ${GREEN}No server-only files detected. Safe to proceed to Phase 2${RESET}\n"
  printf "  (Codex ruthless review).\n"
fi
