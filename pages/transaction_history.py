from pages.dummypay_base import DummyPayBase

class TransactionHistory(DummyPayBase):
    def is_loaded(self):
        return self.page.get_by_role("heading", name="Transaction History").is_visible()