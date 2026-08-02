from datetime import datetime, timedelta, timezone

import pytest

from foundation_lab.tickets import Priority, TicketQueue, TicketStatus


class SequenceClock:
    def __init__(self, *values: datetime) -> None:
        self._values = iter(values)

    def __call__(self) -> datetime:
        return next(self._values)


def test_queue_selects_priority_then_oldest_then_identifier() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)
    queue = TicketQueue(SequenceClock(now, now + timedelta(seconds=1), now))

    queue.add("b", "Second identifier", Priority.HIGH)
    queue.add("low", "Low priority", Priority.LOW)
    queue.add("a", "First identifier", Priority.HIGH)

    assert queue.next_open() is not None
    assert queue.next_open().ticket_id == "a"


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

