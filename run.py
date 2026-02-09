#   py run.py up                  # start db+api, run frontend dev server in foreground (default)
#   py run.py up --ingest         # also run ingest once after db+api are up
#   py run.py up --reset-db       # wipe DB volume first (docker compose down -v)
#   py run.py down                # stop containers
#   py run.py test                # run all tests (starts backend if needed)
#   py run.py test --reset-db     # wipe DB volume first (docker compose down -v)
#   py run.py seed                # Seed DB from ci/seed.sql (demo/offseason dataset)
#   py run.py seed --reset-db     # Wipe DB volume first (docker compose down -v) then seed

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from urllib.request import urlopen


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(REPO_ROOT, "frontend-vue")
SEED_SQL = os.path.join(REPO_ROOT, "ci", "seed.sql")

DB_SERVICE = "db"
API_SERVICE = "api"
INGEST_SERVICE = "ingest"

API_HEALTH_URL = os.environ.get("ARRBO_API_HEALTH_URL", "http://localhost:8080/health")
API_WAIT_SECONDS = int(os.environ.get("ARRBO_API_WAIT_SECONDS", "90"))

FRONTEND_URL = os.environ.get("ARRBO_UI_BASE_URL", "http://localhost:5173")
FRONTEND_WAIT_SECONDS = int(os.environ.get("ARRBO_UI_WAIT_SECONDS", "60"))


def seed_db(*, reset_db: bool, rebuild: bool) -> None:
    ensure_tools(need_npm=False)

    if reset_db:
        compose("down", "-v", "--remove-orphans")

    up_args = ["up", "-d"]
    if rebuild:
        up_args.append("--build")
    up_args += [DB_SERVICE, API_SERVICE]
    compose(*up_args)

    wait_for_url(API_HEALTH_URL, API_WAIT_SECONDS, label="api")

    if not os.path.isfile(SEED_SQL):
        raise SystemExit(f"Seed file not found: {SEED_SQL}")

    print("\nSeeding database from ci/seed.sql ...")
    with open(SEED_SQL, "rb") as f:
        proc = subprocess.run(
            [
                "docker", "compose", "exec", "-T", DB_SERVICE,
                "env", "PGPASSWORD=$POSTGRES_PASSWORD",
                "psql", "-v", "ON_ERROR_STOP=1",
                "-h", "localhost",
                "-U", os.environ.get("POSTGRES_USER", "arrbo"),
                "-d", os.environ.get("POSTGRES_DB", "arrbo"),
            ],
            cwd=REPO_ROOT,
            stdin=f,
        )
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)

    print("Seed complete.")



def run(cmd: list[str], *, cwd: str | None = None, check: bool = True, env: dict | None = None) -> int:
    """Run a command and stream output."""
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=False, env=env)
    if check and result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.returncode


def compose(*args: str, check: bool = True) -> int:
    return run(["docker", "compose", *args], cwd=REPO_ROOT, check=check)


def wait_for_url(url: str, timeout_s: int, *, label: str = "service") -> None:
    print(f"\nWaiting for {label} at {url} (timeout {timeout_s}s)...")
    start = time.time()
    last_err: Exception | None = None
    while time.time() - start < timeout_s:
        try:
            with urlopen(url, timeout=3) as resp:
                print(f"{label} reachable (HTTP {resp.status}).")
                return
        except Exception as e:
            last_err = e
            time.sleep(2)
    raise SystemExit(f"{label} did not become reachable within {timeout_s}s. Last error: {last_err}")


def ensure_tools(*, need_npm: bool) -> None:
    try:
        run(["docker", "--version"], check=False)
    except FileNotFoundError:
        raise SystemExit("Missing required tool on PATH: docker")

    if need_npm:
        try:
            if os.name == "nt":
                run(["cmd", "/c", "npm", "--version"], check=False)
            else:
                run(["npm", "--version"], check=False)
        except FileNotFoundError:
            raise SystemExit("Missing required tool on PATH: npm")


def ensure_frontend_deps() -> None:
    if not os.path.isdir(FRONTEND_DIR):
        raise SystemExit(
            f"Frontend directory not found at {FRONTEND_DIR}\n"
            f"Edit FRONTEND_DIR in run.py if your repo layout differs."
        )

    node_modules = os.path.join(FRONTEND_DIR, "node_modules")
    if os.path.isdir(node_modules):
        return

    print("\nFrontend deps not found (frontend-vue/node_modules). Installing with npm ci...")
    if os.name == "nt":
        run(["cmd", "/c", "npm", "ci"], cwd=FRONTEND_DIR, check=True)
    else:
        run(["npm", "ci"], cwd=FRONTEND_DIR, check=True)


def start_frontend_preview() -> subprocess.Popen:
    """
      npm run build
      npm run preview -- --host 0.0.0.0 --port 5173
    """
    ensure_frontend_deps()

    print("\nBuilding frontend...")
    if os.name == "nt":
        run(["cmd", "/c", "npm", "run", "build"], cwd=FRONTEND_DIR, check=True)
    else:
        run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)

    print("\nStarting frontend preview server (background)...")
    if os.name == "nt":
        p = subprocess.Popen(
            ["cmd", "/c", "npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"],
            cwd=FRONTEND_DIR,
        )
    else:
        p = subprocess.Popen(
            ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"],
            cwd=FRONTEND_DIR,
        )

    wait_for_url(FRONTEND_URL, FRONTEND_WAIT_SECONDS, label="frontend")
    return p


def stop_process(p: subprocess.Popen | None) -> None:
    if not p:
        return
    try:
        p.terminate()
        p.wait(timeout=10)
    except Exception:
        try:
            p.kill()
        except Exception:
            pass


def up(*, ingest: bool, reset_db: bool, rebuild: bool, npm: bool) -> None:
    ensure_tools(need_npm=npm)

    if reset_db:
        compose("down", "-v", "--remove-orphans")

    up_args = ["up", "-d"]
    if rebuild:
        up_args.append("--build")
    up_args += [DB_SERVICE, API_SERVICE]
    compose(*up_args)

    wait_for_url(API_HEALTH_URL, API_WAIT_SECONDS, label="api")

    if ingest:
        ingest_args = ["run", "--rm"]
        if rebuild:
            ingest_args.append("--build")
        ingest_args.append(INGEST_SERVICE)
        compose(*ingest_args)

    # Default behavior: run frontend dev server in foreground
    if npm:
        ensure_frontend_deps()
        print("\nStarting frontend dev server (foreground)... (Ctrl+C to stop)")
        if os.name == "nt":
            run(["cmd", "/c", "npm", "run", "dev"], cwd=FRONTEND_DIR, check=True)
        else:
            run(["npm", "run", "dev"], cwd=FRONTEND_DIR, check=True)


def down(*, reset_db: bool) -> None:
    if reset_db:
        compose("down", "-v", "--remove-orphans")
    else:
        compose("down", "--remove-orphans")


def tests(*, reset_db: bool, rebuild: bool, ingest: bool) -> None:
    """
    Run all test suites: db, api, perf, ui.
    - Ensures db+api are up
    - Resets db volume
    - Runs ingest once
    - Starts a frontend preview server in background for UI tests
    """
    ensure_tools(need_npm=True)

    if reset_db:
        compose("down", "-v", "--remove-orphans")

    up_args = ["up", "-d"]
    if rebuild:
        up_args.append("--build")
    up_args += [DB_SERVICE, API_SERVICE]
    compose(*up_args)

    wait_for_url(API_HEALTH_URL, API_WAIT_SECONDS, label="api")

    if ingest:
        compose("run", "--rm", INGEST_SERVICE)

    frontend_proc: subprocess.Popen | None = None
    try:
        print("\nRunning DB tests...")
        run([sys.executable, "-m", "pytest", "-m", "db", "-vv"], cwd=REPO_ROOT, check=True)

        print("\nRunning API tests...")
        run([sys.executable, "-m", "pytest", "-m", "api", "-vv"], cwd=REPO_ROOT, check=True)

        print("\nRunning perf tests...")
        run([sys.executable, "-m", "pytest", "-m", "perf", "-vv"], cwd=REPO_ROOT, check=True)

        print("\nPreparing UI tests (frontend preview)...")
        frontend_proc = start_frontend_preview()

        print("\nRunning UI tests...")
        env = os.environ.copy()
        env.setdefault("ARRBO_UI_BASE_URL", FRONTEND_URL)
        env.setdefault("UI_HEADLESS", "1")

        run([sys.executable, "-m", "pytest", "-m", "ui", "-vv"], cwd=REPO_ROOT, check=True, env=env)

    finally:
        stop_process(frontend_proc)


def main() -> None:
    parser = argparse.ArgumentParser(prog="run.py", description="Arrbo local dev runner")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_seed = sub.add_parser("seed", help="Seed DB from ci/seed.sql (demo/offseason dataset)")
    p_seed.add_argument("--reset-db", action="store_true", help="Wipe DB volume first (docker compose down -v)")
    p_seed.add_argument("--rebuild", action="store_true", help="Rebuild images before seeding")


    p_up = sub.add_parser("up", help="Start db+api, optionally run ingest, then run frontend dev (default)")
    p_up.add_argument("--ingest", action="store_true", help="Run ingest once after db+api are up")
    p_up.add_argument("--reset-db", action="store_true", help="Wipe DB volume first (docker compose down -v)")
    p_up.add_argument("--rebuild", action="store_true", help="Rebuild images (docker compose up --build)")
    p_up.add_argument("--no-npm", action="store_true", help="Do not run frontend dev (containers only)")

    p_down = sub.add_parser("down", help="Stop containers (optionally wipe DB volume)")
    p_down.add_argument("--reset-db", action="store_true", help="Also wipe DB volume (docker compose down -v)")

    p_test = sub.add_parser("test", help="Run all tests: db, api, perf, ui (starts backend if needed)")
    p_test.add_argument("--reset-db", action="store_true", help="Wipe DB volume first (docker compose down -v)")
    p_test.add_argument("--rebuild", action="store_true", help="Rebuild images before running tests")
    p_test.add_argument("--ingest", action="store_true", help="Run ingest once before tests")

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
    elif args.cmd == "test":
        tests(reset_db=args.reset_db, rebuild=args.rebuild, ingest=args.ingest)
    elif args.cmd == "seed":
        seed_db(reset_db=args.reset_db, rebuild=args.rebuild)



if __name__ == "__main__":
    main()
