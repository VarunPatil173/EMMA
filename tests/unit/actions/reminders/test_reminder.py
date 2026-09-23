from datetime import datetime

from emma.actions.reminders.reminder import (
    Reminder,
    ReminderStatus,
)


def test_reminder_can_be_created():
    scheduled_at = datetime(2026, 9, 23, 20, 0)
    created_at = datetime(2026, 9, 23, 10, 0)

    reminder = Reminder(
        id=None,
        title="Study Physics",
        scheduled_at=scheduled_at,
        status=ReminderStatus.PENDING,
        created_at=created_at,
    )

    assert reminder.id is None
    assert reminder.title == "Study Physics"
    assert reminder.scheduled_at == scheduled_at
    assert reminder.status == ReminderStatus.PENDING
    assert reminder.created_at == created_at


def test_reminder_is_immutable():
    reminder = Reminder(
        id=1,
        title="Study Physics",
        scheduled_at=datetime(2026, 9, 23, 20, 0),
        status=ReminderStatus.PENDING,
        created_at=datetime(2026, 9, 23, 10, 0),
    )

    try:
        reminder.title = "Study SQL"
        assert False
    except AttributeError:
        pass