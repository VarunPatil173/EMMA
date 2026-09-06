from emma.intelligence.conversation import Conversation


def test_conversation_starts_empty():
    conversation = Conversation()

    assert conversation.get_messages() == []


def test_conversation_stores_user_message():
    conversation = Conversation()

    conversation.add_user_message("Hello EMMA")

    messages = conversation.get_messages()

    assert len(messages) == 1
    assert messages[0].role == "user"
    assert messages[0].content == "Hello EMMA"


def test_conversation_stores_assistant_message():
    conversation = Conversation()

    conversation.add_assistant_message("Hello, sir.")

    messages = conversation.get_messages()

    assert len(messages) == 1
    assert messages[0].role == "assistant"
    assert messages[0].content == "Hello, sir."


def test_conversation_preserves_order():
    conversation = Conversation()

    conversation.add_user_message("Hello")
    conversation.add_assistant_message("Hello, sir.")
    conversation.add_user_message("How are you?")

    messages = conversation.get_messages()

    assert [message.role for message in messages] == [
        "user",
        "assistant",
        "user",
    ]


def test_conversation_clear():
    conversation = Conversation()

    conversation.add_user_message("Hello")
    conversation.add_assistant_message("Hello, sir.")

    conversation.clear()

    assert conversation.get_messages() == []