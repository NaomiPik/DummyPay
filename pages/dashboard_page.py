from pages.dummypay_base import DummyPayBase

class DashboardPage(DummyPayBase):
    def get_welcome_text(self):
        return self.page.get_by_text("Welcome back").inner_text()