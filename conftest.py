
# import pytest

# from config import BASE_URL, PASSWORD, USER, VALID_EMAIL, VALID_PASSWORD
# from pages.login_page import LoginPage


# @pytest.fixture
# def login_page(page):
#     lp = LoginPage(page)
#     lp.open(BASE_URL)
#     page.wait_for_load_state("networkidle")
#     return lp


# @pytest.fixture
# def logged_in(login_page):
#     return login_page.login(VALID_EMAIL, VALID_PASSWORD)  # returns DashboardPage


# @pytest.fixture
# def logged_in_conversion(login_page):
#     page = login_page.login(USER, PASSWORD)
#     page.wait_for_load_state("networkidle")
#     return page
#     גרסה ראשונה

import pytest

from config import BASE_URL, PASSWORD, USER, VALID_EMAIL, VALID_PASSWORD
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.open(BASE_URL)
    page.wait_for_load_state("networkidle")
    return lp


@pytest.fixture
def logged_in(login_page):
    # returns DashboardPage
    return login_page.login_successfully(USER, PASSWORD)


@pytest.fixture
def logged_in_conversion(login_page):
    dashboard = login_page.login_successfully(USER, PASSWORD)
    dashboard.page.wait_for_load_state("networkidle")
    return dashboard