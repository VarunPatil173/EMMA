from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from emma.perception.audio.capture import AudioCapture


def test_audio_capture_configuration():
    capture = AudioCapture(
        sample_rate=16_000,
        channels=1,
        frame_duration=0.1,
    )

    assert capture.sample_rate == 16_000
    assert capture.channels == 1
    assert capture._frame_samples == 1_600


def test_audio_capture_requires_start():
    capture = AudioCapture()

    with pytest.raises(RuntimeError):
        capture.read()


@patch("emma.perception.audio.capture.sd.InputStream")
def test_audio_capture_reads_frame(mock_stream_class):
    mock_stream = MagicMock()

    samples = np.zeros((1_600, 1), dtype=np.float32)

    mock_stream.read.return_value = (
        samples,
        None,
    )

    mock_stream_class.return_value = mock_stream

    capture = AudioCapture()

    capture.start()

    frame = capture.read()

    assert frame.sample_rate == 16_000
    assert len(frame.samples) == 1_600
    assert frame.duration == pytest.approx(0.1)

    capture.stop()