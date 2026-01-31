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

def test_top_usage_players_smoke_contract():
    path = "/api/usage/top"

    wait_until_ready(path)

    r = api_get(path)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:250]}"

    ct = (r.headers.get("content-type") or "").lower()
    assert "application/json" in ct, f"Expected JSON response. content-type={ct}"

    data = r.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"

    if not data:
        pytest.skip("Empty dataset returned from /api/usage/top")

    first = data[0]
    assert isinstance(first, dict), f"Expected dict items, got {type(first)}"

    required = [
        "teamId",
        "player1Name", "player1Usage",
        "player2Name", "player2Usage",
        "player3Name", "player3Usage",
        "player4Name", "player4Usage",
        "player5Name", "player5Usage",
    ]
    for k in required:
        assert k in first, f"Missing key '{k}'. Keys: {list(first.keys())}"
