import sqlite3
from datetime import datetime
from pathlib import Path

from emma.actions.reminders.reminder import (
    Reminder,
    ReminderStatus,
)


class ReminderRepository:
    """Persistent storage for reminders backed by SQLite."""

    def __init__(self, database_path: str) -> None:
        self._database_path = Path(database_path)

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._database_path)

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    scheduled_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save(self, reminder: Reminder) -> Reminder:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO reminders (
                    title,
                    scheduled_at,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    reminder.title,
                    reminder.scheduled_at.isoformat(),
                    reminder.status.value,
                    reminder.created_at.isoformat(),
                ),
            )

            reminder_id = cursor.lastrowid

        return Reminder(
            id=reminder_id,
            title=reminder.title,
            scheduled_at=reminder.scheduled_at,
            status=reminder.status,
            created_at=reminder.created_at,
        )

    def get(self, reminder_id: int) -> Reminder | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    id,
                    title,
                    scheduled_at,
                    status,
                    created_at
                FROM reminders
                WHERE id = ?
                """,
                (reminder_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_reminder(row)

    def get_all(self) -> list[Reminder]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    title,
                    scheduled_at,
                    status,
                    created_at
                FROM reminders
                ORDER BY id ASC
                """
            ).fetchall()

        return [
            self._row_to_reminder(row)
            for row in rows
        ]

    def update(self, reminder: Reminder) -> None:
        if reminder.id is None:
            raise ValueError(
                "Cannot update a reminder without an id."
            )

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE reminders
                SET
                    title = ?,
                    scheduled_at = ?,
                    status = ?,
                    created_at = ?
                WHERE id = ?
                """,
                (
                    reminder.title,
                    reminder.scheduled_at.isoformat(),
                    reminder.status.value,
                    reminder.created_at.isoformat(),
                    reminder.id,
                ),
            )

    def delete(self, reminder_id: int) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                DELETE FROM reminders
                WHERE id = ?
                """,
                (reminder_id,),
            )

    @staticmethod
    def _row_to_reminder(row: tuple) -> Reminder:
        return Reminder(
            id=row[0],
            title=row[1],
            scheduled_at=datetime.fromisoformat(row[2]),
            status=ReminderStatus(row[3]),
            created_at=datetime.fromisoformat(row[4]),
        )