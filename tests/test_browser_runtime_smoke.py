import json

from scripts import browser_runtime_smoke as smoke


def test_build_config_uses_staging_defaults():
    args = smoke.parse_args(["--profile", "staging"])
    config = smoke.build_config(args)
    assert config.base_url == "https://xrlab.ucsd.edu/staging_KA"
    assert config.student_email == "jpark@ucsd.edu"


def test_build_config_uses_production_defaults():
    args = smoke.parse_args(["--profile", "production"])
    config = smoke.build_config(args)
    assert config.base_url == "https://xrlab.ucsd.edu/ka"
    assert config.student_email == "ka-smoke-track1@example.com"


def test_renderers_include_summary_counts():
    report = smoke.BrowserSmokeReport(
        generated_at="2026-04-22T00:00:00+00:00",
        config={"profile": "staging", "base_url": "https://xrlab.ucsd.edu/staging_KA"},
        results=[
            smoke.BrowserCheckResult(name="A", status=smoke.PASS, detail="ok"),
            smoke.BrowserCheckResult(name="B", status=smoke.FAIL, detail="bad"),
        ],
    )

    markdown = smoke.render_markdown(report)
    payload = json.loads(smoke.render_json(report))

    assert "- Pass: `1`" in markdown
    assert "- Fail: `1`" in markdown
    assert payload["summary"]["pass"] == 1
    assert payload["summary"]["fail"] == 1
