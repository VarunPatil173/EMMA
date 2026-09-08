from emma.memory.memory import Memory
from emma.memory.sqlite_store import SQLiteMemoryStore


def test_memory_is_saved_and_retrieved(tmp_path):
    database_path = tmp_path / "emma.db"

    store = SQLiteMemoryStore(str(database_path))

    store.save(
        Memory(
            content="User prefers EMMA to address him as sir."
        )
    )

    memories = store.get_all()

    assert len(memories) == 1
    assert memories[0].content == (
        "User prefers EMMA to address him as sir."
    )


def test_memories_preserve_order(tmp_path):
    database_path = tmp_path / "emma.db"

    store = SQLiteMemoryStore(str(database_path))

    store.save(Memory(content="First memory"))
    store.save(Memory(content="Second memory"))

    memories = store.get_all()

    assert [memory.content for memory in memories] == [
        "First memory",
        "Second memory",
    ]


def test_memory_persists_after_store_is_recreated(tmp_path):
    database_path = tmp_path / "emma.db"

    store = SQLiteMemoryStore(str(database_path))

    store.save(
        Memory(
            content="This should survive a restart."
        )
    )

    # Simulate EMMA shutting down and starting again.
    new_store = SQLiteMemoryStore(str(database_path))

    memories = new_store.get_all()

    assert len(memories) == 1
    assert memories[0].content == (
        "This should survive a restart."
    )


def test_delete_all_memories(tmp_path):
    database_path = tmp_path / "emma.db"

    store = SQLiteMemoryStore(str(database_path))

    store.save(Memory(content="Memory one"))
    store.save(Memory(content="Memory two"))

    store.delete_all()

    assert store.get_all() == []