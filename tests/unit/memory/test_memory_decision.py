from emma.memory.memory_decision import MemoryDecision


def test_remember_command_is_detected():
    assert MemoryDecision.should_remember(
        "Remember that I like robotics."
    )


def test_remember_command_is_case_insensitive():
    assert MemoryDecision.should_remember(
        "REMEMBER THAT I like robotics."
    )


def test_normal_message_is_not_memory():
    assert not MemoryDecision.should_remember(
        "I like robotics."
    )


def test_memory_is_extracted():
    memory = MemoryDecision.extract_memory(
        "Remember that I like robotics."
    )

    assert memory == "I like robotics."


def test_memory_extraction_strips_whitespace():
    memory = MemoryDecision.extract_memory(
        "  Remember that   I like robotics.  "
    )

    assert memory == "I like robotics."


def test_empty_memory_is_ignored():
    assert MemoryDecision.extract_memory(
        "Remember that"
    ) is None