import re

from pages.dummypay_base import DummyPayBase


class DashboardPage(DummyPayBase):

    def __init__(self, page):
        super().__init__(page)
        self.account_menu = page.get_by_role("button", name=re.compile("Account menu"))
        self.heading = page.get_by_role("heading", name="Dashboard", level=1)
        self.welcome = page.get_by_text("Welcome back")
        self.send_money = page.get_by_text("Send money", exact=True)
        self.simulated_banner = page.get_by_text("Simulated platform")
        self.total_card = page.get_by_text(
            "Total balance (approximate)", exact=True
        ).locator("xpath=ancestor::div[contains(., 'shown in')][1]")

    def get_welcome_text(self):
        return self.page.get_by_text("Welcome back").inner_text()

    def go_to_bank_accounts(self):
        from pages.bank_accounts import BankAccounts
        self.page.get_by_role("link", name="Bank Accounts").click()
        return BankAccounts(self.page)