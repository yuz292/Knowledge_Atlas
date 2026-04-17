#!/usr/bin/env python3
"""
ka_sso_stub.py — server-side admin authentication scaffold.

This is the production replacement for the client-side demo gate that
currently lives inside ka_admin.html. Today's ka_admin.html accepts any
non-empty admin key, which is adequate for UI prototyping but completely
inadequate for production. The real deployment should route every admin
API call through a server that validates a signed session cookie
produced by UCSD SSO (SAML / Shibboleth or OAuth2 via the UCSD IdP),
and that enforces an instructor-role check on every request.

This file is the scaffold for that server. It contains:
  - A FastAPI endpoint that exchanges an SSO callback for a signed
    session cookie.
  - Middleware that validates the cookie on every admin-API request.
  - A role check that enforces `role == "instructor"` or `role == "ta"`.
  - Audit logging for every admin endpoint touch.

In this prototype build the SSO integration is STUBBED: the /auth/sso
endpoint accepts a hardcoded test token to return a signed cookie. To
deploy for real:
  1. Register the site as a service provider with the UCSD IdP (Shibboleth)
  2. Replace the stub in `validate_sso_callback` with a Shibboleth
     assertion parser (python3-saml is the standard library)
  3. Configure the KA_SSO_* environment variables
  4. Point ka_admin.html's fetch() calls at /api/admin/* and let the
     middleware reject unauthenticated or unauthorised requests

Install:
    pip3 install --break-system-packages fastapi uvicorn itsdangerous python3-saml

Run locally for development:
    uvicorn scripts.ka_sso_stub:app --host 127.0.0.1 --port 8782

Env vars:
    KA_SESSION_SECRET  hex secret for signing session cookies (≥32 bytes)
    KA_SSO_IDP_URL     UCSD Shibboleth metadata URL
    KA_SSO_SP_ENTITY   this site's entity id
    KA_ADMIN_EMAILS    comma-separated emails allowed to bypass the
                       normal group check (bootstrap only; remove once
                       instructor group is correct at the IdP)
"""

import hmac
import hashlib
import json
import os
import secrets
import time
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, Request, HTTPException, Depends, Response
    from fastapi.responses import JSONResponse, RedirectResponse
    FASTAPI_OK = True
except ImportError:
    FASTAPI_OK = False


# ─── Config ──────────────────────────────────────────────────────────

SESSION_SECRET   = os.environ.get("KA_SESSION_SECRET", "")
SESSION_COOKIE   = "ka_admin_session"
SESSION_TTL      = int(os.environ.get("KA_SESSION_TTL", str(8 * 3600)))  # 8h default
ADMIN_EMAILS     = set(filter(None, os.environ.get("KA_ADMIN_EMAILS", "").split(",")))
AUDIT_LOG_PATH   = Path(os.environ.get("KA_AUDIT_LOG", "/var/log/ka/admin_audit.jsonl"))


# ─── Signed session cookies (itsdangerous-style, no external dep) ────

def _sign(payload_b64: str, secret: str) -> str:
    mac = hmac.new(secret.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{mac}"

def _unsign(token: str, secret: str) -> Optional[dict]:
    if "." not in token: return None
    payload_b64, mac = token.rsplit(".", 1)
    expected = hmac.new(secret.encode(), payload_b64.encode(),
                        hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected): return None
    try:
        import base64
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "===").decode())
    except Exception:
        return None
    if payload.get("exp", 0) < time.time(): return None
    return payload

def mint_session(email: str, role: str) -> str:
    if not SESSION_SECRET:
        raise RuntimeError("KA_SESSION_SECRET not configured")
    import base64
    payload = {"email": email, "role": role, "iat": int(time.time()),
               "exp": int(time.time()) + SESSION_TTL,
               "jti": secrets.token_hex(8)}
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return _sign(payload_b64, SESSION_SECRET)


# ─── Audit log ───────────────────────────────────────────────────────

def audit(action: str, actor: str, target: str = "", result: str = "ok"):
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": int(time.time()), "action": action,
             "actor": actor, "target": target, "result": result}
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ─── SSO callback (STUB) ─────────────────────────────────────────────

def validate_sso_callback(assertion: str) -> dict:
    """
    Parse a UCSD Shibboleth assertion and return {email, role, groups}.
    STUB for this prototype — replace with a real Shibboleth parser
    (python3-saml) before deploying.
    """
    if assertion == "STUB-DEV-TOKEN":
        return {"email": "dkirsh@ucsd.edu", "role": "instructor",
                "groups": ["cogs160-instructors"]}
    raise HTTPException(status_code=401, detail="Invalid SSO assertion")


def decide_role(sso_result: dict) -> str:
    email = sso_result.get("email", "")
    groups = set(sso_result.get("groups", []))
    if "cogs160-instructors" in groups or email in ADMIN_EMAILS:
        return "instructor"
    if "cogs160-tas" in groups:
        return "ta"
    raise HTTPException(status_code=403, detail="Not authorised as instructor or TA")


# ─── FastAPI app (only if installed) ─────────────────────────────────

if FASTAPI_OK:
    app = FastAPI()

    @app.get("/auth/sso/callback")
    async def sso_callback(assertion: str, return_to: str = "/160sp/ka_admin.html"):
        sso = validate_sso_callback(assertion)
        role = decide_role(sso)
        token = mint_session(sso["email"], role)
        audit("auth.sso.login", sso["email"], role)
        resp = RedirectResponse(url=return_to)
        resp.set_cookie(SESSION_COOKIE, token,
                        httponly=True, secure=True, samesite="strict",
                        max_age=SESSION_TTL)
        return resp

    @app.post("/auth/signout")
    async def signout(request: Request):
        email = _current_email(request) or "(no session)"
        audit("auth.signout", email)
        resp = JSONResponse({"ok": True})
        resp.delete_cookie(SESSION_COOKIE)
        return resp

    # ─── Middleware: enforce session on /api/admin/* ─────────────
    @app.middleware("http")
    async def guard_admin_endpoints(request: Request, call_next):
        if request.url.path.startswith("/api/admin"):
            session = _verify_request(request)
            if not session:
                return JSONResponse({"detail":"unauthenticated"}, status_code=401)
            if session["role"] not in ("instructor", "ta"):
                return JSONResponse({"detail":"forbidden"}, status_code=403)
            request.state.admin = session
        return await call_next(request)

    @app.get("/api/admin/whoami")
    async def whoami(request: Request):
        return {"ok": True, "admin": request.state.admin}

    @app.get("/api/admin/healthz")
    async def health():
        return {"ok": True,
                "session_secret_configured": bool(SESSION_SECRET),
                "admin_bootstrap_emails": sorted(ADMIN_EMAILS),
                "audit_log": str(AUDIT_LOG_PATH)}


# ─── Helpers ─────────────────────────────────────────────────────────

def _current_email(request) -> Optional[str]:
    s = _verify_request(request)
    return s.get("email") if s else None

def _verify_request(request) -> Optional[dict]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token or not SESSION_SECRET: return None
    return _unsign(token, SESSION_SECRET)


# ─── Migration note ──────────────────────────────────────────────────

MIGRATION_NOTE = """
ka_admin.html migration steps when this server is live:

1. Delete the demo login form and its doAdminLogin() function from
   ka_admin.html; the page becomes protected by cookie presence alone.
2. Add at the top of bootAdminUI():
       const r = await fetch('/api/admin/whoami', {credentials:'same-origin'});
       if (!r.ok) { window.location.href = '/auth/sso/start?return_to=' +
                    encodeURIComponent(location.pathname); return; }
       const me = await r.json();
       SS.setItem('ka.admin', 'yes');
       SS.setItem('ka.adminEmail', me.admin.email);
       SS.setItem('ka.adminRole', me.admin.role);
3. Replace every ADMIN_API stub with fetch() to /api/admin/... — the
   middleware here will reject unauthenticated or misroled requests
   automatically, so the client can stay simple.
4. Keep the impersonation UI client-side; impersonation is a presentation
   mode only and should NOT affect the server's role claim in the
   session cookie.
"""

if __name__ == "__main__":
    # CLI mode: mint a session cookie for local testing
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mint", nargs=2, metavar=("EMAIL", "ROLE"),
                    help="Mint a session cookie for the given email+role (for testing)")
    ap.add_argument("--print-migration", action="store_true",
                    help="Print ka_admin.html migration steps")
    args = ap.parse_args()
    if args.mint:
        email, role = args.mint
        if not SESSION_SECRET:
            print("ERROR: set KA_SESSION_SECRET first", file=__import__("sys").stderr)
            raise SystemExit(2)
        print(mint_session(email, role))
    elif args.print_migration:
        print(MIGRATION_NOTE)
    else:
        print("Run with uvicorn to start the server, or --mint/--print-migration for CLI use.")
