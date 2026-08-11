# AI Assistance Log

Record assistance that materially affects study or portfolio code. Small
autocomplete corrections do not need separate entries.

| Date | Task | Work attempted first | Assistance requested | What changed manually | Test or explanation proving ownership |
|---|---|---|---|---|---|
| Aug 3-8, 2026 | Week 1 ledger normalization and summaries | Implemented normalization, rewrote the validation flow, added edge cases, and built category aggregation and sorting | Pytest/debugger usage; Mapping and TypedDict; bool/int behavior; Decimal conversion and exceptions; sorting and error-policy review | Replaced the `elif` chain with independent validation,added exact Decimal handling and regression checks, chose dictionary aggregation, and propagated invalid data | 19 ledger checks pass; explained Decimal conversion, finite checks, dictionary grouping, tuple sort keys, and the caller contract |
| Aug 10-11, 2026 | Week 2 ticket queue and state transitions | Initialized queue state; implemented `add()`, deterministic selection, closing, and snapshots; wrote focused tests | Review of `self`, visibility, instance versus class state, callables, protocols, iterators, injected clocks, runtime validation, tuple keys, and algorithmic complexity | Added explicit validation, per-instance dictionary state, O(n) ticket selection, deterministic snapshots, controlled close transitions, and a personal close-to-next-open test | 11 ticket checks pass; explained duplicate lookup, clock side effects, shallow tuple immutability, ordering rules, and O(n) versus O(n log n) |

## Week 1 Review

- Personally designed: field validation, normalized transaction output,
  category aggregation, and deterministic sorting.
- Main diagnosed failures: skipped validation in an `elif` chain, `bool` as an
  `int` subclass, float-to-Decimal precision, and silent invalid-row handling.
- Main lesson: validate parameters independently, reason through their possible
  runtime values, and define explicit rules for callers.
- Next time: establish the input contract and edge-case table before writing the
  implementation.

## Week 2 Review

- Personally designed: ticket input validation, dictionary-backed instance
  state, deterministic priority/age/identifier ordering, close transitions,
  immutable collection snapshots, and an additional close-to-next-open test.
- Main diagnosed risks: incidental `AttributeError` for invalid input, sorting
  the entire queue when only one result is needed, and consuming the clock
  during a failed state transition.
- Main lesson: define object invariants and side effects explicitly, inject
  nondeterministic dependencies, and match algorithm cost to the required
  result.
- Complexity explained: `next_open()` is O(n); `all()` is O(n log n) because
  complete sorting dominates tuple construction.
- Next action: begin Week 3 with the `events.py` iterator and generator
  exercises after the Week 2 work is committed.

## Weekly Ownership Check

Answer without an assistant:

1. What behavior did I personally design?
2. Which failure did I diagnose?
3. What generated suggestion did I reject, and why?
4. Which tradeoff can I explain without the repository open?
5. What would I implement differently next time?
