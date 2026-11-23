from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.heading = page.get_by_text("Reset your password", exact=True)
        self.description = page.get_by_text("Enter your account email and ")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.send_button = page.get_by_role("button", name="Send reset link")
        self.back_link = page.get_by_role("link", name="Back to sign in")

    def back_to_sign_in(self):
        self.back_link.click()