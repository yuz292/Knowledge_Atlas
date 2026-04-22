#!/usr/bin/env python3
"""
Browser-level runtime smoke suite for Knowledge Atlas.

This complements site_runtime_smoke.py. It verifies the user-visible state
transitions that HTTP-only checks cannot prove:

- anonymous navbar state
- cached-page auth refresh after login
- A0 DOM assignment rendering after login
- page-state reset after logout across already-open tabs
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"


@dataclass
class BrowserSmokeConfig:
    profile: str
    base_url: str
    student_email: str
    student_password: str
    headed: bool
    timeout_ms: int


@dataclass
class BrowserCheckResult:
    name: str
    status: str
    detail: str
    url: str = ""


@dataclass
class BrowserSmokeReport:
    generated_at: str
    config: dict[str, Any]
    results: list[BrowserCheckResult]

    @property
    def pass_count(self) -> int:
        return sum(1 for result in self.results if result.status == PASS)

    @property
    def fail_count(self) -> int:
        return sum(1 for result in self.results if result.status == FAIL)

    @property
    def skip_count(self) -> int:
        return sum(1 for result in self.results if result.status == SKIP)

    def exit_code(self) -> int:
        return 1 if self.fail_count else 0


def _env_default(*names: str, fallback: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return fallback


def _profile_defaults(profile: str) -> dict[str, str]:
    if profile == "staging":
        return {
            "base_url": _env_default(
                "KA_BROWSER_SMOKE_BASE_URL",
                "KA_SMOKE_STAGING_BASE_URL",
                fallback="https://xrlab.ucsd.edu/staging_KA",
            ),
            "student_email": _env_default(
                "KA_BROWSER_SMOKE_STAGING_STUDENT_EMAIL",
                "KA_SMOKE_STAGING_STUDENT_EMAIL",
                fallback="jpark@ucsd.edu",
            ),
            "student_password": _env_default(
                "KA_BROWSER_SMOKE_STAGING_STUDENT_PASSWORD",
                "KA_SMOKE_STAGING_STUDENT_PASSWORD",
                fallback="StagingPass2026",
            ),
        }
    if profile == "production":
        return {
            "base_url": _env_default(
                "KA_BROWSER_SMOKE_BASE_URL",
                "KA_SMOKE_PRODUCTION_BASE_URL",
                fallback="https://xrlab.ucsd.edu/ka",
            ),
            "student_email": _env_default(
                "KA_BROWSER_SMOKE_PRODUCTION_STUDENT_EMAIL",
                "KA_SMOKE_PRODUCTION_STUDENT_EMAIL",
                fallback="ka-smoke-track1@example.com",
            ),
            "student_password": _env_default(
                "KA_BROWSER_SMOKE_PRODUCTION_STUDENT_PASSWORD",
                "KA_SMOKE_PRODUCTION_STUDENT_PASSWORD",
                fallback="SmokeReset!2026",
            ),
        }
    return {
        "base_url": _env_default("KA_BROWSER_SMOKE_BASE_URL"),
        "student_email": _env_default("KA_BROWSER_SMOKE_STUDENT_EMAIL"),
        "student_password": _env_default("KA_BROWSER_SMOKE_STUDENT_PASSWORD"),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("staging", "production", "custom"), default="staging")
    parser.add_argument("--base-url")
    parser.add_argument("--student-email")
    parser.add_argument("--student-password")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=10000)
    parser.add_argument("--md-out", type=Path)
    parser.add_argument("--json-out", type=Path)
    return parser.parse_args(argv)


def build_config(args: argparse.Namespace) -> BrowserSmokeConfig:
    defaults = _profile_defaults(args.profile)
    base_url = (args.base_url or defaults["base_url"]).rstrip("/")
    student_email = args.student_email or defaults["student_email"]
    student_password = args.student_password or defaults["student_password"]
    if not base_url:
        raise SystemExit("A base URL is required.")
    if not student_email or not student_password:
        raise SystemExit("Student credentials are required for browser smoke.")
    return BrowserSmokeConfig(
        profile=args.profile,
        base_url=base_url,
        student_email=student_email,
        student_password=student_password,
        headed=args.headed,
        timeout_ms=args.timeout_ms,
    )


def _ok(name: str, detail: str, *, url: str = "") -> BrowserCheckResult:
    return BrowserCheckResult(name=name, status=PASS, detail=detail, url=url)


def _fail(name: str, detail: str, *, url: str = "") -> BrowserCheckResult:
    return BrowserCheckResult(name=name, status=FAIL, detail=detail, url=url)


def _wait_for_js_visible(locator) -> bool:
    return locator.evaluate(
        """(el) => {
            const style = window.getComputedStyle(el);
            return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
        }"""
    )


def _nudge_page(page) -> None:
    page.bring_to_front()
    page.wait_for_timeout(300)
    page.evaluate(
        """() => {
            window.dispatchEvent(new Event('focus'));
            document.dispatchEvent(new Event('visibilitychange'));
        }"""
    )
    page.wait_for_timeout(300)


def run_suite(config: BrowserSmokeConfig) -> BrowserSmokeReport:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Playwright is not installed. Install it with `pip install playwright` "
            "and `python -m playwright install chromium`."
        ) from exc

    results: list[BrowserCheckResult] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not config.headed)
        context = browser.new_context()
        context.set_default_timeout(config.timeout_ms)

        home_page = context.new_page()
        user_home_page = context.new_page()
        a0_page = context.new_page()
        login_page = context.new_page()

        try:
            home_url = f"{config.base_url}/ka_home.html"
            user_home_url = f"{config.base_url}/ka_user_home.html"
            a0_url = f"{config.base_url}/160sp/collect-articles-upload.html"
            login_url = f"{config.base_url}/ka_login.html"

            home_page.goto(home_url, wait_until="networkidle")
            user_home_page.goto(user_home_url, wait_until="networkidle")
            a0_page.goto(a0_url, wait_until="networkidle")

            nav_text = home_page.locator(".ka-right").inner_text()
            if "Log in" in nav_text and "Register" in nav_text:
                results.append(_ok("Anonymous home navbar", "Anonymous navbar shows Log in and Register", url=home_url))
            else:
                results.append(_fail("Anonymous home navbar", f"Expected anonymous controls, got: {nav_text!r}", url=home_url))

            if _wait_for_js_visible(a0_page.locator("#login-overlay")):
                results.append(_ok("A0 login overlay", "A0 shows login overlay when anonymous", url=a0_url))
            else:
                results.append(_fail("A0 login overlay", "A0 login overlay was not visible for anonymous user", url=a0_url))

            login_page.goto(login_url, wait_until="networkidle")
            login_page.locator("#email").fill(config.student_email)
            login_page.locator("#password").fill(config.student_password)
            login_page.locator("#loginForm button[type='submit']").click()
            login_page.wait_for_url("**/160sp/**", wait_until="networkidle")
            results.append(_ok("Login flow", f"Student login redirected to {login_page.url}", url=login_page.url))

            _nudge_page(home_page)
            home_nav_text = home_page.locator(".ka-right").inner_text()
            if "160 Student" in home_nav_text and "Register" not in home_nav_text and "Log in" not in home_nav_text:
                results.append(_ok("Home refresh after login", "Previously opened home page refreshed to signed-in student state", url=home_url))
            else:
                results.append(_fail("Home refresh after login", f"Home navbar stayed stale after login: {home_nav_text!r}", url=home_url))

            _nudge_page(user_home_page)
            top_bar_login = user_home_page.locator("#top-bar-login-btn")
            top_bar_logout = user_home_page.locator("#top-bar-logout")
            if (not _wait_for_js_visible(top_bar_login)) and _wait_for_js_visible(top_bar_logout):
                results.append(_ok("User-home refresh after login", "Previously opened user-home page refreshed to authenticated top-bar state", url=user_home_url))
            else:
                results.append(_fail("User-home refresh after login", "User-home top bar did not switch to authenticated state", url=user_home_url))

            _nudge_page(a0_page)
            a0_page.wait_for_function(
                """() => {
                    const hero = document.getElementById('hero-status');
                    const q1 = document.getElementById('prog-q1-id');
                    const q2 = document.querySelectorAll('#q2-topic-select option');
                    return hero && hero.textContent.includes('assigned')
                        && q1 && q1.textContent.trim() !== '—'
                        && q2.length > 0;
                }"""
            )
            q1_id = a0_page.locator("#prog-q1-id").inner_text().strip()
            q2_count = a0_page.locator("#q2-topic-select option").count()
            results.append(_ok("A0 refresh after login", f"A0 rendered assigned question {q1_id} and {q2_count} Question 2 options", url=a0_url))

            _nudge_page(home_page)
            home_page.locator("[data-ka-menu='account']").click()
            home_page.locator(".ka-menu [data-action='sign-out']").click()
            home_page.wait_for_load_state("networkidle")
            results.append(_ok("Logout flow", "Sign out completed from the canonical navbar account menu", url=home_url))

            _nudge_page(user_home_page)
            if _wait_for_js_visible(user_home_page.locator("#top-bar-login-btn")) and not _wait_for_js_visible(user_home_page.locator("#top-bar-logout")):
                results.append(_ok("User-home refresh after logout", "User-home page returned to anonymous top-bar state", url=user_home_url))
            else:
                results.append(_fail("User-home refresh after logout", "User-home page stayed in an authenticated-looking state after logout", url=user_home_url))

            _nudge_page(a0_page)
            overlay_visible = _wait_for_js_visible(a0_page.locator("#login-overlay"))
            q1_id_after_logout = a0_page.locator("#prog-q1-id").inner_text().strip()
            if overlay_visible and q1_id_after_logout == "—":
                results.append(_ok("A0 refresh after logout", "A0 returned to anonymous overlay state and cleared the visible assignment", url=a0_url))
            else:
                results.append(_fail("A0 refresh after logout", f"A0 stayed stale after logout; overlay_visible={overlay_visible}, q1={q1_id_after_logout!r}", url=a0_url))

        except PlaywrightTimeoutError as exc:
            results.append(_fail("Browser runtime smoke", f"Timed out: {exc}"))
        finally:
            context.close()
            browser.close()

    return BrowserSmokeReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        config=asdict(config),
        results=results,
    )


def render_markdown(report: BrowserSmokeReport) -> str:
    lines = [
        "# Knowledge Atlas browser runtime smoke report",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Profile: `{report.config.get('profile')}`",
        f"- Base URL: `{report.config.get('base_url')}`",
        "",
        f"- Pass: `{report.pass_count}`",
        f"- Fail: `{report.fail_count}`",
        f"- Skip: `{report.skip_count}`",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for result in report.results:
        lines.append(
            f"| {result.name.replace('|', '\\|')} | {result.status} | {result.detail.replace('|', '\\|')} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_json(report: BrowserSmokeReport) -> str:
    payload = {
        "generated_at": report.generated_at,
        "config": report.config,
        "summary": {
            "pass": report.pass_count,
            "fail": report.fail_count,
            "skip": report.skip_count,
        },
        "results": [asdict(result) for result in report.results],
    }
    return json.dumps(payload, indent=2)


def write_report(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
