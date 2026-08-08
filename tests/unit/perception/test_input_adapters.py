from emma.perception.input.audio_input import AudioInput
from emma.perception.input.text_input import TextInput


def test_text_input_creates_event():
    adapter = TextInput()

    event = adapter.create_event("  Open YouTube  ")

    assert event.source == "text"
    assert event.text == "Open YouTube"


def test_audio_input_creates_event():
    adapter = AudioInput()

    event = adapter.create_event("Open YouTube")

    assert event.source == "audio"
    assert event.text == "Open YouTube"