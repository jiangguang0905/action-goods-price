import sqlite3
from datetime import timedelta
from pathlib import Path

from config import now

Row = tuple[str, float, float]
Record = tuple[str, str, float, float]


def init(db: Path) -> None:
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS prices (spuid TEXT, date TEXT, jd_price REAL, final_price REAL, PRIMARY KEY (spuid, date))")


def save_all(db: Path, records: list[Record]) -> None:
    with sqlite3.connect(db) as conn:
        conn.executemany("INSERT OR REPLACE INTO prices VALUES (?, ?, ?, ?)", records)


def recent(db: Path, spuid: str, days: int) -> list[Row]:
    start = (now().date() - timedelta(days=days - 1)).isoformat()
    with sqlite3.connect(db) as conn:
        rows = conn.execute("SELECT date, jd_price, final_price FROM prices WHERE spuid = ? AND date >= ? ORDER BY date ASC", (spuid, start)).fetchall()
    return rows
