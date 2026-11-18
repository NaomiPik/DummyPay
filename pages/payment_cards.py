from pages.dummypay_base import DummyPayBase

class PaymentCards(DummyPayBase):
    def is_loaded(self):
        return self.page.get_by_role("Payment Cards", name="Wallets").is_visible()