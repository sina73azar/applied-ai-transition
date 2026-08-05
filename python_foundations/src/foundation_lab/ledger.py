"""Week 1: normalize and summarize transaction-like mappings."""

from collections.abc import Iterable, Mapping

# from curses import raw
from decimal import Decimal
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

    """ empty checks """
    transaction_id = str(raw.get("transaction_id")).strip()
    if not transaction_id:
        raise ValueError("transaction_id is empty")  # type: ignore

    elif not str(raw.get("category")).strip():
        raise ValueError("category is empty")  # type: ignore
    elif not isinstance(raw.get("amount"), (int, float, Decimal, str)):
        raise ValueError("amount is not a number")  # type: ignore
    elif type(raw.get("amount")) is str:
        try:
            Decimal(str(raw.get("amount")))
        except Exception as e:
            raise ValueError("amount is not a number")  # type: ignore
    elif Decimal(str(raw.get("amount"))) <= 0:
        raise ValueError("amount is not strictly positive")  # type: ignore
    elif not isinstance(raw.get("succeeded"), bool):
        raise ValueError("succeeded is not a bool")  # type: ignore
    else:
        return {
            "transaction_id": transaction_id,
            "category": str(raw.get("category")).strip().lower(),
            "amount": Decimal(str(raw.get("amount"))),
            "succeeded": bool(raw.get("succeeded")),
        }


def summarize_succeeded(
    rows: Iterable[Mapping[str, object]],
) -> list[CategoryTotal]:
    """Return totals for successful transactions grouped by category.

    Normalize every input row. Exclude unsuccessful rows. Sort results by amount
    descending and then category ascending. Return an empty list for no
    successful rows.
    """
    """     output: list[CategoryTotal] = {}
    for row in rows:
        normalized_row = normalize_transaction(row)
        print("man injam",normalized_row)
        if normalized_row is not None:
            if normalized_row["succeeded"]:
                category = normalized_row["category"]
                amount = normalized_row["amount"]
                if category in output:
                    output[category]["amount"] += amount
                    output[category]["transaction_count"] += 1
                else:
                    output[category] = {
                        "category": category,
                        "amount": amount,
                        "transaction_count": 1,
                    }

    return list(output.values()) """
    
    raise NotImplementedError("summarize_succeeded is not yet implemented")
        
