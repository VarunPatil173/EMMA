import numpy as np
import pytest

from emma.perception.audio.recognizer import WhisperRecognizer
from emma.perception.audio.speech_segment import SpeechSegment


class FakeWhisperModel:
    def transcribe(self, samples, language=None, vad_filter=False):
        class FakeSegment:
            text = "Open YouTube"

        return [FakeSegment()], None


def test_recognizer_requires_start():

    recognizer = WhisperRecognizer()

    segment = SpeechSegment(
        samples=np.zeros(1600, dtype=np.float32),
        sample_rate=16_000,
    )

    with pytest.raises(RuntimeError):
        recognizer.transcribe(segment)


def test_recognizer_transcribes_segment():

    recognizer = WhisperRecognizer()

    recognizer._model = FakeWhisperModel()

    segment = SpeechSegment(
        samples=np.zeros(1600, dtype=np.float32),
        sample_rate=16_000,
    )

    result = recognizer.transcribe(segment)

    assert result.text == "Open YouTube"