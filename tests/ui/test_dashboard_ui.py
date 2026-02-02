import pytest
from tests.ui.pages.dashboard_page import DashboardPage

pytestmark = pytest.mark.ui

def test_dashboard_loads_and_shows_state(driver, base_url):
    page = DashboardPage(driver, base_url)
    page.open_page()

    assert page.day_games_count() >= 0
    assert page.has_selected_matchup() or page.has_no_games_message()

def test_dashboard_toggle_does_not_crash(driver, base_url):
    page = DashboardPage(driver, base_url)
    page.open_page()

    before = page.day_games_count()
    page.toggle_day()
    after = page.day_games_count()

    assert before >= 0
    assert after >= 0
    assert page.has_selected_matchup() or page.has_no_games_message()


def test_dashboard_toggle_changes_date_badge(driver, base_url):
    page = DashboardPage(driver, base_url)
    page.open_page()

    before = page.date_badge_text()
    page.toggle_day()
    after = page.date_badge_text()

    assert before.startswith("Date:")
    assert after.startswith("Date:")
    assert before != after


def test_if_matchup_selected_then_player_table_renders(driver, base_url):
    page = DashboardPage(driver, base_url)
    page.open_page()

    if page.has_selected_matchup():
        assert page.has_player_table()
    else:
        assert not page.has_player_table()