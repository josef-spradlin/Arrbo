from __future__ import annotations

import logging
import random
import time
import os


from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from arrbo_ingest.db import connect

log = logging.getLogger(__name__)

TEAM_ABBR_TO_ID = {
    'ATL': 1, 'BOS': 2, 'BRO': 3, 'CHA': 4, 'CHI': 5, 'CLE': 6, 'DAL': 7, 'DEN': 8,
    'DET': 9, 'GSW': 10, 'HOU': 11, 'IND': 12, 'LAC': 13, 'LAL': 14, 'MEM': 15, 'MIA': 16,
    'MIL': 17, 'MIN': 18, 'NOP': 19, 'NYK': 20, 'OKL': 21, 'ORL': 22, 'PHI': 23, 'PHX': 24,
    'POR': 25, 'SAC': 26, 'SAS': 27, 'TOR': 28, 'UTA': 29, 'WAS': 30
}

URL = "https://draftedge.com/nba/nba-defense-vs-position/"

POSITION_MAPPING = {
    'PG': ['pg_efficiency', 'sg_efficiency'],
    'SG': ['pg_efficiency', 'sg_efficiency'],
    'SF': ['sf_efficiency', 'pf_efficiency'],
    'PF': ['sf_efficiency', 'pf_efficiency'],
    'C': ['c_efficiency']
}


def _sleep_polite(base: float = 0.20, jitter: float = 0.25) -> None:
    time.sleep(base + random.random() * jitter)


def _build_driver(headless: bool) -> webdriver.Chrome:
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")

    # stability / CI-friendly flags
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--lang=en-US")

    # Explicit paths inside the container
    chrome_bin = os.getenv("CHROME_BIN", "/usr/bin/chromium")
    driver_bin = os.getenv("CHROMEDRIVER_BIN", "/usr/bin/chromedriver")

    chrome_options.binary_location = chrome_bin
    service = Service(executable_path=driver_bin)

    return webdriver.Chrome(service=service, options=chrome_options)



def run(db_path: str, headless: bool = True) -> None:
    log.info("Running defensive efficiency scrape db=%s headless=%s", db_path, headless)

    driver = _build_driver(headless)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(URL)

        # Wait for page to have at least one position button visible
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'PG')]")))
        _sleep_polite(0.4, 0.4)

        # (team_id, column_name, value)
        updates: list[tuple[int, str, float]] = []

        for web_pos, db_cols in POSITION_MAPPING.items():
            log.info("Processing position %s -> %s", web_pos, db_cols)

            try:
                # Click the tab and wait until it becomes active/updates the table
                tab_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{web_pos}')]"))
                )
                driver.execute_script("arguments[0].click();", tab_button)

                # Wait for the table to be present and populated
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                wait.until(lambda d: len(d.find_element(By.TAG_NAME, "table").find_elements(By.TAG_NAME, "tr")) >= 2)
                _sleep_polite()

                table = driver.find_element(By.TAG_NAME, "table")
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # skip header

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) < 2:
                        continue

                    # Team abbreviation stored in data-team attr
                    try:
                        team_abbr = cols[0].find_element(By.CLASS_NAME, "team-click").get_attribute("data-team")
                        team_abbr = (team_abbr or "").strip()
                    except Exception:
                        continue

                    team_id = TEAM_ABBR_TO_ID.get(team_abbr)
                    if not team_id:
                        continue

                    vs_avg_text = (cols[1].text or "").strip()
                    try:
                        vs_avg = float(vs_avg_text)
                    except Exception:
                        continue

                    for col in db_cols:
                        updates.append((team_id, col, vs_avg))

            except Exception as e:
                log.warning("Could not process position %s: %s", web_pos, e)

        with connect(db_path) as conn:
            cur = conn.cursor()

            cur.execute("TRUNCATE TABLE defensive_efficiency;")

            # ensure each team exists once
            team_ids = sorted({t for (t, _, _) in updates})
            if team_ids:
                cur.executemany(
                    """
                    INSERT INTO defensive_efficiency (team_id)
                    VALUES (%s)
                    ON CONFLICT (team_id) DO NOTHING
                    """,
                    [(tid,) for tid in team_ids]
                )

            # Only allow updating known columns
            allowed_cols = {
                "pg_efficiency", "sg_efficiency", "sf_efficiency",
                "pf_efficiency", "c_efficiency"
            }

            for team_id, col, value in updates:
                if col not in allowed_cols:
                    continue
                cur.execute(
                    f"UPDATE defensive_efficiency SET {col} = %s WHERE team_id = %s",
                    (value, team_id)
                )
            conn.commit()

        log.info("Defensive efficiency scrape complete. Updated %d cells.", len(updates))

    finally:
        driver.quit()
