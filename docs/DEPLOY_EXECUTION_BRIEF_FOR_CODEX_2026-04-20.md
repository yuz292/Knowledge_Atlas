# Deploy execution brief — Codex (terminal + SSH authority) — 2026-04-20

*Date*: 2026-04-20
*Executor*: Codex (GPT-5.x) running from DK's Mac with terminal + SSH access to `dkirsh@xrlab.ucsd.edu`
*Owner of decision authority*: DK (approves Phase 7 swap; approves any destructive action outside the runbook)
*Supersedes*: the DK-executes version of Phase 3 onwards in `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md`
*Companion docs*:
  - `docs/STAGING_DEPLOYMENT_PLAN_2026-04-19.md` — the canonical nine-phase runbook; read this first
  - `docs/RUTHLESS_REVIEW_STATUS_2026-04-20.md` — confirms review verdict **CLEANED**
  - `docs/RELEASE_NOTES_2026-04-19.md` — what's in the release
  - `scripts/probe_server_diff.sh` — read-only server probe
  - `scripts/prep_for_push.sh` — one-command readiness check

---

## Why this brief exists

DK had intended to execute Phases 3–7 of the staging plan himself from his Mac. He is delegating that execution to Codex because Codex has both a terminal on DK's Mac (and therefore access to the repo and GitHub credentials via the credential helper) and SSH authority to `xrlab.ucsd.edu` as `dkirsh`. The review phase (Phase 2) is already complete and returned **CLEANED**; the local tree is nineteen commits ahead of `origin/master` and its working tree is clean.

This brief is written to be self-contained. Read it top-to-bottom, execute in order, pause where the brief tells you to pause. Do not skip gates.

## The one hard rule

**Phase 7 (the production symlink swap) is the only irreversible step and must not run without DK's explicit "go". Every other phase you can execute autonomously, but you must pause after Phase 6 and present your findings; DK says "swap" or "don't swap". Do not interpret silence as consent.**

Within that, the standard don't-be-destructive rules apply. Never run `rm -rf`, `git reset --hard`, `git push --force` anywhere on this run; if a recovery step calls for one, stop and ask DK.

---

## Pre-flight state (as of 2026-04-20, end of CW's session)

- Local repo clean; nineteen commits ahead of `origin/master` at tip `ee56f7e`.
- Contract tests pass (`pytest tests/test_journey_pages_contract.py -q` → `3 passed`).
- Validator clean at 0 errors, 106 warnings.
- Codex ruthless review returned **CLEANED** with three fixes landed at `77550b0`.
- Two rubric template stubs authored and committed at `ee56f7e`.
- Server probe ran earlier today per Codex's earlier review; re-run it in Phase 3 to confirm the server is still in the same state.

If your first check of `git log --oneline origin/master..HEAD | wc -l` returns a number other than nineteen, stop and ask DK — somebody else has either pushed or committed since this brief was written.

---

## Status file you maintain as you go

Create and incrementally update `docs/DEPLOY_EXECUTION_STATUS_2026-04-20.md`. Write one section per phase as you complete it, with: phase number, start time, end time, outputs quoted verbatim where relevant, verdict (`OK` / `WARN` / `BLOCKED` / `DK_APPROVAL_NEEDED`), next phase or next action. Commit this file after each phase completes so DK has a live trail he can follow.

The status file is the artefact by which DK audits what you did; terse is fine, invented is not. Quote command output rather than paraphrasing it.

---

## Phase 3 — Push to GitHub

Run from the Mac terminal in `/Users/davidusa/REPOS/Knowledge_Atlas`. The credential helper should already have DK's GitHub PAT cached.

```bash
cd /Users/davidusa/REPOS/Knowledge_Atlas

# Sanity checks that must all pass before pushing
git status                                                  # expect clean
git log --oneline origin/master..HEAD | wc -l               # expect 19
python3 scripts/site_validator.py | tail -3                 # expect 0 errors
python3 -m pytest tests/test_journey_pages_contract.py -q   # expect 3 passed
bash scripts/smoke_test_e2e.sh | tail -5                    # expect all green
bash scripts/probe_server_diff.sh                           # expect no new server-only hotfixes
```

If any of the above fails, stop and write the failure into the status file under a `BLOCKED` verdict; do not push until the failure is understood.

Then tag and push:

```bash
git tag -a v2026-04-20-staging ee56f7e \
    -m "Release candidate 2026-04-20 — T4 deliverables + journey pages + rubric templates"
git push origin master
git push origin v2026-04-20-staging
```

Also create a retroactive tag for yesterday's ruthless-review cleaned state, since the staging plan referenced it and it doesn't yet exist:

```bash
git tag -a v2026-04-19-staging 108d833 \
    -m "Pre-staging ruthless review CLEANED — 2026-04-19"
git push origin v2026-04-19-staging
```

**Go/no-go gate**: push succeeded (exit code 0) and `git ls-remote origin refs/heads/master` returns a SHA matching `ee56f7e`. Log both to the status file and proceed.

---

## Phase 4 — Clone to staging on xrlab

```bash
ssh dkirsh@xrlab.ucsd.edu
```

On xrlab:

```bash
# Confirm expected layout. If /var/www doesn't exist or isn't the right parent,
# STOP and ask DK for the correct parent path.
ls -la /var/www

cd /var/www

# Create the staging tree alongside production (name includes the release date)
git clone https://github.com/dkirsh/Knowledge_Atlas.git ka-staging-2026-04-20

cd ka-staging-2026-04-20

# Confirm it's the tagged release
git log --oneline -1            # expect ee56f7e
git describe --tags             # expect v2026-04-20-staging

# Install Python deps for the class-state backend (user-local, no sudo)
pip3 install --user fastapi uvicorn pydantic pyyaml httpx --break-system-packages
```

Apply the class-state migration (idempotent — safe to re-run):

```bash
python3 -c "
import sqlite3
con = sqlite3.connect('data/ka_auth.db')
con.executescript(open('scripts/migrations/2026-04-17_class_state.sql').read())
con.close()
print('staging migration applied')
"
python3 scripts/seed_class_state.py
```

**The admin token. Do not invent one on your own.** Ask DK: "what should the staging admin token be?" If DK says "generate one", run `openssl rand -hex 24` and show him the value before installing it. The value lives at `/etc/ka/admin_token.txt` with `0600` permissions and will require sudo:

```bash
sudo mkdir -p /etc/ka
printf '%s' "<the token DK approved>" | sudo tee /etc/ka/admin_token.txt >/dev/null
sudo chmod 600 /etc/ka/admin_token.txt
```

**Go/no-go gate**: clone succeeded, tag matches, migration applied without error, admin token in place. Log each check to status.

---

## Phase 5 — Wire staging into Apache

Edit the Apache config (the file is typically `/etc/apache2/sites-available/xrlab.ucsd.edu.conf` or similar; if a different name is obvious on the server, use that). Append this block inside the existing `<VirtualHost>` for xrlab:

```apache
# ── Knowledge Atlas staging (v2026-04-20-staging) ──
Alias /ka-staging /var/www/ka-staging-2026-04-20
<Directory /var/www/ka-staging-2026-04-20>
    Require all granted
    Options -Indexes +FollowSymLinks
    DirectoryIndex ka_home.html
</Directory>
ProxyPass        /ka-staging/api/admin/class  http://127.0.0.1:8081/api/admin/class
ProxyPassReverse /ka-staging/api/admin/class  http://127.0.0.1:8081/api/admin/class
```

Validate the config, then reload Apache:

```bash
sudo apache2ctl configtest      # expect "Syntax OK"
sudo systemctl reload apache2   # no output on success
```

Start the staging FastAPI on port 8081 (production uses 8080, so they don't collide):

```bash
cd /var/www/ka-staging-2026-04-20
nohup uvicorn scripts.ka_class_api:app --host 127.0.0.1 --port 8081 \
    >/var/log/ka-staging-api.log 2>&1 &
disown
sleep 2
curl -fsS http://127.0.0.1:8081/api/admin/class/health \
    -H "X-Admin-Token: <the staging token>" | head -5
```

**Go/no-go gate**: `configtest` returned `Syntax OK`, apache reloaded without error, FastAPI health endpoint returned JSON with `"ok": true`. Log the health JSON body to status verbatim.

---

## Phase 6 — Test staging

From your Mac (or anywhere with HTTPS access to xrlab), walk this checklist. For each step, record PASS / FAIL plus a one-line note. Do not skim; this is the step that decides whether the swap is safe.

1. `curl -sS https://xrlab.ucsd.edu/ka-staging/ka_home.html | head -80` — confirm the role-router markup is present and there are no obvious template placeholders (`${...}`).
2. Open `https://xrlab.ucsd.edu/ka-staging/ka_home.html` in a real browser; click each of the four role buttons; confirm each lands where the role router says it should.
3. `curl -sS https://xrlab.ucsd.edu/ka-staging/ka_topic_facet_view.html` — confirm it returns 200 and contains the progressive-disclosure mount point.
4. `curl -sS https://xrlab.ucsd.edu/ka-staging/ka_article_view.html?id=PDF-0007` — 200, and the article payload renders (visible title and abstract).
5. `curl -sS https://xrlab.ucsd.edu/ka-staging/160sp/ka_admin.html` — 200, and the auth gate is the visible content; the admin data must NOT render pre-auth. Visit in a real browser to confirm the gate.
6. `curl -sS https://xrlab.ucsd.edu/ka-staging/ka_journeys.html` — 200, all twelve journey links point to `ka_journey_*.html` paths that resolve.
7. Spot-check one journey page: `curl -sS https://xrlab.ucsd.edu/ka-staging/ka_journey_en.html | grep 'data-ka-active'` — expect `data-ka-active=""` (Codex's Probe 11a fix).
8. Walk one Track 4 deliverable page in a real browser: `https://xrlab.ucsd.edu/ka-staging/160sp/ka_t4_a_heuristic_audit.html`. Confirm the header strip, siblings row, section cards, and the workspace form all render; fill one text box and confirm `localStorage` saves (open DevTools → Application → Local Storage and look for `ka.t4a_draft`).
9. Exercise the mail system (the xrlab-specific integration DK named as the reason for staging). Trigger the forgot-password flow at `https://xrlab.ucsd.edu/ka-staging/ka_forgot_password.html` using the test address `dkirsh+kastage@gmail.com` (NOT a real student address). If an email arrives within 2 minutes, PASS. If the flow returns an error, capture the error and log FAIL; do not proceed to Phase 7 until DK has reviewed.
10. Confirm the class-state API is reachable through Apache:
    ```bash
    curl -H "X-Admin-Token: <staging-token>" \
         https://xrlab.ucsd.edu/ka-staging/api/admin/class/health
    ```
    Expected body includes `"ok": true` and the offering count from the seed.

After the ten checks, summarise in the status file:

```
Phase 6 results:
  1. PASS — role router present, no placeholder leaks
  2. PASS — all four role buttons route as specified
  ...
  9. PASS — mail arrived in 00:47
  10. PASS — {"ok": true, "db": "...", "offerings": 1}
Verdict: ALL PASS / N FAILS / DK_APPROVAL_NEEDED
```

**This is the check-in gate.** After writing the Phase 6 section to `DEPLOY_EXECUTION_STATUS_2026-04-20.md`, commit and push the status file, then stop. Post a short message along the lines of "Phase 6 complete — ALL PASS, awaiting DK go-ahead for Phase 7 swap" (or "FAILS on steps X, Y; staging copy is up but should not replace production"). Do not proceed to Phase 7 until DK types "swap" or equivalent. If any of steps 1–10 failed, you must not proceed to Phase 7 even if DK types "swap" — ask him to confirm he is overriding a failing check, and quote the failure back to him.

---

## Phase 7 — The swap (only after DK's explicit "go")

When DK has given the go-ahead:

```bash
ssh dkirsh@xrlab.ucsd.edu
cd /var/www

# Capture current prod state for rollback
ls -la ka                                    # log current symlink target
readlink ka > /tmp/ka_previous_target_$(date +%s)   # save atomically

# Retire current prod by renaming; this is the irreversible-ish step
# (reversal is easy but requires knowing the old target)
mv ka ka-prod-pre-2026-04-20

# Atomic flip
ln -s ka-staging-2026-04-20 ka

# Rotate the FastAPI: stop the old one on 8080, start the new one on 8080
pkill -f 'uvicorn.*8080' || true
sleep 2
cd /var/www/ka
nohup uvicorn scripts.ka_class_api:app --host 127.0.0.1 --port 8080 \
    >/var/log/ka-api.log 2>&1 &
disown
sleep 2
curl -fsS http://127.0.0.1:8080/api/admin/class/health \
    -H "X-Admin-Token: <the production token>" | head -5

# Reload Apache so the /ka alias picks up the new symlink
sudo systemctl reload apache2
```

Immediate post-swap verification (do these BEFORE considering the swap done):

```bash
curl -fsS https://xrlab.ucsd.edu/ka/ka_home.html | head -20
curl -fsS https://xrlab.ucsd.edu/ka/ka_topic_facet_view.html | head -20
curl -fsS https://xrlab.ucsd.edu/ka/ka_journeys.html | head -10
curl -fsS https://xrlab.ucsd.edu/ka/160sp/ka_t4_a_heuristic_audit.html | head -10
curl -fsS https://xrlab.ucsd.edu/ka/api/admin/class/health \
    -H "X-Admin-Token: <production token>"
```

If any of these post-swap checks returns a non-200 or an unexpected body, **initiate rollback immediately** (Phase 8 below). Don't wait.

If everything is 200 and the bodies look right, write a Phase 7 success section to the status file with timestamps and the verified URLs. Post the completion message to DK: "Phase 7 complete — production now serves v2026-04-20-staging. Rollback directory: ka-prod-pre-2026-04-20. Rollback cutoff: 48h."

---

## Phase 8 — Rollback (only if needed)

```bash
ssh dkirsh@xrlab.ucsd.edu
cd /var/www

pkill -f 'uvicorn.*8080' || true
rm ka
ln -s ka-prod-pre-2026-04-20 ka
cd /var/www/ka
# Restart the old API using whatever command it was using before; if unknown,
# check /var/log/ka-api.log for recent start lines, or ask DK.
nohup uvicorn scripts.ka_class_api:app --host 127.0.0.1 --port 8080 \
    >/var/log/ka-api.log 2>&1 &
disown
sudo systemctl reload apache2

# Verify rollback
curl -fsS https://xrlab.ucsd.edu/ka/ka_home.html | head -10
```

Write a Phase 8 section explaining what triggered rollback, what commands ran, and what the post-rollback state looks like. Do not proceed to any further phase; DK will decide next steps.

---

## Phase 9 — Clean up (do NOT run unless DK explicitly asks; earliest one week after the swap)

The cleanup phase deletes `ka-staging-2026-04-20` (by then it's the same tree as `ka`), archives `ka-prod-pre-2026-04-20` to the 5 TB backup disk, and removes the `/ka-staging` Apache alias. These are destructive or semi-destructive actions; Codex must not execute Phase 9 autonomously. Wait for DK to say "clean up staging" at least seven days after Phase 7.

---

## Safety rules that govern every phase

1. **No `rm -rf`** anywhere. If a step says to remove a directory, do it with a move (`mv ... /tmp/retired_$(date +%s)_$(basename ...)`) and let DK or a later cleanup delete once confirmed unneeded.
2. **No `git push --force`** under any circumstances. If a push is rejected, run `git fetch && git status` to see the divergence and ask DK.
3. **No secrets in the status file.** The admin tokens, DK's PAT, his SSH private key, any API keys — none of them go into `DEPLOY_EXECUTION_STATUS_2026-04-20.md` and none of them get echoed in a command output you paste. If a command's output contains a token, redact it to `<REDACTED>` before logging.
4. **No student data in logs.** If Phase 6 step 9 (mail test) surfaces anything that looks like a student email or a real PID, stop and redact before pasting.
5. **No Phase 7 without DK's "go".** Already stated. Worth repeating.
6. **No Apache restarts on production** that are not part of the runbook. An errant `systemctl restart` during working hours on xrlab can interrupt unrelated services; prefer `reload` and do it only when the runbook prescribes.
7. **Log before you act.** Write the planned command to status, then run it, then log the output. This is the audit trail.

## Escalation — when to stop and ask DK

Stop and ask, don't guess, in any of these situations:

- `/var/www` isn't the staging parent (layout has changed).
- `sudo` prompts for a password you don't have.
- A Phase 5 Apache change doesn't pass `configtest`.
- A Phase 6 check fails and the failure is not obviously fixable by retry.
- The mail system test (Phase 6 step 9) hangs for > 2 minutes.
- A path in the runbook doesn't match what you see on the server.
- You run into any permission-denied error on xrlab paths where sudo shouldn't have been needed.
- At any point a command's output contains something that looks like it might be a secret being exposed.

When you ask DK, post the question to the status file under a `### DK decision needed` heading, commit, push, and say so in a plain sentence — not a wall of text.

## Completion criteria

The deploy is done when:

- `docs/DEPLOY_EXECUTION_STATUS_2026-04-20.md` has sections for Phases 3 through 7, each marked `OK`, with timestamps, quoted outputs, and the post-swap verification URLs returning 200.
- `https://xrlab.ucsd.edu/ka/ka_home.html` returns the v2026-04-20-staging content.
- `https://xrlab.ucsd.edu/ka/ka_journeys.html` and `https://xrlab.ucsd.edu/ka/160sp/ka_t4_a_heuristic_audit.html` both load cleanly.
- The rollback directory `/var/www/ka-prod-pre-2026-04-20` exists and is intact.
- The final message you post to DK says: "Staging deploy complete. v2026-04-20-staging live on /ka. Rollback available for 48h at ka-prod-pre-2026-04-20."

That is the end of this brief. If you get there, everything CW wanted DK to do has been done.
