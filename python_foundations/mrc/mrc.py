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


def test_mrc_transaction_empty_check() -> None:
    try:
        result = normalize_transaction(
            {
                "transaction_id": " ",
                "category": 0,
                "amount": 10.25,
                "succeeded": True,
            }
        )
    except ValueError as e:
        assert str(e) == "transaction_id is empty"


def test_mrc_category_empty_check() -> None:
    try:
        result = normalize_transaction(
            {
                "transaction_id": " asdasd",
                "category": " ",
                "amount": 10.25,
                "succeeded": True,
            }
        )
    except ValueError as e:
        assert str(e) == "category is empty"


def test_mrc_category_lowercase_check() -> None:
    result = normalize_transaction(
        {
            "transaction_id": " asdasd",
            "category": " ASDSAD ",
            "amount": 10.25,
            "succeeded": True,
        }
    )
    assert result == {
        "transaction_id": "asdasd",
        "category": "asdsad",
        "amount": Decimal("10.25"),
        "succeeded": True,
    }


@pytest.mark.parametrize(
    ("raw", "field"),
    [
        (
            {"transaction_id": "", "category": "a", "amount": 1, "succeeded": True},
            "transaction_id",
        ),
        (
            {"transaction_id": "1", "category": " ", "amount": 1, "succeeded": True},
            "category",
        ),
        (
            {"transaction_id": "1", "category": "a", "amount": 0, "succeeded": True},
            "amount",
        ),
        (
            {"transaction_id": "1", "category": "a", "amount": 12.54545, "succeeded": True},
            "amount",
        ),
        (
            {
                "transaction_id": "1",
                "category": "a",
                "amount": "bad",
                "succeeded": True,
            },
            "amount",
        ),
        (
            {
                "transaction_id": "1",
                "category": "a",
                "amount": "1254",
                "succeeded": True,
            },
            "amount",
        ),
        (
            {
                "transaction_id": "1",
                "category": "a",
                "amount": "12.5454",
                "succeeded": True,
            },
            "amount",
        ),
        (
            {"transaction_id": "1", "category": "a", "amount": 1, "succeeded": 1},
            "succeeded",
        ),
    ],
)
def test_mrc_amount_accepts_valid_types(
    raw: dict[str, object],
    field: str,
) -> None:
    with pytest.raises(ValueError, match=field):
        normalize_transaction(raw)
