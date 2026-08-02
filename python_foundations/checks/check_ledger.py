from decimal import Decimal

import pytest

from foundation_lab.ledger import normalize_transaction, summarize_succeeded


def test_normalize_transaction_trims_and_converts_values() -> None:
    result = normalize_transaction(
        {
            "transaction_id": " tx-1 ",
            "category": " Transfer ",
            "amount": 10.25,
            "succeeded": True,
        }
    )

    assert result == {
        "transaction_id": "tx-1",
        "category": "transfer",
        "amount": Decimal("10.25"),
        "succeeded": True,
    }


@pytest.mark.parametrize(
    ("raw", "field"),
    [
        ({"transaction_id": "", "category": "a", "amount": 1, "succeeded": True}, "transaction_id"),
        ({"transaction_id": "1", "category": " ", "amount": 1, "succeeded": True}, "category"),
        ({"transaction_id": "1", "category": "a", "amount": 0, "succeeded": True}, "amount"),
        ({"transaction_id": "1", "category": "a", "amount": "bad", "succeeded": True}, "amount"),
        ({"transaction_id": "1", "category": "a", "amount": 1, "succeeded": 1}, "succeeded"),
    ],
)
def test_normalize_transaction_rejects_invalid_fields(
    raw: dict[str, object],
    field: str,
) -> None:
    with pytest.raises(ValueError, match=field):
        normalize_transaction(raw)


def test_summarize_succeeded_groups_and_sorts() -> None:
    result = summarize_succeeded(
        [
            {"transaction_id": "1", "category": "bill", "amount": "7.50", "succeeded": True},
            {"transaction_id": "2", "category": "transfer", "amount": 20, "succeeded": True},
            {"transaction_id": "3", "category": "Bill", "amount": "12.50", "succeeded": True},
            {"transaction_id": "4", "category": "ignored", "amount": 100, "succeeded": False},
            {"transaction_id": "5", "category": "airtime", "amount": 20, "succeeded": True},
        ]
    )

    assert result == [
        {"category": "airtime", "amount": Decimal("20"), "transaction_count": 1},
        {"category": "bill", "amount": Decimal("20.00"), "transaction_count": 2},
        {"category": "transfer", "amount": Decimal("20"), "transaction_count": 1},
    ]

