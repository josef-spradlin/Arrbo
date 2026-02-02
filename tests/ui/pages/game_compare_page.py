from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


@dataclass
class GameComparePage(BasePage):
    PATH_PREFIX = "/game"  # /game/{gameId}

    ROOT = (By.CSS_SELECTOR, "[data-testid='game-compare-view']")
    TITLE = (By.CSS_SELECTOR, "[data-testid='game-compare-title']")
    GAME_ID = (By.CSS_SELECTOR, "[data-testid='game-compare-game-id']")
    MATCHUP_BADGE = (By.CSS_SELECTOR, "[data-testid='game-compare-matchup-badge']")
    DATE_BADGE = (By.CSS_SELECTOR, "[data-testid='game-compare-date-badge']")

    HEADER_SPINNER = (By.CSS_SELECTOR, "[data-testid='game-compare-loading-spinner']")
    LOADING_BLOCK = (By.CSS_SELECTOR, "[data-testid='game-compare-loading']")
    ERROR_BLOCK = (By.CSS_SELECTOR, "[data-testid='game-compare-error']")
    CONTENT = (By.CSS_SELECTOR, "[data-testid='game-compare-content']")

    LEADERS_CARD = (By.CSS_SELECTOR, "[data-testid='game-compare-leaders-card']")
    LEADERS_GRID = (By.CSS_SELECTOR, "[data-testid='game-compare-leaders-grid']")
    NO_LEADERS = (By.CSS_SELECTOR, "[data-testid='game-compare-no-leaders']")

    HOME_CARD = (By.CSS_SELECTOR, "[data-testid='game-compare-home-card']")
    AWAY_CARD = (By.CSS_SELECTOR, "[data-testid='game-compare-away-card']")
    HOME_COUNT = (By.CSS_SELECTOR, "[data-testid='game-compare-home-count']")
    AWAY_COUNT = (By.CSS_SELECTOR, "[data-testid='game-compare-away-count']")

    HOME_TABLE = (By.CSS_SELECTOR, "[data-testid='game-compare-home-table']")
    AWAY_TABLE = (By.CSS_SELECTOR, "[data-testid='game-compare-away-table']")

    def open_with(self, game_id: str, home: str | None = None, away: str | None = None, date: str | None = None):
        path = f"{self.PATH_PREFIX}/{game_id}"

        params: dict[str, str] = {}
        if home is not None:
            params["home"] = str(home)
        if away is not None:
            params["away"] = str(away)
        if date is not None:
            params["date"] = str(date)

        if params:
            path = f"{path}?{urlencode(params)}"

        self.open(path)
        self.wait_present(*self.ROOT)

    def wait_settled(self, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.find_elements(*self.LOADING_BLOCK)) == 0
        )

    def has_error(self) -> bool:
        return len(self.driver.find_elements(*self.ERROR_BLOCK)) > 0

    def has_content(self) -> bool:
        return len(self.driver.find_elements(*self.CONTENT)) > 0

    def leaders_state_ok(self) -> bool:
        has_grid = len(self.driver.find_elements(*self.LEADERS_GRID)) > 0
        has_empty = len(self.driver.find_elements(*self.NO_LEADERS)) > 0
        return has_grid or has_empty

    def game_id_text(self) -> str:
        return self.wait_visible(*self.GAME_ID).text.strip()

    def matchup_badge_text(self) -> str:
        return self.wait_visible(*self.MATCHUP_BADGE).text.strip()

    def home_count(self) -> int:
        txt = self.wait_visible(*self.HOME_COUNT).text.strip()
        return int(txt) if txt.isdigit() else 0

    def away_count(self) -> int:
        txt = self.wait_visible(*self.AWAY_COUNT).text.strip()
        return int(txt) if txt.isdigit() else 0
