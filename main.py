"""
EMMA Entry Point

Starts the EMMA application.

Author: Varun Patil
"""

import asyncio
from emma.core.config import settings
from emma.intelligence.general_agent import GeneralAgent
from emma.intelligence.gemini_provider import GeminiProvider
from emma.intelligence.model_router import ModelRouter
from emma.intelligence.ollama_provider import OllamaProvider
from emma.interface.text_interface import TextInterface
from emma.perception.engine import PerceptionEngine
from emma.perception.perception_service import PerceptionService
from emma.runtime.application import Application
from emma.runtime.dummy_service import DummyService
from emma.memory.memory_manager import MemoryManager
from emma.memory.sqlite_store import SQLiteMemoryStore


async def main() -> None:
    """Main entry point."""

    app = Application()

    # Build intelligence
    primary = GeminiProvider()
    fallback = OllamaProvider("qwen3:8b")

    model = ModelRouter(
        primary=primary,
        fallback=fallback,
    )

    memory_store = SQLiteMemoryStore(
        settings.database.sqlite_path
    )

    memory_manager = MemoryManager(memory_store)

    agent = GeneralAgent(
        model,
        memory_manager=memory_manager,
    )

    # Build perception engine
    engine = PerceptionEngine()

    # Build text interface
    interface = TextInterface(
        engine=engine,
        agent=agent,
    )

    # Create perception service without audio worker.
    perception = PerceptionService(
        engine=engine,
    )

    # Register services
    app.register_service("dummy", DummyService())
    app.register_service("perception", perception)

    try:
        await app.start()

        await interface.run()

    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())