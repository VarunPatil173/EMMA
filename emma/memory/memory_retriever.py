from emma.memory.memory import Memory


class MemoryRetriever:
    """Retrieves memories relevant to a user's message."""

    def __init__(self, max_results: int = 5) -> None:
        self._max_results = max_results

    def retrieve(
        self,
        query: str,
        memories: list[Memory],
    ) -> list[Memory]:
        """Return the most relevant memories for the query."""

        query_words = self._tokenize(query)

        if not query_words:
            return []

        scored_memories: list[tuple[int, Memory]] = []

        for memory in memories:
            memory_words = self._tokenize(memory.content)

            score = len(query_words & memory_words)

            if score > 0:
                scored_memories.append(
                    (score, memory)
                )

        scored_memories.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            memory
            for _, memory in scored_memories[:self._max_results]
        ]

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        """Convert text into normalized words."""

        return {
            word.strip(".,!?;:\"'()[]{}").lower()
            for word in text.split()
            if word.strip(".,!?;:\"'()[]{}")
        }