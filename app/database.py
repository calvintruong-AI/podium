import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

_DB_PATH = Path(os.environ.get("DATA_DIR", "data")) / "podium.db"


def _connect() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(_DB_PATH)


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                track     TEXT    NOT NULL,
                prompt    TEXT    NOT NULL,
                story     TEXT    NOT NULL,
                scores    TEXT    NOT NULL,
                feedback  TEXT    NOT NULL,
                strengths TEXT    NOT NULL,
                drill     TEXT    NOT NULL
            )
        """)


def save_session(track: str, prompt: str, story: str, analysis: dict) -> int:
    with _connect() as conn:
        cursor = conn.execute(
            """INSERT INTO sessions
               (timestamp, track, prompt, story, scores, feedback, strengths, drill)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now().isoformat(),
                track,
                prompt,
                story,
                json.dumps(analysis["scores"]),
                json.dumps(analysis["feedback"]),
                json.dumps(analysis["strengths"]),
                analysis["drill"],
            ),
        )
        return cursor.lastrowid


def get_recent_sessions(limit: int = 10) -> list[dict]:
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
    sessions = []
    for row in rows:
        s = dict(row)
        s["scores"] = json.loads(s["scores"])
        s["feedback"] = json.loads(s["feedback"])
        s["strengths"] = json.loads(s["strengths"])
        sessions.append(s)
    return sessions
