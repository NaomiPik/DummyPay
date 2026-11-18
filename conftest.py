import pytest

from config import BASE_URL, PASSWORD, USER
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.open(BASE_URL)
    return lp

@pytest.fixture
def logged_in(login_page):
    return login_page.login(USER, PASSWORD)   # return DashboardPage