from __future__ import annotations

import logging
import math
from datetime import date, datetime
from typing import Optional

from nba_api.stats.endpoints import scoreboardv2

from arrbo_ingest.db import connect

log = logging.getLogger(__name__)


def _to_mmddyyyy(d: date) -> str:
    return d.strftime("%m/%d/%Y")


def _parse_iso(dt_str: Optional[str]) -> Optional[datetime]:
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(str(dt_str).replace("Z", "+00:00"))
    except Exception:
        return None


def _safe_int(val) -> int:
    """Convert NBA API numeric fields to int, handling None/NaN/empty."""
    if val is None:
        return 0
    try:
        if isinstance(val, float) and math.isnan(val):
            return 0
        return int(float(val))
    except Exception:
        return 0


def run(game_date: date) -> None:
    log.info("Fetching games for %s", game_date.isoformat())

    sb = scoreboardv2.ScoreboardV2(
        game_date=_to_mmddyyyy(game_date),
        league_id="00",
        timeout=60,
    )

    game_header = sb.get_data_frames()[0]
    line_score = sb.get_data_frames()[1]

    # Map: (game_id, team_id) -> (abbr, score)
    team_rows: dict[tuple[str, int], tuple[str, int]] = {}
    for _, r in line_score.iterrows():
        gid = str(r.get("GAME_ID") or "")
        tid = int(r.get("TEAM_ID") or 0)
        if not gid or not tid:
            continue
        team_rows[(gid, tid)] = (
            str(r.get("TEAM_ABBREVIATION") or ""),
            _safe_int(r.get("PTS")),
        )

    rows = []
    for _, g in game_header.iterrows():
        game_id = str(g.get("GAME_ID") or "")
        if not game_id:
            continue

        home_team_id = int(g.get("HOME_TEAM_ID") or 0)
        away_team_id = int(g.get("VISITOR_TEAM_ID") or 0)
        status_text = str(g.get("GAME_STATUS_TEXT") or "")
        start_time_utc = _parse_iso(g.get("GAME_DATE_TIME_UTC"))

        home_abbr, home_score = team_rows.get((game_id, home_team_id), ("", 0))
        away_abbr, away_score = team_rows.get((game_id, away_team_id), ("", 0))

        rows.append(
            (
                game_id,
                game_date,
                start_time_utc,
                status_text,
                home_team_id,
                home_abbr,
                home_score,
                away_team_id,
                away_abbr,
                away_score,
            )
        )

    with connect(None) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM games WHERE game_date = %s", (game_date,))

            if rows:
                cur.executemany(
                    """
                    INSERT INTO games (
                      game_id, game_date, start_time_utc, status_text,
                      home_team_id, home_team_abbr, home_team_score,
                      away_team_id, away_team_abbr, away_team_score
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (game_id) DO UPDATE SET
                      game_date = EXCLUDED.game_date,
                      start_time_utc = EXCLUDED.start_time_utc,
                      status_text = EXCLUDED.status_text,
                      home_team_id = EXCLUDED.home_team_id,
                      home_team_abbr = EXCLUDED.home_team_abbr,
                      home_team_score = EXCLUDED.home_team_score,
                      away_team_id = EXCLUDED.away_team_id,
                      away_team_abbr = EXCLUDED.away_team_abbr,
                      away_team_score = EXCLUDED.away_team_score
                    """,
                    rows,
                )

    log.info("Upserted %d games for %s", len(rows), game_date.isoformat())
