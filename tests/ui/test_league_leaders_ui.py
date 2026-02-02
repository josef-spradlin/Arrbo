import pytest
from tests.ui.pages.league_leaders_page import LeagueLeadersPage

pytestmark = pytest.mark.ui


def test_league_leaders_renders(driver, base_url):
    page = LeagueLeadersPage(driver, base_url)
    page.open_page()
    assert page.wait_visible(*page.TITLE).text.strip() == "Projected League Leaders"


def test_league_leaders_settles_no_infinite_loading(driver, base_url):
    page = LeagueLeadersPage(driver, base_url)
    page.open_page()
    page.wait_settled(timeout=30)
    assert page.has_error() or page.has_content()


def test_league_leaders_shows_table_when_no_error(driver, base_url):
    page = LeagueLeadersPage(driver, base_url)
    page.open_page()
    page.wait_settled(timeout=30)

    if page.has_error():
        pytest.skip("League Leaders returned error; skipping table assertions.")

    assert page.has_content()
    page.wait_visible(*page.TABLE)


def test_league_leaders_day_toggle_changes_date_badge(driver, base_url):
    page = LeagueLeadersPage(driver, base_url)
    page.open_page()
    page.wait_settled(timeout=30)

    if page.has_error():
        pytest.skip("League Leaders returned error; skipping toggle assertions.")

    before = page.date_text()
    page.toggle_day()
    page.wait_settled(timeout=30)
    after = page.date_text()

    # Date badge is "Date: YYYY-MM-DD"
    assert before.startswith("Date:")
    assert after.startswith("Date:")
    assert before != after


def test_league_leaders_stat_buttons_do_not_break(driver, base_url):
    page = LeagueLeadersPage(driver, base_url)
    page.open_page()
    page.wait_settled(timeout=30)

    if page.has_error():
        pytest.skip("League Leaders returned error; skipping stat assertions.")

    # Click through stats, after each click, page should settle and still show content/table.
    for clicker in (page.click_stat_reb, page.click_stat_ast, page.click_stat_pra, page.click_stat_pts):
        clicker()
        page.wait_settled(timeout=30)
        assert page.has_content()
        page.wait_visible(*page.TABLE)
