import json
import os
import time
import datetime as dt
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import pytest
import requests
from dotenv import load_dotenv

pytestmark = pytest.mark.perf

load_dotenv(".env.test")


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    idx = int((len(xs) - 1) * p)
    idx = max(0, min(len(xs) - 1, idx))
    return xs[idx]


def perf_config() -> dict[str, Any]:
    return {
        "base_url": os.getenv("PERF_API_BASE_URL", "http://localhost:8080").rstrip("/"),
        "date": os.getenv("PERF_GAMES_DATE") or time.strftime("%Y-%m-%d"),
        "total": int(os.getenv("PERF_TOTAL", "100")),
        "concurrency": int(os.getenv("PERF_CONCURRENCY", "10")),
        "warmup": int(os.getenv("PERF_WARMUP", "10")),
        "timeout_s": float(os.getenv("PERF_TIMEOUT_S", "5")),
    }


def run_load(url: str, total: int, concurrency: int, warmup: int, timeout_s: float) -> dict[str, Any]:
    session = requests.Session()

    # Warmup (not counted)
    for _ in range(warmup):
        try:
            session.get(url, timeout=timeout_s)
        except Exception:
            pass

    latencies_ms: list[float] = []
    status_codes: list[int] = []
    errors = 0

    def one_request():
        t0 = time.perf_counter()
        try:
            r = session.get(url, timeout=timeout_s)
            dt = (time.perf_counter() - t0) * 1000.0
            return dt, r.status_code, None
        except Exception as e:
            dt = (time.perf_counter() - t0) * 1000.0
            return dt, None, repr(e)

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(one_request) for _ in range(total)]
        for f in as_completed(futures):
            dt, status, err = f.result()
            latencies_ms.append(dt)
            if err is not None:
                errors += 1
            else:
                status_codes.append(status)

    status_counts: dict[str, int] = {}
    for s in status_codes:
        status_counts[str(s)] = status_counts.get(str(s), 0) + 1

    return {
        "total": total,
        "errors": errors,
        "error_rate": (errors / total) if total else 0.0,
        "p50_ms": percentile(latencies_ms, 0.50),
        "p95_ms": percentile(latencies_ms, 0.95),
        "p99_ms": percentile(latencies_ms, 0.99),
        "min_ms": min(latencies_ms) if latencies_ms else 0.0,
        "max_ms": max(latencies_ms) if latencies_ms else 0.0,
        "status_counts": status_counts,
    }


def write_artifact(name: str, payload: dict[str, Any]) -> str:
    out_dir = os.path.join("test-artifacts", "perf")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path


def assert_perf(report: dict[str, Any], p95_limit_ms: float):
    assert report["error_rate"] < 0.01, f"Error rate too high: {report['error_rate']:.2%} report={report}"
    assert report["p95_ms"] < p95_limit_ms, f"p95 too slow: {report['p95_ms']:.1f}ms > {p95_limit_ms}ms report={report}"


@pytest.mark.parametrize(
    "path, p95_limit_ms",
    [
        ("/api/averages", 500),
        ("/api/positions", 500),
        ("/api/usage/top", 400),
        ("/api/defense/efficiency", 400),
    ],
)
def test_perf_smoke_simple_endpoints(path, p95_limit_ms):
    cfg = perf_config()
    url = f"{cfg['base_url']}{path}"

    report = run_load(
        url=url,
        total=cfg["total"],
        concurrency=cfg["concurrency"],
        warmup=cfg["warmup"],
        timeout_s=cfg["timeout_s"],
    )
    write_artifact(path.strip("/").replace("/", "_"), {"url": url, **report})
    assert_perf(report, p95_limit_ms)


def _pick_games_date(base_url: str, timeout_s: float) -> str | None:
    today = dt.date.today().isoformat()
    tomorrow = (dt.date.today() + dt.timedelta(days=1)).isoformat()

    for d in (today, tomorrow):
        r = requests.get(f"{base_url}/api/games?date={d}", timeout=timeout_s)
        if r.status_code != 200:
            continue
        if r.json():  
            return d

    return None


def test_perf_smoke_games_by_date():
    cfg = perf_config()
    base = cfg["base_url"]

    picked = _pick_games_date(base, cfg["timeout_s"])
    if not picked:
        pytest.skip("No games found for today or tomorrow; skipping /api/games perf test.")

    url = f"{base}/api/games?date={picked}"

    report = run_load(
        url=url,
        total=cfg["total"],
        concurrency=cfg["concurrency"],
        warmup=cfg["warmup"],
        timeout_s=cfg["timeout_s"],
    )
    write_artifact("api_games_by_date", {"url": url, "date": picked, **report})
    assert_perf(report, 500)
