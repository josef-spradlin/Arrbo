from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


# This will return the current NBA season in the format "YYYY-YY Ex. 2025-26"
def get_current_nba_season(now: datetime | None = None) -> str:
    now = now or datetime.today()
    year = now.year
    month = now.month
    if month >= 10:  # Ensure that the current season will be the one we use, the season starts in October 
        return f"{year}-{str(year + 1)[-2:]}"
    return f"{year - 1}-{str(year)[-2:]}"


# NBA TEAM_ID
TEAM_ID_MAPPING: dict[str, int] = {
    "1610612737": 1, "1610612738": 2, "1610612751": 3, "1610612766": 4, "1610612741": 5,
    "1610612739": 6, "1610612742": 7, "1610612743": 8, "1610612765": 9, "1610612744": 10,
    "1610612745": 11, "1610612754": 12, "1610612746": 13, "1610612747": 14, "1610612763": 15,
    "1610612748": 16, "1610612749": 17, "1610612750": 18, "1610612740": 19, "1610612752": 20,
    "1610612760": 21, "1610612753": 22, "1610612755": 23, "1610612756": 24, "1610612757": 25,
    "1610612758": 26, "1610612759": 27, "1610612761": 28, "1610612762": 29, "1610612764": 30
}


@dataclass(frozen=True)
class IngestConfig:
    db_path: str
    season: str
    headless: bool = True
