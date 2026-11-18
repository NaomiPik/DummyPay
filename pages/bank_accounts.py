from pages.dummypay_base import DummyPayBase


class BankAccounts(DummyPayBase):
    def is_loaded(self):
        return self.page.get_by_role("heading", name="Bank Accounts").is_visible()