from __future__ import annotations

from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


@dataclass
class LeagueLeadersPage(BasePage):
    PATH = "/league-leaders"

    ROOT = (By.CSS_SELECTOR, "[data-testid='league-leaders-view']")
    TITLE = (By.CSS_SELECTOR, "[data-testid='league-leaders-title']")
    DATE_BADGE = (By.CSS_SELECTOR, "[data-testid='league-leaders-date-badge']")

    TOGGLE = (By.CSS_SELECTOR, "[data-testid='league-leaders-day-toggle']")
    SPINNER = (By.CSS_SELECTOR, "[data-testid='league-leaders-spinner']")
    LOADING = (By.CSS_SELECTOR, "[data-testid='league-leaders-loading']")

    ERROR = (By.CSS_SELECTOR, "[data-testid='league-leaders-error']")
    CONTENT = (By.CSS_SELECTOR, "[data-testid='league-leaders-content']")
    TABLE = (By.CSS_SELECTOR, "[data-testid='league-leaders-table']")

    STAT_PTS = (By.CSS_SELECTOR, "[data-testid='league-leaders-stat-pts']")
    STAT_REB = (By.CSS_SELECTOR, "[data-testid='league-leaders-stat-reb']")
    STAT_AST = (By.CSS_SELECTOR, "[data-testid='league-leaders-stat-ast']")
    STAT_PRA = (By.CSS_SELECTOR, "[data-testid='league-leaders-stat-pra']")

    def open_page(self):
        self.open(self.PATH)
        self.wait_present(*self.ROOT)

    def date_text(self) -> str:
        return self.wait_visible(*self.DATE_BADGE).text.strip()

    def toggle_day(self):
        self.click(*self.TOGGLE)

    def click_stat_pts(self):
        self.click(*self.STAT_PTS)

    def click_stat_reb(self):
        self.click(*self.STAT_REB)

    def click_stat_ast(self):
        self.click(*self.STAT_AST)

    def click_stat_pra(self):
        self.click(*self.STAT_PRA)

    def wait_settled(self, timeout: int = 25):
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.find_elements(*self.LOADING)) == 0
        )

    def has_error(self) -> bool:
        return len(self.driver.find_elements(*self.ERROR)) > 0

    def has_content(self) -> bool:
        return len(self.driver.find_elements(*self.CONTENT)) > 0
