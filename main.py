"""
EMMA Entry Point

Starts the EMMA application.

Author: Varun Patil
"""

import asyncio

from emma.perception.engine import PerceptionEngine
from emma.perception.perception_service import PerceptionService
from emma.runtime.application import Application
from emma.runtime.dummy_service import DummyService


async def main() -> None:
    """Main entry point."""

    app = Application()

    # Build perception engine
    engine = PerceptionEngine()

    # Create perception service without audio worker.
    perception = PerceptionService(
        engine=engine,
    )

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