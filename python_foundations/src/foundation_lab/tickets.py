"""Week 2: model a small, deterministic support-ticket queue."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntEnum
from typing import Protocol


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TicketStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class Clock(Protocol):
    def __call__(self) -> datetime: ...


@dataclass
class Ticket:
    ticket_id: str
    title: str
    priority: Priority
    created_at: datetime
    status: TicketStatus = TicketStatus.OPEN
    closed_at: datetime | None = None


class TicketQueue:
    """Store tickets and choose the next open ticket deterministically."""

    def __init__(self, clock: Clock | Callable[[], datetime]) -> None:
        raise NotImplementedError("Complete this during week 2")

    def add(self, ticket_id: str, title: str, priority: Priority) -> Ticket:
        """Add a ticket.

        Trim identifiers and titles. Reject empty values and duplicate
        identifiers with ValueError.
        """

        raise NotImplementedError("Complete this during week 2")

    def next_open(self) -> Ticket | None:
        """Return the highest-priority open ticket.

        For equal priority, return the oldest ticket. Break a remaining tie by
        ticket_id. Return None when no ticket is open.
        """

        raise NotImplementedError("Complete this during week 2")

    def close(self, ticket_id: str) -> Ticket:
        """Close an open ticket and return it.

        Raise KeyError for an unknown identifier and ValueError when already
        closed.
        """

        raise NotImplementedError("Complete this during week 2")

    def all(self) -> tuple[Ticket, ...]:
        """Return an immutable snapshot ordered by creation and identifier."""

        raise NotImplementedError("Complete this during week 2")
