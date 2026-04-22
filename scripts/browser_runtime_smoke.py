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
    reset_email: str
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
            "reset_email": _env_default(
                "KA_BROWSER_SMOKE_RESET_EMAIL",
                "KA_BROWSER_SMOKE_STAGING_RESET_EMAIL",
                "KA_SMOKE_STAGING_RESET_EMAIL",
                fallback="",
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
            "reset_email": _env_default(
                "KA_BROWSER_SMOKE_RESET_EMAIL",
                "KA_BROWSER_SMOKE_PRODUCTION_RESET_EMAIL",
                "KA_SMOKE_PRODUCTION_RESET_EMAIL",
                fallback="",
            ),
        }
    return {
        "base_url": _env_default("KA_BROWSER_SMOKE_BASE_URL"),
        "student_email": _env_default("KA_BROWSER_SMOKE_STUDENT_EMAIL"),
        "student_password": _env_default("KA_BROWSER_SMOKE_STUDENT_PASSWORD"),
        "reset_email": _env_default("KA_BROWSER_SMOKE_RESET_EMAIL"),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("staging", "production", "custom"), default="staging")
    parser.add_argument("--base-url")
    parser.add_argument("--student-email")
    parser.add_argument("--student-password")
    parser.add_argument("--reset-email")
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
    reset_email = args.reset_email or defaults["reset_email"]
    if not base_url:
        raise SystemExit("A base URL is required.")
    if not student_email or not student_password:
        raise SystemExit("Student credentials are required for browser smoke.")
    return BrowserSmokeConfig(
        profile=args.profile,
        base_url=base_url,
        student_email=student_email,
        student_password=student_password,
        reset_email=reset_email,
        headed=args.headed,
        timeout_ms=args.timeout_ms,
    )


def _ok(name: str, detail: str, *, url: str = "") -> BrowserCheckResult:
    return BrowserCheckResult(name=name, status=PASS, detail=detail, url=url)


def _fail(name: str, detail: str, *, url: str = "") -> BrowserCheckResult:
    return BrowserCheckResult(name=name, status=FAIL, detail=detail, url=url)


def _skip(name: str, detail: str, *, url: str = "") -> BrowserCheckResult:
    return BrowserCheckResult(name=name, status=SKIP, detail=detail, url=url)


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
        forgot_page = context.new_page()
        reset_page = context.new_page()
        admin_page = context.new_page()
        login_page = context.new_page()
        article_page = context.new_page()
        theory_page = context.new_page()
        theory_journey_page = context.new_page()
        topic_page = context.new_page()
        heatmap_page = context.new_page()
        full_facets_page = context.new_page()
        topic_dashboard_page = context.new_page()
        quick_lookup_page = context.new_page()
        classic_topics_page = context.new_page()
        mechanism_page = context.new_page()
        article_theory_page = context.new_page()
        article_topic_page = context.new_page()
        topic_to_theory_page = context.new_page()
        theory_mechanism_page = context.new_page()

        try:
            home_url = f"{config.base_url}/ka_home.html"
            user_home_url = f"{config.base_url}/ka_user_home.html"
            a0_url = f"{config.base_url}/160sp/collect-articles-upload.html"
            forgot_url = f"{config.base_url}/ka_forgot_password.html"
            reset_url = f"{config.base_url}/ka_reset_password.html?token=invalid-browser-smoke-token"
            admin_url = f"{config.base_url}/160sp/ka_admin.html"
            login_url = f"{config.base_url}/ka_login.html"
            article_url = f"{config.base_url}/ka_article_view.html?id=PDF-0071"
            theory_url = f"{config.base_url}/ka_home_theory.html"
            theory_journey_url = f"{config.base_url}/ka_journey_theory.html"
            topic_url = f"{config.base_url}/ka_topic_facet_view.html"
            heatmap_url = f"{config.base_url}/ka_topic_heatmap_view.html"
            full_facets_url = f"{config.base_url}/ka_topic_full_facets_view.html"
            topic_dashboard_url = f"{config.base_url}/ka_topic_dashboard_view.html"
            quick_lookup_url = f"{config.base_url}/ka_topic_quick_lookup_view.html"
            classic_topics_url = f"{config.base_url}/ka_topics.html"
            mechanism_url = f"{config.base_url}/ka_journey_mechanism.html"

            home_page.goto(home_url, wait_until="networkidle")
            user_home_page.goto(user_home_url, wait_until="networkidle")
            a0_page.goto(a0_url, wait_until="networkidle")
            forgot_page.goto(forgot_url, wait_until="networkidle")
            reset_page.goto(reset_url, wait_until="networkidle")
            admin_page.goto(admin_url, wait_until="networkidle")
            article_page.goto(article_url, wait_until="networkidle")
            theory_page.goto(theory_url, wait_until="networkidle")
            theory_journey_page.goto(theory_journey_url, wait_until="networkidle")
            topic_page.goto(topic_url, wait_until="networkidle")
            heatmap_page.goto(heatmap_url, wait_until="networkidle")
            full_facets_page.goto(full_facets_url, wait_until="networkidle")
            topic_dashboard_page.goto(topic_dashboard_url, wait_until="networkidle")
            quick_lookup_page.goto(quick_lookup_url, wait_until="networkidle")
            classic_topics_page.goto(classic_topics_url, wait_until="networkidle")
            mechanism_page.goto(mechanism_url, wait_until="networkidle")
            article_theory_page.goto(article_url, wait_until="networkidle")
            article_topic_page.goto(article_url, wait_until="networkidle")
            topic_to_theory_page.goto(topic_url, wait_until="networkidle")
            theory_mechanism_page.goto(theory_url, wait_until="networkidle")

            nav_text = home_page.locator(".ka-right").inner_text()
            if "Log in" in nav_text and "Register" in nav_text:
                results.append(_ok("Anonymous home navbar", "Anonymous navbar shows Log in and Register", url=home_url))
            else:
                results.append(_fail("Anonymous home navbar", f"Expected anonymous controls, got: {nav_text!r}", url=home_url))

            if _wait_for_js_visible(a0_page.locator("#login-overlay")):
                results.append(_ok("A0 login overlay", "A0 shows login overlay when anonymous", url=a0_url))
            else:
                results.append(_fail("A0 login overlay", "A0 login overlay was not visible for anonymous user", url=a0_url))

            admin_prompt = admin_page.locator(".auth-sub").inner_text()
            if "Sign in with your UCSD instructor account." in admin_prompt:
                results.append(_ok("Admin gate shell", "Admin page shows the protected instructor sign-in gate", url=admin_url))
            else:
                results.append(_fail("Admin gate shell", f"Admin page did not show the expected sign-in prompt: {admin_prompt!r}", url=admin_url))

            reset_page.locator("#password").fill("BrowserSmoke!2026")
            reset_page.locator("#confirm").fill("BrowserSmoke!2026")
            reset_page.locator("#submitBtn").click()
            reset_page.wait_for_timeout(800)
            invalid_text = ""
            error_visible = _wait_for_js_visible(reset_page.locator("#msg-error"))
            invalid_visible = _wait_for_js_visible(reset_page.locator("#invalid-token"))
            if error_visible:
                invalid_text = reset_page.locator("#msg-error").inner_text().strip()
            elif invalid_visible:
                invalid_text = reset_page.locator("#invalid-token").inner_text().strip()
            if "invalid" in invalid_text.lower() or "already been used" in invalid_text.lower():
                results.append(_ok("Reset invalid-token handling", f"Reset page rejected an invalid token honestly: {invalid_text}", url=reset_url))
            else:
                results.append(_fail("Reset invalid-token handling", f"Reset page did not surface a clear invalid-token message: {invalid_text!r}", url=reset_url))

            article_page.wait_for_selector(".gallery-card img")
            gallery_count = article_page.locator(".gallery-card img").count()
            theory_chips = article_page.locator("#evidence .chip, #evidence .chip-link").count()
            if gallery_count >= 1 and theory_chips >= 1:
                results.append(_ok("Article enrichment surface", f"Article page rendered {gallery_count} visual surfaces and {theory_chips} evidence chips", url=article_url))
            else:
                results.append(_fail("Article enrichment surface", f"Article page did not render the expected enriched surface: gallery_count={gallery_count}, theory_chips={theory_chips}", url=article_url))

            article_theory_page.wait_for_selector(".article-theory-link")
            article_theory_page.locator(".article-theory-link").first.click()
            article_theory_page.wait_for_url("**/ka_home_theory.html?theory=*", wait_until="networkidle")
            selected_theory = article_theory_page.locator("#live-theory-select").input_value()
            if selected_theory:
                results.append(_ok("Article-to-theory journey", f"Article theory link opened theory focus {selected_theory}", url=article_theory_page.url))
            else:
                results.append(_fail("Article-to-theory journey", f"Article theory link changed route but did not select a theory: {article_theory_page.url}", url=article_theory_page.url))

            article_topic_page.wait_for_selector(".article-primary-topic-link")
            focused_topic_label = article_topic_page.locator(".article-primary-topic-link").first.inner_text().strip()
            article_topic_page.locator(".article-primary-topic-link").first.click()
            article_topic_page.wait_for_url("**/ka_topic_facet_view.html?topic=*", wait_until="networkidle")
            article_topic_page.wait_for_selector("#__ka_topic_focus")
            topic_focus_text = article_topic_page.locator("#__ka_topic_focus").inner_text()
            if focused_topic_label and focused_topic_label in topic_focus_text:
                results.append(_ok("Article-to-topic journey", f"Article topic link opened a focused topic briefing for {focused_topic_label}", url=article_topic_page.url))
            else:
                results.append(_fail("Article-to-topic journey", f"Topic focus did not preserve the article topic handoff: {topic_focus_text!r}", url=article_topic_page.url))

            theory_page.wait_for_selector("#live-theory-select")
            theory_options = theory_page.locator("#live-theory-select option").count()
            theory_cards = theory_page.locator(".live-card").count()
            mechanism_title = theory_page.locator("text=Mechanism inventory snapshot").count()
            if theory_options >= 5 and theory_cards >= 3 and mechanism_title >= 1:
                results.append(_ok("Theory live index", f"Theory explorer rendered {theory_options} selectable theories and {theory_cards} featured theory cards", url=theory_url))
            else:
                results.append(_fail("Theory live index", f"Theory explorer did not render the live index as expected: options={theory_options}, cards={theory_cards}, mechanism_title={mechanism_title}", url=theory_url))

            theory_mechanism_page.wait_for_selector("#live-mechanism-journey-link")
            theory_mechanism_page.locator("#live-mechanism-journey-link").click()
            theory_mechanism_page.wait_for_url("**/ka_journey_mechanism.html?theory=*", wait_until="networkidle")
            theory_mechanism_page.wait_for_selector("#j-mechanism-focus")
            mechanism_focus_text = theory_mechanism_page.locator("#j-mechanism-focus").inner_text()
            if "Opened from theory" in mechanism_focus_text:
                results.append(_ok("Theory-to-mechanism journey", "Theory explorer handed its focus into the mechanism layer", url=theory_mechanism_page.url))
            else:
                results.append(_fail("Theory-to-mechanism journey", f"Mechanism page did not surface a theory handoff note: {mechanism_focus_text!r}", url=theory_mechanism_page.url))

            theory_journey_page.wait_for_selector("#j-theory-live .j-theory-card")
            journey_theory_cards = theory_journey_page.locator("#j-theory-live .j-theory-card").count()
            journey_theory_metrics = theory_journey_page.locator("#j-theory-live .j-theory-metric").count()
            if journey_theory_cards >= 4 and journey_theory_metrics >= 4:
                results.append(_ok("Theory journey live companion", f"Theory journey rendered {journey_theory_metrics} metrics and {journey_theory_cards} live companion cards", url=theory_journey_url))
            else:
                results.append(_fail("Theory journey live companion", f"Theory journey did not render the live companion layer as expected: metrics={journey_theory_metrics}, cards={journey_theory_cards}", url=theory_journey_url))

            topic_page.wait_for_selector("#__ka_topic_briefing .brief-card")
            topic_cards = topic_page.locator("#__ka_topic_briefing .brief-card").count()
            topic_metrics = topic_page.locator("#__ka_topic_briefing .brief-metric").count()
            if topic_cards >= 4 and topic_metrics >= 4:
                results.append(_ok("Topic briefing layer", f"Topic facet page rendered {topic_metrics} summary metrics and {topic_cards} briefing cards", url=topic_url))
            else:
                results.append(_fail("Topic briefing layer", f"Topic facet page did not render the live briefing layer as expected: metrics={topic_metrics}, cards={topic_cards}", url=topic_url))

            topic_to_theory_page.wait_for_selector(".brief-chip-link")
            topic_to_theory_page.locator(".brief-chip-link").first.click()
            topic_to_theory_page.wait_for_url("**/ka_home_theory.html?theory=*", wait_until="networkidle")
            selected_from_topic = topic_to_theory_page.locator("#live-theory-select").input_value()
            if selected_from_topic:
                results.append(_ok("Topic-to-theory journey", f"Topic theory chip opened theory focus {selected_from_topic}", url=topic_to_theory_page.url))
            else:
                results.append(_fail("Topic-to-theory journey", f"Topic theory chip changed route but did not preserve a theory focus: {topic_to_theory_page.url}", url=topic_to_theory_page.url))

            heatmap_page.wait_for_selector("#__ka_heatmap_briefing .heat-card")
            heatmap_cards = heatmap_page.locator("#__ka_heatmap_briefing .heat-card").count()
            heatmap_metrics = heatmap_page.locator("#__ka_heatmap_briefing .heat-metric").count()
            if heatmap_cards >= 2 and heatmap_metrics >= 4:
                results.append(_ok("Topic heatmap briefing", f"Topic heatmap rendered {heatmap_metrics} metrics and {heatmap_cards} density cards", url=heatmap_url))
            else:
                results.append(_fail("Topic heatmap briefing", f"Topic heatmap did not render the live briefing layer as expected: metrics={heatmap_metrics}, cards={heatmap_cards}", url=heatmap_url))

            full_facets_page.wait_for_selector("#__ka_full_briefing .full-card")
            full_facets_cards = full_facets_page.locator("#__ka_full_briefing .full-card").count()
            full_facets_metrics = full_facets_page.locator("#__ka_full_briefing .full-metric").count()
            if full_facets_cards >= 2 and full_facets_metrics >= 4:
                results.append(_ok("Topic full-facets briefing", f"Topic full-facets rendered {full_facets_metrics} metrics and {full_facets_cards} facet cards", url=full_facets_url))
            else:
                results.append(_fail("Topic full-facets briefing", f"Topic full-facets did not render the live briefing layer as expected: metrics={full_facets_metrics}, cards={full_facets_cards}", url=full_facets_url))

            topic_dashboard_page.wait_for_selector("#__ka_dashboard_briefing .dash-card")
            dashboard_cards = topic_dashboard_page.locator("#__ka_dashboard_briefing .dash-card").count()
            dashboard_metrics = topic_dashboard_page.locator("#__ka_dashboard_briefing .dash-metric").count()
            if dashboard_cards >= 4 and dashboard_metrics >= 4:
                results.append(_ok("Topic dashboard briefing", f"Topic dashboard rendered {dashboard_metrics} metrics and {dashboard_cards} coordination cards", url=topic_dashboard_url))
            else:
                results.append(_fail("Topic dashboard briefing", f"Topic dashboard did not render the live coordination layer as expected: metrics={dashboard_metrics}, cards={dashboard_cards}", url=topic_dashboard_url))

            quick_lookup_page.wait_for_selector("#__ka_quick_briefing .quick-card")
            quick_lookup_cards = quick_lookup_page.locator("#__ka_quick_briefing .quick-card").count()
            quick_lookup_metrics = quick_lookup_page.locator("#__ka_quick_briefing .quick-metric").count()
            if quick_lookup_cards >= 2 and quick_lookup_metrics >= 4:
                results.append(_ok("Topic quick-lookup guide", f"Topic quick lookup rendered {quick_lookup_metrics} metrics and {quick_lookup_cards} guide cards", url=quick_lookup_url))
            else:
                results.append(_fail("Topic quick-lookup guide", f"Topic quick lookup did not render the live guide layer as expected: metrics={quick_lookup_metrics}, cards={quick_lookup_cards}", url=quick_lookup_url))

            classic_topics_page.wait_for_selector("#__ka_topics_overview .topics-live-card")
            classic_topic_cards = classic_topics_page.locator("#__ka_topics_overview .topics-live-card").count()
            classic_topic_metrics = classic_topics_page.locator("#__ka_topics_overview .topics-live-metric").count()
            if classic_topic_cards >= 2 and classic_topic_metrics >= 4:
                results.append(_ok("Classic topics overview", f"Classic topics rendered {classic_topic_metrics} metrics and {classic_topic_cards} overview cards", url=classic_topics_url))
            else:
                results.append(_fail("Classic topics overview", f"Classic topics did not render the live overview layer as expected: metrics={classic_topic_metrics}, cards={classic_topic_cards}", url=classic_topics_url))

            mechanism_page.wait_for_selector("#j-mechanism-live .j-live-card")
            mechanism_cards = mechanism_page.locator("#j-mechanism-live .j-live-card").count()
            mechanism_metrics = mechanism_page.locator("#j-mechanism-live .j-live-metric").count()
            if mechanism_cards >= 4 and mechanism_metrics >= 4:
                results.append(_ok("Mechanism inventory layer", f"Mechanism journey rendered {mechanism_metrics} metrics and {mechanism_cards} live inventory cards", url=mechanism_url))
            else:
                results.append(_fail("Mechanism inventory layer", f"Mechanism journey did not render the live inventory layer as expected: metrics={mechanism_metrics}, cards={mechanism_cards}", url=mechanism_url))

            if config.reset_email:
                forgot_page.locator("#email").fill(config.reset_email)
                forgot_page.locator("#submitBtn").click()
                forgot_page.wait_for_timeout(1000)
                ok_visible = _wait_for_js_visible(forgot_page.locator("#okAlert"))
                err_visible = _wait_for_js_visible(forgot_page.locator("#errAlert"))
                if ok_visible and not err_visible:
                    message = forgot_page.locator("#okAlert").inner_text().strip()
                    results.append(_ok("Forgot-password browser action", f"Forgot-password page surfaced a success message: {message}", url=forgot_url))
                else:
                    message = forgot_page.locator("#errAlert").inner_text().strip() if err_visible else ""
                    results.append(_fail("Forgot-password browser action", f"Forgot-password page did not surface a success state: {message!r}", url=forgot_url))
            else:
                results.append(_skip("Forgot-password browser action", "No reset email configured for browser smoke", url=forgot_url))

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

            home_page.locator("[data-ka-menu='account']").click()
            home_page.locator(".ka-menu [data-action='navigate']").click()
            home_page.wait_for_url("**/160sp/ka_student_profile.html", wait_until="networkidle")
            profile_heading = home_page.locator("text=160 Student Profile").count()
            if profile_heading >= 1:
                results.append(_ok("Profile navigation", "Account menu My profile item opened the student profile page", url=home_page.url))
            else:
                results.append(_fail("Profile navigation", f"Profile route changed but the expected heading was missing at {home_page.url}", url=home_page.url))

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
