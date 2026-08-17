import pytest

from foundation_lab.events import (
    EventParseError,
    iter_error_events,
    iter_json_events,
    measure_operation,
)


def test_json_events_skip_blanks_and_report_source_line() -> None:
    events = iter_json_events(['{"level": "info"}', " ", '{"level": "error"}'])

    assert list(events) == [{"level": "info"}, {"level": "error"}]

    with pytest.raises(EventParseError, match="line 2"):
        list(iter_json_events(['{"ok": true}', "[]"]))


def test_error_filter_is_lazy_and_case_insensitive() -> None:
    consumed: list[int] = []

    def source():
        for index, level in enumerate(("info", "ERROR", "warning")):
            consumed.append(index)
            yield {"level": level, "index": index}

    errors = iter_error_events(source())
    assert consumed == []
    assert next(errors) == {"level": "ERROR", "index": 1}
    assert consumed == [0, 1]


def test_measure_operation_records_success() -> None:
    times = iter((10.0, 10.25))
    sink: list[dict[str, object]] = []

    with measure_operation("retrieve", clock=lambda: next(times), sink=sink):
        pass

    assert sink == [{"name": "retrieve", "status": "ok", "duration_seconds": 0.25}]


def test_measure_operation_records_error_and_reraises() -> None:
    times = iter((10.0, 9.0))
    sink: list[dict[str, object]] = []

    with pytest.raises(RuntimeError, match="dependency"):
        with measure_operation("generate", clock=lambda: next(times), sink=sink):
            raise RuntimeError("dependency unavailable")

    assert sink == [{"name": "generate", "status": "error", "duration_seconds": 0.0}]
