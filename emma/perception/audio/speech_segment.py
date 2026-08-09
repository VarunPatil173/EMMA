"""
Speech segment model for EMMA perception.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SpeechSegment:
    """
    Represents one continuous segment of human speech.
    """

    samples: np.ndarray
    sample_rate: int

    @property
    def duration(self) -> float:
        """Return segment duration in seconds."""

        if self.sample_rate <= 0:
            return 0.0

        return len(self.samples) / self.sample_rate