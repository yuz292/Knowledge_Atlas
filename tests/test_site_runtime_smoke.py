import json

from scripts import site_runtime_smoke as smoke


def _fake_request(self, path, *, method="GET", json_body=None, headers=None):
    headers = headers or {}
    if path == "ka_home.html":
        return smoke.ResponseData("http://test/ka_home.html", 200, "Knowledge Atlas A Large Knowledge Model GUI workbench")
    if path == "ka_login.html":
        return smoke.ResponseData("http://test/ka_login.html", 200, "Knowledge Atlas Forgot password")
    if path == "ka_forgot_password.html":
        return smoke.ResponseData("http://test/ka_forgot_password.html", 200, "Reset your password Open the public workspace")
    if path == "ka_reset_password.html?token=smoke-test-token":
        return smoke.ResponseData("http://test/ka_reset_password.html?token=smoke-test-token", 200, "Choose a new password Request a new reset link")
    if path == "ka_user_home.html":
        return smoke.ResponseData("http://test/ka_user_home.html", 200, "GUI track workbench Theory Explorer")
    if path == "160sp/collect-articles-upload.html":
        return smoke.ResponseData("http://test/160sp/collect-articles-upload.html", 200, "Loading your assigned questions Part 2: Q2 — Open Corpus")
    if path == "ka_topic_facet_view.html":
        return smoke.ResponseData("http://test/ka_topic_facet_view.html", 200, "Topic Page (Facet View) topic_crosswalk.json")
    if path == "ka_article_view.html?id=PDF-0007":
        return smoke.ResponseData("http://test/ka_article_view.html?id=PDF-0007", 200, "Loading article record article_details.json")
    if path == "ka_journeys.html":
        return smoke.ResponseData("http://test/ka_journeys.html", 200, "The harder pages of Knowledge Atlas Article Finder problems")
    if path == "ka_home_theory.html":
        return smoke.ResponseData("http://test/ka_home_theory.html", 200, "Theory Explorer Knowledge Atlas")
    if path == "ka_journey_mechanism.html":
        return smoke.ResponseData("http://test/ka_journey_mechanism.html", 200, "Mechanism layer data/ka_payloads/mechanisms.json")
    if path == "160sp/ka_admin.html":
        return smoke.ResponseData("http://test/160sp/ka_admin.html", 200, "This console lets you run the class roster Sign in with your UCSD instructor account")
    if path == "160sp/ka_track2_hub.html":
        return smoke.ResponseData("http://test/160sp/ka_track2_hub.html", 200, "Article Finder Unified pipeline reference")
    if path == "ka_canonical_navbar.js":
        return smoke.ResponseData("http://test/ka_canonical_navbar.js", 200, "KA.nav buildNavbar retireLegacyTopNavs")
    if path == "ka_user_type.js":
        return smoke.ResponseData("http://test/ka_user_type.js", 200, "KA.userType mountBanner applyElementGates")
    if path == "ka_atlas_shell.css":
        return smoke.ResponseData("http://test/ka_atlas_shell.css", 200, ".ka-topnav .ka-shell .ka-journey-nav")
    if path == "ka_journey_page.css":
        return smoke.ResponseData("http://test/ka_journey_page.css", 200, ".j-siblings .j-section .j-section-naive")
    if path == "favicon.ico":
        return smoke.ResponseData("http://test/favicon.ico", 200, "ICON")
    if path == "data/ka_payloads/topic_crosswalk.json":
        return smoke.ResponseData(
            "http://test/data/ka_payloads/topic_crosswalk.json",
            200,
            json.dumps({"rows": [{"id": 1}], "outcome_index": {}, "iv_root_index": {}}),
        )
    if path == "data/ka_payloads/article_details.json":
        return smoke.ResponseData(
            "http://test/data/ka_payloads/article_details.json",
            200,
            json.dumps({"details": {"PDF-0007": {"title": "Sample"}}}),
        )
    if path == "health":
        return smoke.ResponseData(
            "http://test/health",
            200,
            json.dumps({"ok": True, "modules": ["auth", "articles"], "article_module_loaded": True}),
        )
    if path == "auth/forgot-password" and method == "POST":
        return smoke.ResponseData(
            "http://test/auth/forgot-password",
            200,
            json.dumps({"registered": True, "email_sent": True}),
        )
    if path == "auth/login" and method == "POST":
        if json_body == {"email": "jpark@ucsd.edu", "password": "secret"}:
            return smoke.ResponseData("http://test/auth/login", 200, json.dumps({"access_token": "token-123"}))
        return smoke.ResponseData("http://test/auth/login", 401, json.dumps({"detail": "denied"}), error="denied")
    if path == "auth/me":
        if headers.get("Authorization") == "Bearer token-123":
            return smoke.ResponseData(
                "http://test/auth/me",
                200,
                json.dumps({"email": "jpark@ucsd.edu", "track": "track4", "question_id": "Q01"}),
            )
        return smoke.ResponseData("http://test/auth/me", 401, json.dumps({"detail": "bad token"}), error="bad token")
    if path == "api/assignments":
        if headers.get("Authorization") == "Bearer token-123":
            return smoke.ResponseData(
                "http://test/api/assignments",
                200,
                json.dumps({"assigned": True, "question_id": "Q01"}),
            )
        return smoke.ResponseData("http://test/api/assignments", 401, json.dumps({"detail": "bad token"}), error="bad token")
    if path == "api/student/assignments":
        if headers.get("Authorization") == "Bearer token-123":
            return smoke.ResponseData(
                "http://test/api/student/assignments",
                200,
                json.dumps({
                    "q1": {"question_id": "Q01", "question_text": "What is the assigned question?"},
                    "q2": None,
                    "brownie": [],
                }),
            )
        return smoke.ResponseData("http://test/api/student/assignments", 401, json.dumps({"detail": "bad token"}), error="bad token")
    if path == "api/student/topics-needed":
        if headers.get("Authorization") == "Bearer token-123":
            return smoke.ResponseData(
                "http://test/api/student/topics-needed",
                200,
                json.dumps({"topics": [{"question_id": "Q05", "label": "Sample topic"}]}),
            )
        return smoke.ResponseData("http://test/api/student/topics-needed", 401, json.dumps({"detail": "bad token"}), error="bad token")
    if path == "api/admin/class/health":
        if headers.get("X-Admin-Token") == "admin-token":
            return smoke.ResponseData("http://test/api/admin/class/health", 200, json.dumps({"ok": True}))
        return smoke.ResponseData("http://test/api/admin/class/health", 401, json.dumps({"detail": "bad admin token"}), error="bad admin token")
    if path == "api/admin/class/roster":
        if headers.get("X-Admin-Token") == "admin-token":
            return smoke.ResponseData("http://test/api/admin/class/roster", 200, json.dumps({"students": [{"sid": "s01"}]}))
        return smoke.ResponseData("http://test/api/admin/class/roster", 401, json.dumps({"detail": "bad admin token"}), error="bad admin token")
    if path == "api/admin/class/grading":
        if headers.get("X-Admin-Token") == "admin-token":
            return smoke.ResponseData(
                "http://test/api/admin/class/grading",
                200,
                json.dumps({"class_summary": {"avg": 1}, "students": [{"sid": "s01"}]}),
            )
        return smoke.ResponseData("http://test/api/admin/class/grading", 401, json.dumps({"detail": "bad admin token"}), error="bad admin token")
    raise AssertionError(f"unexpected request: {method} {path}")


def test_run_suite_passes_with_mocked_http(monkeypatch):
    monkeypatch.setattr(smoke.HttpClient, "request", _fake_request)
    config = smoke.SmokeConfig(
        profile="custom",
        site_base_url="http://test",
        api_base_url="http://test",
        reset_email="dkirsh@ucsd.edu",
        student_email="jpark@ucsd.edu",
        student_password="secret",
        admin_token="admin-token",
        expected_track="track4",
        expected_question_id="Q01",
        with_site_validator=False,
    )
    report = smoke.run_suite(config)
    assert report.fail_count == 0
    assert report.skip_count == 0
    assert report.pass_count == len(report.results)
    assert "Forgot-password action" in smoke.render_markdown(report)


def test_run_suite_skips_checks_without_credentials(monkeypatch):
    monkeypatch.setattr(smoke.HttpClient, "request", _fake_request)
    config = smoke.SmokeConfig(
        profile="production",
        site_base_url="http://test",
        api_base_url="http://test",
        with_site_validator=False,
    )
    report = smoke.run_suite(config)
    statuses = {result.name: result.status for result in report.results}
    assert statuses["Forgot-password action"] == smoke.SKIP
    assert statuses["Student login action"] == smoke.SKIP
    assert statuses["Admin class health"] == smoke.SKIP


def test_auth_health_requires_article_module():
    assert smoke._auth_health_ok({"ok": True, "modules": ["auth", "articles"], "article_module_loaded": True}) is True
    assert smoke._auth_health_ok({"ok": True}) is False
    assert smoke._auth_health_ok({"ok": True, "modules": ["auth"]}) is False
    assert smoke._auth_health_ok({"ok": True, "modules": ["auth", "articles"], "article_module_loaded": False}) is False


def test_render_json_contains_summary(monkeypatch):
    monkeypatch.setattr(smoke.HttpClient, "request", _fake_request)
    config = smoke.SmokeConfig(
        profile="custom",
        site_base_url="http://test",
        api_base_url="http://test",
        reset_email="dkirsh@ucsd.edu",
        student_email="jpark@ucsd.edu",
        student_password="secret",
        admin_token="admin-token",
        expected_track="track4",
        expected_question_id="Q01",
        with_site_validator=False,
    )
    report = smoke.run_suite(config)
    payload = json.loads(smoke.render_json(report))
    assert payload["summary"]["fail"] == 0
    assert payload["summary"]["pass"] == len(report.results)
