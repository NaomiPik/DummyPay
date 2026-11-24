import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_forgot_password_link_opens_reset_page(login_page):
    reset_page = login_page.go_to_forgot_password()
    expect(reset_page.heading).to_be_visible()
    expect(reset_page.description).to_be_visible()
    expect(reset_page.email_input).to_be_visible()
    expect(reset_page.send_button).to_be_visible()


def test_back_to_sign_in_from_reset_page(login_page):
    reset_page = login_page.go_to_forgot_password()
    reset_page.back_to_sign_in()
    expect(login_page.sign_in_button).to_be_visible()
    expect(reset_page.heading).not_to_be_visible()