import time
import pytest

from qa.api.client import api_get

pytestmark = pytest.mark.api


def wait_until_ready(path: str, timeout_s: int = 45) -> None:
    start = time.time()
    last_error = None
    while time.time() - start < timeout_s:
        try:
            r = api_get(path)
            if r.status_code < 500:
                return
        except Exception as e:
            last_error = str(e)
        time.sleep(2)
    raise AssertionError(f"API not reachable after {timeout_s}s. Last error: {last_error}")


REQUIRED_GAME_FIELDS = [
    "gameId",
    "gameDate",
    "startTimeUtc",
    "statusText",
    "homeTeamId",
    "homeTeamAbbr",
    "homeTeamScore",
    "awayTeamId",
    "awayTeamAbbr",
    "awayTeamScore",
]


def assert_json_response(r):
    ct = (r.headers.get("content-type") or "").lower()
    assert "application/json" in ct, f"Expected JSON response. content-type={ct}"
    return r.json()


def get_available_dates() -> list[str]:
    path = "/api/games/available-dates"
    wait_until_ready(path)
    r = api_get(path)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:250]}"
    data = assert_json_response(r)
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    # expect ISO YYYY-MM-DD strings
    for d in data[:5]:
        assert isinstance(d, str) and len(d) == 10, f"Unexpected date format: {d}"
    return data


def pick_two_dates(dates_asc: list[str]) -> tuple[str, str]:
    assert dates_asc, "available-dates returned empty list"
    if len(dates_asc) == 1:
        return dates_asc[0], dates_asc[0]
    # Lowest is first, highest is last (assuming asc)
    return dates_asc[0], dates_asc[-1]


def test_available_dates_and_latest_date_contract():
    # available dates contract
    dates = get_available_dates()
    assert len(dates) >= 1

    # latest-date should equal the max available date
    r = api_get("/api/games/latest-date")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:250]}"
    latest = r.text.strip().strip('"')
    assert latest == dates[-1], f"latest-date={latest} did not match max available date={dates[-1]}"


def test_games_by_date_smoke_contract_uses_available_dates():
    dates = get_available_dates()
    date_str, _ = pick_two_dates(dates)

    path = f"/api/games?date={date_str}"
    wait_until_ready(path)

    r = api_get(path)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:250]}"

    data = assert_json_response(r)
    assert isinstance(data, list), f"Expected list, got {type(data)}"

    if not data:
        pytest.skip(f"Empty dataset returned for date={date_str}")

    first = data[0]
    assert isinstance(first, dict), f"Expected dict items, got {type(first)}"
    for k in REQUIRED_GAME_FIELDS:
        assert k in first, f"Missing key '{k}'. Keys: {list(first.keys())}"


def test_games_by_date_second_date_smoke_contract():
    dates = get_available_dates()
    _, date_str = pick_two_dates(dates)

    path = f"/api/games?date={date_str}"
    wait_until_ready(path)

    r = api_get(path)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:250]}"

    data = assert_json_response(r)
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    # allow empty, but still confirms endpoint works for another valid DB date


def test_game_by_id_smoke_contract_uses_available_dates():
    dates = get_available_dates()
    date_str, _ = pick_two_dates(dates)

    list_path = f"/api/games?date={date_str}"
    wait_until_ready(list_path)

    r_list = api_get(list_path)
    assert r_list.status_code == 200, f"Expected 200, got {r_list.status_code}. Body: {r_list.text[:250]}"

    games = assert_json_response(r_list)
    assert isinstance(games, list), f"Expected list, got {type(games)}"

    if not games:
        pytest.skip(f"No games available to fetch by ID for date={date_str}")

    game_id = games[0].get("gameId")
    assert game_id, f"No gameId found in first game object: {games[0]}"

    detail_path = f"/api/games/{game_id}"
    r = api_get(detail_path)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:250]}"

    obj = assert_json_response(r)
    assert isinstance(obj, dict), f"Expected dict, got {type(obj)}"

    for k in REQUIRED_GAME_FIELDS:
        assert k in obj, f"Missing key '{k}'. Keys: {list(obj.keys())}"

    assert obj["gameId"] == game_id, f"Expected gameId={game_id}, got {obj.get('gameId')}"
