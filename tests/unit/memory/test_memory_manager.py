from emma.memory.memory import Memory
from emma.memory.memory_manager import MemoryManager


class FakeMemoryStore:
    def __init__(self) -> None:
        self.memories: list[Memory] = []

    def save(self, memory: Memory) -> None:
        self.memories.append(memory)

    def get_all(self) -> list[Memory]:
        return list(self.memories)

    def delete_all(self) -> None:
        self.memories.clear()


def test_remember_saves_memory():
    store = FakeMemoryStore()
    manager = MemoryManager(store)

    manager.remember("User likes robotics.")

    memories = manager.recall()

    assert len(memories) == 1
    assert memories[0].content == "User likes robotics."


def test_remember_strips_whitespace():
    store = FakeMemoryStore()
    manager = MemoryManager(store)

    manager.remember("  User likes robotics.  ")

    memories = manager.recall()

    assert memories[0].content == "User likes robotics."


def test_empty_memory_is_not_saved():
    store = FakeMemoryStore()
    manager = MemoryManager(store)

    manager.remember("   ")

    assert manager.recall() == []


def test_forget_all_clears_memory():
    store = FakeMemoryStore()
    manager = MemoryManager(store)

    manager.remember("Memory one.")
    manager.remember("Memory two.")

    manager.forget_all()

    assert manager.recall() == []