from datetime import datetime, timedelta, timezone

import pytest

from foundation_lab.tickets import Priority, TicketQueue, TicketStatus


class SequenceClock:
    def __init__(self, *values: datetime) -> None:
        self._values = iter(values)

    def __call__(self) -> datetime:
        return next(self._values)


def test_add_creates_normalized_open_ticket() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(lambda: now)

    ticket = queue.add(" 1 ", " First ", Priority.LOW)

    assert ticket.ticket_id == "1"
    assert ticket.title == "First"
    assert ticket.priority is Priority.LOW
    assert ticket.status is TicketStatus.OPEN
    assert ticket.created_at == now
    assert ticket.closed_at is None


def test_empty_id_ticket_rejected() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(lambda: now)

    with pytest.raises(ValueError, match="ticket identifier cannot be empty"):
        queue.add(" ", "First", Priority.LOW)


def test_empty_title_ticket_rejected() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(lambda: now)

    with pytest.raises(ValueError, match="ticket title cannot be empty"):
        queue.add("1", " ", Priority.LOW)


def test_duplicate_ticket_id_rejected() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(lambda: now)

    queue.add("1", "First", Priority.LOW)
    with pytest.raises(ValueError, match="duplicate ticket identifier"):
        queue.add("1", "Duplicate", Priority.HIGH)


def test_add_rejects_non_string_ticket_id() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(lambda: now)
    with pytest.raises(ValueError, match="ticket identifier must be a string"):
        queue.add(123, "Title", Priority.LOW)


def test_add_rejects_non_string_ticket_title() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(lambda: now)
    with pytest.raises(ValueError, match="ticket title must be a string"):
        queue.add("1", 123, Priority.LOW)
    with pytest.raises(ValueError, match="ticket title cannot be None"):
        queue.add("1", None, Priority.LOW)


def test_queue_selects_priority_then_oldest_then_identifier() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(SequenceClock(now, now + timedelta(seconds=1), now))

    queue.add("b", "Second identifier", Priority.HIGH)
    queue.add("low", "Low priority", Priority.LOW)
    queue.add("a", "First identifier", Priority.HIGH)
    next_open = queue.next_open()
    assert next_open is not None
    assert next_open.ticket_id == "a"


def test_close_sets_status_and_time_and_rejects_second_close() -> None:
    created = datetime(2026, 8, 3, tzinfo=timezone.utc)
    closed = created + timedelta(minutes=5)
    queue = TicketQueue(SequenceClock(created, closed))
    queue.add("ticket-1", "Cannot log in", Priority.CRITICAL)

    ticket = queue.close("ticket-1")

    assert ticket.status is TicketStatus.CLOSED
    assert ticket.closed_at == closed
    assert queue.next_open() is None
    with pytest.raises(ValueError, match="closed"):
        queue.close("ticket-1")


def test_queue_validates_input_and_returns_snapshot() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(lambda: now)
    first = queue.add(" 2 ", " Second ", Priority.MEDIUM)
    second = queue.add("1", "First", Priority.LOW)

    assert first.ticket_id == "2"
    assert first.title == "Second"
    assert queue.all() == (second, first)
    with pytest.raises(ValueError, match="duplicate"):
        queue.add("2", "Duplicate", Priority.HIGH)
    with pytest.raises(KeyError):
        queue.close("missing")
