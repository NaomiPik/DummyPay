from pages.dummypay_base import DummyPayBase

class WalletsPage(DummyPayBase):
    def is_loaded(self):
        return self.page.get_by_role("heading", name="Wallets").is_visible()