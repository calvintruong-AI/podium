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
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT    NOT NULL,
                track           TEXT    NOT NULL,
                prompt          TEXT    NOT NULL,
                story           TEXT    NOT NULL,
                scores          TEXT    NOT NULL,
                feedback        TEXT    NOT NULL,
                strengths       TEXT    NOT NULL,
                drill           TEXT    NOT NULL,
                drill_dimension TEXT    DEFAULT '',
                drill_completed INTEGER DEFAULT 0
            )
        """)
        # Migrate existing databases that predate drill tracking columns
        for col, definition in [
            ("drill_dimension", "TEXT DEFAULT ''"),
            ("drill_completed", "INTEGER DEFAULT 0"),
        ]:
            try:
                conn.execute(f"ALTER TABLE sessions ADD COLUMN {col} {definition}")
            except sqlite3.OperationalError:
                pass

        conn.execute("""
            CREATE TABLE IF NOT EXISTS training_sessions (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT    NOT NULL,
                dimension       TEXT    NOT NULL,
                difficulty      TEXT    NOT NULL,
                instruction     TEXT    NOT NULL,
                source_material TEXT    NOT NULL,
                response        TEXT    NOT NULL,
                score           INTEGER NOT NULL,
                feedback        TEXT    NOT NULL,
                what_worked     TEXT    NOT NULL,
                try_instead     TEXT    NOT NULL
            )
        """)


def save_session(track: str, prompt: str, story: str, analysis: dict) -> int:
    scores = analysis["scores"]
    drill_dimension = min(
        ["structure", "language", "pacing", "emotion"],
        key=lambda d: scores[d],
    ).capitalize()
    with _connect() as conn:
        cursor = conn.execute(
            """INSERT INTO sessions
               (timestamp, track, prompt, story, scores, feedback, strengths,
                drill, drill_dimension, drill_completed)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)""",
            (
                datetime.now().isoformat(),
                track,
                prompt,
                story,
                json.dumps(scores),
                json.dumps(analysis["feedback"]),
                json.dumps(analysis["strengths"]),
                analysis["drill"],
                drill_dimension,
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


def get_pending_drill() -> dict | None:
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """SELECT id, drill, drill_dimension FROM sessions
               WHERE drill_completed = 0 ORDER BY timestamp DESC LIMIT 1"""
        ).fetchone()
    return dict(row) if row else None


def mark_drill_complete(session_id: int) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE sessions SET drill_completed = 1 WHERE id = ?", (session_id,)
        )


def save_training_session(
    dimension: str,
    difficulty: str,
    instruction: str,
    source_material: str,
    response: str,
    result: dict,
) -> None:
    with _connect() as conn:
        conn.execute(
            """INSERT INTO training_sessions
               (timestamp, dimension, difficulty, instruction, source_material,
                response, score, feedback, what_worked, try_instead)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now().isoformat(),
                dimension,
                difficulty,
                instruction,
                source_material,
                response,
                result["score"],
                result["feedback"],
                result["what_worked"],
                result["try_instead"],
            ),
        )


def get_recent_training_sessions(limit: int = 10) -> list[dict]:
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM training_sessions ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


def get_coaches_pick() -> str:
    sessions = get_recent_sessions(5)
    if not sessions:
        return "Structure"
    dims = ["structure", "language", "pacing", "emotion"]
    averages = {
        dim: sum(s["scores"][dim] for s in sessions) / len(sessions)
        for dim in dims
    }
    return min(dims, key=lambda d: averages[d]).capitalize()


def get_auto_difficulty(dimension: str) -> str:
    sessions = get_recent_sessions(5)
    if not sessions:
        return "Beginner"
    dim_key = dimension.lower()
    avg = sum(s["scores"].get(dim_key, 50) for s in sessions) / len(sessions)
    if avg <= 50:
        return "Beginner"
    elif avg <= 75:
        return "Intermediate"
    else:
        return "Advanced"
