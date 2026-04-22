# Knowledge Atlas Server Control-Transfer Runbook

Date: 2026-04-21  
Audience: `dkirsh` on `xrlab`

## Purpose

This runbook moves Knowledge Atlas operations away from an accidental dependence on another person's service context and toward a cleaner model:

- `dkirsh` remains the practical deploy operator;
- production code becomes group-managed rather than person-managed;
- the auth service runs under a clear and intended account;
- runtime data remains writable in a way SQLite and routine deploys can tolerate.

## Why This Is Now Feasible

Your current `sudo -l` output includes:

```text
(root) ALL
```

So you do not need Tanishq to execute the root-owned parts. You can do them yourself.

## The Numbered Scripts

These live in:

- `/Users/davidusa/REPOS/Knowledge_Atlas/scripts/server_control_transfer/`

When the repo is present on `xrlab`, run them in this order.

### 1. Audit first

```bash
sudo bash scripts/server_control_transfer/01_audit_current_state.sh
```

This changes nothing. It reports:

- current service state
- current unit definition
- current ownership and group state
- your sudo rights

### 2. Prepare the shared deploy group

```bash
sudo bash scripts/server_control_transfer/02_prepare_shared_control.sh
```

Defaults:

- deploy group: `ka-deploy`
- primary operator: `dkirsh`
- legacy service user: `trathore`

If the legacy user differs, override it:

```bash
sudo LEGACY_SERVICE_USER=<actual-user> bash scripts/server_control_transfer/02_prepare_shared_control.sh
```

### 3. Align production and staging permissions

```bash
sudo bash scripts/server_control_transfer/03_align_tree_permissions.sh
```

This does three important things:

- makes production group-managed by `ka-deploy`
- preserves executable bits by using `chmod ... X`, not a blunt `664`
- makes staging owned by `dkirsh:ka-deploy`

### 4. Move `ka-auth.service` to the intended operator

```bash
sudo bash scripts/server_control_transfer/04_set_ka_auth_service_user.sh
```

This installs a systemd drop-in instead of rewriting the whole unit file. That is safer and easier to reverse.

Default effect:

- `User=dkirsh`
- `Group=ka-deploy`
- `SupplementaryGroups=ka-deploy`
- `WorkingDirectory=/var/www/xrlab/ka`

### 5. Verify the result

```bash
sudo bash scripts/server_control_transfer/05_verify_transfer.sh
```

This runs:

- service status
- unit inspection
- permission checks
- passwordless `nginx -t`
- passwordless `systemctl status ka-auth.service`
- the production smoke suite

## Recommended Execution Pattern

Do not run all five blindly as one shell chain. Run them one by one, in order. Inspect the output after each.

That is still much easier than an improvised migration, but it keeps the blast radius small.

## If The Repo Is Not Yet Updated On `xrlab`

From your server shell:

```bash
git -C /home/dkirsh/ka-staging-2026-04-20 pull --rebase --autostash origin master
```

Then either run the scripts from that checkout, or copy them to a temporary admin workspace.

## What This Runbook Deliberately Does Not Do

It does **not**:

- hand you ownership of all of `/var/www`
- rewrite `nginx` ownership
- grant `NOPASSWD: ALL`
- replace the full service unit when a drop-in is enough

Those would be coarser actions than the present problem requires.
