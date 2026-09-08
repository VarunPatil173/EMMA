from dataclasses import dataclass


@dataclass(frozen=True)
class Memory:
    content: str