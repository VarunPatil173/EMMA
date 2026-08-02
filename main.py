"""
EMMA Entry Point

Starts the EMMA application.

Author: Varun Patil
"""

import asyncio

from emma.runtime.application import Application
from emma.runtime.dummy_service import DummyService


async def main() -> None:
    """
    Main entry point.
    """

    app = Application()

    # Register services
    app.register_service("dummy", DummyService())

    try:
        await app.start()

        input("\nPress Enter to shut down EMMA...\n")

    finally:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())