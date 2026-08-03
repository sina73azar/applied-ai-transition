from foundation_lab.ledger import normalize_transaction


def test_normalize_transaction_custom() -> None:
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