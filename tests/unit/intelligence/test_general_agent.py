import pytest

from emma.intelligence.general_agent import GeneralAgent
from emma.perception.input.text_input import TextInput


@pytest.mark.anyio
async def test_general_agent_responds_to_text():
    agent = GeneralAgent()
    text_input = TextInput()

    event = text_input.create_event("Hello EMMA")

    response = await agent.run(event)

    assert response == "You said: Hello EMMA"