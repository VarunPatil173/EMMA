import asyncio

import numpy as np
import pytest

from emma.perception.audio.speech_segment import SpeechSegment
from emma.perception.audio.worker import PerceptionWorker
from emma.perception.audio.recognizer import Transcript


class FakeStream:

    def __init__(self):
        self.started = False
        self.stopped = False
        self._queue = asyncio.Queue()

    async def start(self):
        self.started = True

    async def read(self):
        return await self._queue.get()

    async def stop(self):
        self.stopped = True


class FakeSegmenter:

    def process(self, samples):
        return SpeechSegment(
            samples=np.zeros(1600, dtype=np.float32),
            sample_rate=16_000,
        )


class FakeRecognizer:

    def __init__(self):
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def transcribe(self, segment):
        return Transcript(text="Open YouTube")

    def stop(self):
        self.stopped = True


@pytest.mark.anyio
async def test_perception_worker_lifecycle():

    stream = FakeStream()
    segmenter = FakeSegmenter()
    recognizer = FakeRecognizer()

    worker = PerceptionWorker(
        stream=stream,
        segmenter=segmenter,
        recognizer=recognizer,
    )

    await worker.start()

    assert stream.started
    assert recognizer.started

    await worker.stop()

    assert stream.stopped
    assert recognizer.stopped