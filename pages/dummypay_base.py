from pages.base_page import BasePage

class DummyPayBase(BasePage):
    def go_to_wallets(self):
        from pages.wallets_page import WalletsPage
        self.page.get_by_role("link", name="Wallets").click()
        return WalletsPage(self.page)

    def go_to_dashboard(self):
        from pages.dashboard_page import DashboardPage
        self.page.get_by_role("link", name="Dashboard").click()
        return DashboardPage(self.page)