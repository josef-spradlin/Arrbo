from __future__ import annotations

import logging
import random
import time
from typing import Callable, TypeVar

from nba_api.stats.endpoints import leaguedashplayerstats

from arrbo_ingest.db import connect

log = logging.getLogger(__name__)
T = TypeVar("T")


def _sleep_polite(base: float = 0.35, jitter: float = 0.35) -> None:
    time.sleep(base + random.random() * jitter)


def _with_retries(fn: Callable[[], T], *, attempts: int = 3, base_sleep: float = 1.0) -> T:
    last_exc: Exception | None = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if i == attempts - 1:
                raise
            sleep_for = base_sleep * (2 ** i) + random.random() * 0.35
            log.warning(
                "Request failed (attempt %d/%d): %s | sleeping %.2fs",
                i + 1, attempts, e, sleep_for
            )
            time.sleep(sleep_for)
    raise last_exc or RuntimeError("Unknown retry failure")


def run(db_path: str, season: str) -> None:
    log.info("Running averages ingestion for season=%s db=%s", season, db_path)

    log.info("Fetching LeagueDashPlayerStats (PerGame/Base)")

    def fetch_stats():
        _sleep_polite()
        return leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            per_mode_detailed="PerGame",
            measure_type_detailed_defense="Base",
            timeout=90,
        ).get_data_frames()[0]

    stats = _with_retries(fetch_stats, attempts=3, base_sleep=1.0)

    player_data: list[tuple[str, float, float, float, float]] = []
    for _, row in stats.iterrows():
        try:
            player_name = str(row["PLAYER_NAME"]).strip()
            pts = float(row["PTS"])
            reb = float(row["REB"])
            ast = float(row["AST"])
            pra = pts + reb + ast
            if player_name:
                player_data.append((player_name, pts, reb, ast, pra))
        except Exception:
            continue

    with connect(db_path) as conn:
        cur = conn.cursor()

        # Clears table and resets SERIAL/IDENTITY counter
        cur.execute("TRUNCATE TABLE averages RESTART IDENTITY;")

        if player_data:
            cur.executemany(
                """
                INSERT INTO averages (player_name, player_pts, player_reb, player_ast, player_pra)
                VALUES (%s, %s, %s, %s, %s)
                """,
                player_data
            )

        conn.commit()

    log.info("Averages ingestion complete: %d rows", len(player_data))
