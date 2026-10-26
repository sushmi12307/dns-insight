
import sqlite3
from pathlib import Path
from datetime import datetime

# Store the database inside the main project's data folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "dns_history.db"


def initialize_database():
    DATA_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS dns_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                record_type TEXT NOT NULL,
                status TEXT NOT NULL,
                records TEXT,
                latency_ms REAL,
                queried_at TEXT NOT NULL
            )
        """)


def save_query(result):
    initialize_database()

    records = ", ".join(result.get("records", []))

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            INSERT INTO dns_history
            (domain, record_type, status, records, latency_ms, queried_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            result.get("domain", ""),
            result.get("record_type", "A"),
            result.get("status", "unknown"),
            records,
            result.get("latency_ms"),
            datetime.now().isoformat(timespec="seconds")
        ))


def get_history(limit=50):
    initialize_database()

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT *
            FROM dns_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]
