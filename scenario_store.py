import sqlite3
from contextlib import closing
import json
from datetime import datetime, timezone

DATABASE_FILE = "atlas_scenarios.db"


def initialize_database():
    with closing(sqlite3.connect(DATABASE_FILE)) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                name TEXT NOT NULL,
                failed_equipment TEXT NOT NULL,
                downtime_hours INTEGER NOT NULL,
                selling_price REAL NOT NULL,
                contribution_margin REAL NOT NULL,
                existing_production REAL NOT NULL,
                production_loss REAL NOT NULL,
                recommended_strategy TEXT NOT NULL,
                estimated_impact REAL NOT NULL
            )
        """)


def save_scenario(
    name,
    failed_equipment,
    downtime_hours,
    selling_price,
    contribution_margin,
    existing_production,
    production_loss,
    recommended_strategy,
    estimated_impact
):
    if not name.strip():
        raise ValueError("Scenario name cannot be empty.")

    initialize_database()

    with closing(sqlite3.connect(DATABASE_FILE)) as conn, conn:
        cursor = conn.execute(
            """
            INSERT INTO scenarios (
                created_at,
                name,
                failed_equipment,
                downtime_hours,
                selling_price,
                contribution_margin,
                existing_production,
                production_loss,
                recommended_strategy,
                estimated_impact
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                name.strip(),
                json.dumps(failed_equipment),
                downtime_hours,
                selling_price,
                contribution_margin,
                existing_production,
                production_loss,
                recommended_strategy,
                estimated_impact
            )
        )

        return cursor.lastrowid


def load_scenarios():
    initialize_database()

    with closing(sqlite3.connect(DATABASE_FILE)) as conn, conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            """
            SELECT *
            FROM scenarios
            ORDER BY id DESC
            """
        ).fetchall()

    results = []

    for row in rows:
        scenario = dict(row)
        scenario["failed_equipment"] = json.loads(
            scenario["failed_equipment"]
        )
        results.append(scenario)

    return results
