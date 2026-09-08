from emma.memory.memory import Memory
from emma.memory.memory_retriever import MemoryRetriever
from emma.memory.sqlite_store import SQLiteMemoryStore


class MemoryManager:
    """High-level interface for EMMA's persistent memory."""

    def __init__(
        self,
        store: SQLiteMemoryStore,
        retriever: MemoryRetriever | None = None,
    ) -> None:
        self._store = store
        self._retriever = retriever or MemoryRetriever()

    def remember(self, content: str) -> None:
        content = content.strip()

        if not content:
            return

        self._store.save(
            Memory(content=content)
        )

    def recall(self) -> list[Memory]:
        """Return all stored long-term memories."""
        return self._store.get_all()

    def retrieve(self, query: str) -> list[Memory]:
        """Return memories relevant to the user's query."""
        memories = self.recall()

        return self._retriever.retrieve(
            query=query,
            memories=memories,
        )

    def forget_all(self) -> None:
        self._store.delete_all()