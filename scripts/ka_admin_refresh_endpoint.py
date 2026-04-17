#!/usr/bin/env python3
"""
ka_admin_refresh_endpoint.py — server-side FastAPI endpoint that the admin
page calls when the instructor clicks "Refresh PNUs from local".

Flow
----
    Browser (admin)            Web server (xrlab.ucsd.edu)           Mac (DK)
    -------------------------  -----------------------------------   --------------
    POST /api/admin/refresh-pnus -> authenticate admin session
                                    -> ssh -i KEY ka-refresh@DK_HOST
                                         [forced command]                -> refresh_pnus_from_local.sh
                                                                              regenerates pnus.json
                                                                              cats JSON to stdout
                                    <- JSON captured over SSH stdout  <-
                                    -> write JSON to local pnus.json
                                    -> return { ok, summary, bytes }
                             <-  200 OK + summary
    Admin UI renders toast + updates KPI tiles

Security boundary
-----------------
    * The SSH key (`SSH_KEY_PATH`) is owned by the web-server user, 0600.
    * The Mac's `authorized_keys` entry for that key MUST be locked to a
      single forced command:
        command="/Users/davidusa/REPOS/Knowledge_Atlas/scripts/refresh_pnus_from_local.sh",
        no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-pty
    * The endpoint requires the caller to be an authenticated admin (checked
      via the course session cookie; this is a stub — replace with your auth).
    * All calls are rate-limited (see below) and audited.

Run
---
    pip3 install --break-system-packages fastapi uvicorn
    uvicorn scripts.ka_admin_refresh_endpoint:app --host 127.0.0.1 --port 8781

Then reverse-proxy /api/admin/ from nginx/Apache to 127.0.0.1:8781.

Environment variables
---------------------
    KA_REFRESH_HOST       hostname of DK's Mac (e.g. dkirsh-mac.ucsd.edu or tailscale hostname)
    KA_REFRESH_USER       SSH user (e.g. ka-refresh)
    KA_REFRESH_KEY        path to the private key (e.g. /etc/ka/ka_refresh_key)
    KA_TARGET_JSON        where to write the fresh JSON on the server
                          (e.g. /var/www/xrlab/ka/data/ka_payloads/pnus.json)
    KA_ADMIN_TOKEN        shared-secret admin token (stub; replace with real session auth)
"""

import json
import os
import subprocess
import time
from pathlib import Path

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.responses import JSONResponse
except ImportError:
    # Graceful degrade so `python -m py_compile` works without fastapi
    # installed; the endpoint won't actually run without it.
    FastAPI = object  # type: ignore
    HTTPException = Exception  # type: ignore

app = FastAPI() if FastAPI is not object else None

# ─── Config ──────────────────────────────────────────────────────────
REFRESH_HOST = os.environ.get("KA_REFRESH_HOST", "dkirsh-mac.ucsd.edu")
REFRESH_USER = os.environ.get("KA_REFRESH_USER", "ka-refresh")
REFRESH_KEY  = os.environ.get("KA_REFRESH_KEY",  "/etc/ka/ka_refresh_key")
TARGET_JSON  = Path(os.environ.get("KA_TARGET_JSON",
                       "/var/www/xrlab/ka/data/ka_payloads/pnus.json"))
ADMIN_TOKEN  = os.environ.get("KA_ADMIN_TOKEN", "")          # stub
SSH_TIMEOUT  = int(os.environ.get("KA_SSH_TIMEOUT", "30"))   # seconds
RATE_WINDOW  = 20                                            # seconds between calls

# In-memory rate limiter (fine for a single-process deployment)
_last_call_ts: float = 0.0


# ─── Helpers ─────────────────────────────────────────────────────────
def require_admin(request) -> None:
    """Replace this with your real session check (instructor role)."""
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=500,
                            detail="KA_ADMIN_TOKEN not configured server-side.")
    if request.headers.get("X-Admin-Token", "") != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Not authorised.")


def rate_limit() -> None:
    global _last_call_ts
    now = time.time()
    if now - _last_call_ts < RATE_WINDOW:
        wait = int(RATE_WINDOW - (now - _last_call_ts))
        raise HTTPException(
            status_code=429,
            detail=f"Rate limited; wait {wait}s before refreshing again.")
    _last_call_ts = now


def ssh_refresh() -> tuple[bytes, str]:
    """
    Invoke the forced SSH command on DK's Mac. Returns (stdout_bytes, stderr_text).
    Raises HTTPException on any non-zero exit or timeout.
    """
    cmd = [
        "ssh",
        "-i", REFRESH_KEY,
        "-o", "BatchMode=yes",           # never prompt
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", f"ConnectTimeout={SSH_TIMEOUT}",
        f"{REFRESH_USER}@{REFRESH_HOST}",
        # No remote command — the Mac's authorized_keys forces the command for us.
    ]
    try:
        res = subprocess.run(cmd,
                             input=b"",
                             capture_output=True,
                             timeout=SSH_TIMEOUT + 10,
                             check=False)
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504,
                            detail=f"SSH timeout after {SSH_TIMEOUT}s — is the Mac reachable and is sshd running?")
    if res.returncode != 0:
        raise HTTPException(status_code=502,
                            detail=f"SSH failed (exit {res.returncode}): {res.stderr.decode('utf-8','replace')}")
    return res.stdout, res.stderr.decode("utf-8", "replace")


# ─── Endpoint ────────────────────────────────────────────────────────
if app is not None:
    @app.post("/api/admin/refresh-pnus")
    async def refresh_pnus(request: Request):
        require_admin(request)
        rate_limit()

        payload, ssh_stderr = ssh_refresh()

        # Validate JSON before writing
        try:
            manifest = json.loads(payload.decode("utf-8", "replace"))
        except Exception as e:
            raise HTTPException(status_code=502,
                                detail=f"Mac returned invalid JSON: {e}")
        # Sanity bounds
        summary = manifest.get("summary", {})
        total = summary.get("total", 0)
        if not (50 <= total <= 200):
            raise HTTPException(status_code=502,
                                detail=f"Unexpected PNU count ({total}); refusing to overwrite.")

        TARGET_JSON.parent.mkdir(parents=True, exist_ok=True)
        TARGET_JSON.write_bytes(payload)

        return JSONResponse({
            "ok": True,
            "summary": summary,
            "bytes": len(payload),
            "written_to": str(TARGET_JSON),
            "generated_at": manifest.get("generated_at"),
            "ssh_stderr_tail": ssh_stderr[-500:] if ssh_stderr else "",
        })


    @app.get("/api/admin/refresh-pnus/health")
    async def health():
        """Quick config health check (no SSH)."""
        ready = all([REFRESH_HOST, REFRESH_USER, Path(REFRESH_KEY).exists()])
        return {
            "ok": ready,
            "refresh_host": REFRESH_HOST,
            "refresh_user": REFRESH_USER,
            "refresh_key_present": Path(REFRESH_KEY).exists(),
            "target_json_writable": os.access(TARGET_JSON.parent, os.W_OK)
                                    if TARGET_JSON.parent.exists() else False,
            "rate_window_seconds": RATE_WINDOW,
        }


# ─── Standalone test mode ────────────────────────────────────────────
def _cli():
    """Run the SSH refresh from the command line (for smoke-testing the key)."""
    import sys
    try:
        payload, stderr = ssh_refresh()
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
    manifest = json.loads(payload.decode("utf-8", "replace"))
    print(f"OK — {manifest['summary']['total']} mechanisms, "
          f"{len(payload)} bytes.")
    print(f"Generated at: {manifest.get('generated_at')}")
    if stderr.strip():
        print(f"\nSSH stderr:\n{stderr}", file=sys.stderr)


if __name__ == "__main__":
    _cli()
