#!/usr/bin/env python3
"""
Server-runnable runtime smoke suite for the Knowledge Atlas.

This suite is meant to run from any KA checkout, including the live server
tree and the staging clone. It probes the public site shell, payload reach-
ability, authenticated flows, admin flows, and optionally the local static
site validator in one pass.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"


@dataclass
class SmokeConfig:
    profile: str
    site_base_url: str
    api_base_url: str
    auth_health_path: str = "health"
    reset_email: str = ""
    student_email: str = ""
    student_password: str = ""
    admin_token: str = ""
    expected_track: str = ""
    expected_question_id: str = ""
    sample_article_id: str = "PDF-0007"
    repo_root: str = ""
    with_site_validator: bool = True
    fail_on_skip: bool = False
    timeout: float = 20.0


@dataclass
class ResponseData:
    url: str
    code: int | None
    body: str
    headers: dict[str, str] = field(default_factory=dict)
    error: str = ""


@dataclass
class CheckResult:
    name: str
    category: str
    status: str
    detail: str
    url: str = ""
    http_code: int | None = None


@dataclass
class SmokeReport:
    generated_at: str
    config: dict[str, Any]
    results: list[CheckResult]

    @property
    def pass_count(self) -> int:
        return sum(1 for result in self.results if result.status == PASS)

    @property
    def fail_count(self) -> int:
        return sum(1 for result in self.results if result.status == FAIL)

    @property
    def skip_count(self) -> int:
        return sum(1 for result in self.results if result.status == SKIP)

    def by_category(self) -> dict[str, dict[str, int]]:
        counts: dict[str, dict[str, int]] = {}
        for result in self.results:
            bucket = counts.setdefault(result.category, {PASS: 0, FAIL: 0, SKIP: 0})
            bucket[result.status] += 1
        return counts

    def exit_code(self, fail_on_skip: bool) -> int:
        if self.fail_count:
            return 1
        if fail_on_skip and self.skip_count:
            return 1
        return 0


class HttpClient:
    def __init__(self, base_url: str, timeout: float = 20.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._ssl_context = ssl.create_default_context()
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor()
        )

    def build_url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        path = path.lstrip("/")
        return urllib.parse.urljoin(self.base_url + "/", path)

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
        json_body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> ResponseData:
        url = self.build_url(path)
        request_headers = dict(headers or {})
        body_bytes = None
        if json_body is not None:
            request_headers.setdefault("Content-Type", "application/json")
            body_bytes = json.dumps(json_body).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=body_bytes,
            headers=request_headers,
            method=method,
        )

        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8", errors="replace")
                return ResponseData(
                    url=url,
                    code=response.getcode(),
                    body=body,
                    headers=dict(response.headers.items()),
                )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return ResponseData(
                url=url,
                code=exc.code,
                body=body,
                headers=dict(exc.headers.items()) if exc.headers else {},
                error=str(exc),
            )
        except Exception as exc:  # pragma: no cover - exercised in integration
            return ResponseData(url=url, code=None, body="", error=str(exc))


def _env_default(*names: str, fallback: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return fallback


def _auth_health_ok(payload: dict[str, Any]) -> bool:
    healthy = payload.get("ok") is True or payload.get("status") == "ok"
    modules = payload.get("modules")
    if not healthy:
        return False
    if not isinstance(modules, list):
        return False
    if "auth" not in modules or "articles" not in modules:
        return False
    if payload.get("article_module_loaded") is not True:
        return False
    return True


def _profile_defaults(profile: str) -> dict[str, str]:
    if profile == "staging":
        return {
            "site_base_url": _env_default(
                "KA_SMOKE_BASE_URL",
                "KA_SMOKE_SITE_BASE_URL",
                "KA_SMOKE_STAGING_BASE_URL",
                fallback="https://xrlab.ucsd.edu/staging_KA",
            ),
            "api_base_url": _env_default(
                "KA_SMOKE_API_BASE_URL",
                "KA_SMOKE_STAGING_API_BASE_URL",
                fallback="https://xrlab.ucsd.edu/staging_KA",
            ),
            "reset_email": _env_default(
                "KA_SMOKE_RESET_EMAIL",
                "KA_SMOKE_STAGING_RESET_EMAIL",
                fallback="",
            ),
            "auth_health_path": _env_default(
                "KA_SMOKE_AUTH_HEALTH_PATH",
                "KA_SMOKE_STAGING_AUTH_HEALTH_PATH",
                fallback="health",
            ),
            "student_email": _env_default(
                "KA_SMOKE_STAGING_STUDENT_EMAIL",
                fallback="jpark@ucsd.edu",
            ),
            "student_password": _env_default(
                "KA_SMOKE_STAGING_STUDENT_PASSWORD",
                fallback="StagingPass2026",
            ),
            "admin_token": _env_default(
                "KA_SMOKE_ADMIN_TOKEN",
                "KA_SMOKE_STAGING_ADMIN_TOKEN",
                fallback="STAGING_TOKEN_HERE",
            ),
            "expected_track": _env_default(
                "KA_SMOKE_STAGING_EXPECTED_TRACK",
                fallback="track4",
            ),
            "expected_question_id": _env_default(
                "KA_SMOKE_STAGING_EXPECTED_QUESTION_ID",
                fallback="Q01",
            ),
        }

    if profile == "production":
        return {
            "site_base_url": _env_default(
                "KA_SMOKE_BASE_URL",
                "KA_SMOKE_SITE_BASE_URL",
                "KA_SMOKE_PRODUCTION_BASE_URL",
                fallback="https://xrlab.ucsd.edu/ka",
            ),
            "api_base_url": _env_default(
                "KA_SMOKE_API_BASE_URL",
                "KA_SMOKE_PRODUCTION_API_BASE_URL",
                fallback="https://xrlab.ucsd.edu",
            ),
            "reset_email": _env_default(
                "KA_SMOKE_RESET_EMAIL",
                "KA_SMOKE_PRODUCTION_RESET_EMAIL",
                fallback="",
            ),
            "auth_health_path": _env_default(
                "KA_SMOKE_AUTH_HEALTH_PATH",
                "KA_SMOKE_PRODUCTION_AUTH_HEALTH_PATH",
                fallback="http://127.0.0.1:8765/health",
            ),
            "student_email": _env_default("KA_SMOKE_PRODUCTION_STUDENT_EMAIL"),
            "student_password": _env_default("KA_SMOKE_PRODUCTION_STUDENT_PASSWORD"),
            "admin_token": _env_default(
                "KA_SMOKE_ADMIN_TOKEN",
                "KA_SMOKE_PRODUCTION_ADMIN_TOKEN",
            ),
            "expected_track": _env_default("KA_SMOKE_PRODUCTION_EXPECTED_TRACK"),
            "expected_question_id": _env_default(
                "KA_SMOKE_PRODUCTION_EXPECTED_QUESTION_ID"
            ),
        }

    return {
        "site_base_url": _env_default("KA_SMOKE_BASE_URL", "KA_SMOKE_SITE_BASE_URL"),
        "api_base_url": _env_default("KA_SMOKE_API_BASE_URL"),
        "reset_email": _env_default("KA_SMOKE_RESET_EMAIL"),
        "auth_health_path": _env_default("KA_SMOKE_AUTH_HEALTH_PATH", fallback="health"),
        "student_email": _env_default("KA_SMOKE_STUDENT_EMAIL"),
        "student_password": _env_default("KA_SMOKE_STUDENT_PASSWORD"),
        "admin_token": _env_default("KA_SMOKE_ADMIN_TOKEN"),
        "expected_track": _env_default("KA_SMOKE_EXPECTED_TRACK"),
        "expected_question_id": _env_default("KA_SMOKE_EXPECTED_QUESTION_ID"),
    }


def _production_health_default(repo_root: str, api_base_url: str) -> str:
    normalized = str(Path(repo_root).resolve())
    if normalized.endswith("/var/www/xrlab/ka") or normalized.endswith("/private/var/www/xrlab/ka"):
        return "http://127.0.0.1:8765/health"
    return ""


def build_config(args: argparse.Namespace) -> SmokeConfig:
    defaults = _profile_defaults(args.profile)
    site_base_url = (args.site_base_url or args.base_url or defaults["site_base_url"]).rstrip("/")
    api_base_url = (args.api_base_url or defaults["api_base_url"] or site_base_url).rstrip("/")
    if not site_base_url:
        raise SystemExit("A site base URL is required. Use --site-base-url, --base-url, or a profile default.")
    if not api_base_url:
        raise SystemExit("An API base URL is required. Use --api-base-url or a profile default.")

    repo_root = str((args.repo_root or REPO_ROOT).resolve()) if not args.no_site_validator else ""
    auth_health_path = (
        args.auth_health_path if args.auth_health_path is not None else defaults["auth_health_path"]
    )
    if args.profile == "production" and auth_health_path == "http://127.0.0.1:8765/health":
        auth_health_path = _production_health_default(repo_root or str(REPO_ROOT), api_base_url)

    return SmokeConfig(
        profile=args.profile,
        site_base_url=site_base_url,
        api_base_url=api_base_url,
        reset_email=args.reset_email if args.reset_email is not None else defaults["reset_email"],
        auth_health_path=auth_health_path,
        student_email=args.student_email if args.student_email is not None else defaults["student_email"],
        student_password=args.student_password if args.student_password is not None else defaults["student_password"],
        admin_token=args.admin_token if args.admin_token is not None else defaults["admin_token"],
        expected_track=args.expected_track if args.expected_track is not None else defaults["expected_track"],
        expected_question_id=(
            args.expected_question_id
            if args.expected_question_id is not None
            else defaults["expected_question_id"]
        ),
        sample_article_id=args.sample_article_id,
        repo_root=repo_root,
        with_site_validator=not args.no_site_validator,
        fail_on_skip=args.fail_on_skip,
        timeout=args.timeout,
    )


def _result(
    name: str,
    category: str,
    status: str,
    detail: str,
    *,
    response: ResponseData | None = None,
) -> CheckResult:
    return CheckResult(
        name=name,
        category=category,
        status=status,
        detail=detail,
        url=response.url if response else "",
        http_code=response.code if response else None,
    )


def _missing_markers(body: str, markers: Iterable[str]) -> list[str]:
    return [marker for marker in markers if marker not in body]


def _parse_json(response: ResponseData) -> tuple[Any | None, str]:
    try:
        return json.loads(response.body), ""
    except Exception as exc:
        return None, str(exc)


def check_page_contains(
    client: HttpClient,
    name: str,
    path: str,
    markers: Iterable[str],
    *,
    category: str = "public",
) -> CheckResult:
    response = client.request(path)
    if response.code != 200:
        detail = f"HTTP {response.code or 'ERR'}; {response.error or 'page did not load'}"
        return _result(name, category, FAIL, detail, response=response)

    missing = _missing_markers(response.body, markers)
    if missing:
        detail = f"HTTP 200; missing markers: {', '.join(missing)}"
        return _result(name, category, FAIL, detail, response=response)

    return _result(name, category, PASS, "HTTP 200; expected markers present", response=response)


def check_asset_contains(
    client: HttpClient,
    name: str,
    path: str,
    markers: Iterable[str],
    *,
    category: str = "public",
) -> CheckResult:
    response = client.request(path)
    if response.code != 200:
        detail = f"HTTP {response.code or 'ERR'}; {response.error or 'asset did not load'}"
        return _result(name, category, FAIL, detail, response=response)

    missing = _missing_markers(response.body, markers)
    if missing:
        detail = f"HTTP 200; missing asset markers: {', '.join(missing)}"
        return _result(name, category, FAIL, detail, response=response)

    return _result(name, category, PASS, "HTTP 200; expected asset markers present", response=response)


def check_asset_ok(
    client: HttpClient,
    name: str,
    path: str,
    *,
    category: str = "public",
) -> CheckResult:
    response = client.request(path)
    if response.code != 200:
        detail = f"HTTP {response.code or 'ERR'}; {response.error or 'asset did not load'}"
        return _result(name, category, FAIL, detail, response=response)
    return _result(name, category, PASS, "HTTP 200; asset is reachable", response=response)


def check_json_payload(
    client: HttpClient,
    name: str,
    path: str,
    *,
    required_keys: Iterable[str] = (),
    body_markers: Iterable[str] = (),
    category: str = "payload",
) -> CheckResult:
    response = client.request(path)
    if response.code != 200:
        detail = f"HTTP {response.code or 'ERR'}; {response.error or 'payload not reachable'}"
        return _result(name, category, FAIL, detail, response=response)

    payload, json_error = _parse_json(response)
    if payload is None:
        detail = f"HTTP 200; response was not valid JSON ({json_error})"
        return _result(name, category, FAIL, detail, response=response)

    missing_keys = [key for key in required_keys if key not in payload]
    missing_markers = _missing_markers(response.body, body_markers)
    if missing_keys or missing_markers:
        bits = []
        if missing_keys:
            bits.append("missing keys: " + ", ".join(missing_keys))
        if missing_markers:
            bits.append("missing markers: " + ", ".join(missing_markers))
        return _result(name, category, FAIL, "HTTP 200; " + "; ".join(bits), response=response)

    return _result(name, category, PASS, "HTTP 200; JSON shape looks sound", response=response)


def check_json_field(
    client: HttpClient,
    name: str,
    path: str,
    *,
    predicate,
    success_detail: str,
    failure_detail: str,
    category: str,
    headers: dict[str, str] | None = None,
) -> CheckResult:
    response = client.request(path, headers=headers)
    if response.code != 200:
        detail = f"HTTP {response.code or 'ERR'}; {response.error or 'request failed'}"
        return _result(name, category, FAIL, detail, response=response)
    payload, json_error = _parse_json(response)
    if payload is None:
        detail = f"HTTP 200; invalid JSON ({json_error})"
        return _result(name, category, FAIL, detail, response=response)
    if predicate(payload):
        return _result(name, category, PASS, success_detail, response=response)
    return _result(name, category, FAIL, failure_detail, response=response)


def check_forgot_password(client: HttpClient, email: str) -> CheckResult:
    response = client.request(
        "auth/forgot-password",
        method="POST",
        json_body={"email": email},
    )
    if response.code != 200:
        detail = f"HTTP {response.code or 'ERR'}; {response.error or 'forgot-password failed'}"
        return _result("Forgot-password action", "auth", FAIL, detail, response=response)
    payload, json_error = _parse_json(response)
    if payload is None:
        detail = f"HTTP 200; invalid JSON ({json_error})"
        return _result("Forgot-password action", "auth", FAIL, detail, response=response)

    if payload.get("registered") is True and payload.get("email_sent") is True:
        return _result(
            "Forgot-password action",
            "auth",
            PASS,
            "HTTP 200; registered=true and email_sent=true",
            response=response,
        )
    detail = "HTTP 200; expected registered=true and email_sent=true"
    return _result("Forgot-password action", "auth", FAIL, detail, response=response)


def login_student(client: HttpClient, email: str, password: str) -> tuple[CheckResult, str]:
    response = client.request(
        "auth/login",
        method="POST",
        json_body={"email": email, "password": password},
    )
    if response.code != 200:
        detail = f"HTTP {response.code or 'ERR'}; {response.error or 'login failed'}"
        return _result("Student login action", "auth", FAIL, detail, response=response), ""
    payload, json_error = _parse_json(response)
    if payload is None:
        detail = f"HTTP 200; invalid JSON ({json_error})"
        return _result("Student login action", "auth", FAIL, detail, response=response), ""
    token = payload.get("access_token", "")
    if token:
        return (
            _result("Student login action", "auth", PASS, "HTTP 200; access token returned", response=response),
            token,
        )
    return (
        _result("Student login action", "auth", FAIL, "HTTP 200; no access token returned", response=response),
        "",
    )


def run_site_validator(repo_root: str) -> CheckResult:
    validator = Path(repo_root) / "scripts" / "site_validator.py"
    if not validator.exists():
        return _result(
            "Local site validator",
            "validator",
            SKIP,
            f"Validator not found at {validator}",
        )

    validator_skip = ["archive", "__pycache__", "node_modules", ".git", "ka_live_snapshot", ".venv"]
    completed = subprocess.run(
        [sys.executable, str(validator), "--root", repo_root, "--json", "--skip", *validator_skip],
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        detail = completed.stderr.strip() or completed.stdout.strip() or "validator execution failed"
        return _result("Local site validator", "validator", FAIL, detail[:240])

    try:
        payload = json.loads(completed.stdout)
    except Exception as exc:
        return _result("Local site validator", "validator", FAIL, f"Could not parse validator JSON: {exc}")

    summary = payload.get("summary", {}).get("by_severity", {})
    errors = int(summary.get("error", 0))
    warns = int(summary.get("warn", 0))
    if errors == 0:
        return _result(
            "Local site validator",
            "validator",
            PASS,
            f"0 errors; {warns} warnings",
        )
    return _result(
        "Local site validator",
        "validator",
        FAIL,
        f"{errors} errors; {warns} warnings",
    )


def skip_result(name: str, category: str, reason: str) -> CheckResult:
    return _result(name, category, SKIP, reason)


def run_suite(config: SmokeConfig) -> SmokeReport:
    site_client = HttpClient(config.site_base_url, timeout=config.timeout)
    api_client = HttpClient(config.api_base_url, timeout=config.timeout)
    results: list[CheckResult] = []

    if config.with_site_validator and config.repo_root:
        results.append(run_site_validator(config.repo_root))

    page_checks = [
        ("Home page shell", "ka_home.html", ["A Large Knowledge Model", "GUI workbench"]),
        ("Login page shell", "ka_login.html", ["Knowledge Atlas", "Forgot password"]),
        ("Forgot-password page shell", "ka_forgot_password.html", ["Reset your password", "Open the public workspace"]),
        ("Reset-password page shell", "ka_reset_password.html?token=smoke-test-token", ["Choose a new password", "Request a new reset link"]),
        ("User home shell", "ka_user_home.html", ["GUI track workbench", "Theory Explorer"]),
        ("A0 upload shell", "160sp/collect-articles-upload.html", ["Loading your assigned questions", "Part 2: Q2 — Open Corpus"]),
        ("Topic facet shell", "ka_topic_facet_view.html", ["Topic Page (Facet View)", "Current Atlas topic briefings", "paper_pnus.json"]),
        ("Article page shell", f"ka_article_view.html?id={config.sample_article_id}", ["Loading article record", "Visual support gallery", "Study record"]),
        ("Journeys index shell", "ka_journeys.html", ["The harder pages of Knowledge Atlas", "Article Finder"]),
        ("Theory explorer shell", "ka_home_theory.html", ["Current Atlas theory index", "theories.json", "mechanisms.json"]),
        ("Mechanism journey shell", "ka_journey_mechanism.html", ["Current mechanism inventory", "data/ka_payloads/mechanisms.json", "data/ka_payloads/theories.json"]),
        ("Admin page shell", "160sp/ka_admin.html", ["This console lets you run the class roster", "Sign in with your UCSD instructor account"]),
        ("Track 2 hub shell", "160sp/ka_track2_hub.html", ["Article Finder", "Unified pipeline reference"]),
    ]
    for name, path, markers in page_checks:
        results.append(check_page_contains(site_client, name, path, markers))

    asset_checks = [
        ("Canonical navbar asset", "ka_canonical_navbar.js", ["KA.nav", "buildNavbar", "retireLegacyTopNavs"]),
        ("User-type asset", "ka_user_type.js", ["KA.userType", "mountBanner", "applyElementGates"]),
        ("Atlas shell CSS asset", "ka_atlas_shell.css", [".ka-topnav", ".ka-shell", ".ka-journey-nav"]),
        ("Journey page CSS asset", "ka_journey_page.css", [".j-siblings", ".j-section", ".j-section-naive"]),
    ]
    for name, path, markers in asset_checks:
        results.append(check_asset_contains(site_client, name, path, markers))
    results.append(check_asset_ok(site_client, "Favicon asset", "favicon.ico"))

    results.append(
        check_json_payload(
            site_client,
            "Crosswalk payload",
            "data/ka_payloads/topic_crosswalk.json",
            required_keys=("rows", "outcome_index", "iv_root_index"),
            body_markers=('"rows"',),
        )
    )
    results.append(
        check_json_payload(
            site_client,
            "Article details payload",
            "data/ka_payloads/article_details.json",
            required_keys=("details",),
            body_markers=(config.sample_article_id,),
        )
    )
    results.append(
        check_json_payload(
            site_client,
            "Paper PNU payload",
            "data/ka_payloads/paper_pnus.json",
            required_keys=("papers",),
            body_markers=(config.sample_article_id,),
        )
    )
    results.append(
        check_json_payload(
            site_client,
            "Theory payload",
            "data/ka_payloads/theories.json",
            required_keys=("theories",),
            body_markers=('"source_kind": "soft_rebuild_theory_index"',),
        )
    )
    results.append(
        check_json_payload(
            site_client,
            "Mechanism payload",
            "data/ka_payloads/mechanisms.json",
            required_keys=("mechanisms",),
            body_markers=('"source_kind": "mechanism_profile_manifest"',),
        )
    )
    if config.auth_health_path:
        results.append(
            check_json_field(
                api_client,
                "Auth health endpoint",
                config.auth_health_path,
                predicate=_auth_health_ok,
                success_detail="HTTP 200; health payload reported a healthy auth+article state",
                failure_detail="HTTP 200; health payload was missing the article/A0 module or healthy status",
                category="auth",
            )
        )
    else:
        results.append(skip_result("Auth health endpoint", "auth", "No auth health path configured for this run"))

    if config.reset_email:
        results.append(check_forgot_password(api_client, config.reset_email))
    else:
        results.append(skip_result("Forgot-password action", "auth", "No reset email configured"))

    bearer_headers: dict[str, str] | None = None
    if config.student_email and config.student_password:
        login_result, access_token = login_student(api_client, config.student_email, config.student_password)
        results.append(login_result)
        if access_token:
            bearer_headers = {"Authorization": f"Bearer {access_token}"}
            results.append(
                check_json_field(
                    api_client,
                    "Student auth/me state",
                    "auth/me",
                    predicate=lambda payload: (
                        payload.get("email") == config.student_email
                        and (not config.expected_track or payload.get("track") == config.expected_track)
                        and (not config.expected_question_id or payload.get("question_id") == config.expected_question_id)
                    ),
                    success_detail=(
                        "HTTP 200; expected student identity, track, and question are present"
                    ),
                    failure_detail=(
                        "HTTP 200; auth/me did not match the expected student state"
                    ),
                    category="auth",
                    headers=bearer_headers,
                )
            )
            results.append(
                check_json_field(
                    api_client,
                    "Student assignments state",
                    "api/assignments",
                    predicate=lambda payload: payload.get("assigned") is True
                    and bool(payload.get("question_id")),
                    success_detail="HTTP 200; assigned=true and question_id present",
                    failure_detail="HTTP 200; assignments payload was not an assigned paper state",
                    category="auth",
                    headers=bearer_headers,
                )
            )
            results.append(
                check_json_field(
                    api_client,
                    "A0 assignment state",
                    "api/student/assignments",
                    predicate=lambda payload: isinstance(payload.get("q1"), dict)
                    and bool(payload["q1"].get("question_id"))
                    and bool(payload["q1"].get("question_text")),
                    success_detail="HTTP 200; A0 Question 1 assignment is present",
                    failure_detail="HTTP 200; A0 Question 1 assignment was missing or incomplete",
                    category="auth",
                    headers=bearer_headers,
                )
            )
            results.append(
                check_json_field(
                    api_client,
                    "A0 Question 2 topic pool",
                    "api/student/topics-needed",
                    predicate=lambda payload: isinstance(payload.get("topics"), list)
                    and len(payload["topics"]) >= 1
                    and bool(payload["topics"][0].get("question_id")),
                    success_detail="HTTP 200; A0 Question 2 topics are available",
                    failure_detail="HTTP 200; A0 Question 2 topics were missing",
                    category="auth",
                    headers=bearer_headers,
                )
            )
        else:
            results.append(skip_result("Student auth/me state", "auth", "Skipped because login failed"))
            results.append(skip_result("Student assignments state", "auth", "Skipped because login failed"))
            results.append(skip_result("A0 assignment state", "auth", "Skipped because login failed"))
            results.append(skip_result("A0 Question 2 topic pool", "auth", "Skipped because login failed"))
    else:
        results.append(skip_result("Student login action", "auth", "No student credentials configured"))
        results.append(skip_result("Student auth/me state", "auth", "No student credentials configured"))
        results.append(skip_result("Student assignments state", "auth", "No student credentials configured"))
        results.append(skip_result("A0 assignment state", "auth", "No student credentials configured"))
        results.append(skip_result("A0 Question 2 topic pool", "auth", "No student credentials configured"))

    if config.admin_token:
        admin_headers = {"X-Admin-Token": config.admin_token}
        results.append(
            check_json_field(
                api_client,
                "Admin class health",
                "api/admin/class/health",
                predicate=lambda payload: payload.get("ok") is True,
                success_detail="HTTP 200; ok=true",
                failure_detail="HTTP 200; admin health did not report ok=true",
                category="admin",
                headers=admin_headers,
            )
        )
        results.append(
            check_json_field(
                api_client,
                "Admin roster state",
                "api/admin/class/roster",
                predicate=lambda payload: isinstance(payload.get("students"), list) and len(payload["students"]) >= 1,
                success_detail="HTTP 200; roster contains at least one student",
                failure_detail="HTTP 200; roster payload did not contain students",
                category="admin",
                headers=admin_headers,
            )
        )
        results.append(
            check_json_field(
                api_client,
                "Admin grading state",
                "api/admin/class/grading",
                predicate=lambda payload: isinstance(payload.get("students"), list)
                and len(payload["students"]) >= 1
                and isinstance(payload.get("class_summary"), dict),
                success_detail="HTTP 200; grading payload contains class_summary and students",
                failure_detail="HTTP 200; grading payload was incomplete",
                category="admin",
                headers=admin_headers,
            )
        )
    else:
        results.append(skip_result("Admin class health", "admin", "No admin token configured"))
        results.append(skip_result("Admin roster state", "admin", "No admin token configured"))
        results.append(skip_result("Admin grading state", "admin", "No admin token configured"))

    config_view = asdict(config)
    if config_view.get("student_password"):
        config_view["student_password"] = "***"
    if config_view.get("admin_token"):
        config_view["admin_token"] = "***"
    return SmokeReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        config=config_view,
        results=results,
    )


def _markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_markdown(report: SmokeReport) -> str:
    lines = [
        "# Knowledge Atlas runtime smoke report",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Profile: `{report.config.get('profile')}`",
        f"- Site base URL: `{report.config.get('site_base_url')}`",
        f"- API base URL: `{report.config.get('api_base_url')}`",
        f"- Site validator: `{'on' if report.config.get('with_site_validator') else 'off'}`",
        "",
        f"- Pass: `{report.pass_count}`",
        f"- Fail: `{report.fail_count}`",
        f"- Skip: `{report.skip_count}`",
        "",
        "## By category",
        "",
        "| Category | Pass | Fail | Skip |",
        "| --- | ---: | ---: | ---: |",
    ]
    for category, counts in sorted(report.by_category().items()):
        lines.append(
            f"| {category} | {counts[PASS]} | {counts[FAIL]} | {counts[SKIP]} |"
        )

    lines.extend(
        [
            "",
            "## Checks",
            "",
            "| Check | Category | Status | Detail |",
            "| --- | --- | --- | --- |",
        ]
    )
    for result in report.results:
        lines.append(
            f"| {_markdown_escape(result.name)} | {result.category} | {result.status} | {_markdown_escape(result.detail)} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_report(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_json(report: SmokeReport) -> str:
    payload = {
        "generated_at": report.generated_at,
        "config": report.config,
        "summary": {
            "pass": report.pass_count,
            "fail": report.fail_count,
            "skip": report.skip_count,
            "by_category": report.by_category(),
        },
        "results": [asdict(result) for result in report.results],
    }
    return json.dumps(payload, indent=2)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("staging", "production", "custom"), default="staging")
    parser.add_argument("--base-url", help="Legacy alias for --site-base-url")
    parser.add_argument("--site-base-url")
    parser.add_argument("--api-base-url")
    parser.add_argument("--reset-email")
    parser.add_argument("--student-email")
    parser.add_argument("--student-password")
    parser.add_argument("--admin-token")
    parser.add_argument("--auth-health-path")
    parser.add_argument("--expected-track")
    parser.add_argument("--expected-question-id")
    parser.add_argument("--sample-article-id", default="PDF-0007")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--no-site-validator", action="store_true")
    parser.add_argument("--fail-on-skip", action="store_true")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--md-out", type=Path)
    parser.add_argument("--json-out", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = build_config(args)
    report = run_suite(config)
    markdown = render_markdown(report)
    json_text = render_json(report)
    print(markdown)
    if args.md_out:
        write_report(args.md_out, markdown)
    if args.json_out:
        write_report(args.json_out, json_text)
    return report.exit_code(config.fail_on_skip)


if __name__ == "__main__":
    raise SystemExit(main())
