# Normal start with no ingest - py run.py up
# Start with ingest - py run.py up --ingest
# Start with ingest and rebuild - py run.py up --rebuild --ingest

#Stop everything - py run.py down
#Stop and reset DB - py run.py down --reset-db

from __future__ import annotations

import argparse
import os
import subprocess
import time
from urllib.request import urlopen


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.join(REPO_ROOT, "frontend-vue")



DB_SERVICE = "db"
API_SERVICE = "api"
INGEST_SERVICE = "ingest"

API_HEALTH_URL = os.environ.get("ARRBO_API_HEALTH_URL", "http://localhost:8080/health")

API_WAIT_SECONDS = 90


def run(cmd: list[str], *, cwd: str | None = None, check: bool = True) -> int:
    """Run a command and stream output."""
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=False)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def compose(*args: str, check: bool = True) -> int:
    return run(["docker", "compose", *args], cwd=REPO_ROOT, check=check)


def wait_for_url(url: str, timeout_s: int) -> None:
    print(f"\nWaiting for API at {url} (timeout {timeout_s}s)...")
    start = time.time()
    last_err = None
    while time.time() - start < timeout_s:
        try:
            with urlopen(url, timeout=3) as resp:
                print(f"API reachable (HTTP {resp.status}).")
                return
        except Exception as e:
            last_err = e
            time.sleep(2)

    raise SystemExit(f"API did not become reachable within {timeout_s}s. Last error: {last_err}")


def ensure_tools() -> None:
    for tool in ("docker", "npm"):
        try:
            if os.name == "nt" and tool == "npm":
                run(["cmd", "/c", "npm", "--version"], check=False)
            else:
                run([tool, "--version"], check=False)
        except FileNotFoundError:
            raise SystemExit(f"Missing required tool on PATH: {tool}")



def up(*, ingest: bool, reset_db: bool, rebuild: bool, npm: bool) -> None:
    ensure_tools()

    if reset_db:
        compose("down", "-v", "--remove-orphans")

    up_args = ["up", "-d"]
    if rebuild:
        up_args.append("--build")
    up_args += [DB_SERVICE, API_SERVICE]
    compose(*up_args)

    wait_for_url(API_HEALTH_URL, API_WAIT_SECONDS)

    if ingest:
        ingest_args = ["run", "--rm"]
        if rebuild:
            ingest_args.append("--build")
        ingest_args.append(INGEST_SERVICE)
        compose(*ingest_args)

    if npm:
        if not os.path.isdir(FRONTEND_DIR):
            raise SystemExit(
                f"Frontend directory not found at {FRONTEND_DIR}\n"
                f"Edit FRONTEND_DIR in dev.py to match your repo."
            )
        if os.name == "nt":
            run(["cmd", "/c", "npm", "run", "dev"], cwd=FRONTEND_DIR, check=True)
        else:
            run(["npm", "run", "dev"], cwd=FRONTEND_DIR, check=True)



def down(*, reset_db: bool) -> None:
    if reset_db:
        compose("down", "-v", "--remove-orphans")
    else:
        compose("down", "--remove-orphans")


def main() -> None:
    parser = argparse.ArgumentParser(prog="dev.py", description="Arrbo local dev runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_up = sub.add_parser("up", help="Start db+api, optionally run ingest, optionally run npm dev")
    p_up.add_argument("--ingest", action="store_true", help="Run ingest after db+api are up")
    p_up.add_argument("--reset-db", action="store_true", help="Wipe DB volume first (docker compose down -v)")
    p_up.add_argument("--rebuild", action="store_true", help="Rebuild images (docker compose up --build)")
    p_up.add_argument("--no-npm", action="store_true", help="Do not run npm dev (containers only)")

    p_down = sub.add_parser("down", help="Stop containers (optionally wipe DB volume)")
    p_down.add_argument("--reset-db", action="store_true", help="Also wipe DB volume (docker compose down -v)")

    args = parser.parse_args()

    if args.cmd == "up":
        up(
            ingest=args.ingest,
            reset_db=args.reset_db,
            rebuild=args.rebuild,
            npm=not args.no_npm,
        )
    elif args.cmd == "down":
        down(reset_db=args.reset_db)


if __name__ == "__main__":
    main()
