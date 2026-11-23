



import pytest
from decimal import Decimal
from playwright.sync_api import expect


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def conversion(logged_in):
    """
    Open the Wallets page and return
    its conversion calculator component.
    """
    wallets = logged_in.go_to_wallets()
    return wallets.get_conversion()


# ============================================================
# CON-004: Amount Too Small
# ============================================================

def test_CON_004_amount_too_small(conversion):
    """
    Verify that a very small conversion amount
    displays the expected validation message.
    """

    # Arrange & Act
    conversion.set_conversion(
        amount="0.01",
        from_currency="ILS",
        to_currency="EUR"
    )

    # Assert: Verify the exact validation message
    expect(
        conversion.page.get_by_role("alert")
    ).to_contain_text(
        "Amount is too small to convert."
    )


# ============================================================
# CON-005: More Than Two Decimal Places
# ============================================================

def test_CON_005_more_than_two_decimal_places(conversion):
    """
    Verify that an amount containing more than
    two decimal places displays a validation error.
    """

    # Arrange & Act
    conversion.set_conversion(
        amount="0.001",
        from_currency="ILS",
        to_currency="EUR"
    )

    # Assert: Verify the expected application error
    expect(
        conversion.page.get_by_role("alert")
    ).to_contain_text(
        "Use at most 2 decimal places."
    )


# ============================================================
# CON-006: Amount Above Maximum
# ============================================================

@pytest.mark.skip(
    reason="Maximum conversion amount is not confirmed in requirements"
)
def test_CON_006_amount_above_maximum(conversion):
    """
    Verify that an amount exceeding the maximum
    allowed value is rejected.

    Pending clarification of the maximum amount.
    """

    # Arrange & Act
    conversion.set_conversion(
        amount="1000000.01",
        from_currency="ILS",
        to_currency="USD"
    )

    # Read validation information
    state = conversion.get_amount_validation_state()
    alerts = conversion.get_validation_alerts()

    print("Input:", conversion.get_amount_value())
    print("Browser validation:", state)
    print("Application alerts:", alerts)

    # Assert: Invalid amount must be rejected
    assert not state["valid"] or any(
        alert.strip() for alert in alerts
    ), (
        "Amount above the maximum was not rejected. "
        f"Validation: {state}, Alerts: {alerts}"
    )


# ============================================================
# CON-007: High Valid Amount
# ============================================================



def test_CON_007_high_valid_amount(conversion):
    """
    CON-007: Verify that a high valid amount
    is accepted and a positive conversion
    result is displayed.

    Exchange rate accuracy is outside this test's scope.
    """

    amount = "999999.99"

    # Step 1: Set conversion
    conversion.set_conversion(
        amount=amount,
        from_currency="ILS",
        to_currency="USD"
    )

    # Step 2: Verify the entered amount is preserved
    expect(
        conversion.amount_input
    ).to_have_value(amount)

    # Step 3: Wait for the conversion result
    conversion.wait_for_large_conversion_result()

    # Step 4: Read the displayed result
    actual_amount = conversion.get_converted_amount()

    # Step 5: Verify a positive result
    assert actual_amount > Decimal("0"), (
        "CON-007 FAILED: Expected a positive "
        f"conversion result, got {actual_amount}"
    )

    print(f"Entered amount: {amount}")
    print(f"Displayed converted amount: {actual_amount}")

# ============================================================
# CON-008: Non-Numeric Amount
# ============================================================

def test_CON_008_non_numeric_amount(conversion):
    """
    Verify that non-numeric input displays
    the expected validation error.
    """

    # Arrange & Act
    conversion.set_conversion(
        amount="abc",
        from_currency="ILS",
        to_currency="USD"
    )

    # Assert: Verify the exact validation message
    expect(
        conversion.page.get_by_role("alert")
    ).to_contain_text(
        "Enter a valid positive number."
    )




