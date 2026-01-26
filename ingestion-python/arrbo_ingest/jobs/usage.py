from __future__ import annotations

import logging
import random
import time
from typing import Callable, TypeVar

from nba_api.stats.endpoints import leaguedashplayerstats, commonteamroster

from arrbo_ingest.config import TEAM_ID_MAPPING
from arrbo_ingest.db import connect

log = logging.getLogger(__name__)

T = TypeVar("T")


def _sleep_polite(base: float = 0.35, jitter: float = 0.35) -> None:
    time.sleep(base + random.random() * jitter)


def _with_retries(fn: Callable[[], T], *, attempts: int = 4, base_sleep: float = 1.0) -> T:
    last_exc: Exception | None = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if i == attempts - 1:
                raise
            sleep_for = base_sleep * (2 ** i) + random.random() * 0.35
            log.warning("Request failed (attempt %d/%d): %s | sleeping %.2fs",
                        i + 1, attempts, e, sleep_for)
            time.sleep(sleep_for)
    raise last_exc or RuntimeError("Unknown retry failure")


def _get_roster_players(nba_team_id: int, season: str, timeout: int = 60) -> set[str]:
    def fetch():
        _sleep_polite()
        return commonteamroster.CommonTeamRoster(
            team_id=nba_team_id,
            season=season,
            timeout=timeout,
        ).get_data_frames()[0]

    df = _with_retries(fetch, attempts=4, base_sleep=1.0)
    # normalize whitespace just in case
    return {str(name).strip() for name in df["PLAYER"].tolist() if name}



def run(db_path: str, season: str) -> None:
    log.info("Running usage ingestion for season=%s db=%s", season, db_path)

    log.info("Fetching LeagueDashPlayerStats (Usage)")
    def fetch_usage():
        _sleep_polite()
        return leaguedashplayerstats.LeagueDashPlayerStats(
            season=season,
            per_mode_detailed="PerGame",
            measure_type_detailed_defense="Usage",
            timeout=90,
        ).get_data_frames()[0]

    try:
        all_players = _with_retries(fetch_usage, attempts=3, base_sleep=1.0)
    except Exception as e:
        log.error("Failed to fetch league usage stats after retries: %s", e)
        raise

    inserts: list[tuple[int, str, float, str, float]] = []
    failed_teams: list[str] = []

    for nba_team_id_str, db_team_id in TEAM_ID_MAPPING.items():
        nba_team_id = int(nba_team_id_str)
        log.info("Processing team nba_team_id=%s db_team_id=%s", nba_team_id, db_team_id)

        try:
            current_players = _get_roster_players(nba_team_id, season, timeout=60)
        except Exception as e:
            log.warning("Failed roster fetch for team %s: %s", nba_team_id, e)
            failed_teams.append(nba_team_id_str)
            continue

        team_players = all_players[all_players["TEAM_ID"] == nba_team_id]
        if team_players.empty:
            log.warning("No usage rows for team %s", nba_team_id)
            continue

        # Keep only current roster
        team_players = team_players[team_players["PLAYER_NAME"].isin(current_players)]
        if team_players.empty:
            log.warning("No current players found in usage data for team %s", nba_team_id)
            continue

        # Sort by usage %
        team_players = team_players.sort_values("USG_PCT", ascending=False)
        top2 = team_players.head(2)
        if len(top2) < 2:
            log.warning("Not enough usage rows for team %s", nba_team_id)
            continue

        p1 = top2.iloc[0]
        p2 = top2.iloc[1]
        inserts.append(
            (db_team_id,
             str(p1["PLAYER_NAME"]), float(p1["USG_PCT"]),
             str(p2["PLAYER_NAME"]), float(p2["USG_PCT"]))
        )

        _sleep_polite(0.20, 0.25)

    with connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute("TRUNCATE TABLE top_usage_players;")

        if inserts:
            cur.executemany(
                """
                INSERT INTO top_usage_players
                (team_id, player1_name, player1_usage, player2_name, player2_usage)
                VALUES (%s, %s, %s, %s, %s)
                """,
                inserts,
            )
        conn.commit()

    log.info("Usage ingestion complete. Inserted %d teams.", len(inserts))
    if failed_teams:
        log.warning("Roster fetch failed for %d teams: %s", len(failed_teams), ", ".join(failed_teams))
