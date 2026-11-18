from pages.dummypay_base import DummyPayBase

class SendMoney(DummyPayBase):
    def is_loaded(self):
        return self.page.get_by_role("heading", name="Send Money").is_visible()