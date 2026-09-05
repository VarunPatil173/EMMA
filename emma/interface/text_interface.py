"""
Terminal text interface for EMMA.
"""

from __future__ import annotations

from emma.intelligence.agent import Agent
from emma.perception.engine import PerceptionEngine


class TextInterface:
    """Interactive terminal interface for EMMA."""

    def __init__(
        self,
        engine: PerceptionEngine,
        agent: Agent,
    ) -> None:
        self.engine = engine
        self.agent = agent

    async def run(self) -> None:
        """Run the interactive text loop."""

        print("\nEMMA is ready.")
        print("Type 'exit' to shut down.\n")

        while True:
            text = input("You: ").strip()

            if text.lower() in {"exit", "quit"}:
                break

            if not text:
                continue

            event = await self.engine.process_text(text)
            print("EMMA: ", end="", flush=True)

            async for chunk in self.agent.stream(event):
                print(chunk, end="", flush=True)

            print("\n")