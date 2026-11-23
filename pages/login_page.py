from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.forgot_password_page import ForgotPasswordPage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.heading = page.locator("[data-slot='card-title']", has_text="Sign in")
        self.subtitle = page.get_by_text("Access your simulated wallets.")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.sign_in_button = page.get_by_role("button", name="Sign in")
        self.forgot_password_link = page.get_by_role("link", name="Forgot password?")
        self.create_account_link = page.get_by_role("link", name="Create an account")
        self.error_banner = page.get_by_text("Incorrect email or password.")
        self.email_error = page.get_by_text("Enter a valid email address.")
        self.password_error = page.get_by_text("Enter your password.")

    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()

    def login_successfully(self, email, password):
        self.login(email, password)
        return DashboardPage(self.page)

    def go_to_forgot_password(self):
        self.forgot_password_link.click()
        return ForgotPasswordPage(self.page)

    