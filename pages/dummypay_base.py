# from pages.base_page import BasePage


# class DummyPayBase(BasePage):

#  def go_to_wallets(self):
#     """
#     Navigate to the Wallets page and wait
#     until the page URL is updated.
#     """

#     from pages.wallets_page import WalletsPage

#     # Click the Wallets navigation link
#     self.page.get_by_role(
#         "link", name="Wallets", exact=True
#     ).click()

#     # Wait until navigation to the Wallets page completes
#     self.page.wait_for_url("**/wallets")

#     # Return the Wallets page object
#     return WalletsPage(self.page)


#     def go_to_dashboard(self):
#         from pages.dashboard_page import DashboardPage
#         self.page.get_by_role("link", name="Dashboard").click()
#         return DashboardPage(self.page)









from playwright.sync_api import expect

from pages.base_page import BasePage


class DummyPayBase(BasePage):
    """
    Base page for authenticated DummyPay pages.
    Contains shared navigation methods.
    """

    def go_to_wallets(self):
        """
        Navigate to Wallets and wait for the page content.
        """

        from pages.wallets_page import WalletsPage

        # Click the Wallets navigation link
        self.page.get_by_role(
            "link", name="Wallets", exact=True
        ).click()

        # Wait for the Wallets URL
        self.page.wait_for_url("**/wallets")

        # Wait for the Wallets page heading
        expect(
            self.page.get_by_role(
                "heading", name="Wallets", exact=True
            )
        ).to_be_visible(timeout=15000)

        # Wait for the wallet cards to be rendered
        expect(
            self.page.get_by_text(
                "Israeli Shekel", exact=False
            )
        ).to_be_visible(timeout=15000)

        # Return the Wallets page object
        return WalletsPage(self.page)

    def go_to_dashboard(self):
        """
        Navigate to the Dashboard page.
        """

        from pages.dashboard_page import DashboardPage

        # Click the Dashboard navigation link
        self.page.get_by_role(
            "link", name="Dashboard", exact=True
        ).click()

        return DashboardPage(self.page)
