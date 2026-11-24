import re

from playwright.sync_api import expect

from config import BASE_URL, RESET_PASS, RESET_USER
from pages.reset_password_page import ResetPasswordPage
from utils.supabase import get_session


def test_login_session_token_is_not_accepted_as_reset_link(page):
    s = get_session(RESET_USER, RESET_PASS)
    page.goto(
        f"{BASE_URL}/reset-password#access_token={s['access_token']}"
        f"&refresh_token={s['refresh_token']}&type=recovery&token_type=bearer"
    )
    reset_page = ResetPasswordPage(page)
    expect(reset_page.invalid_heading).to_be_visible()
    expect(reset_page.heading).not_to_be_visible()


def test_reset_page_without_token_shows_invalid_link(page):
    page.goto(f"{BASE_URL}/reset-password")
    reset_page = ResetPasswordPage(page)
    expect(reset_page.invalid_heading).to_be_visible()
    expect(reset_page.invalid_message).to_be_visible()
    expect(reset_page.heading).not_to_be_visible()


def test_invalid_link_request_new_link_goes_to_forgot_password(page):
    page.goto(f"{BASE_URL}/reset-password")
    ResetPasswordPage(page).request_new_link.click()
    expect(page).to_have_url(re.compile(r"/forgot-password"))