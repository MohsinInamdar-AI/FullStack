"""
db.py - SQLite database layer for storing image generation history.
"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "generations.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the generations table if it doesn't exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            negative_prompt TEXT,
            model_id TEXT NOT NULL,
            image_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_generation(prompt: str, negative_prompt: str, model_id: str, image_path: str) -> int:
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO generations (prompt, negative_prompt, model_id, image_path, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (prompt, negative_prompt, model_id, image_path, datetime.utcnow().isoformat()),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_all_generations(limit: int = 50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM generations ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows


def delete_generation(gen_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM generations WHERE id = ?", (gen_id,))
    conn.commit()
    conn.close()