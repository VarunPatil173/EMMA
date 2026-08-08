"""
Input Source

Defines every supported perception input source.
"""

from enum import Enum


class InputSource(str, Enum):
    """
    Supported perception input sources.
    """

    AUDIO = "audio"
    TEXT = "text"
    VISION = "vision"
    SCREEN = "screen"
    SENSOR = "sensor"