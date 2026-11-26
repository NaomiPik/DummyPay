import pytest

from utilities.backend.wallets_api import get_wallet_summary
from utilities.consts import CURENCY


@pytest.mark.smoke
def test_API_001_wallet_summary_contract():
    summary = get_wallet_summary()

    assert isinstance(summary, list) and len(summary) == 1
    row = summary[0]

    expected_keys = {
        "preferred_currency", "total_minor", "wallet_count",
        "rates_as_of", "rates_stale",
    }
    assert expected_keys <= set(row), f"Missing keys: {expected_keys - set(row)}"

    assert row["preferred_currency"] in {c.value for c in CURENCY}
    assert isinstance(row["total_minor"], int) and row["total_minor"] >= 0
    assert 1 <= row["wallet_count"] <= 4
    assert isinstance(row["rates_stale"], bool)