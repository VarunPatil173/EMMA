"""
Microphone audio capture for EMMA perception.
"""

from __future__ import annotations

import time

import numpy as np
import sounddevice as sd

from emma.core.logger import get_logger
from emma.perception.audio.frame import AudioFrame


logger = get_logger(__name__)


class AudioCapture:
    """
    Captures raw audio from the system microphone.
    """

    def __init__(
        self,
        sample_rate: int = 16_000,
        channels: int = 1,
        frame_duration: float = 0.1,
    ) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.frame_duration = frame_duration

        self._stream: sd.InputStream | None = None

        self._frame_samples = int(
            self.sample_rate * self.frame_duration
        )

    def start(self) -> None:
        """
        Start microphone capture.
        """

        if self._stream is not None:
            return

        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=self._frame_samples,
        )

        self._stream.start()

        logger.info(
            "Audio capture started: %d Hz, %d channel(s)",
            self.sample_rate,
            self.channels,
        )

    def read(self) -> AudioFrame:
        """
        Read one frame of microphone audio.
        """

        if self._stream is None:
            raise RuntimeError("Audio capture is not running.")

        samples, _ = self._stream.read(self._frame_samples)

        samples = np.asarray(
            samples,
            dtype=np.float32,
        ).reshape(-1)

        return AudioFrame(
            samples=samples,
            sample_rate=self.sample_rate,
            timestamp=time.perf_counter(),
        )

    def stop(self) -> None:
        """
        Stop microphone capture.
        """

        if self._stream is None:
            return

        self._stream.stop()
        self._stream.close()
        self._stream = None

        logger.info("Audio capture stopped.")