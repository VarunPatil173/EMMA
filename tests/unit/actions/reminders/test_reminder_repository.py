from datetime import datetime

from emma.actions.reminders.reminder import (
    Reminder,
    ReminderStatus,
)
from emma.actions.reminders.reminder_repository import (
    ReminderRepository,
)


def create_reminder() -> Reminder:
    return Reminder(
        id=None,
        title="Study Physics",
        scheduled_at=datetime(2026, 9, 23, 20, 0),
        status=ReminderStatus.PENDING,
        created_at=datetime(2026, 9, 23, 10, 0),
    )


def test_reminder_is_saved_and_retrieved(tmp_path):
    database_path = tmp_path / "emma.db"

    repository = ReminderRepository(str(database_path))

    saved = repository.save(create_reminder())

    reminder = repository.get(saved.id)

    assert reminder == saved


def test_reminders_preserve_order(tmp_path):
    database_path = tmp_path / "emma.db"

    repository = ReminderRepository(str(database_path))

    first = repository.save(create_reminder())

    second = repository.save(
        Reminder(
            id=None,
            title="Learn SQL",
            scheduled_at=datetime(2026, 9, 24, 18, 0),
            status=ReminderStatus.PENDING,
            created_at=datetime(2026, 9, 23, 10, 0),
        )
    )

    reminders = repository.get_all()

    assert reminders == [first, second]


def test_reminder_persists_after_repository_is_recreated(tmp_path):
    database_path = tmp_path / "emma.db"

    repository = ReminderRepository(str(database_path))

    saved = repository.save(create_reminder())

    new_repository = ReminderRepository(str(database_path))

    reminder = new_repository.get(saved.id)

    assert reminder == saved


def test_reminder_can_be_updated(tmp_path):
    database_path = tmp_path / "emma.db"

    repository = ReminderRepository(str(database_path))

    saved = repository.save(create_reminder())

    updated = Reminder(
        id=saved.id,
        title="Study SQL",
        scheduled_at=datetime(2026, 9, 23, 21, 0),
        status=ReminderStatus.PENDING,
        created_at=saved.created_at,
    )

    repository.update(updated)

    assert repository.get(saved.id) == updated


def test_reminder_can_be_deleted(tmp_path):
    database_path = tmp_path / "emma.db"

    repository = ReminderRepository(str(database_path))

    saved = repository.save(create_reminder())

    repository.delete(saved.id)

    assert repository.get(saved.id) is None