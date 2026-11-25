import re
from decimal import Decimal

import pytest
from playwright.sync_api import expect


@pytest.mark.skip(
    reason="Requires a user with fewer than four wallet types"
)
def test_add_wallet_enabled(logged_in):
    """
    WAL-001: Verify that the Add wallet button is enabled
    when the user has fewer than four wallet types.
    """

    # Arrange: Navigate to the Wallets page
    wallets = logged_in.go_to_wallets()

    # Assert: The Add wallet button should be enabled
    assert wallets.is_add_wallet_enabled(), (
        "Add wallet should be enabled "
        "when a wallet type is missing"
    )



def test_WAL_001_all_wallets_displayed(logged_in):
    """
    WAL-001: Verify that all four currency wallets
    are displayed on the Wallets page.
    """
    wallets = logged_in.go_to_wallets()

    expected_wallets = {
        "ILS": "Israeli Shekel",
        "EUR": "Euro",
        "USD": "US Dollar",
        "GBP": "British Pound"
    }

    # Verify each wallet title is visible
    for currency, name in expected_wallets.items():
        expect(
            wallets.page.get_by_text(
                f"{currency} · {name}",
                exact=True
            )
        ).to_be_visible()


def test_WAL_002_wallet_balances_displayed(logged_in):
    """
    WAL-002: Verify that each wallet displays
    its available balance in the correct currency.
    """
    wallets = logged_in.go_to_wallets()

    # Expected wallet titles and currency symbols
    wallet_data = {
        "ILS": ("Israeli Shekel", "₪"),
        "EUR": ("Euro", "€"),
        "USD": ("US Dollar", "$"),
        "GBP": ("British Pound", "£")
    }

    for currency, (name, symbol) in wallet_data.items():
        # Find the wallet card containing its title
        card = wallets.page.locator("div").filter(
            has=wallets.page.get_by_text(
                f"{currency} · {name}", exact=True
            )
        ).filter(
            has_text="Available balance"
        ).last

        # Verify the balance label and currency symbol
        expect(card.get_by_text("Available balance")).to_be_visible()
        assert symbol in card.inner_text(), (
            f"{currency} wallet should show {symbol}"
        )


def test_WAL_003_add_wallet_disabled(logged_in):
    """
    WAL-003: Verify that Add wallet is disabled
    when all four wallet types exist.
    """
    wallets = logged_in.go_to_wallets()

    # Verify all four wallets exist
    for name in ["Israeli Shekel", "Euro", "US Dollar", "British Pound"]:
        expect(
            wallets.page.get_by_text(name, exact=False)
        ).to_be_visible()

    # Verify the Add wallet button is disabled
    expect(wallets.add_wallet_button).to_be_disabled()



def test_WAL_004_wallets_persist_after_refresh(logged_in):
    """
    WAL-004: Verify that all four wallets and their
    balances remain unchanged after refreshing the page.
    """

    # Arrange: Navigate to the Wallets page
    wallets = logged_in.go_to_wallets()

    # Define the expected wallet currencies
    expected_currencies = ["ILS", "EUR", "USD", "GBP"]

    # Capture wallet balances before refresh
    balances_before = wallets.get_all_wallet_balances()

    # Act: Refresh the page
    wallets.page.reload()

    # Assert: Verify that all wallet titles are visible
    for currency in expected_currencies:
        assert wallets.is_wallet_visible(currency), (
            f"Wallet {currency} is missing after refresh"
        )

    # Capture wallet balances after refresh
    balances_after = wallets.get_all_wallet_balances()

    # Assert: Verify that balances remain unchanged
    assert balances_before == balances_after, (
        f"Wallet balances changed after refresh.\n"
        f"Before: {balances_before}\n"
        f"After: {balances_after}"
    )

def test_WAL_005_wallet_balance_format(logged_in):
    """
    WAL-005: Verify that wallet balances
    are displayed in a valid numeric format.
    """

   
    wallets = logged_in.go_to_wallets()

    currencies = ["ILS", "EUR", "USD", "GBP"]

    for currency in currencies:
        # Read the displayed balance
        balance_text = wallets.get_wallet_balance(currency)

        print(f"{currency} balance: {balance_text}")

        # Verify numeric format with up to 2 decimal places
        match = re.search(
            r"-?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|-?\d+(?:\.\d{1,2})?",
            balance_text
        )

        assert match is not None, (
            f"Invalid balance format for {currency}: "
            f"{balance_text}"
        )

        # Convert the extracted value to Decimal
        amount = Decimal(
            match.group().replace(",", "")
        )

        # Verify balance is non-negative
        assert amount >= 0, (
            f"Negative balance found for {currency}: "
            f"{amount}"
        )

def test_WAL_006_wallets_are_unique(logged_in):
    """
    WAL-006: Verify that each currency wallet
    appears exactly once with the correct name.
    """

    wallets = logged_in.go_to_wallets()

    # Expected currencies and wallet names
    expected_wallets = {
        "ILS": "Israeli Shekel",
        "EUR": "Euro",
        "USD": "US Dollar",
        "GBP": "British Pound"
    }

    # Verify that every wallet appears exactly once
    for currency, name in expected_wallets.items():

        wallet_title = wallets.get_wallet_title(currency)

        # Verify the wallet is visible
        expect(wallet_title).to_be_visible()

        # Verify exactly one wallet exists
        expect(wallet_title).to_have_count(1)

        # Verify the exact currency code and name
        expect(wallet_title).to_have_text(
            f"{currency} · {name}"
        )

        print(f"Verified unique wallet: {currency} - {name}")

def test_WAL_007_navigate_away_and_back(logged_in):
    """
    WAL-007: Verify wallets remain visible
    after navigating away and returning.
    """

    wallets = logged_in.go_to_wallets()

    expected_currencies = ["ILS", "EUR", "USD", "GBP"]

    # Step 1: Verify wallets before navigation
    for currency in expected_currencies:
        expect(wallets.get_wallet_title(currency)).to_be_visible()

    # Step 2: Navigate back to the previous page
    wallets.page.go_back()

    # Step 3: Navigate forward to Wallets again
    wallets.page.go_forward()

    # Step 4: Verify all wallets are still visible
    for currency in expected_currencies:
        expect(wallets.get_wallet_title(currency)).to_be_visible()

    print("All wallets remained visible after navigation.")

def test_WAL_008_balances_after_navigation(logged_in):
    """
    WAL-008: Verify that wallet balances remain unchanged
    after navigating away and returning to Wallets.
    """

    wallets = logged_in.go_to_wallets()

    # Step 1: Capture balances before navigation
    balances_before = wallets.get_all_wallet_balances()

    print(f"Balances before: {balances_before}")

    # Step 2: Navigate away from Wallets
    wallets.page.go_back()

    # Step 3: Return to Wallets
    wallets.page.go_forward()

    # Step 4: Verify all wallets are visible
    for currency in ["ILS", "EUR", "USD", "GBP"]:
        expect(wallets.get_wallet_title(currency)).to_be_visible()

    # Step 5: Capture balances after navigation
    balances_after = wallets.get_all_wallet_balances()

    print(f"Balances after: {balances_after}")

    # Step 6: Compare balances
    assert balances_before == balances_after, (
        f"Wallet balances changed after navigation.\n"
        f"Before: {balances_before}\n"
        f"After: {balances_after}"
    )

def test_WAL_009_wallets_stable_after_multiple_refreshes(logged_in):
    """
    WAL-009: Verify that wallet balances and wallet
    visibility remain stable after multiple page refreshes.
    """

    wallets = logged_in.go_to_wallets()

    expected_currencies = ["ILS", "EUR", "USD", "GBP"]

    # Capture initial balances
    balances_before = wallets.get_all_wallet_balances()

    # Refresh the page three times
    for refresh_number in range(1, 4):

        wallets.page.reload()

        # Verify all wallets are visible
        for currency in expected_currencies:
            expect(
                wallets.get_wallet_title(currency)
            ).to_be_visible(timeout=10000)

        # Read balances after refresh
        balances_after = wallets.get_all_wallet_balances()

        print(
            f"Refresh {refresh_number}: {balances_after}"
        )

        # Verify balances remain unchanged
        assert balances_after == balances_before, (
            f"Balances changed after refresh "
            f"{refresh_number}.\n"
            f"Before: {balances_before}\n"
            f"After: {balances_after}"
        )

def test_WAL_010_total_balance_calculation(logged_in):
    """
    WAL-010: Verify that the total balance in ILS
    equals the ILS wallet balance when all foreign
    currency wallets have zero balance.
    """

    import re
    from decimal import Decimal

    wallets = logged_in.go_to_wallets()

    # Step 1: Read all wallet balances
    balances = wallets.get_all_wallet_balances()

    def parse_amount(text):
        value = re.sub(r"[^\d.-]", "", text)
        return Decimal(value.replace(",", ""))

    ils_balance = parse_amount(balances["ILS"])

    foreign_balances = {
        currency: parse_amount(balances[currency])
        for currency in ["EUR", "USD", "GBP"]
    }

    # Step 2: Verify foreign currency balances are zero
    for currency, amount in foreign_balances.items():
        assert amount == Decimal("0.00"), (
            f"Test precondition failed: "
            f"{currency} balance is {amount}, expected 0.00"
        )

   
    # Step 3: Locate the total balance label
    total_label = wallets.page.get_by_text(
        "Total balance (approximate)",
        exact=True
    )

    # Locate the parent card containing the total amount
    total_card = total_label.locator(
        "xpath=ancestor::div[.//*[contains(text(), '₪')]][1]"
    )

    # Step 4: Read the displayed total
    total_text = total_card.inner_text()

    print(f"Total card text: {total_text}")

    match = re.search(
        r"₪\s*[\d,]+(?:\.\d{1,2})?",
        total_text
    )

    

    actual_total = parse_amount(match.group())

    # Step 5: Compare total with ILS wallet balance
    expected_total = ils_balance

    print(f"ILS wallet balance: {ils_balance}")
    print(f"Displayed total: {actual_total}")

    assert actual_total == expected_total, (
        f"Total balance mismatch. "
        f"Expected {expected_total}, got {actual_total}"
    )



def test_WAL_011_preferred_wallet(logged_in):
    """
    WAL-011: Verify that exactly one wallet is preferred
    and the preference persists after page refresh.
    """

    wallets = logged_in.go_to_wallets()

    currencies = ["ILS", "EUR", "USD", "GBP"]

    def get_preferred_currency():
        preferred_currencies = []

        for currency in currencies:
            card = wallets.get_wallet_card(currency)

            preferred_label = card.get_by_text(
                "Preferred",
                exact=True
            )

            if preferred_label.count() == 1:
                preferred_currencies.append(currency)

        assert len(preferred_currencies) == 1, (
            "Expected exactly one preferred wallet, "
            f"found: {preferred_currencies}"
        )

        return preferred_currencies[0]

    # Step 1: Identify the currently preferred wallet
    preferred_before = get_preferred_currency()

    print(f"Preferred wallet before refresh: {preferred_before}")

    # Step 2: Verify only one Preferred label exists
    expect(
        wallets.page.get_by_text("Preferred", exact=True)
    ).to_have_count(1)

    # Step 3: Refresh the page
    wallets.page.reload()

    # Step 4: Wait for wallets to load
    for currency in currencies:
        expect(
            wallets.get_wallet_title(currency)
        ).to_be_visible(timeout=10000)

    # Step 5: Identify the preferred wallet after refresh
    preferred_after = get_preferred_currency()

    print(f"Preferred wallet after refresh: {preferred_after}")

    # Step 6: Verify preference persists
    assert preferred_before == preferred_after, (
        f"Preferred wallet changed after refresh: "
        f"{preferred_before} -> {preferred_after}"
    )

    # Step 7: Verify exactly one preferred wallet remains
    expect(
        wallets.page.get_by_text("Preferred", exact=True)
    ).to_have_count(1)



def test_WAL_012_change_preferred_currency(logged_in):
    """
    WAL-012: Verify that changing the preferred currency
    updates the preferred wallet and persists after refresh.

    Restore the original preferred currency after the test.
    """

    wallets = logged_in.go_to_wallets()
    page = wallets.page

    # Step 1: Get the original preferred currency
    original_currency = wallets.get_preferred_currency()

    new_currency = next(
        currency
        for currency in ["ILS", "EUR", "USD", "GBP"]
        if currency != original_currency
    )

    print(f"Original preferred currency: {original_currency}")
    print(f"New preferred currency: {new_currency}")

    def change_preferred_currency(currency):
        """
        Change preferred currency in Settings,
        confirm the change, verify persistence,
        and verify the preferred wallet.
        """

        # Step 2: Navigate to Settings
        page.goto("https://dummypay.vercel.app/settings")

        expect(
            page.get_by_role(
                "heading",
                name="Profile & Settings"
            )
        ).to_be_visible(timeout=15000)

        currency_select = page.get_by_role(
            "combobox",
            name="Currency"
        )

        expect(currency_select).to_be_visible(timeout=15000)

        # Step 3: Select the requested currency
        currency_select.click()

        page.get_by_role(
            "option",
            name=(
                f"{currency} — "
                f"{wallets.WALLET_NAMES[currency]}"
            ),
            exact=True
        ).click()

        expect(currency_select).to_contain_text(
            currency,
            timeout=10000
        )

        # Step 4: Click Change and confirm
        change_button = page.get_by_role(
            "button",
            name="Change",
            exact=True
        )

        expect(change_button).to_be_visible(timeout=10000)

        if change_button.is_enabled():

            change_button.click()

            print(f"Clicked Change for currency: {currency}")

            # Wait for confirmation dialog
            confirmation_dialog = page.get_by_role(
                "alertdialog",
                name=f"Change preferred currency to {currency}?"
            )

            expect(confirmation_dialog).to_be_visible(
                timeout=10000
            )

            # Confirm the currency change
            confirmation_dialog.get_by_role(
                "button",
                name="Confirm change"
            ).click()

            # Wait for dialog to close
            expect(confirmation_dialog).to_be_hidden(
                timeout=15000
            )

            print(
                f"Confirmed preferred currency change to {currency}"
            )

        else:
            print(
                f"Change button disabled for {currency}. "
                "Verifying existing preference."
            )

        # Step 5: Reload Settings and verify persistence
        page.reload()

        expect(
            page.get_by_role(
                "heading",
                name="Profile & Settings"
            )
        ).to_be_visible(timeout=15000)

        currency_select = page.get_by_role(
            "combobox",
            name="Currency"
        )

        expect(currency_select).to_contain_text(
            currency,
            timeout=15000
        )

        print(
            f"Verified saved currency in Settings: {currency}"
        )

        # Step 6: Navigate to Wallets
        page.goto("https://dummypay.vercel.app/wallets")

        expect(
            wallets.get_wallet_title(currency)
        ).to_be_visible(timeout=15000)

        # Step 7: Verify preferred wallet
        preferred_badge = (
            wallets.get_wallet_card(currency)
            .get_by_text("Preferred", exact=True)
        )

        expect(preferred_badge).to_be_visible(
            timeout=15000
        )

        actual_currency = wallets.get_preferred_currency()

        assert actual_currency == currency, (
            f"Expected preferred currency {currency}, "
            f"got {actual_currency}"
        )

        print(
            f"Verified preferred wallet: {actual_currency}"
        )

    try:
        # Step 8: Change preferred currency
        change_preferred_currency(new_currency)

        # Step 9: Refresh Wallets
        page.reload()

        # Step 10: Verify persistence after refresh
        expect(
            wallets.get_wallet_card(new_currency).get_by_text(
                "Preferred",
                exact=True
            )
        ).to_be_visible(timeout=15000)

        actual_currency = wallets.get_preferred_currency()

        assert actual_currency == new_currency, (
            f"Preferred currency was not preserved. "
            f"Expected {new_currency}, got {actual_currency}"
        )

        print(
            "Preferred currency updated and persisted "
            "after refresh."
        )

    finally:
        # Step 11: Restore original preferred currency
        print(
            f"Restoring original currency: {original_currency}"
        )

        try:
            change_preferred_currency(original_currency)

            print(
                "Original preferred currency restored."
            )

        except Exception as restore_error:
            print(
                "WARNING: Failed to restore original "
                f"preferred currency: {restore_error}"
            )
            raise


@pytest.mark.parametrize(
    "currency",
    ["EUR", "USD", "GBP"]
)
def test_WAL_013_exchange_rates(logged_in, currency):
    """
    WAL-013: Diagnose exchange rate consistency
    between Wallets and Conversion preview.
    """

    wallets = logged_in.go_to_wallets()

    displayed_rate = wallets.get_exchange_rate(currency)

    conversion = wallets.get_conversion()

    conversion.set_conversion(
        amount="100",
        from_currency="ILS",
        to_currency=currency
    )

    # Verify the selected currencies
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text(currency)

    # Wait for the rate label to show the correct pair
    rate_locator = conversion.section.get_by_text(
        re.compile(
            rf"Rate:\s*1\s+ILS\s*=\s*[\d.]+\s+{currency}\b"
        )
    )

    expect(rate_locator).to_be_visible(timeout=15000)
# Wait until the calculator rate matches
# the exchange rate shown in Wallets
    expect(rate_locator).to_contain_text(
    f"= {displayed_rate} {currency}",
    timeout=15000
)
    # Collect diagnostic information
    actual_from = conversion.get_from_currency()
    actual_to = conversion.get_to_currency()
    rate_text = rate_locator.inner_text()
    conversion_rate = conversion.get_displayed_rate()
    converted_amount = conversion.get_converted_amount()

    print("\n========== WAL-013 DIAGNOSTICS ==========")
    print("Expected target currency:", currency)
    print("Selected source currency:", actual_from)
    print("Selected target currency:", actual_to)
    print("Wallets exchange rate:", displayed_rate)
    print("Calculator rate text:", rate_text)
    print("Calculator extracted rate:", conversion_rate)
    print("Converted amount for 100 ILS:", converted_amount)
    print("========================================\n")
# Calculate the expected converted amount
    expected_amount = conversion.calculate_expected_amount(
    amount="100",
    rate=conversion_rate
)

# Read the actual converted amount
    actual_amount = conversion.get_converted_amount()

    print(f"Expected converted amount: {expected_amount}")
    print(f"Actual converted amount: {actual_amount}")

# Verify the conversion calculation
    assert abs(actual_amount - expected_amount) <= Decimal("0.01"), (
    f"Incorrect conversion for ILS -> {currency}. "
    f"Expected: {expected_amount}, "
    f"Actual: {actual_amount}"
)
    # Verify the exchange rates
    assert abs(
        displayed_rate - conversion_rate
    ) <= Decimal("0.000001"), (
        f"Rate mismatch for ILS -> {currency}. "
        f"Wallets: {displayed_rate}, "
        f"Calculator: {conversion_rate}, "
        f"Rate text: {rate_text}"
    )

@pytest.mark.parametrize(
    "currency",
    ["EUR", "USD", "GBP"]
)

def test_WAL_014_exchange_rates_after_refresh(
    logged_in,
    currency
):
    """
    WAL-014: Verify that exchange rates remain
    available and valid after refreshing Wallets.
    """

    wallets = logged_in.go_to_wallets()

    # Read rate before refresh
    rate_before = wallets.get_exchange_rate(currency)

    assert rate_before > 0, (
        f"Invalid {currency} rate before refresh: {rate_before}"
    )

    # Refresh the page
    wallets.page.reload()

    # Read rate after refresh
    rate_after = wallets.get_exchange_rate(currency)

    assert rate_after > 0, (
        f"Invalid {currency} rate after refresh: {rate_after}"
    )

    print(f"Currency: {currency}")
    print(f"Rate before refresh: {rate_before}")
    print(f"Rate after refresh: {rate_after}")

    if rate_before != rate_after:
        print(
            "Exchange rate changed after refresh. "
            "This may be a legitimate rate update."
        )
    else:
        print("Exchange rate remained unchanged.")



