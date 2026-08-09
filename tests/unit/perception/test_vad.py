import numpy as np

from emma.perception.audio.vad import VoiceActivityDetector


def test_vad_initializes():
    vad = VoiceActivityDetector()

    assert vad.sample_rate == 16_000
    assert vad.threshold == 0.5


def test_empty_audio_is_not_speech():
    vad = VoiceActivityDetector()

    samples = np.array([], dtype=np.float32)

    assert vad.is_speech(samples) is False