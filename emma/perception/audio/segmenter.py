"""
Speech segmentation for EMMA perception.
"""

from __future__ import annotations

import numpy as np

from emma.perception.audio.speech_segment import SpeechSegment
from emma.perception.audio.vad import VoiceActivityDetector


class SpeechSegmenter:
    """
    Converts audio frames into continuous speech segments.
    """

    def __init__(
        self,
        vad: VoiceActivityDetector,
        sample_rate: int = 16_000,
        silence_duration: float = 0.6,
        max_segment_duration: float = 15.0,
    ) -> None:

        self.vad = vad
        self.sample_rate = sample_rate

        self.silence_duration = silence_duration
        self.max_segment_duration = max_segment_duration

        self._frames: list[np.ndarray] = []
        self._speech_active = False
        self._silence_samples = 0

    def process(
        self,
        samples: np.ndarray,
    ) -> SpeechSegment | None:
        """
        Process one audio frame.

        Returns a SpeechSegment when a speech segment ends.
        Otherwise returns None.
        """

        if samples.size == 0:
            return None

        is_speech = self.vad.is_speech(samples)

        if is_speech:
            self._frames.append(samples.copy())
            self._speech_active = True
            self._silence_samples = 0

            if self._duration() >= self.max_segment_duration:
                return self._finish_segment()

            return None

        if not self._speech_active:
            return None

        self._silence_samples += len(samples)

        if (
            self._silence_samples
            >= self.silence_duration * self.sample_rate
        ):
            return self._finish_segment()

        return None

    def _duration(self) -> float:
        """Return the duration of the current segment."""

        total_samples = sum(
            len(frame)
            for frame in self._frames
        )

        return total_samples / self.sample_rate

    def _finish_segment(self) -> SpeechSegment:
        """Finish and return the current speech segment."""

        samples = np.concatenate(self._frames)

        segment = SpeechSegment(
            samples=samples,
            sample_rate=self.sample_rate,
        )

        self._frames.clear()
        self._speech_active = False
        self._silence_samples = 0

        return segment
    