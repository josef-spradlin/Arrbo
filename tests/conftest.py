from dotenv import load_dotenv
import os
import psycopg
import pytest

load_dotenv(".env.test")

@pytest.fixture(scope="session")
def db_conn():
    conn = psycopg.connect(
        host=os.getenv("ARRBO_DB_HOST", "localhost"),
        port=os.getenv("ARRBO_DB_PORT", "5432"),
        dbname=os.getenv("ARRBO_DB_NAME", "arrbo"),
        user=os.getenv("ARRBO_DB_USER", "arrbo"),
        password=os.getenv("ARRBO_DB_PASSWORD", ""),
    )
    yield conn
    conn.close()

@pytest.fixture
def db_cursor(db_conn):
    with db_conn.cursor() as cur:
        yield cur
