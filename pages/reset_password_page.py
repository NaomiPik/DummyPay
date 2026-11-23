from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # דף הסיסמה החדשה (דורש טוקן תקף)
        self.heading = page.get_by_text("Choose a new password", exact=True)
        self.new_password = page.get_by_label("New password", exact=True)
        self.confirm_password = page.get_by_label("Confirm new password")
        self.update_button = page.get_by_role("button", name="Update password")
        self.mismatch_error = page.get_by_text("Passwords do not match.")
        self.too_short_error = page.get_by_text("Password must be at least 8 characters.")
        # דף קישור לא תקף
        self.invalid_heading = page.get_by_text("Reset link invalid", exact=True)
        self.invalid_message = page.get_by_text("This link is invalid or has expired.")
        self.request_new_link = page.get_by_role("link", name="Request a new link")
        self.back_link = page.get_by_role("link", name="Back to sign in")