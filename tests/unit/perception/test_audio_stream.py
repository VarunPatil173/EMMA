import asyncio
from unittest.mock import MagicMock

import numpy as np
import pytest

from emma.perception.audio.capture import AudioCapture
from emma.perception.audio.stream import AudioStream


@pytest.mark.anyio
async def test_audio_stream_reads_frames():
    capture = MagicMock(spec=AudioCapture)

    capture.read.return_value = MagicMock(
        samples=np.zeros(1600, dtype=np.float32),
        sample_rate=16000,
        timestamp=0.0,
    )

    stream = AudioStream(capture)

    await stream.start()

    frame = await asyncio.wait_for(
        stream.read(),
        timeout=1.0,
    )

    assert frame.sample_rate == 16000
    assert len(frame.samples) == 1600

    await stream.stop()