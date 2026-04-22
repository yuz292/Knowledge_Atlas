from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
A0_PAGE = REPO_ROOT / "160sp" / "collect-articles-upload.html"


def test_a0_page_loads_shared_config_before_using_api_base():
    text = A0_PAGE.read_text()
    assert '<script src="../ka_config.js"></script>' in text
    assert "const API = (window.__KA_CONFIG__?.apiBase ?? '').replace(/\\/$/, '');" in text


def test_a0_page_does_not_call_root_student_endpoints_directly():
    text = A0_PAGE.read_text()
    forbidden = [
        "fetch('/api/student/q1-options'",
        "fetch('/api/student/repair-q1'",
        "fetch('/api/student/topics-needed'",
        "fetch('/api/student/choose-q2'",
    ]
    for fragment in forbidden:
        assert fragment not in text, f"unexpected root-relative endpoint remains: {fragment}"
