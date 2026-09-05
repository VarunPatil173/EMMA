from emma.intelligence.personality import emma_personality
from emma.intelligence.personality_prompt import build_personality_prompt


def test_emma_personality_defaults():
    assert emma_personality.name == "EMMA"
    assert emma_personality.user_title == "sir"
    assert "concise" in emma_personality.response_style


def test_emma_personality_prompt_contains_core_rules():
    prompt = build_personality_prompt(emma_personality)

    assert "EMMA" in prompt
    assert "sir" in prompt
    assert "generic question-and-answer chatbot" in prompt
    assert "briefly" in prompt