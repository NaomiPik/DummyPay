
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

from pages.conversion_page import ConversionPage
from pages.dummypay_base import DummyPayBase


class WalletsPage(DummyPayBase):
    """
    Page Object for the DummyPay Wallets page.
    Contains wallet locators, actions, and data retrieval methods.
    """
    
    def __init__(self, page):
        super().__init__(page)

        # Locator: Add wallet button
        self.add_wallet_button = page.get_by_role(
            "button",
            name="Add wallet"
        )

    def click_add_wallet(self):
        """
        Click the Add wallet button.
        """
        self.add_wallet_button.click()

    def is_add_wallet_disabled(self):
        """
        Return True if the Add wallet button is disabled.
        """
        return self.add_wallet_button.is_disabled()

    def is_add_wallet_enabled(self):
        """
        Return True if the Add wallet button is enabled.
        """
        return self.add_wallet_button.is_enabled()

    def get_wallet_title(self, currency):
        """
        Return the locator for a wallet's currency title.
        """
        name = self.WALLET_NAMES[currency]

        # Locate the exact wallet title
        return self.page.get_by_text(
            f"{currency} · {name}",
            exact=True
        )

    def is_wallet_visible(self, currency):
        """
        Wait for the requested wallet title to become visible.
        Return True if visible, otherwise False.
        """
        wallet = self.get_wallet_title(currency)

        try:
            # Wait up to 10 seconds for the wallet title
            wallet.wait_for(
                state="visible",
                timeout=10000
            )
            return True

        except PlaywrightTimeoutError:
            return False

    def get_wallet_card(self, currency):
        """
        Locate the wallet card containing the requested
        currency title and available balance.
        """
        title = self.get_wallet_title(currency)

        # Find the closest ancestor containing a balance label
        return title.locator(
            "xpath=ancestor::*["
            ".//*[normalize-space()='Available balance']"
            "][1]"
        )

    def get_wallet_balance(self, currency):
        """
        Return the displayed balance of the requested wallet,
        including its currency symbol.
        """
        card = self.get_wallet_card(currency)

        # Locate the Available balance label
        balance_label = card.get_by_text(
            "Available balance",
            exact=True
        )

        # Read the element immediately following the label
        balance = balance_label.locator(
            "xpath=following-sibling::*[1]"
        )

        # Wait until the balance element is visible
        expect(balance).to_be_visible(timeout=10000)

        return balance.inner_text().strip()

    def get_all_wallet_balances(self):
        """
        Return a dictionary containing the displayed
        balances of all four wallet currencies.
        """
        balances = {}

        # Collect each wallet's displayed balance
        for currency in self.WALLET_NAMES:
            balances[currency] = self.get_wallet_balance(
                currency
            )

        return balances
    def get_conversion(self):
        """
        Return the conversion calculator
        located inside the Wallets page.
        """
        return ConversionPage(self.page)


    
    def get_preferred_currency(self):
        """
        Return the currency code of the preferred wallet.
        """
        for currency in self.WALLET_NAMES:
            card = self.get_wallet_card(currency)

            if card.get_by_text("Preferred", exact=True).count() == 1:
                return currency

        raise AssertionError("No preferred wallet found")


    
    def get_exchange_rate(self, currency):
        """
        Read the exchange rate displayed in Wallets.
        Wait for the requested rate to load.
        """
        import re
        from decimal import Decimal

        from playwright.sync_api import expect

        if currency not in ("EUR", "USD", "GBP"):
            raise ValueError(f"Unsupported currency: {currency}")

        heading = self.page.get_by_text(
            "Exchange rates",
            exact=True
        )

        expect(heading).to_be_visible(timeout=10000)

        # Locate the exact currency pair, not the conversion preview
        pair = self.page.get_by_text(
            re.compile(rf"1\s+ILS\s*→\s*{currency}\b")
        )

        expect(pair).to_be_visible(timeout=15000)

        # Read the rate from the same row/card
        row = pair.locator("xpath=..")
        text = row.inner_text()

        print(f"Rate row for {currency}: {text}")

        match = re.search(
            rf"1\s+ILS\s*→\s*{currency}\s+"
            rf"(\d+(?:\.\d+)?)",
            text
        )

        if not match:
            raise AssertionError(
                f"Could not extract rate for {currency}. "
                f"Row content: {text}"
            )

        return Decimal(match.group(1))
