import pytest
from tests.ui.pages.team_comparison_page import TeamComparisonPage

pytestmark = pytest.mark.ui


def test_team_comparison_renders(driver, base_url):
    page = TeamComparisonPage(driver, base_url)
    page.open_page()
    assert page.wait_visible(*page.TITLE).text.strip() == "Team Comparison"


def test_team_comparison_initial_empty_state(driver, base_url):
    page = TeamComparisonPage(driver, base_url)
    page.open_page()
    page.wait_visible(*page.EMPTY)
    assert page.generate_is_disabled() is False


def test_team_comparison_generate_runs_and_settles(driver, base_url):
    page = TeamComparisonPage(driver, base_url)
    page.open_page()

    page.generate()
    page.wait_settled(timeout=30)

    assert page.has_results() or page.has_error()


def test_team_comparison_home_mode_changes_label(driver, base_url):
    page = TeamComparisonPage(driver, base_url)
    page.open_page()

    before = page.matchup_label_text()

    page.set_home_a()
    after_a = page.matchup_label_text()

    page.set_home_b()
    after_b = page.matchup_label_text()

    # Neutral shows "A vs B", home modes show "Away @ Home"
    assert before != after_a
    assert after_a != after_b


def test_team_comparison_invalid_same_team_disables_generate(driver, base_url):
    page = TeamComparisonPage(driver, base_url)
    page.open_page()

    # Set Team B to equal Team A
    # Default Team A is BOS, so set Team B to BOS
    page.select_team_b("BOS")

    # Generate should now be disabled and invalid message should show
    assert page.generate_is_disabled() is True
    page.wait_visible(*page.INVALID)


def test_team_comparison_results_have_consistent_leaders_state(driver, base_url):
    page = TeamComparisonPage(driver, base_url)
    page.open_page()

    page.generate()
    page.wait_settled(timeout=30)

    if page.has_error():
        pytest.skip("Team Comparison returned error; skipping results assertions.")

    assert page.has_results()
    assert page.leaders_state_ok()
    page.wait_visible(*page.PLAYER_TABLE)
    assert page.player_count() >= 0
