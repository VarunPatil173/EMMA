import numpy as np

from emma.perception.audio.segmenter import SpeechSegmenter


class FakeVAD:
    def __init__(self, results):
        self.results = iter(results)

    def is_speech(self, samples):
        return next(self.results)


def test_segmenter_creates_segment_after_silence():

    frame = np.ones(1600, dtype=np.float32)

    vad = FakeVAD(
        [
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ]
    )

    segmenter = SpeechSegmenter(
        vad=vad,
        sample_rate=16_000,
        silence_duration=0.5,
    )

    # Speech begins.
    assert segmenter.process(frame) is None
    assert segmenter.process(frame) is None

    # First four silence frames.
    assert segmenter.process(frame) is None
    assert segmenter.process(frame) is None
    assert segmenter.process(frame) is None
    assert segmenter.process(frame) is None

    # Fifth silence frame completes the 0.5 second silence.
    segment = segmenter.process(frame)

    assert segment is not None
    assert segment.sample_rate == 16_000
    assert segment.duration == 0.2