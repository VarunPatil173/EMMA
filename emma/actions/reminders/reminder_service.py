import asyncio
from collections.abc import Callable
from datetime import datetime

from emma.actions.reminders.reminder import Reminder
from emma.actions.reminders.reminder_repository import ReminderRepository
from emma.runtime.base_service import BaseService


class ReminderService(BaseService):
    """Monitors reminders and processes those that become due."""

    def __init__(
        self,
        repository: ReminderRepository,
        handler: Callable[[Reminder], None],
        poll_interval: float = 1.0,
    ) -> None:
        super().__init__(
            name="reminder_service",
            description="Monitors and processes due reminders.",
        )

        self._repository = repository
        self._handler = handler
        self._poll_interval = poll_interval
        self._task: asyncio.Task | None = None
        self._running = False

    async def initialize(self) -> None:
        self._running = False

    async def start(self) -> None:
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(
            self._run()
        )

    async def stop(self) -> None:
        if not self._running:
            return

        self._running = False

        if self._task is not None:
            await self._task
            self._task = None

    async def _run(self) -> None:
        while self._running:
            self._process_due_reminders()

            await asyncio.sleep(
                self._poll_interval
            )

    def _process_due_reminders(self) -> None:
        current_time = datetime.now()

        reminders = self._repository.get_due(
            current_time
        )

        for reminder in reminders:
            self._handler(reminder)