from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select

from .base_page import BasePage


@dataclass
class TeamComparisonPage(BasePage):
    PATH = "/team-comparison"

    ROOT = (By.CSS_SELECTOR, "[data-testid='team-comparison-view']")
    TITLE = (By.CSS_SELECTOR, "[data-testid='team-comparison-title']")
    MATCHUP_LABEL = (By.CSS_SELECTOR, "[data-testid='team-comparison-matchup-label']")
    SPINNER = (By.CSS_SELECTOR, "[data-testid='team-comparison-spinner']")

    TEAM_A_SELECT = (By.CSS_SELECTOR, "[data-testid='team-comparison-team-a']")
    TEAM_B_SELECT = (By.CSS_SELECTOR, "[data-testid='team-comparison-team-b']")

    HOME_NEUTRAL = (By.CSS_SELECTOR, "[data-testid='team-comparison-home-neutral']")
    HOME_A = (By.CSS_SELECTOR, "[data-testid='team-comparison-home-a']")
    HOME_B = (By.CSS_SELECTOR, "[data-testid='team-comparison-home-b']")

    GENERATE = (By.CSS_SELECTOR, "[data-testid='team-comparison-generate']")
    INVALID = (By.CSS_SELECTOR, "[data-testid='team-comparison-invalid']")

    ERROR = (By.CSS_SELECTOR, "[data-testid='team-comparison-error']")
    LOADING = (By.CSS_SELECTOR, "[data-testid='team-comparison-loading']")
    EMPTY = (By.CSS_SELECTOR, "[data-testid='team-comparison-empty']")

    RESULTS = (By.CSS_SELECTOR, "[data-testid='team-comparison-results']")
    INSIGHTS_CARD = (By.CSS_SELECTOR, "[data-testid='team-comparison-insights-card']")
    RESULTS_BADGE = (By.CSS_SELECTOR, "[data-testid='team-comparison-results-badge']")

    LEADERS_GRID = (By.CSS_SELECTOR, "[data-testid='team-comparison-leaders-grid']")
    NO_LEADERS = (By.CSS_SELECTOR, "[data-testid='team-comparison-no-leaders']")

    TABLE_CARD = (By.CSS_SELECTOR, "[data-testid='team-comparison-table-card']")
    PLAYER_COUNT = (By.CSS_SELECTOR, "[data-testid='team-comparison-player-count']")
    PLAYER_TABLE = (By.CSS_SELECTOR, "[data-testid='team-comparison-player-table']")

    def open_page(self):
        self.open(self.PATH)
        self.wait_present(*self.ROOT)

    def matchup_label_text(self) -> str:
        return self.wait_visible(*self.MATCHUP_LABEL).text.strip()

    def select_team_a(self, abbr: str):
        el = self.wait_visible(*self.TEAM_A_SELECT)
        Select(el).select_by_value(abbr)

    def select_team_b(self, abbr: str):
        el = self.wait_visible(*self.TEAM_B_SELECT)
        Select(el).select_by_value(abbr)

    def set_home_neutral(self):
        self.click(*self.HOME_NEUTRAL)

    def set_home_a(self):
        self.click(*self.HOME_A)

    def set_home_b(self):
        self.click(*self.HOME_B)

    def generate(self):
        self.click(*self.GENERATE)

    def generate_is_disabled(self) -> bool:
        btn = self.wait_visible(*self.GENERATE)
        disabled = btn.get_attribute("disabled")
        return disabled is not None

    def wait_settled(self, timeout: int = 25):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.find_elements(*self.LOADING)) == 0 and len(d.find_elements(*self.SPINNER)) == 0
        )

    def has_error(self) -> bool:
        return len(self.driver.find_elements(*self.ERROR)) > 0

    def has_results(self) -> bool:
        return len(self.driver.find_elements(*self.RESULTS)) > 0

    def leaders_state_ok(self) -> bool:
        has_grid = len(self.driver.find_elements(*self.LEADERS_GRID)) > 0
        has_empty = len(self.driver.find_elements(*self.NO_LEADERS)) > 0
        return has_grid or has_empty

    def player_count(self) -> int:
        txt = self.wait_visible(*self.PLAYER_COUNT).text.strip()
        # "12 players" -> 12
        parts = txt.split()
        return int(parts[0]) if parts and parts[0].isdigit() else 0
