"""
Input Event

Represents a normalized perception event.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from emma.perception.shared.input_source import InputSource


class InputEvent(BaseModel):
    """
    Represents a normalized user input.
    """

    source: InputSource

    text: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)