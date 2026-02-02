import os
import pathlib
import pytest
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


# Separate env file from other tests
load_dotenv(".env.ui")

ARTIFACTS_DIR = pathlib.Path("test-artifacts/ui")
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("UI_BASE_URL", "http://localhost:5173").rstrip("/")


@pytest.fixture(scope="session")
def headless() -> bool:
    v = os.getenv("UI_HEADLESS", "1").strip().lower()
    return v in ("1", "true", "yes", "y")


@pytest.fixture
def driver(headless: bool):
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")

    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    d = webdriver.Chrome(options=opts)

    d.implicitly_wait(0)
    yield d
    d.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call":
        return

    if rep.failed and "driver" in item.fixturenames:
        d = item.funcargs["driver"]
        safe = item.nodeid.replace("::", "__").replace("/", "_").replace("\\", "_")

        try:
            d.save_screenshot(str(ARTIFACTS_DIR / f"{safe}.png"))
        except Exception:
            pass

        try:
            (ARTIFACTS_DIR / f"{safe}.html").write_text(d.page_source, encoding="utf-8")
        except Exception:
            pass
