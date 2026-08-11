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

        self._tickets: dict[str, Ticket] = {}
        self._clock = clock

    def add(self, ticket_id: str, title: str, priority: Priority) -> Ticket:
        """Add a ticket.

        Trim identifiers and titles. Reject empty values and duplicate
        identifiers with ValueError.
        """
        # reject empty values
        if ticket_id is None:
            raise ValueError("ticket identifier cannot be None")
        if not isinstance(ticket_id, str):
            raise ValueError("ticket identifier must be a string")
        ticket_id = ticket_id.strip()
        if not ticket_id:
            raise ValueError("ticket identifier cannot be empty")
        if title is None:
            raise ValueError("ticket title cannot be None")
        if not isinstance(title, str):
            raise ValueError("ticket title must be a string")
        title = title.strip()
        if not title:
            raise ValueError("ticket title cannot be empty")

        # check duplicate identifiers
        if ticket_id in self._tickets:
            raise ValueError(f"duplicate ticket identifier: {ticket_id}")

        ticket = Ticket(
            ticket_id=ticket_id,
            title=title,
            priority=priority,
            created_at=self._clock(),
        )
        self._tickets[ticket_id] = ticket

        return ticket

    def next_open(self) -> Ticket | None:

        """Return the highest-priority open ticket.

        For equal priority, return the oldest ticket. Break a remaining tie by
        ticket_id. Return None when no ticket is open.
        """

        #  filter only open status
        open_tickets = [
            ticket
            for ticket in self._tickets.values()
            if ticket.status == TicketStatus.OPEN
        ]
        if not open_tickets:
            return None

        # default sorting is ascending, so we need to sort by negative priority to get descending order

        # In Python, min() efficiently finds the smallest element in an iterable without sorting the entire sequence, making it faster for this specific task. Conversely, sorted() returns a new list with all elements ordered, which is more computationally expensive. Use min() when only the smallest value is needed; use sorted() when ordering all elements is required. The key parameter in both functions allows custom comparison logic, enhancing flexibility.

        return min(
            open_tickets, key=lambda t: (-t.priority, t.created_at, t.ticket_id)
        )

    def close(self, ticket_id: str) -> Ticket:
        """Close an open ticket and return it.

        Raise KeyError for an unknown identifier and ValueError when already
        closed.
        """

        raise NotImplementedError("Complete this during week 2")

    def all(self) -> tuple[Ticket, ...]:
        """Return an immutable snapshot ordered by creation and identifier."""

        raise NotImplementedError("Complete this during week 2")
