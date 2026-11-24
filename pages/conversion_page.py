
import re
from decimal import ROUND_HALF_UP, Decimal

from playwright.sync_api import expect

from pages.dummypay_base import DummyPayBase


class ConversionPage(DummyPayBase):
    """
    Page Object for the currency conversion preview
    inside the Wallets page.
    """

    def __init__(self, page):
        super().__init__(page)

        # Locate the conversion preview section
        self.section = page.locator("div").filter(
            has=page.get_by_text(
                "Conversion preview", exact=True
            )
        ).filter(
            has_text="Converted amount"
        ).last

        # Locate the amount input
        self.amount_input = self.section.get_by_role(
            "textbox", name="Amount"
        )

        # Locate source and target currency selectors
        self.from_currency = self.section.get_by_label(
            "From", exact=True
        )
        self.to_currency = self.section.get_by_label(
            "To", exact=True
        )

        # Locate the Swap button
        self.swap_button = self.section.get_by_role(
            "button", name="Swap"
        )

    
    def set_conversion(self, amount, from_currency, to_currency):
        """
        Set the conversion amount and select the source
        and target currencies using custom dropdowns.
        """

        # Enter the conversion amount
        self.amount_input.fill(str(amount))

        # Open the source currency dropdown
        self.from_currency.click()

        # Select the source currency
        self.page.get_by_role(
            "option",
            name=from_currency,
            exact=True
        ).click()

        # Open the target currency dropdown
        self.to_currency.click()

        # Select the target currency
        self.page.get_by_role(
            "option",
            name=to_currency,
            exact=True
        ).click()

    def get_displayed_rate(self):
        """
        Wait for the exchange rate to match
        the selected currency pair, then return it.
        """
      

        # Read selected currencies
        from_currency = self.get_from_currency()
        to_currency = self.get_to_currency()

        # Wait until the displayed rate matches
        # the selected currency pair
        rate_locator = self.section.get_by_text(
            re.compile(
                rf"Rate:\s*1\s+{re.escape(from_currency)}"
                rf"\s*=\s*[\d.]+\s+{re.escape(to_currency)}\b"
            )
        )

        expect(rate_locator).to_be_visible(timeout=15000)

        # Read the updated rate
        rate_text = rate_locator.inner_text()

        match = re.search(
            r"=\s*([\d.]+)\s+\w+",
            rate_text
        )

        assert match, f"Invalid rate text: {rate_text}"

        return Decimal(match.group(1))


    def get_converted_amount(self):
        """
        Wait for a numeric conversion result
        and return it as Decimal.
        """

        result = self.section.get_by_text(
            "Converted amount",
            exact=True
        ).locator(
            "xpath=following-sibling::*[1]"
        )

        expect(result).to_be_visible(timeout=15000)

        expect(result).to_contain_text(
            re.compile(r"-?\d[\d,]*(?:\.\d+)?"),
            timeout=15000
        )

        text = result.inner_text().strip()
        number = re.sub(r"[^\d.-]", "", text)

        assert number not in ("", "-", "."), (
            f"Invalid conversion result: {text!r}"
        )

        return Decimal(number)

    def calculate_expected_amount(self, amount, rate):
        """
        Calculate the expected converted amount
        using decimal arithmetic.
        """
        return (
            Decimal(str(amount)) * rate
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )




    def set_amount(self, amount):
        """
        Enter an amount in the conversion calculator.
        """
        self.amount_input.fill(str(amount))
    def get_validation_alerts(self):
        """
        Return all alert messages displayed by the application.
        """
        return self.page.get_by_role("alert").all_text_contents()

    def get_amount_value(self):
        """
        Return the current amount input value.
        """
        return self.amount_input.input_value()

    def get_validation_message(self, message):
        """
        Locate a specific validation message
        inside the conversion calculator.
        """
        return self.section.get_by_text(
            message,
            exact=True
        )

    def get_amount_validation_state(self):
        """
        Return the browser validation state
        of the amount input.
        """
        return self.amount_input.evaluate(
            """element => ({
                valid: element.validity.valid,
                rangeOverflow: element.validity.rangeOverflow,
                rangeUnderflow: element.validity.rangeUnderflow,
                stepMismatch: element.validity.stepMismatch,
                badInput: element.validity.badInput,
                validationMessage: element.validationMessage
            })"""
        )
    def wait_for_large_conversion_result(self):
        """
        Wait until the conversion result reflects
        a large amount rather than the default value.
        """
        self.page.wait_for_function(
            """() => {
                const label = [...document.querySelectorAll('p')]
                    .find(el => el.textContent.trim() === 'Converted amount');

                if (!label) return false;

                const result = label.nextElementSibling;
                if (!result) return false;

                const value = Number(
                    result.textContent.replace(/[^0-9.-]/g, '')
                );

                return Number.isFinite(value) && value > 1000;
            }""",
            timeout=10000
        )


    def get_from_currency(self):
        """
        Return the selected source currency.
        """
        return self.from_currency.inner_text().strip()

    def get_to_currency(self):
        """
        Return the selected target currency.
        """
        return self.to_currency.inner_text().strip()

    def swap_currencies(self):
        """
        Swap the source and target currencies.
        """
        self.swap_button.click()

