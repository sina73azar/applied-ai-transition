# AI Assistance Log

Record assistance that materially affects study or portfolio code. Small
autocomplete corrections do not need separate entries.

| Date | Task | Work attempted first | Assistance requested | What changed manually | Test or explanation proving ownership |
|---|---|---|---|---|---|
| Aug 3-8, 2026 | Week 1 ledger normalization and summaries | Implemented normalization, rewrote the validation flow, added edge cases, and built category aggregation and sorting | Pytest/debugger usage; Mapping and TypedDict; bool/int behavior; Decimal conversion and exceptions; sorting and error-policy review | Replaced the `elif` chain with independent validation,added exact Decimal handling and regression checks, chose dictionary aggregation, and propagated invalid data | 19 ledger checks pass; explained Decimal conversion, finite checks, dictionary grouping, tuple sort keys, and the caller contract |

## Week 1 Review

- Personally designed: field validation, normalized transaction output,
  category aggregation, and deterministic sorting.
- Main diagnosed failures: skipped validation in an `elif` chain, `bool` as an
  `int` subclass, float-to-Decimal precision, and silent invalid-row handling.
- Main lesson: validate parameters independently, reason through their possible
  runtime values, and define explicit rules for callers.
- Next time: establish the input contract and edge-case table before writing the
  implementation.

## Weekly Ownership Check

Answer without an assistant:

1. What behavior did I personally design?
2. Which failure did I diagnose?
3. What generated suggestion did I reject, and why?
4. Which tradeoff can I explain without the repository open?
5. What would I implement differently next time?
