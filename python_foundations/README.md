# Python Foundations: August-September 2026

The first four weeks use small exercises. Weeks five through eight build a
FastAPI capstone from a blank directory so that prior agent-written application
code cannot hide gaps.

## Setup and Check Commands

Run from the repository root:

```bash
.venv/bin/python -m compileall -q python_foundations/src
.venv/bin/pytest -q -c python_foundations/pyproject.toml \
  python_foundations/checks
```

The checks initially fail with `NotImplementedError`. Implement only the module
for the current week. These files are named `check_*.py`, so the application's
normal `PYTHONPATH=. .venv/bin/pytest` command does not discover them.

## Study Method

1. Read the relevant sections of <https://docs.python.org/3/tutorial/>.
2. Write examples in a disposable REPL or notebook.
3. Read the week's module and check file.
4. Implement without AI assistance for at least 45-60 minutes.
5. Run one check at a time and investigate the failure.
6. Ask an assistant for a hint or review only after writing down the diagnosis.
7. Record material help in `AI_USAGE_LOG.md`.
8. Explain the implementation aloud without looking at it.

Do not ask an AI assistant to provide the completed exercise.

## Week 1: August 3-9

Topics: functions, mappings, iterables, comprehensions, sorting, exceptions,
`Decimal`, and type hints.

Implement `foundation_lab/ledger.py`.

```bash
.venv/bin/pytest -q -c python_foundations/pyproject.toml \
  python_foundations/checks/check_ledger.py
```

Completion:

- all ledger checks pass;
- invalid input behavior is explained;
- the reason for avoiding binary floats for money is explained;
- one additional edge-case check is written personally.

## Week 2: August 10-16

Topics: dataclasses, enums, protocols, object invariants, optional values, and
deterministic ordering.

Implement `foundation_lab/tickets.py`.

```bash
.venv/bin/pytest -q -c python_foundations/pyproject.toml \
  python_foundations/checks/check_tickets.py
```

Completion:

- all ticket checks pass;
- queue ordering and duplicate behavior are explained;
- one additional state-transition check is written personally.

## Week 3: August 17-23

Topics: iterators, generators, JSON, custom exceptions, context managers,
callables, and logging-style events.

Implement `foundation_lab/events.py`.

```bash
.venv/bin/pytest -q -c python_foundations/pyproject.toml \
  python_foundations/checks/check_events.py
```

Completion:

- all event checks pass;
- laziness and exception propagation are explained;
- one additional malformed-input check is written personally.

## Week 4: August 24-30

Topics: async functions, tasks, semaphores, bounded concurrency, retries,
preserved ordering, and exception isolation.

Implement `foundation_lab/async_checks.py`.

```bash
.venv/bin/pytest -q -c python_foundations/pyproject.toml \
  python_foundations/checks/check_async_checks.py
```

Completion:

- all async checks pass;
- bounded concurrency and retry count are explained;
- the implementation is rewritten once from a blank file;
- weeks 1-3 checks still pass.

## Week 5: August 31-September 6

Create a new private or public repository named `support-operations-api`.
Do not copy `app/rag_api.py`.

Deliver:

- a short API contract before implementation;
- FastAPI application factory and typed models;
- create, read, list, update-status, and comment endpoints;
- in-memory repository behind a protocol;
- validation and consistent error responses;
- unit and API checks for happy and failure paths.

## Week 6: September 7-13

Replace the in-memory implementation with PostgreSQL:

- schema and migration;
- repository implementation;
- explicit transaction boundary for a status change plus audit record;
- pagination with deterministic ordering;
- integration checks using an isolated test database.

Explain connection pooling, transactions, rollback, indexes, and the difference
between domain and persistence models.

## Week 7: September 14-20

Add:

- password or token authentication;
- user roles and authorization checks;
- one background operation with retry limits;
- structured request and job logs;
- health/readiness endpoints;
- tests for unauthorized access, dependency failure, and exhausted retries.

## Week 8: September 21-27

Finish:

- Dockerfile and Docker Compose;
- environment configuration without committed secrets;
- CI for tests;
- architecture and operational README;
- 90-minute exit exercise: add an assigned endpoint and diagnose an injected
  failure without an assistant.

Record the result in `PROGRESS.md`. Repeat the weak area before starting
the ML phase if the exit exercise fails.
