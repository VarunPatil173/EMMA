import pytest

from emma.intelligence.conversation import Message
from emma.intelligence.general_agent import GeneralAgent
from emma.intelligence.model import ModelProvider
from emma.perception.shared.input_event import InputEvent
from emma.memory.memory_manager import MemoryManager


class FakeModel(ModelProvider):
    def __init__(self) -> None:
        self.last_prompt = None
        self.last_system_prompt = None
        self.last_history = None

    @property
    def name(self) -> str:
        return "fake"

    @property
    def model(self) -> str:
        return "fake-model"

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history: list[Message] | None = None,
    ) -> str:
        self.last_prompt = prompt
        self.last_system_prompt = system_prompt
        self.last_history = history

        return "Hello, sir."

    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
        history: list[Message] | None = None,
    ):
        self.last_prompt = prompt
        self.last_system_prompt = system_prompt
        self.last_history = history

        yield "Hello, "
        yield "sir."

    async def health_check(self) -> bool:
        return True


@pytest.mark.asyncio
async def test_general_agent_responds_to_text():
    model = FakeModel()
    agent = GeneralAgent(model)

    event = InputEvent(
        source="text",
        text="Hello EMMA",
    )

    response = await agent.run(event)

    assert response == "Hello, sir."


@pytest.mark.asyncio
async def test_general_agent_streams_text():
    model = FakeModel()
    agent = GeneralAgent(model)

    event = InputEvent(
        source="text",
        text="Hello EMMA",
    )

    chunks = []

    async for chunk in agent.stream(event):
        chunks.append(chunk)

    assert "".join(chunks) == "Hello, sir."


@pytest.mark.asyncio
async def test_general_agent_stores_conversation():
    model = FakeModel()
    agent = GeneralAgent(model)

    event = InputEvent(
        source="text",
        text="My name is Varun.",
    )

    await agent.run(event)

    messages = agent.get_conversation()

    assert len(messages) == 2

    assert messages[0].role == "user"
    assert messages[0].content == "My name is Varun."

    assert messages[1].role == "assistant"
    assert messages[1].content == "Hello, sir."


@pytest.mark.asyncio
async def test_general_agent_passes_previous_history():
    model = FakeModel()
    agent = GeneralAgent(model)

    first_event = InputEvent(
        source="text",
        text="My name is Varun.",
    )

    await agent.run(first_event)

    second_event = InputEvent(
        source="text",
        text="What is my name?",
    )

    await agent.run(second_event)

    history = model.last_history

    assert history is not None
    assert len(history) == 2

    assert history[0].role == "user"
    assert history[0].content == "My name is Varun."

    assert history[1].role == "assistant"
    assert history[1].content == "Hello, sir."


@pytest.mark.asyncio
async def test_general_agent_stream_stores_conversation():
    model = FakeModel()
    agent = GeneralAgent(model)

    event = InputEvent(
        source="text",
        text="Hello EMMA",
    )

    chunks = []

    async for chunk in agent.stream(event):
        chunks.append(chunk)

    messages = agent.get_conversation()

    assert len(messages) == 2

    assert messages[0].role == "user"
    assert messages[0].content == "Hello EMMA"

    assert messages[1].role == "assistant"
    assert messages[1].content == "Hello, sir."


@pytest.mark.asyncio
async def test_general_agent_can_clear_conversation():
    model = FakeModel()
    agent = GeneralAgent(model)

    event = InputEvent(
        source="text",
        text="Hello EMMA",
    )

    await agent.run(event)

    assert len(agent.get_conversation()) == 2

    agent.clear_conversation()

    assert agent.get_conversation() == []

class FakeMemoryStore:
    def __init__(self) -> None:
        self.memories = []

    def save(self, memory) -> None:
        self.memories.append(memory)

    def get_all(self):
        return list(self.memories)

    def delete_all(self) -> None:
        self.memories.clear()


@pytest.mark.asyncio
async def test_general_agent_saves_explicit_memory():
    store = FakeMemoryStore()
    memory_manager = MemoryManager(store)

    agent = GeneralAgent(
        FakeModel(),
        memory_manager=memory_manager,
    )

    event = InputEvent(
        source="text",
        text="Remember that I like robotics.",
    )

    response = await agent.run(event)

    assert response == "I'll remember that, sir."

    memories = memory_manager.recall()

    assert len(memories) == 1
    assert memories[0].content == "I like robotics."


@pytest.mark.asyncio
async def test_general_agent_does_not_save_normal_message():
    store = FakeMemoryStore()
    memory_manager = MemoryManager(store)

    agent = GeneralAgent(
        FakeModel(),
        memory_manager=memory_manager,
    )

    event = InputEvent(
        source="text",
        text="I like robotics.",
    )

    await agent.run(event)

    assert memory_manager.recall() == []


@pytest.mark.asyncio
async def test_general_agent_stream_saves_explicit_memory():
    store = FakeMemoryStore()
    memory_manager = MemoryManager(store)

    agent = GeneralAgent(
        FakeModel(),
        memory_manager=memory_manager,
    )

    event = InputEvent(
        source="text",
        text="Remember that I love engineering.",
    )

    chunks = []

    async for chunk in agent.stream(event):
        chunks.append(chunk)

    assert "".join(chunks) == "I'll remember that, sir."

    memories = memory_manager.recall()

    assert len(memories) == 1
    assert memories[0].content == "I love engineering."