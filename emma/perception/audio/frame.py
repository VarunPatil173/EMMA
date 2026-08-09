"""
Audio frame primitives for EMMA perception.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class AudioFrame:
    """
    A single chunk of microphone audio.

    Attributes:
        samples: Audio samples as a NumPy array.
        sample_rate: Samples per second.
        timestamp: Time at which the frame was captured.
    """

    samples: np.ndarray
    sample_rate: int
    timestamp: float

    @property
    def duration(self) -> float:
        """Return the duration of this audio frame in seconds."""

        return len(self.samples) /  self.sample_rate