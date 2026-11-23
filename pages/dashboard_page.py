import re

from pages.base_page import BasePage


class DashboardPage(BasePage):

    def get_welcome_text(self):
            return self.page.get_by_text("Welcome back").inner_text()
     
    def __init__(self, page):
        super().__init__(page)
        self.account_menu = page.get_by_role("button", name=re.compile("Account menu"))
        self.heading = page.get_by_role("heading", name="Dashboard", level=1)

