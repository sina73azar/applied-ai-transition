"""Week 4: bounded, retrying asynchronous health checks."""

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class HealthResult:
    name: str
    healthy: bool
    attempts: int
    detail: str


async def collect_health_checks(
    names: Sequence[str],
    check: Callable[[str], Awaitable[str]],
    *,
    max_concurrency: int,
    retries: int,
) -> list[HealthResult]:
    """Run checks concurrently while preserving input order.

    Requirements:
    - max_concurrency must be positive and retries must be non-negative;
    - at most max_concurrency calls to check may be active;
    - retry raised Exceptions up to `retries` additional attempts;
    - a successful detail is returned with healthy=True;
    - an exhausted failure is isolated and returned with healthy=False and the
      final exception text;
    - cancellation must continue to propagate.
    """

    raise NotImplementedError("Complete this during week 4")

