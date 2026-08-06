"""Week 1: normalize and summarize transaction-like mappings."""

from collections.abc import Iterable, Mapping

from decimal import Decimal, InvalidOperation
from typing import TypedDict


class Transaction(TypedDict):
    transaction_id: str
    category: str
    amount: Decimal
    succeeded: bool


class CategoryTotal(TypedDict):
    category: str
    amount: Decimal
    transaction_count: int


def normalize_transaction(raw: Mapping[str, object]) -> Transaction:
    """Validate and normalize one transaction.

    Requirements:
    - transaction_id and category must be non-empty strings after trimming;
    - category is returned in lowercase;
    - amount accepts Decimal, int, float, or a numeric string, and must be
      strictly positive;
    - succeeded must be an actual bool, not an integer;
    - invalid values raise ValueError with the invalid field name.
    """

    # transaction_id
    raw_tran = raw.get("transaction_id")
    if raw_tran is None:
        raise ValueError("transaction_id is None")
    if not isinstance(raw_tran, str):
        raise ValueError("transaction_id is not a string")
    tran_id = raw_tran.strip()
    if not tran_id:
        raise ValueError("transaction_id is empty")

    # category
    raw_cat = raw.get("category")
    if raw_cat is None:
        raise ValueError("category is None")
    if not isinstance(raw_cat, str):
        raise ValueError("category is not a string")
    cat = raw_cat.strip()
    if not cat:
        raise ValueError("category is empty")

    # amount
    amt = raw.get("amount")
    if isinstance(amt, bool):
        raise ValueError("amount is not a number")
    if not isinstance(amt, (int, float, Decimal, str)):
        raise ValueError("amount is not a number")

    try:
        amt = Decimal(str(amt))
    except InvalidOperation as error:
        raise ValueError("amount is not a number") from error

    if amt.is_nan():
        raise ValueError("amount is a Nan")

    if amt.is_infinite():
        raise ValueError("amount is infinite")

    if not amt.is_finite() or amt <= 0:
        raise ValueError("amount is not strictly positive")

    # succeeded
    succ = raw.get("succeeded")
    if not isinstance(succ, bool):
        raise ValueError("succeeded is not a bool")

    return {
        "transaction_id": tran_id,
        "category": cat.lower(),
        "amount": amt,
        "succeeded": succ,
    }


def summarize_succeeded(
    rows: Iterable[Mapping[str, object]],
) -> list[CategoryTotal]:
    """Return totals for successful transactions grouped by category.

    Normalize every input row. Exclude unsuccessful rows. Sort results by amount
    descending and then category ascending. Return an empty list for no
    successful rows.
    """

    groups: dict[str, CategoryTotal] = {}
    for row in rows:
        tx = normalize_transaction(row)
        if not tx["succeeded"]:
            continue
        cat = tx["category"]
        if cat not in groups:
            groups[cat] = {
                "category": cat,
                "amount": Decimal(0),
                "transaction_count": 0,
            }
        groups[cat]["amount"] += tx["amount"]
        groups[cat]["transaction_count"] += 1

    return sorted(
        groups.values(),
        key=category_sort_key,
    )


def category_sort_key(x: CategoryTotal) -> tuple[Decimal, str]:
    return (-x["amount"], x["category"])
