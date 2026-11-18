from pages.dummypay_base import DummyPayBase

class Notifications(DummyPayBase):
    def is_loaded(self):
        return self.page.get_by_role("heading", name="Notifications").is_visible()