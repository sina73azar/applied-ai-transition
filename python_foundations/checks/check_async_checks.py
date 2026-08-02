import asyncio

import pytest

from foundation_lab.async_checks import HealthResult, collect_health_checks


def test_health_checks_bound_concurrency_and_preserve_order() -> None:
    active = 0
    maximum_active = 0

    async def check(name: str) -> str:
        nonlocal active, maximum_active
        active += 1
        maximum_active = max(maximum_active, active)
        await asyncio.sleep(0)
        active -= 1
        return f"{name}:ok"

    result = asyncio.run(
        collect_health_checks(
            ["qdrant", "model", "database"],
            check,
            max_concurrency=2,
            retries=0,
        )
    )

    assert maximum_active == 2
    assert result == [
        HealthResult("qdrant", True, 1, "qdrant:ok"),
        HealthResult("model", True, 1, "model:ok"),
        HealthResult("database", True, 1, "database:ok"),
    ]


def test_health_checks_retry_and_isolate_exhausted_failure() -> None:
    attempts: dict[str, int] = {}

    async def check(name: str) -> str:
        attempts[name] = attempts.get(name, 0) + 1
        if name == "eventual" and attempts[name] == 1:
            raise RuntimeError("temporary")
        if name == "failed":
            raise RuntimeError(f"failure-{attempts[name]}")
        return "ready"

    result = asyncio.run(
        collect_health_checks(
            ["eventual", "failed"],
            check,
            max_concurrency=1,
            retries=1,
        )
    )

    assert result == [
        HealthResult("eventual", True, 2, "ready"),
        HealthResult("failed", False, 2, "failure-2"),
    ]


@pytest.mark.parametrize(
    ("max_concurrency", "retries", "message"),
    [(0, 0, "max_concurrency"), (1, -1, "retries")],
)
def test_health_checks_validate_limits(
    max_concurrency: int,
    retries: int,
    message: str,
) -> None:
    async def check(_: str) -> str:
        return "unused"

    with pytest.raises(ValueError, match=message):
        asyncio.run(
            collect_health_checks(
                ["service"],
                check,
                max_concurrency=max_concurrency,
                retries=retries,
            )
        )

