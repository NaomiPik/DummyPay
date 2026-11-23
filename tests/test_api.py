import random

import pytest

from utilities.backend.transaction_api import send_funds
from utilities.backend.wallets_api import get_wallet_summary
from utilities.consts import CURENCY


@pytest.mark.smoke
def test_successfull_transfer() -> None:
    
    amount = random.randint(1, 30)
    print(f'amount: {amount}')

    wallet_summary_before_transfer = get_wallet_summary()
    print(f'response: {wallet_summary_before_transfer}')
    
    transaction = send_funds('mirka.g@gmail.com', amount, CURENCY.ILS)
    print(f'transaction: {transaction}')
    
    wallet_summary_after_transfer = get_wallet_summary()
    print(f'response: {wallet_summary_after_transfer}')
    
    assert transaction.get("status") == 'completed'
    assert wallet_summary_before_transfer[0].get("total_minor") - wallet_summary_after_transfer[0].get("total_minor") == amount

@pytest.mark.regression
def test_insufficient_funds() -> None:
    wallet_sum = get_wallet_summary()[0]
    print(wallet_sum)
    with pytest.raises(RuntimeError, match="INSUFFICIENT_FUNDS"):
        send_funds('mirka.g@gmail.com', wallet_sum.get("total_minor") + 1, wallet_sum.get("preferred_currency"))