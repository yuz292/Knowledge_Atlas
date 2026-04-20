import re
from pathlib import Path

from scripts import gen_journey_pages
from scripts.site_validator import check_html, load_regime_items


ROOT = Path(__file__).resolve().parents[1]


def _role_labels(rendered_html: str) -> list[str]:
    block = re.search(r'<ul class="role-list">(.*?)</ul>', rendered_html, re.S)
    assert block is not None
    return re.findall(r'<span class="role-label">([^<]+)</span>', block.group(1))


def test_generated_journey_pages_use_blank_nav_active_and_canonical_role_order():
    expected_order = [
        "Public visitor",
        "COGS 160 student",
        "Researcher",
        "Practitioner",
        "Administrator",
    ]

    for page in gen_journey_pages.PAGES:
        rendered = gen_journey_pages.render_page(page)
        assert 'data-ka-active=""' in rendered
        assert _role_labels(rendered) == expected_order


def test_site_validator_allows_track4_draft_storage_keys(tmp_path):
    (tmp_path / "ka_canonical_navbar.js").write_text("", encoding="utf-8")
    page = tmp_path / "draft_page.html"
    page.write_text(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head><script src="ka_canonical_navbar.js" defer></script></head>
        <body data-ka-regime="global" data-ka-active="">
          <div id="ka-navbar-slot"></div>
          <script>
            const saved = localStorage.getItem('ka.t4f_draft');
            localStorage.setItem('ka.t4f_draft', saved || '');
          </script>
        </body>
        </html>
        """,
        encoding="utf-8",
    )

    violations = check_html(
        page,
        tmp_path,
        load_regime_items(ROOT / "ka_canonical_navbar.js"),
        archive_entries=set(),
    )

    assert [v.code for v in violations] == []


def test_site_validator_still_flags_unguarded_personalized_localstorage(tmp_path):
    (tmp_path / "ka_canonical_navbar.js").write_text("", encoding="utf-8")
    page = tmp_path / "unsafe_page.html"
    page.write_text(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head><script src="ka_canonical_navbar.js" defer></script></head>
        <body data-ka-regime="global" data-ka-active="">
          <div id="ka-navbar-slot"></div>
          <script>
            const name = localStorage.getItem('ka.userDisplayName');
          </script>
        </body>
        </html>
        """,
        encoding="utf-8",
    )

    violations = check_html(
        page,
        tmp_path,
        load_regime_items(ROOT / "ka_canonical_navbar.js"),
        archive_entries=set(),
    )

    assert [v.code for v in violations] == ["SEC001"]
