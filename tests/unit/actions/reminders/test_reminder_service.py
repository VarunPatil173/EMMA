import asyncio
from datetime import datetime

from emma.actions.reminders.reminder import (
    Reminder,
    ReminderStatus,
)
from emma.actions.reminders.reminder_repository import (
    ReminderRepository,
)
from emma.actions.reminders.reminder_service import (
    ReminderService,
)


def test_service_processes_due_reminder(tmp_path):
    database_path = tmp_path / "emma.db"

    repository = ReminderRepository(
        str(database_path)
    )

    reminder = repository.save(
        Reminder(
            id=None,
            title="Study Physics",
            scheduled_at=datetime.now(),
            status=ReminderStatus.PENDING,
            created_at=datetime.now(),
        )
    )

    processed = []

    def handler(received_reminder):
        processed.append(received_reminder)

    service = ReminderService(
        repository=repository,
        handler=handler,
        poll_interval=0.01,
    )

    async def run_service():
        await service.initialize()
        await service.start()

        await asyncio.sleep(0.05)

        await service.stop()

    asyncio.run(run_service())

    assert processed == [reminder]