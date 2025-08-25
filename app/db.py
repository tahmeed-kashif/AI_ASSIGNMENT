import os
import sqlite3
from typing import Iterable, Optional


def ensure_dir_exists(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def get_connection(db_path: str) -> sqlite3.Connection:
    ensure_dir_exists(db_path)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL UNIQUE,
            name TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()


def add_subscriber(conn: sqlite3.Connection, phone: str, name: Optional[str]) -> None:
    conn.execute(
        """
        INSERT INTO subscribers (phone, name, active)
        VALUES (?, ?, 1)
        ON CONFLICT(phone) DO UPDATE SET
            name=excluded.name,
            active=1,
            updated_at=CURRENT_TIMESTAMP
        ;
        """,
        (phone, name),
    )
    conn.commit()


def set_active(conn: sqlite3.Connection, phone: str, active: bool) -> None:
    conn.execute(
        "UPDATE subscribers SET active=?, updated_at=CURRENT_TIMESTAMP WHERE phone=?",
        (1 if active else 0, phone),
    )
    conn.commit()


def list_active_subscribers(conn: sqlite3.Connection) -> Iterable[sqlite3.Row]:
    return conn.execute("SELECT phone, name FROM subscribers WHERE active=1 ORDER BY id ASC").fetchall()


def list_all_subscribers(conn: sqlite3.Connection) -> Iterable[sqlite3.Row]:
    return conn.execute(
        "SELECT phone, name, active, created_at, updated_at FROM subscribers ORDER BY id ASC"
    ).fetchall()

