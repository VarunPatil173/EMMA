import asyncio

import numpy as np
import pytest

from emma.perception.audio.recognizer import Transcript
from emma.perception.audio.speech_segment import SpeechSegment
from emma.perception.audio.worker import PerceptionWorker
from emma.perception.input.audio_input import AudioInput


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


class FakeEngine:
    def __init__(self):
        self.events = []

    async def process(self, event):
        self.events.append(event)
        return event


@pytest.mark.anyio
async def test_perception_worker_lifecycle():

    stream = FakeStream()
    segmenter = FakeSegmenter()
    recognizer = FakeRecognizer()
    audio_input = AudioInput()
    engine = FakeEngine()

    worker = PerceptionWorker(
        stream=stream,
        segmenter=segmenter,
        recognizer=recognizer,
        audio_input=audio_input,
        engine=engine,
    )

    await worker.start()

    assert stream.started
    assert recognizer.started

    await worker.stop()

    assert stream.stopped
    assert recognizer.stopped


@pytest.mark.anyio
async def test_perception_worker_sends_event_to_engine():

    stream = FakeStream()
    segmenter = FakeSegmenter()
    recognizer = FakeRecognizer()
    audio_input = AudioInput()
    engine = FakeEngine()

    worker = PerceptionWorker(
        stream=stream,
        segmenter=segmenter,
        recognizer=recognizer,
        audio_input=audio_input,
        engine=engine,
    )

    await worker.start()

    # Put a fake audio frame into the stream.
    frame = type(
        "FakeFrame",
        (),
        {
            "samples": np.zeros(1600, dtype=np.float32),
        },
    )()

    await stream._queue.put(frame)

    # Give the worker a moment to process the frame.
    await asyncio.sleep(0.05)

    assert len(engine.events) == 1

    event = engine.events[0]

    assert event.source.value == "audio"
    assert event.text == "Open YouTube"

    await worker.stop()