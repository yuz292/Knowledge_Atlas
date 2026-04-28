# Codex Prompt — install atlas_shared into xrlab KA envs, then stage and promote

You are Codex on `xrlab`. Your task is to finish the `atlas_shared` deployment
for Knowledge Atlas and then run the normal staging and production gates.

## Ground truth you must respect

1. The Knowledge Atlas documentation update is already on `master` at commit:
   - `dd6d076` — `Document atlas_shared intake usage for Track 2`

2. The upstream `atlas_shared` cleanup is on GitHub as:
   - repo: `https://github.com/dkirsh/atlas_shared`
   - branch: `cleanup-sprint-2026-04-21`
   - PR: `https://github.com/dkirsh/atlas_shared/pull/1`

3. The live `xrlab` server does **not** currently have `atlas_shared` installed in
   either of these places:
   - `/home/dkirsh/atlas_shared`
   - `/var/www/xrlab/atlas_shared`

4. Therefore the necessary edit is **not** “pull a sibling checkout only”.
   The necessary edit is:
   - create or update a local checkout of `atlas_shared`
   - install it into the staging and production KA virtual environments
   - restart the production auth service so the running Python process sees it

5. Do not vendor `atlas_shared` into the Knowledge Atlas repo.

## Phase 1 — choose the atlas_shared ref

If PR 1 has already been merged, use:

```bash
ATLAS_SHARED_REF=main
```

If it has **not** been merged yet, use:

```bash
ATLAS_SHARED_REF=cleanup-sprint-2026-04-21
```

## Phase 2 — create or update the shared checkout

Run:

```bash
set -euo pipefail

ATLAS_SHARED_REF="${ATLAS_SHARED_REF:-main}"

if [ ! -d /home/dkirsh/atlas_shared/.git ]; then
  git clone https://github.com/dkirsh/atlas_shared.git /home/dkirsh/atlas_shared
fi

git -C /home/dkirsh/atlas_shared fetch origin
git -C /home/dkirsh/atlas_shared checkout "$ATLAS_SHARED_REF"
git -C /home/dkirsh/atlas_shared pull --ff-only origin "$ATLAS_SHARED_REF"
git -C /home/dkirsh/atlas_shared rev-parse --short HEAD
```

## Phase 3 — install atlas_shared into both KA virtualenvs

Run:

```bash
/home/dkirsh/ka-staging-2026-04-20/.venv/bin/pip install -e /home/dkirsh/atlas_shared
/var/www/xrlab/ka/.venv/bin/pip install -e /home/dkirsh/atlas_shared
```

Then verify:

```bash
/home/dkirsh/ka-staging-2026-04-20/.venv/bin/python -c "import atlas_shared; print(atlas_shared.__version__)"
/var/www/xrlab/ka/.venv/bin/python -c "import atlas_shared; print(atlas_shared.__version__)"
```

Expected:
- both print `0.3.0`

## Phase 4 — update staging Knowledge Atlas and run the staging gate

Run:

```bash
git -C /home/dkirsh/ka-staging-2026-04-20 pull --rebase --autostash origin master
cd /home/dkirsh/ka-staging-2026-04-20
bash scripts/server_release_cycle.sh staging
```

## Phase 5 — promote to production and restart the auth service

Run:

```bash
cd /home/dkirsh/ka-staging-2026-04-20
bash scripts/server_release_cycle.sh promote
sudo /bin/systemctl restart ka-auth.service
sudo /bin/systemctl status ka-auth.service --no-pager | sed -n '1,20p'
```

Expected:
- `Active: active (running)`

## Phase 6 — run production verification

Run:

```bash
cd /var/www/xrlab/ka
bash scripts/run_site_runtime_smoke.sh production
python3 scripts/server_verify_served_tree.py --profile production --repo-root /var/www/xrlab/ka
```

Then verify that the running env can import the shared package:

```bash
/var/www/xrlab/ka/.venv/bin/python -c "import atlas_shared; print(atlas_shared.__version__)"
```

## Phase 7 — verify the Track 2 documentation landed

Run:

```bash
curl -s https://xrlab.ucsd.edu/ka/160sp/ka_track2_hub.html | grep -c 'ka_track2_resources.html#atlas-shared-module'
curl -s https://xrlab.ucsd.edu/ka/160sp/ka_track2_resources.html | grep -c 'ATLAS_SHARED_TRACK2_INTAKE_CHEAT_SHEET_2026-04-22.md'
```

Expected:
- both counts are `1` or higher

## Output format

Report:

- the atlas_shared ref used
- the installed atlas_shared version in staging and production
- staging smoke result
- production smoke result
- whether `ka-auth.service` restarted cleanly
- whether the Track 2 hub and resources page both show the new atlas_shared intake guidance

If anything fails, stop at the failing step and report the exact command and output. Do not improvise around the failure.
