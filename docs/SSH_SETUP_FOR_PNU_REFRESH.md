# SSH setup for the "Refresh PNUs from local" admin button

**Date**: 2026-04-17
**Purpose**: Configuration steps so the admin button on `ka_admin.html` can
safely trigger a PNU manifest refresh on the instructor's Mac.
**Prerequisite**: `ka_admin_refresh_endpoint.py` deployed on the web server,
`refresh_pnus_from_local.sh` present on the Mac.

---

## 1. The flow in one picture

```
┌──────────────────┐    POST /api/admin/refresh-pnus     ┌────────────────────────────┐
│  Admin browser   │───────────────────────────────────▶│  Web server                │
│  ka_admin.html   │                                    │  xrlab.ucsd.edu            │
└──────────────────┘                                    │                            │
       ▲                                                │  1. auth the admin session │
       │   toast: "71 mechanisms, 54 full"              │  2. rate-limit (20s)       │
       │                                                │  3. ssh -i KEY user@MAC    │
       │                                                └────────────┬───────────────┘
       │                                                             │ forced-command SSH
       │                                                             │ (nothing else possible)
       │                                                             ▼
       │                                           ┌─────────────────────────────────┐
       │                                           │  DK's Mac                       │
       │                                           │  ~/REPOS/Knowledge_Atlas/       │
       │                                           │   └── scripts/                  │
       │                                           │        └── refresh_pnus_from_local.sh
       │                                           │              │                  │
       │                                           │              ▼                  │
       │                                           │   python3 scripts/              │
       │                                           │    regenerate_pnus_json.py      │
       │                                           │              │                  │
       │                                           │              ▼                  │
       │                                           │   cat data/ka_payloads/         │
       │                                           │         pnus.json               │
       │                                           └───────────┬─────────────────────┘
       │                                                       │ stdout over SSH
       │                                                       ▼
       │                          ┌────────────────────────────────────────────┐
       │                          │  Web server: write received JSON into      │
       └──────────────────────────│  /var/www/xrlab/ka/data/ka_payloads/       │
                                  │  pnus.json — return {ok, summary, bytes}   │
                                  └────────────────────────────────────────────┘
```

The Mac never accepts commands from the server except this one forced command.
The server never pushes data to the Mac.

---

## 2. On the Mac (DK's laptop) — one-time setup

### 2.1 Enable SSH (System Settings → General → Sharing → Remote Login: ON)

Note the hostname shown there (e.g. `dkirshs-MacBook-Pro.local`). If you
want the server to reach the Mac from off-campus, set up **Tailscale**
(easiest) or **dynamic DNS**; a LAN-only setup is fine for on-campus.

### 2.2 Create a dedicated low-privilege user OR use your own account

Either is acceptable. A dedicated user is cleaner. This doc uses the
account `davidusa` (your own account) for simplicity; substitute the name
you choose throughout.

### 2.3 Generate a new SSH key pair for this purpose only

On the **web server** (NOT on the Mac):

```bash
sudo mkdir -p /etc/ka
sudo ssh-keygen -t ed25519 -f /etc/ka/ka_refresh_key -C "ka-refresh@xrlab.ucsd.edu" -N ""
sudo chown www-data:www-data /etc/ka/ka_refresh_key
sudo chmod 0600 /etc/ka/ka_refresh_key
sudo cat /etc/ka/ka_refresh_key.pub
# → copy the public key for the next step
```

### 2.4 Add the key to the Mac's authorized_keys with a FORCED COMMAND

On the **Mac**:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Now edit `~/.ssh/authorized_keys` and add ONE line that looks exactly like
this (replace `ssh-ed25519 AAAA...` with the public key from step 2.3):

```
command="/Users/davidusa/REPOS/Knowledge_Atlas/scripts/refresh_pnus_from_local.sh",no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-pty,from="xrlab.ucsd.edu" ssh-ed25519 AAAA... ka-refresh@xrlab.ucsd.edu
```

**Every option matters:**
- `command="..."` — the ONLY command this key can invoke. Anything the
  server tries to send is discarded; this script runs instead.
- `no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-pty` — the
  key cannot tunnel traffic, reuse your agent, open an X11 window, or get
  an interactive shell.
- `from="xrlab.ucsd.edu"` — the key only works when the incoming
  connection's reverse DNS matches. Replace with the server's actual
  hostname or IP range.

### 2.5 Make the script executable

```bash
chmod +x ~/REPOS/Knowledge_Atlas/scripts/refresh_pnus_from_local.sh
```

### 2.6 Test locally

```bash
~/REPOS/Knowledge_Atlas/scripts/refresh_pnus_from_local.sh | head -3
# should print the first lines of the JSON manifest
```

---

## 3. On the web server — one-time setup

### 3.1 Install dependencies

```bash
sudo apt install openssh-client python3-pip
pip3 install --break-system-packages fastapi uvicorn
```

### 3.2 Configure env vars for the endpoint

Create `/etc/ka/refresh.env`:

```
KA_REFRESH_HOST=dkirshs-MacBook-Pro.local   # or tailscale hostname
KA_REFRESH_USER=davidusa
KA_REFRESH_KEY=/etc/ka/ka_refresh_key
KA_TARGET_JSON=/var/www/xrlab/ka/data/ka_payloads/pnus.json
KA_ADMIN_TOKEN=<long-random-hex; share with the admin UI>
KA_SSH_TIMEOUT=30
```

### 3.3 Systemd service

`/etc/systemd/system/ka-admin-refresh.service`:

```ini
[Unit]
Description=KA admin refresh endpoint (SSH-driven PNU refresh)
After=network-online.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/xrlab/ka
EnvironmentFile=/etc/ka/refresh.env
ExecStart=/usr/bin/python3 -m uvicorn scripts.ka_admin_refresh_endpoint:app \
    --host 127.0.0.1 --port 8781
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ka-admin-refresh
```

### 3.4 Reverse-proxy in nginx

Inside your existing `xrlab.ucsd.edu` server block, add:

```nginx
location /api/admin/ {
    proxy_pass http://127.0.0.1:8781;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### 3.5 Smoke-test from the server's shell

```bash
sudo -u www-data ssh -i /etc/ka/ka_refresh_key davidusa@dkirshs-MacBook-Pro.local | python3 -c 'import json,sys; m=json.load(sys.stdin); print(m["summary"])'
```

You should see something like:
`{'total': 71, 'framework_count': 15, ...}`

If it prompts for a password or fails, re-check steps 2.3, 2.4, and 3.2.

### 3.6 End-to-end test from the admin UI

Open `https://xrlab.ucsd.edu/ka/160sp/ka_admin.html`, sign in, click the
"⟳ Refresh PNUs from local Mac" button. The toast should show `71
mechanisms, 54 full / 11 brief / 6 stub` within five seconds.

---

## 4. What the security model guarantees

- The web server can only invoke **one specific script** on the Mac. It
  cannot read files, push files, run shells, or execute arbitrary code.
- The script accepts **no arguments or stdin**; the server cannot alter
  its behaviour.
- If the Mac is unreachable (asleep, off-network), the button fails
  gracefully and nothing on the server changes — the previous manifest
  stays in place.
- Every successful call is **logged on both sides**:
  - Mac: `~/Library/Logs/ka_refresh_pnus.log`
  - Server: `journalctl -u ka-admin-refresh`
- Failed calls are recorded in the admin-console audit log
  (`pnus.refresh.fail` events) for 365 days.

---

## 5. Fallbacks

If SSH is unavailable (e.g. you're travelling and your Mac isn't
reachable), the weekly scheduled task already runs the same generator
locally once a week, so the site never goes fully stale. You can also run
the script manually by hand:

```bash
cd ~/REPOS/Knowledge_Atlas && python3 scripts/regenerate_pnus_json.py
git add data/ka_payloads/pnus.json && git commit -m "manual PNU refresh"
git push
```

---

## 6. Off-switch

If you ever want to disable the refresh button globally:

```bash
sudo systemctl stop ka-admin-refresh
sudo systemctl disable ka-admin-refresh
```

The button on the admin page will then receive a 502 and display a clear
error toast. No secrets are exposed by disabling the service.
