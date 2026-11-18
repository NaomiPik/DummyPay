from pages.dummypay_base import DummyPayBase

class ProfileSettings(DummyPayBase):
    def is_loaded(self):
        return self.page.get_by_role("heading", name="Profile & Settings").is_visible()