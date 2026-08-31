import asyncio

from emma.interface.text_interface import TextInterface
from emma.perception.engine import PerceptionEngine


async def main():
    engine = PerceptionEngine()

    await engine.start()

    interface = TextInterface(engine)

    await interface.run()

    await engine.stop()


asyncio.run(main())