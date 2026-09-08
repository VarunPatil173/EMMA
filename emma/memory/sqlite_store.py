import sqlite3
from pathlib import Path

from emma.memory.memory import Memory


class SQLiteMemoryStore:
    """Persistent memory storage backed by SQLite."""

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
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL
                )
                """
            )

    def save(self, memory: Memory) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO memories (content)
                VALUES (?)
                """,
                (memory.content,),
            )

    def get_all(self) -> list[Memory]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT content
                FROM memories
                ORDER BY id ASC
                """
            ).fetchall()

        return [
            Memory(content=row[0])
            for row in rows
        ]

    def delete_all(self) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM memories"
            )