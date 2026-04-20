# Staging deployment — end-to-end runbook

*Date*: 2026-04-19
*Owner*: DK executes; CW prepared
*Supersedes*: any ad-hoc deploy notes from prior pushes
*Related artefacts*: `docs/RUTHLESS_REVIEW_BRIEF_FOR_CODEX_2026-04-19.md`, `docs/RELEASE_NOTES_2026-04-19.md`, `scripts/probe_server_diff.sh`

---

## The shape of the deploy

The production site lives at `xrlab.ucsd.edu/ka/...` and is many versions behind the tip of `master`. The local development repo has landed substantial new work: the class-state database backend, the rubric and AI-grading system, the per-persona variants, the five topic-page variants, the classifier audit, the persona-audit report, the strategic panels thinking. Pushing straight to production would be reckless because no integration test has run against the xrlab environment (its SMTP, its DNS, its Apache configuration).

The safe path is **stage first, swap second, keep the previous dir for rollback**. The staging copy on xrlab lives in a parallel directory to production, serves on a parallel URL path (`/ka-staging/` or a separate port), and gets tested against the xrlab-specific integrations (mail, real-domain links, any reverse proxy). Once the staging copy is green, an atomic symlink flip replaces production.

Two principles we hold throughout:

- **GitHub is the canonical tip.** All deploys pull from GitHub. No direct edits on the server that don't round-trip back through git.
- **The symlink is the deploy unit.** A deploy is a symlink flip, not a file overwrite. This makes rollback one command.

---

## Phase 0 — Pre-push prep (CW does this; mostly already done)

CW prepares the release candidate by ensuring:

- The local repo is clean (`git status` shows no uncommitted changes that belong in the release).
- The site validator reports 0 errors (`python3 scripts/site_validator.py`).
- The end-to-end smoke test passes (`bash scripts/smoke_test_e2e.sh`).
- A release notes doc exists at `docs/RELEASE_NOTES_2026-04-19.md`.
- A ruthless-review brief exists at `docs/RUTHLESS_REVIEW_BRIEF_FOR_CODEX_2026-04-19.md` for Codex to pick up.
- The server-diff probe script exists at `scripts/probe_server_diff.sh`.

**Status as of 2026-04-19**: validator 0 errors, 176 warns. Smoke test: 11 stages passing against a throwaway DB. 10 commits ahead of origin/master.

---

## Phase 1 — Probe the server (DK does this; read-only)

Before anything ships, DK runs the probe script from his Mac to answer three questions: (a) is the server reachable and has its basic layout changed; (b) are there any files on xrlab that differ from our github tip (hotfixes or stale state); (c) how many files are in the current production tree so we know what a clone will replace.

```bash
cd /Users/davidusa/REPOS/Knowledge_Atlas
bash scripts/probe_server_diff.sh
```

Expected output: a summary table of file counts, a list of any files on the server that differ from our `origin/master` tip, and a go/no-go signal.

If the probe surfaces hotfixes on xrlab that are not in git, those must be captured as commits *before* Phase 4. Skipping this step risks overwriting live work.

---

## Phase 2 — Ruthless review (Codex executes)

DK sends Codex the path to `docs/RUTHLESS_REVIEW_BRIEF_FOR_CODEX_2026-04-19.md`. The brief structures the review as nine targeted probes (broken links, unauthenticated admin paths, persona-awareness regressions, copy contradictions, validator warnings above threshold, mobile breakage, dead code, payload staleness, security leaks). Codex lands any fixes as commits on `master` — each commit attributed to Codex per the coworker-boundaries rule.

Codex signals completion by writing a one-paragraph status note to `docs/RUTHLESS_REVIEW_STATUS_2026-04-19.md` with the verdict: *clean*, *cleaned with N fixes*, or *blocked on decision X*.

---

## Phase 3 — Push to GitHub (DK executes on Mac)

After Codex has signalled completion:

```bash
cd /Users/davidusa/REPOS/Knowledge_Atlas

# Final sanity check
git status                    # should be clean
git log --oneline origin/master..HEAD | wc -l    # how many commits are about to land
python3 scripts/site_validator.py | tail -3     # should still show 0 errors
bash scripts/smoke_test_e2e.sh                  # all 11 stages green

# Tag the release before pushing so rollback has a named target
git tag -a v2026-04-19-staging -m "Release candidate 2026-04-19 — staging deploy"

# Push the commits and the tag
git push origin master
git push origin v2026-04-19-staging
```

If the push fails on auth, see `docs/SHIBBOLETH_INTERIM_NOTE_2026-04-18.md` for the PAT approach; the simpler path is to use a credential-helper-equipped terminal on the Mac.

---

## Phase 4 — Clone to staging on xrlab (DK executes via SSH)

```bash
ssh dkirsh@xrlab.ucsd.edu

# Create the staging tree alongside (not replacing) production
cd /var/www                             # adjust path if different on xrlab
git clone https://github.com/dkirsh/Knowledge_Atlas.git ka-staging-2026-04-19

# Verify it's the tagged release
cd ka-staging-2026-04-19
git log --oneline -1                    # should show the v2026-04-19-staging commit
git describe --tags                     # should print v2026-04-19-staging

# Install Python dependencies needed for the class-state backend
pip3 install --user fastapi uvicorn pydantic pyyaml httpx --break-system-packages

# Apply the class-state migration (idempotent; creates tables if absent)
python3 -c "
import sqlite3
con = sqlite3.connect('data/ka_auth.db')
con.executescript(open('scripts/migrations/2026-04-17_class_state.sql').read())
con.close()
print('staging migration applied')
"

# Seed the class state (adds demo offering + deliverables; safe to re-run)
python3 scripts/seed_class_state.py

# Set the admin token for the staging backend
sudo mkdir -p /etc/ka
echo "<pick-a-staging-token>" | sudo tee /etc/ka/admin_token.txt
sudo chmod 600 /etc/ka/admin_token.txt
```

---

## Phase 5 — Wire staging into Apache (DK executes)

The staging site needs a URL path or a parallel vhost. The simplest option is a path prefix, e.g. `xrlab.ucsd.edu/ka-staging/...`, served from the new directory. In the Apache config for xrlab:

```apache
Alias /ka-staging /var/www/ka-staging-2026-04-19
<Directory /var/www/ka-staging-2026-04-19>
    Require all granted
    Options -Indexes +FollowSymLinks
    DirectoryIndex ka_home.html
</Directory>

# If the class-state FastAPI backend runs behind the same Apache:
ProxyPass        /ka-staging/api/admin/class  http://127.0.0.1:8081/api/admin/class
ProxyPassReverse /ka-staging/api/admin/class  http://127.0.0.1:8081/api/admin/class
```

Note the port `8081` for the staging FastAPI (production uses `8080`, so they don't collide). Start it:

```bash
cd /var/www/ka-staging-2026-04-19
nohup uvicorn scripts.ka_class_api:app --host 127.0.0.1 --port 8081 \
    >/var/log/ka-staging-api.log 2>&1 &
```

Reload Apache: `sudo systemctl reload apache2`.

---

## Phase 6 — Test staging (DK executes; CW provides the checklist)

1. Open `https://xrlab.ucsd.edu/ka-staging/ka_home.html` — confirm the role router renders and each of the four buttons lands on a sensible page.
2. Open `ka-staging/ka_topic_facet_view.html` — confirm the progressive-disclosure browser loads the crosswalk.
3. Open `ka-staging/ka_article_view.html?id=PDF-0007` — confirm a full paper record renders.
4. Open `ka-staging/160sp/ka_admin.html` — confirm the auth gate blocks you until you sign in with the staging token.
5. Exercise the mail system: try the forgot-password flow on staging (`ka-staging/ka_forgot_password.html`) and confirm the SMTP path works or fails cleanly with a useful error. This is the xrlab-specific integration DK named as the reason for staging.
6. Confirm the class-state API responds:
   ```
   curl -H "X-Admin-Token: <staging-token>" \
        https://xrlab.ucsd.edu/ka-staging/api/admin/class/health
   ```
   Expected: `{"ok": true, "db": "...", "offerings": 1}`.
7. Walk the audit's top-ten findings against the staging copy — each should now be addressed.

If any step fails, fix, re-push, re-clone staging (or `git pull` inside staging).

---

## Phase 7 — The swap (DK executes; atomic)

Only run this once Phase 6 is fully green.

```bash
ssh dkirsh@xrlab.ucsd.edu
cd /var/www

# Save a pointer to the current prod for quick rollback
ls -la ka                               # note what ka currently points at
mv ka ka-prod-pre-2026-04-19            # retire current prod by renaming

# Atomic flip: point ka at the staging tree
ln -s ka-staging-2026-04-19 ka

# Stop the old FastAPI, swap its port to 8080, start from the new tree
pkill -f 'uvicorn.*8080' || true        # if production API was on 8080
cd /var/www/ka
nohup uvicorn scripts.ka_class_api:app --host 127.0.0.1 --port 8080 \
    >/var/log/ka-api.log 2>&1 &

# Reload Apache so the alias picks up the new symlink target
sudo systemctl reload apache2
```

Verify: `https://xrlab.ucsd.edu/ka/ka_home.html` now shows the new home.

---

## Phase 8 — Rollback (if needed, any time in first 48h)

```bash
ssh dkirsh@xrlab.ucsd.edu
cd /var/www

# Stop the new API, flip the symlink back, restart the old API
pkill -f 'uvicorn.*8080' || true
rm ka
ln -s ka-prod-pre-2026-04-19 ka
# Restart Apache and the old API at whatever port/start command it used before
sudo systemctl reload apache2
```

The rollback directory `ka-prod-pre-2026-04-19` is retained for at least two weeks after the swap, then archived to the 5 TB disk per `docs/END_OF_QUARTER_WORKFLOW_2026-04-18.md`.

---

## Phase 9 — Clean up (one week after swap, if no rollback)

- Remove `ka-staging-2026-04-19` (it's now the same tree as `ka`).
- Delete the `/etc/apache2` staging alias (Phase 5).
- Archive `ka-prod-pre-2026-04-19` to the 5 TB backup; keep a git tag `v2026-04-19-pre-swap-snapshot` so the state is reconstructable from git plus archived files.

---

## What can go wrong, and what we can do about it

| Failure mode | Detection | Fix |
|---|---|---|
| `git push` rejected (non-fast-forward) | push output shows `rejected` | `git fetch origin && git rebase origin/master`; resolve any conflicts; re-push |
| Server `git clone` fails on auth | SSH session output | Use a deploy key on the xrlab user; add the public key to `github.com/dkirsh/Knowledge_Atlas` deploy keys |
| Migration errors on staging | Python traceback | Copy the trace to a new file `docs/staging_migration_error_2026-04-19.md`; do not proceed with the swap; fix locally and re-push |
| FastAPI backend doesn't start | `tail /var/log/ka-staging-api.log` | Usually a missing dep or a port conflict; `pip3 install` the missing dep, or change the port and update the Apache ProxyPass |
| Mail system integration broken | Phase 6 step 5 fails | File it as a P1 bug; fix locally; re-push; re-stage; do NOT swap production |
| Staging OK but swap makes production 500 | `curl ka_home.html` post-swap | Immediate rollback per Phase 8 |

---

## What CW does not do

- SSH to xrlab (no credentials in the Cowork environment).
- Push to GitHub (no credentials).
- Restart Apache or FastAPI on xrlab.
- Swap the production symlink.

CW prepares the repo, writes the runbook, writes the release notes, writes the Codex ruthless-review brief, maintains the smoke test and validator. DK executes the deployment.
