
from decimal import Decimal
from playwright.sync_api import expect
import pytest
import re
from pages.conversion_page import ConversionPage


CURRENCIES = ["ILS", "EUR", "USD", "GBP"]


@pytest.mark.parametrize(
    "from_currency,to_currency",
    [
        (source, target)
        for source in CURRENCIES
        for target in CURRENCIES
    ]
)

def test_CON_all_currency_pairs(
    logged_in_conversion,
    from_currency,
    to_currency
):
    """
    Verify that all 16 currency pairs can be selected
    and display a valid conversion result.

    Exchange rate accuracy is outside this test's scope.
    """

    wallets = logged_in_conversion.go_to_wallets()
    conversion = wallets.get_conversion()

    conversion.set_conversion(
        amount="100",
        from_currency=from_currency,
        to_currency=to_currency
    )

    expect(conversion.from_currency).to_contain_text(
        from_currency
    )

    expect(conversion.to_currency).to_contain_text(
        to_currency
    )

    expect(conversion.amount_input).to_have_value("100")

    actual = conversion.get_converted_amount()

    assert actual > Decimal("0"), (
        f"Invalid conversion result for "
        f"{from_currency} -> {to_currency}: {actual}"
    )



def test_CON_009_swap_currencies(logged_in_conversion):
    """
    CON-009: Verify that the Swap button
    reverses the source and target currencies.
    """

    # Arrange: Open the conversion calculator
    wallets = logged_in_conversion.go_to_wallets()
    conversion = wallets.get_conversion()

    # Set the initial conversion
    conversion.set_conversion(
        amount="100",
        from_currency="ILS",
        to_currency="USD"
    )

    # Verify the initial currencies
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text("USD")

    # Act: Click the Swap button
    conversion.swap_currencies()

    # Assert: Verify that the currencies were swapped
    expect(conversion.from_currency).to_contain_text("USD")
    expect(conversion.to_currency).to_contain_text("ILS")

    # Verify that the amount remains unchanged
    assert conversion.get_amount_value() == "100"

    # Verify that a conversion result is available
    actual = conversion.get_converted_amount()

    assert actual > 0, (
        f"Expected a positive conversion result "
        f"after Swap, got {actual}"
    )



def test_CON_010_double_swap_restores_original_currencies(logged_in_conversion):
    """
    CON-010: Verify that clicking Swap twice
    restores the original currency selection
    and preserves the entered amount.
    """

    # Arrange: Open the conversion calculator
    wallets = logged_in_conversion.go_to_wallets()
    conversion = wallets.get_conversion()

    conversion.set_conversion(
        amount="100",
        from_currency="ILS",
        to_currency="USD"
    )

    # Verify the initial state
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text("USD")
    assert conversion.get_amount_value() == "100"

    # Act: Perform the first swap
    conversion.swap_currencies()

    # Assert: Verify the reversed currencies
    expect(conversion.from_currency).to_contain_text("USD")
    expect(conversion.to_currency).to_contain_text("ILS")

    # Act: Perform the second swap
    conversion.swap_currencies()

    # Assert: Verify the original currencies are restored
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text("USD")

    # Verify the entered amount is preserved
    assert conversion.get_amount_value() == "100"



def test_CON_011_double_swap_restores_conversion_result(logged_in_conversion):
    """
    CON-011: Verify that swapping currencies twice
    restores the original conversion result.
    """

    # Arrange: Open the conversion calculator
    wallets = logged_in_conversion.go_to_wallets()
    conversion = wallets.get_conversion()

    # Set the initial conversion
    conversion.set_conversion(
        amount="100",
        from_currency="ILS",
        to_currency="USD"
    )

    # Verify the initial currencies
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text("USD")

    # Save the original conversion result
    original_result = conversion.get_converted_amount()

    # Act: Perform the first swap
    conversion.swap_currencies()

    # Verify the currencies were reversed
    expect(conversion.from_currency).to_contain_text("USD")
    expect(conversion.to_currency).to_contain_text("ILS")

    # Act: Perform the second swap
    conversion.swap_currencies()

    # Verify the original currencies were restored
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text("USD")

        # Verify the original conversion result was restored
    restored_result = conversion.get_converted_amount()

    assert restored_result == original_result, (
        f"Conversion result was not restored. "
        f"Expected {original_result}, got {restored_result}"
    )




@pytest.mark.parametrize("currency", [
    "ILS",
    "USD",
    "EUR",
    "GBP"
])
def test_CON_012_same_currency_conversion(logged_in_conversion, currency):
    """
    CON-012: Verify that converting a currency
    to itself preserves the amount and uses rate 1.
    """

    wallets = logged_in_conversion.go_to_wallets()
    conversion = wallets.get_conversion()

    amount = "100"

    conversion.set_conversion(
        amount=amount,
        from_currency=currency,
        to_currency=currency
    )

    # Verify selected currencies
    expect(conversion.from_currency).to_contain_text(currency)
    expect(conversion.to_currency).to_contain_text(currency)

    # Verify the entered amount
    expect(conversion.amount_input).to_have_value(amount)

    # Wait for the exact expected exchange rate
    expected_rate_text = (
    f"Rate: 1 {currency} = 1.00 {currency}"
   )

    expect(
        conversion.section.get_by_text(
            expected_rate_text,
            exact=True
        )
    ).to_be_visible(timeout=10000)

    # Verify the numeric exchange rate
    rate = conversion.get_displayed_rate()

    assert rate == Decimal("1"), (
        f"Expected rate 1 for {currency} -> {currency}, "
        f"got {rate}"
    )

    # Verify the converted amount
    actual = conversion.get_converted_amount()

    assert actual == Decimal(amount), (
        f"Expected {amount} {currency}, "
        f"got {actual}"
    )


def test_CON_013_dynamic_amount_update(logged_in_conversion):
    """
    CON-013: Verify that changing the conversion amount
    updates the result correctly without changing
    the exchange rate.
    """

    # Arrange: Open Wallets
    wallets = logged_in_conversion.go_to_wallets()

    # Read the current USD exchange rate
    wallet_rate = wallets.get_exchange_rate("USD")

    conversion = wallets.get_conversion()

    # Step 1: Set initial conversion
    conversion.set_conversion(
        amount="100",
        from_currency="ILS",
        to_currency="USD"
    )

    # Verify initial amount
    expect(conversion.amount_input).to_have_value("100")

    # Step 2: Wait for the correct exchange rate
    rate_locator = conversion.section.get_by_text(
        re.compile(
            r"Rate:\s*1\s+ILS\s*=\s*[\d.]+\s+USD"
        )
    )

    expect(rate_locator).to_contain_text(
        f"= {wallet_rate} USD",
        timeout=15000
    )

    # Read initial rate
    rate_before = conversion.get_displayed_rate()

    # Step 3: Change the amount
    conversion.set_amount("200")

    # Verify new input value
    expect(conversion.amount_input).to_have_value("200")

    # Step 4: Verify rate remains unchanged
    rate_after = conversion.get_displayed_rate()

    assert rate_after == rate_before, (
        f"Exchange rate changed unexpectedly: "
        f"{rate_before} -> {rate_after}"
    )

    # Step 5: Calculate expected result
    expected_amount = conversion.calculate_expected_amount(
        "200",
        rate_after
    )

    # Step 6: Wait for the converted amount to update
    conversion.page.wait_for_function(
        """expected => {
            const label = [...document.querySelectorAll('p')]
                .find(el =>
                    el.textContent.trim() === 'Converted amount'
                );

            if (!label || !label.nextElementSibling) {
                return false;
            }

            const actual = Number(
                label.nextElementSibling.textContent
                    .replace(/[^0-9.-]/g, '')
            );

            return Number.isFinite(actual) &&
                Math.abs(actual - expected) <= 0.01;
        }""",
        arg=float(expected_amount),
        timeout=15000
    )

    # Step 7: Read actual result
    actual_amount = conversion.get_converted_amount()

    # Diagnostics
    print(f"Rate before: {rate_before}")
    print(f"Rate after: {rate_after}")
    print(f"Expected amount: {expected_amount}")
    print(f"Actual amount: {actual_amount}")

    # Step 8: Final assertion
    assert abs(
        actual_amount - expected_amount
    ) <= Decimal("0.01"), (
        f"Incorrect conversion result. "
        f"Expected {expected_amount}, "
        f"got {actual_amount}"
    )


def test_CON_014_change_target_currency(logged_in_conversion):
    """
    CON-014: Verify that changing the target currency
    updates the conversion preview correctly.

    Exchange rate accuracy is outside this test's scope.
    """

    wallets = logged_in_conversion.go_to_wallets()
    conversion = wallets.get_conversion()

    # Step 1: Set initial conversion
    conversion.set_conversion(
        amount="100",
        from_currency="ILS",
        to_currency="USD"
    )

    # Step 2: Verify initial state
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text("USD")
    expect(conversion.amount_input).to_have_value("100")

    # Step 3: Change target currency to EUR
    conversion.to_currency.click()

    conversion.page.get_by_role(
        "option",
        name="EUR",
        exact=True
    ).click()

    # Step 4: Verify source currency remains unchanged
    expect(conversion.from_currency).to_contain_text("ILS")

    # Step 5: Verify target currency changed
    expect(conversion.to_currency).to_contain_text("EUR")

    # Step 6: Verify amount is preserved
    expect(conversion.amount_input).to_have_value("100")

    # Step 7: Verify conversion preview shows new pair
    rate_label = conversion.section.get_by_text(
        re.compile(
            r"Rate:\s*1\s+ILS\s*=\s*[\d.]+\s+EUR\b"
        )
    )

    expect(rate_label).to_be_visible(timeout=15000)

    # Step 8: Verify a numeric result is displayed
    actual_amount = conversion.get_converted_amount()

    assert actual_amount > Decimal("0"), (
        "CON-014 FAILED: Expected a positive "
        f"conversion result, got {actual_amount}"
    )

    print("\nCON-014 PASSED")
    print("Source currency: ILS")
    print("Target currency: EUR")
    print("Entered amount: 100")
    print(f"Displayed converted amount: {actual_amount}")


def test_CON_015_change_source_currency(logged_in_conversion):
    """
    CON-015: Verify that changing the source currency
    updates the conversion preview correctly.

    Exchange rate accuracy is outside this test's scope.
    """

    wallets = logged_in_conversion.go_to_wallets()
    conversion = wallets.get_conversion()

    # Step 1: Set initial conversion
    conversion.set_conversion(
        amount="100",
        from_currency="ILS",
        to_currency="USD"
    )

    # Step 2: Verify initial state
    expect(conversion.from_currency).to_contain_text("ILS")
    expect(conversion.to_currency).to_contain_text("USD")
    expect(conversion.amount_input).to_have_value("100")

    # Step 3: Change source currency to EUR
    conversion.from_currency.click()

    conversion.page.get_by_role(
        "option",
        name="EUR",
        exact=True
    ).click()

    # Step 4: Verify source currency changed
    expect(conversion.from_currency).to_contain_text("EUR")

    # Step 5: Verify target currency remains unchanged
    expect(conversion.to_currency).to_contain_text("USD")

    # Step 6: Verify amount is preserved
    expect(conversion.amount_input).to_have_value("100")

    # Step 7: Verify conversion preview shows new pair
    rate_label = conversion.section.get_by_text(
        re.compile(
            r"Rate:\s*1\s+EUR\s*=\s*[\d.]+\s+USD\b"
        )
    )

    expect(rate_label).to_be_visible(timeout=15000)

    # Step 8: Verify a numeric result is displayed
    actual_amount = conversion.get_converted_amount()

    assert actual_amount > Decimal("0"), (
        "CON-015 FAILED: Expected a positive "
        f"conversion result, got {actual_amount}"
    )

    print("\nCON-015 PASSED")
    print("Source currency: EUR")
    print("Target currency: USD")
    print("Entered amount: 100")
    print(f"Displayed converted amount: {actual_amount}")
