import pytest
from playwright.sync_api import expect

from config import VALID_EMAIL, VALID_PASSWORD

WRONG_PASSWORD = "WrongPass123!"
DUMMY_PASSWORD = "SomePass123"
NONEXISTENT_EMAIL = "abc@gmail.com"


@pytest.mark.smoke
def test_login_page_elements_are_visible(login_page):
    expect(login_page.heading).to_be_visible()
    expect(login_page.subtitle).to_be_visible()
    expect(login_page.email_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()
    expect(login_page.sign_in_button).to_be_visible()
    expect(login_page.forgot_password_link).to_be_visible()
    expect(login_page.create_account_link).to_be_visible()


# ---------- Email validation ----------

@pytest.mark.negative
@pytest.mark.parametrize("bad_email", [
    "abcgmail.com",  # without @
    "abc@",  # without domain
    "@gmail.com",  # without username
    "abc@gmail",  # without extension
    "abc @gmail.com",  # with a space
])
def test_invalid_email_format_shows_validation_error(login_page, bad_email):
    login_page.login(bad_email, DUMMY_PASSWORD)
    expect(login_page.email_error).to_be_visible()
    expect(login_page.sign_in_button).to_be_visible()


@pytest.mark.negative
def test_invalid_email_and_wrong_password(login_page):
    login_page.login("abcgmail.com", WRONG_PASSWORD)
    expect(login_page.email_error).to_be_visible()


# ---------- Failed and Successful Login ----------

@pytest.mark.smoke
@pytest.mark.negative
def test_valid_email_wrong_password(login_page):
    login_page.login(VALID_EMAIL, WRONG_PASSWORD)
    expect(login_page.error_banner).to_be_visible()
    expect(login_page.email_error).not_to_be_visible()


@pytest.mark.negative
def test_nonexistent_email_shows_generic_error(login_page):
    login_page.login(NONEXISTENT_EMAIL, WRONG_PASSWORD)
    expect(login_page.error_banner).to_be_visible()
    expect(login_page.email_error).not_to_be_visible()


@pytest.mark.smoke
def test_valid_email_valid_password(login_page):
    dashboard = login_page.login_successfully(VALID_EMAIL, VALID_PASSWORD)
    expect(dashboard.account_menu).to_be_visible()
    expect(login_page.sign_in_button).not_to_be_visible()


# ---------- Empty Fields ----------

@pytest.mark.negative
def test_empty_email_and_password(login_page):
    login_page.sign_in_button.click()
    expect(login_page.email_error).to_be_visible()
    expect(login_page.password_error).to_be_visible()


@pytest.mark.negative
def test_empty_email_with_password(login_page):
    login_page.login("", DUMMY_PASSWORD)
    expect(login_page.email_error).to_be_visible()
    expect(login_page.password_error).not_to_be_visible()


@pytest.mark.negative
def test_valid_email_with_empty_password(login_page):
    login_page.login(VALID_EMAIL, "")
    expect(login_page.password_error).to_be_visible()
    expect(login_page.email_error).not_to_be_visible()