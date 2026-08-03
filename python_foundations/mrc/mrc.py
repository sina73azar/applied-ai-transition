

from decimal import Decimal

import pytest
from foundation_lab.ledger import normalize_transaction


def test_mrc() -> None:
    result = normalize_transaction(
        {
            "transaction_id": " aa ",
            "category": 0,
            "amount": 10.25,
            "succeeded": True,
        }
    )

    assert result == {
        "transaction_id": "aa",
        "category": "0",
        "amount": Decimal("10.25"),
        "succeeded": True,
    }