"""
Voice Activity Detection for EMMA perception.
"""

from __future__ import annotations

import numpy as np
import torch

from emma.core.logger import get_logger


logger = get_logger(__name__)


class VoiceActivityDetector:
    """
    Detects whether an audio frame contains human speech.

    Uses the pretrained Silero VAD model.
    """

    def __init__(
        self,
        sample_rate: int = 16_000,
        threshold: float = 0.5,
    ) -> None:
        self.sample_rate = sample_rate
        self.threshold = threshold

        self._model = None

        self._load_model()

    def _load_model(self) -> None:
        """Load the pretrained Silero VAD model."""

        from silero_vad import load_silero_vad

        self._model = load_silero_vad()

        logger.info(
            "Silero VAD loaded at %d Hz.",
            self.sample_rate,
        )

    def is_speech(self, samples: np.ndarray) -> bool:
        """
        Determine whether an audio frame contains speech.

        Args:
            samples: Float32 audio samples.

        Returns:
            True if speech probability exceeds the threshold.
        """

        if samples.size == 0:
            return False

        audio = torch.from_numpy(
            samples.astype(np.float32)
        )

        probability = self._model(
            audio,
            self.sample_rate,
        ).item()

        return probability >= self.threshold