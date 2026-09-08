from emma.memory.memory import Memory
from emma.memory.memory_retriever import MemoryRetriever


def test_retrieves_relevant_memory() -> None:
    retriever = MemoryRetriever()

    memories = [
        Memory("I am learning Python"),
        Memory("I like playing guitar"),
        Memory("I am building EMMA"),
    ]

    results = retriever.retrieve(
        "What programming language am I learning?",
        memories,
    )

    assert Memory("I am learning Python") in results


def test_ignores_irrelevant_memories() -> None:
    retriever = MemoryRetriever()

    memories = [
        Memory("I am learning Python"),
        Memory("I like playing guitar"),
        Memory("I am building EMMA"),
    ]

    results = retriever.retrieve(
        "What instrument do I play?",
        memories,
    )

    assert Memory("I like playing guitar") in results


def test_returns_empty_for_no_match() -> None:
    retriever = MemoryRetriever()

    memories = [
        Memory("I am learning Python"),
        Memory("I am building EMMA"),
    ]

    results = retriever.retrieve(
        "What is my favorite food?",
        memories,
    )

    assert results == []


def test_limits_number_of_results() -> None:
    retriever = MemoryRetriever(max_results=2)

    memories = [
        Memory("I am learning Python programming"),
        Memory("I use Python for EMMA"),
        Memory("Python is one of my skills"),
        Memory("I am building EMMA"),
    ]

    results = retriever.retrieve(
        "Tell me about Python",
        memories,
    )

    assert len(results) == 2