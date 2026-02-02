from dataclasses import dataclass
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10

@dataclass
class BasePage:
    driver: WebDriver
    base_url: str

    def open(self, path: str):
        self.driver.get(f"{self.base_url}{path}")

    def wait_visible(self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def wait_present(self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def wait_clickable(self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )

    def click(self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT):
        self.wait_clickable(by, locator, timeout).click()
