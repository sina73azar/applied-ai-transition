"""Week 3: lazy event parsing and reliable operation measurement."""

from collections.abc import Callable, Iterable, Iterator, MutableSequence
from contextlib import contextmanager
from typing import Any


class EventParseError(ValueError):
    """Raised when a non-empty event line is not a valid JSON object."""


def iter_json_events(lines: Iterable[str]) -> Iterator[dict[str, Any]]:
    """Lazily yield JSON objects from non-empty input lines.

    Raise EventParseError with the one-based input line number when JSON is
    invalid or its top-level value is not an object.
    """

    for i, item in enumerate(lines,start=1):
        line = item.strip()
        if not line:
            continue

        try:
            import json

            event = json.loads(line)
        except Exception as exc:
            raise EventParseError(f"line {i}: {exc}") from exc

        if not isinstance(event, dict):
            raise EventParseError(f"line {i}: expected object, got {type(event)}")

        yield event
"""     items = iter(lines)
    for i, line in enumerate(items, start=1):
        line = line.strip()
        if not line:
            continue

        try:
            import json

            event = json.loads(line)
        except Exception as exc:
            raise EventParseError(f"line {i}: {exc}") from exc

        if not isinstance(event, dict):
            raise EventParseError(f"line {i}: expected object, got {type(event)}")

        yield event """



def iter_error_events(
    events: Iterable[dict[str, Any]],
) -> Iterator[dict[str, Any]]:
    """Lazily yield events whose `level` is `error`, case-insensitively."""

    raise NotImplementedError("Complete this during week 3")


@contextmanager
def measure_operation(
    name: str,
    *,
    clock: Callable[[], float],
    sink: MutableSequence[dict[str, object]],
) -> Iterator[None]:
    """Append one timing event after the managed operation finishes.

    The event contains name, status, and duration_seconds. Status is `ok` on
    success and `error` when the body raises. Never swallow the original
    exception. Negative clock differences are recorded as zero.
    """

    raise NotImplementedError("Complete this during week 3")

