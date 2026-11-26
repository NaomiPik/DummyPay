

import random
import re
from decimal import ROUND_HALF_UP, Decimal

import pytest
from playwright.sync_api import expect

from config import BASE_URL, WALLET_NAMES
from pages.wallets_page import WalletsPage
from utilities.backend.backend_base import rpc
from utilities.backend.transaction_api import send_funds
from utilities.backend.wallets_api import get_wallet_summary
from utilities.consts import CURENCY

CURRENCY_SYMBOLS = {"ILS": "₪", "EUR": "€", "USD": "$", "GBP": "£"}
RECIPIENT = "mirka.g@gmail.com"   # same recipient as in test_api.py


# ---------------------------------------------------------------- helpers

def count_transactions():
    return rpc("list_my_transactions", {"p_limit": 1, "p_offset": 0})[0]["total_count"]


def read_rate(page, base, target):
    """Read the 'base -> target' rate from the dashboard rates widget."""
    pair = page.get_by_text(re.compile(rf"1\s+{base}\s*→\s*{target}\b"))
    expect(pair).to_be_visible()
    text = pair.locator("xpath=..").inner_text()
    match = re.search(rf"→\s*{target}\s+(\d+(?:\.\d+)?)", text)
    assert match, f"Rate not found in: {text!r}"
    return Decimal(match.group(1))


def select_currency(page, currency):
    """Open Settings and pick a currency in the dropdown (not saved yet)."""
    page.goto(f"{BASE_URL}/settings")
    select = page.get_by_role("combobox", name="Currency")
    expect(select).to_be_visible(timeout=15000)
    select.click()
    page.get_by_role(
        "option", name=f"{currency} — {WALLET_NAMES[currency]}", exact=True
    ).click()


def set_preferred_currency(page, currency):
    """Change the preferred currency in Settings, then return to Dashboard."""
    select_currency(page, currency)
    change = page.get_by_role("button", name="Change", exact=True)
    if change.is_enabled():
        change.click()
        dialog = page.get_by_role(
            "alertdialog", name=f"Change preferred currency to {currency}?"
        )
        expect(dialog).to_be_visible()
        dialog.get_by_role("button", name="Confirm change").click()
        expect(dialog).to_be_hidden(timeout=15000)
    page.get_by_role("link", name="Dashboard", exact=True).click()


# ------------------------------------------------------------------ smoke

@pytest.mark.smoke
def test_DASH_001_dashboard_loads(logged_in):
    expect(logged_in.heading).to_be_visible()
    expect(logged_in.welcome).to_be_visible()
    expect(logged_in.send_money).to_be_visible()
    expect(logged_in.simulated_banner).to_be_visible()


@pytest.mark.smoke
def test_DASH_002_wallet_cards_match_api(logged_in):
    summary = get_wallet_summary()[0]
    page = logged_in.page

    expect(page.get_by_text("Available balance", exact=True)).to_have_count(
        summary["wallet_count"]
    )
    expect(page.get_by_text("Preferred", exact=True)).to_have_count(1)
    assert WalletsPage(page).get_preferred_currency() == summary["preferred_currency"]


@pytest.mark.smoke
def test_DASH_003_total_balance_matches_api(logged_in):
    summary = get_wallet_summary()[0]
    total_text = f"{Decimal(summary['total_minor']) / 100:,.2f}"
    symbol = CURRENCY_SYMBOLS[summary["preferred_currency"]]

    expect(logged_in.total_card).to_contain_text(
        re.compile(rf"{re.escape(symbol)}\s*{re.escape(total_text)}")
    )


# ------------------------------------------------------------- regression

@pytest.mark.regression
def test_DASH_004_rates_widget_matches_wallets_page(logged_in):
    page = logged_in.page
    if get_wallet_summary()[0]["preferred_currency"] != "ILS":
        pytest.skip("The rates widget is ILS-based only when ILS is preferred")

    dashboard_rates = {cur: read_rate(page, "ILS", cur) for cur in ("EUR", "GBP", "USD")}
    assert all(rate > 0 for rate in dashboard_rates.values())

    wallets = logged_in.go_to_wallets()
    for currency, rate in dashboard_rates.items():
        assert wallets.get_exchange_rate(currency) == rate, currency


@pytest.mark.regression
def test_DASH_005_transfer_updates_dashboard(logged_in):
    """After an API transfer the total drops and the history shows it."""
    page = logged_in.page
    amount = random.randint(101, 999)          # minor units: 347 = ₪3.47

    summary = get_wallet_summary()[0]
    if summary["preferred_currency"] != "ILS":
        pytest.skip("Test assumes ILS is the preferred currency")

    tx = send_funds(RECIPIENT, amount, CURENCY.ILS)
    assert tx["status"] == "completed"

    expected_total = f"{Decimal(summary['total_minor'] - amount) / 100:,.2f}"
    amount_text = f"{Decimal(amount) / 100:,.2f}"
    recipient_name = tx["recipient_display_name"]

    page.reload()    # the dashboard loads its data on page load

    expect(logged_in.total_card).to_contain_text(
        re.compile(rf"₪\s*{re.escape(expected_total)}")
    )

    # Newest matching history row: recipient name and a minus sign + amount
    row = page.get_by_role("listitem").filter(
        has_text=re.compile(
            rf"To {re.escape(recipient_name)}"
            rf".*[-\u2212]\s*₪\s*{re.escape(amount_text)}"
        )
    ).first
    expect(row).to_be_visible()


@pytest.mark.regression
@pytest.mark.parametrize("link,destination,path", [
    ("Recent transactions", "Transaction History", "/history"),
    ("Recent notifications", "Notifications", "/notifications"),
    ("Send money", "Send Money", "/send"),
])
def test_DASH_006_links_open_correct_page(logged_in, link, destination, path):
    page = logged_in.page
    if link == "Send money":
        logged_in.send_money.click()
    else:
        page.get_by_text(link, exact=True).locator(
            "xpath=following::a[normalize-space()='View all'][1]"
        ).click()
    expect(page).to_have_url(re.compile(rf"{re.escape(path)}$"))
    expect(page.get_by_role("heading", name=destination, exact=True)).to_be_visible()


@pytest.mark.regression
@pytest.mark.parametrize("target", ["USD", "EUR", "GBP"])
def test_DASH_008_total_converts_when_preferred_currency_changes(logged_in, target):
    """Changing the preferred currency re-expresses the total using the rate."""
    page = logged_in.page
    before = get_wallet_summary()[0]
    original = before["preferred_currency"]
    if target == original:
        pytest.skip("Target equals the current preferred currency")

    # Calculation: expected total = old total x displayed rate
    rate = read_rate(page, original, target)
    expected_minor = (Decimal(before["total_minor"]) * rate).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP
    )

    try:
        set_preferred_currency(page, target)
        expect(logged_in.heading).to_be_visible()
        page.reload()
        expect(logged_in.heading).to_be_visible()

        # API: new preferred currency and converted total (+-1 minor unit)
        after = get_wallet_summary()[0]
        assert after["preferred_currency"] == target
        assert abs(Decimal(after["total_minor"]) - expected_minor) <= 1, (
            f"Expected ~{expected_minor}, got {after['total_minor']}"
        )

        # UI: total, currency label and Preferred badge
        amount_text = f"{Decimal(after['total_minor']) / 100:,.2f}"
        symbol = CURRENCY_SYMBOLS[target]
        expect(logged_in.total_card).to_contain_text(
            re.compile(rf"{re.escape(symbol)}\s*{re.escape(amount_text)}")
        )
        expect(logged_in.total_card).to_contain_text(f"shown in {target}")
        expect(
            WalletsPage(page).get_wallet_card(target).get_by_text("Preferred", exact=True)
        ).to_be_visible()

        # Calculation: the rate and its inverse multiply to ~1
        inverse = read_rate(page, target, original)
        assert abs(rate * inverse - 1) < Decimal("0.001")
    finally:
        set_preferred_currency(page, original)


# --------------------------------------------------------------- negative

@pytest.mark.negative
def test_DASH_N01_dashboard_requires_login(page):
    """Without logging in, the app root shows sign-in, not the dashboard."""
    page.goto(BASE_URL)
    expect(page.get_by_role("button", name="Sign in")).to_be_visible()
    expect(page.get_by_role("heading", name="Dashboard", level=1)).not_to_be_visible()


@pytest.mark.negative
def test_DASH_N02_failed_transfer_changes_nothing(logged_in):
    """A rejected transfer must not change the total or the history."""
    summary = get_wallet_summary()[0]
    currency = summary["preferred_currency"]
    count_before = count_transactions()

    with pytest.raises(RuntimeError, match="INSUFFICIENT_FUNDS"):
        send_funds(RECIPIENT, summary["total_minor"] + 1, currency)

    assert get_wallet_summary()[0]["total_minor"] == summary["total_minor"]
    assert count_transactions() == count_before

    logged_in.page.reload()
    total_text = f"{Decimal(summary['total_minor']) / 100:,.2f}"
    symbol = CURRENCY_SYMBOLS[currency]
    expect(logged_in.total_card).to_contain_text(
        re.compile(rf"{re.escape(symbol)}\s*{re.escape(total_text)}")
    )


@pytest.mark.negative
def test_DASH_N03_cancelled_currency_change_keeps_preference(logged_in):
    """Cancelling the confirmation dialog must not change the preference."""
    page = logged_in.page
    original = get_wallet_summary()[0]["preferred_currency"]
    target = "USD" if original != "USD" else "EUR"

    select_currency(page, target)
    page.get_by_role("button", name="Change", exact=True).click()
    dialog = page.get_by_role(
        "alertdialog", name=f"Change preferred currency to {target}?"
    )
    expect(dialog).to_be_visible()
    dialog.get_by_role("button", name="Cancel").click()
    expect(dialog).to_be_hidden()

    assert get_wallet_summary()[0]["preferred_currency"] == original

    page.get_by_role("link", name="Dashboard", exact=True).click()
    expect(
        WalletsPage(page).get_wallet_card(original).get_by_text("Preferred", exact=True)
    ).to_be_visible()
