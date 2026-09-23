from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ReminderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Reminder:
    id: int | None
    title: str
    scheduled_at: datetime
    status: ReminderStatus
    created_at: datetime