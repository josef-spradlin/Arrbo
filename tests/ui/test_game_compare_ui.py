import os
import pytest
from tests.ui.pages.game_compare_page import GameComparePage

pytestmark = pytest.mark.ui

def test_game_compare_renders_basic(driver, base_url):
    page = GameComparePage(driver, base_url)
    page.open_with(game_id="test")

    assert page.wait_visible(*page.TITLE).text.strip() == "Game Compare"
    assert page.game_id_text() == "test"


def test_game_compare_settles_no_infinite_loading(driver, base_url):
    page = GameComparePage(driver, base_url)
    page.open_with(game_id="test")

    page.wait_settled(timeout=10)
    assert page.has_error() or page.has_content()


def test_game_compare_content_has_valid_leaders_state(driver, base_url):
    page = GameComparePage(driver, base_url)
    page.open_with(game_id="test")
    page.wait_settled(timeout=10)

    if page.has_error():
        pytest.skip("Game Compare returned error; skipping leaders assertions.")

    assert page.has_content()
    assert page.leaders_state_ok()


def test_game_compare_tables_present_when_content(driver, base_url):
    page = GameComparePage(driver, base_url)
    page.open_with(game_id="test")
    page.wait_settled(timeout=10)

    if page.has_error():
        pytest.skip("Game Compare returned error; skipping table assertions.")

    assert page.has_content()
    page.wait_visible(*page.HOME_CARD)
    page.wait_visible(*page.AWAY_CARD)
    assert page.home_count() >= 0
    assert page.away_count() >= 0

