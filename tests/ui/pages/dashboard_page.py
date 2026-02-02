from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage


class DashboardPage(BasePage):
    PATH = "/"

    ROOT = (By.CSS_SELECTOR, "[data-testid='dashboard-view']")
    TOGGLE = (By.CSS_SELECTOR, "[data-testid='day-toggle']")
    DAY_GAMES_COUNT = (By.CSS_SELECTOR, "[data-testid='day-games-count']")
    DATE_BADGE = (By.CSS_SELECTOR, "[data-testid='date-badge']")
    MATCHUP_BADGE = (By.CSS_SELECTOR, "[data-testid='selected-matchup-badge']")
    NO_GAMES_MESSAGE = (By.CSS_SELECTOR, "[data-testid='no-games-message']")
    PLAYER_TABLE_CARD = (By.CSS_SELECTOR, "[data-testid='player-table-card']")
    PLAYER_TABLE = (By.CSS_SELECTOR, "[data-testid='player-table']")
    PLAYERS_LOADING = (By.CSS_SELECTOR, "[data-testid='players-loading']")

    def open_page(self):
        self.open(self.PATH)
        self.wait_present(*self.ROOT)

    def toggle_day(self):
        self.click(*self.TOGGLE)

    def day_games_count(self) -> int:
        txt = self.wait_visible(*self.DAY_GAMES_COUNT).text.strip()
        return int(txt) if txt.isdigit() else 0

    def date_badge_text(self) -> str:
        return self.wait_visible(*self.DATE_BADGE).text.strip()

    def has_selected_matchup(self) -> bool:
        try:
            self.wait_present(*self.MATCHUP_BADGE, timeout=6)
            return True
        except Exception:
            return False

    def has_no_games_message(self) -> bool:
        try:
            self.wait_present(*self.NO_GAMES_MESSAGE, timeout=3)
            return True
        except Exception:
            return False

    def has_player_table(self) -> bool:
        try:
            self.wait_present(*self.PLAYER_TABLE, timeout=5)
            return True
        except Exception:
            return False

    def wait_loading_gone(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.find_elements(*self.PLAYERS_LOADING)) == 0
        )
