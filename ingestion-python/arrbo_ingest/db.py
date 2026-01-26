from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

import psycopg


def _build_dsn() -> str:
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    db = os.getenv("POSTGRES_DB", "arrbo")
    user = os.getenv("POSTGRES_USER", "arrbo")
    password = os.getenv("POSTGRES_PASSWORD", "arrbo_password")
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


@contextmanager
def connect(_: str | None = None) -> Iterator[psycopg.Connection]:
    dsn = _build_dsn()
    conn = psycopg.connect(dsn)
    try:
        # optional but nice
        conn.execute("SET TIME ZONE 'UTC';")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
