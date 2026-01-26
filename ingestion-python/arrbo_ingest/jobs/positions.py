from __future__ import annotations

import logging
import random
import time
from typing import Callable, TypeVar

from nba_api.stats.endpoints import commonteamroster

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
            log.warning(
                "Request failed (attempt %d/%d): %s | sleeping %.2fs",
                i + 1, attempts, e, sleep_for
            )
            time.sleep(sleep_for)
    raise last_exc or RuntimeError("Unknown retry failure")


def _fetch_team_roster(team_id: int, season: str, timeout: int = 60):
    def fetch():
        _sleep_polite()
        return commonteamroster.CommonTeamRoster(
            team_id=team_id,
            season=season,
            timeout=timeout,
        ).get_data_frames()[0]
    return _with_retries(fetch, attempts=4, base_sleep=1.0)


def run(db_path: str, season: str) -> None:
    log.info("Running positions ingestion for season=%s db=%s", season, db_path)

    all_players_positions: list[tuple[str, str]] = []
    failed_teams: list[str] = []

    # De-dupe: keep latest position seen for a player
    seen: dict[str, str] = {}

    for nba_team_id in TEAM_ID_MAPPING.keys():
        log.info("Fetching roster for team %s", nba_team_id)
        try:
            roster_df = _fetch_team_roster(int(nba_team_id), season, timeout=60)
            for _, row in roster_df.iterrows():
                player_name = row.get("PLAYER")
                player_position = row.get("POSITION")
                if player_name and player_position:
                    name = str(player_name).strip()
                    pos = str(player_position).strip()
                    if name and pos:
                        seen[name] = pos
        except Exception as e:
            log.warning("Failed to fetch roster for team %s: %s", nba_team_id, e)
            failed_teams.append(nba_team_id)
        finally:
            # extra pacing between teams
            _sleep_polite(0.20, 0.25)

    all_players_positions = [(name, pos) for name, pos in seen.items()]

    with connect(db_path) as conn:
        cur = conn.cursor()

        # Clear table + reset SERIAL id back to 1 to prevent duplicates
        cur.execute("TRUNCATE TABLE positions RESTART IDENTITY;")

        if all_players_positions:
            cur.executemany(
                "INSERT INTO positions (player_name, player_position) VALUES (%s, %s)",
                all_players_positions
            )
        conn.commit()

    log.info("Positions ingestion complete: %d rows", len(all_players_positions))
    if failed_teams:
        log.warning("Roster fetch failed for %d teams: %s", len(failed_teams), ", ".join(failed_teams))
