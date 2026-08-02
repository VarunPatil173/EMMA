"""
EMMA Configuration System

This module manages all configuration for EMMA.

Author: Varun Patil
"""

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# -----------------------------
# Application Settings
# -----------------------------
class AppSettings(BaseModel):
    """General application settings."""

    name: str = "EMMA"
    version: str = "0.1.0"
    debug: bool = True


# -----------------------------
# Language Model Settings
# -----------------------------
class LLMSettings(BaseModel):
    """LLM configuration."""

    provider: str = "gemini"
    model: str = "gemini-2.5-pro"
    api_key: str = ""


# -----------------------------
# Audio Settings
# -----------------------------
class AudioSettings(BaseModel):
    """Audio configuration."""

    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024


# -----------------------------
# Text To Speech Settings
# -----------------------------
class TTSSettings(BaseModel):
    """Text-to-Speech configuration."""

    voice: str = "en-US-AvaMultilingualNeural"
    rate: str = "+8%"
    pitch: str = "+0Hz"
    volume: str = "+0%"


# -----------------------------
# Database Settings
# -----------------------------
class DatabaseSettings(BaseModel):
    """Database configuration."""

    sqlite_path: str = "data/sqlite/emma.db"


# -----------------------------
# Main Settings
# -----------------------------
class Settings(BaseSettings):
    """
    Root configuration object.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app: AppSettings = AppSettings()
    llm: LLMSettings = LLMSettings()
    audio: AudioSettings = AudioSettings()
    tts: TTSSettings = TTSSettings()
    database: DatabaseSettings = DatabaseSettings()


settings = Settings()