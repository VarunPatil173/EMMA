"""
EMMA Entry Point

Starts the EMMA application.

Author: Varun Patil
"""

import asyncio

from emma.perception.audio.capture import AudioCapture
from emma.perception.audio.recognizer import WhisperRecognizer
from emma.perception.audio.segmenter import SpeechSegmenter
from emma.perception.audio.stream import AudioStream
from emma.perception.audio.vad import VoiceActivityDetector
from emma.perception.audio.worker import PerceptionWorker
from emma.perception.engine import PerceptionEngine
from emma.perception.input.audio_input import AudioInput
from emma.perception.perception_service import PerceptionService
from emma.runtime.application import Application
from emma.runtime.dummy_service import DummyService


async def main() -> None:
    """Main entry point."""

    app = Application()

    # Build perception dependencies
    capture = AudioCapture()
    stream = AudioStream(capture)

    vad = VoiceActivityDetector()
    segmenter = SpeechSegmenter(vad)

    recognizer = WhisperRecognizer()
    audio_input = AudioInput()
    engine = PerceptionEngine()

    worker = PerceptionWorker(
        stream=stream,
        segmenter=segmenter,
        recognizer=recognizer,
        audio_input=audio_input,
        engine=engine,
    )

    perception = PerceptionService(worker)

    # Register services
    app.register_service("dummy", DummyService())
    app.register_service("perception", perception)

    try:
        await app.start()

        input("\nPress Enter to shut down EMMA...\n")

    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())