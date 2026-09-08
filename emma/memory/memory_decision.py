class MemoryDecision:
    """Determines whether a user message explicitly requests memory storage."""

    PREFIX = "remember that"

    @classmethod
    def should_remember(cls, text: str) -> bool:
        return text.strip().lower().startswith(cls.PREFIX)

    @classmethod
    def extract_memory(cls, text: str) -> str | None:
        text = text.strip()

        if not cls.should_remember(text):
            return None

        memory = text[len(cls.PREFIX):].strip()

        if not memory:
            return None

        return memory