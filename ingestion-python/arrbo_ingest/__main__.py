from __future__ import annotations

import argparse
import logging
from datetime import date, datetime, timedelta

from arrbo_ingest.config import get_current_nba_season
from arrbo_ingest.logging_config import setup_logging
from arrbo_ingest.jobs import usage, positions, averages, defensive_efficiency, games

log = logging.getLogger(__name__)


def _parse_yyyy_mm_dd(s: str) -> date:
    # Accepts YYYY-MM-DD
    return datetime.strptime(s, "%Y-%m-%d").date()


def add_common_args(p: argparse.ArgumentParser, *, include_headless: bool = False, include_games_days: bool = False) -> None:
    p.add_argument("--db", default="arrbo.db", help="DB identifier/path (env-driven for Postgres)")
    p.add_argument("--season", default=None, help="Season like 2025-26 (default: auto)")
    p.add_argument("--log-level", default="INFO", help="DEBUG/INFO/WARNING/ERROR")

    if include_headless:
        p.add_argument("--headless", action="store_true", help="Run browser headless")

    if include_games_days:
        p.add_argument(
            "--games-days",
            type=int,
            default=2,
            help="How many days to ingest games starting today (2 = today+tomorrow)",
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="arrbo_ingest",
        description="ARRBO ingestion service",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_usage = sub.add_parser("usage", help="Ingest top usage players")
    add_common_args(p_usage)

    p_positions = sub.add_parser("positions", help="Ingest player positions")
    add_common_args(p_positions)

    p_averages = sub.add_parser("averages", help="Ingest per-game averages")
    add_common_args(p_averages)

    p_defeff = sub.add_parser("def-eff", help="Scrape defensive efficiency")
    add_common_args(p_defeff, include_headless=True)

    #games for a specific date
    p_games = sub.add_parser("games", help="Ingest games for a given date (NBA scoreboard)")
    add_common_args(p_games)
    p_games.add_argument(
        "--date",
        default=None,
        help="Game date in YYYY-MM-DD (default: today)",
    )

    p_all = sub.add_parser("all", help="Run all ingestion jobs")
    add_common_args(p_all, include_headless=True, include_games_days=True)

    args = parser.parse_args()
    setup_logging(args.log_level)

    season = args.season or get_current_nba_season()

    if args.cmd == "usage":
        usage.run(args.db, season)

    elif args.cmd == "positions":
        positions.run(args.db, season)

    elif args.cmd == "averages":
        averages.run(args.db, season)

    elif args.cmd == "def-eff":
        defensive_efficiency.run(args.db, headless=args.headless)

    elif args.cmd == "games":
        d = _parse_yyyy_mm_dd(args.date) if args.date else date.today()
        games.run(d)

    elif args.cmd == "all":
        usage.run(args.db, season)
        positions.run(args.db, season)
        averages.run(args.db, season)
        defensive_efficiency.run(args.db, headless=True)

        #games for today + next N-1 days (default 2 = today+tomorrow)
        days = max(1, int(getattr(args, "games_days", 2)))
        start = date.today()
        for i in range(days):
            games.run(start + timedelta(days=i))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
