import pytest
from config import BASE_URL, VALID_PASSWORD, VALID_EMAIL 
from pages.login_page import LoginPage



@pytest.fixture
def login_page(page):
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    return LoginPage(page)



@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.open(BASE_URL)
    return lp

@pytest.fixture
def logged_in(login_page):
    return login_page.login(VALID_EMAIL , VALID_PASSWORD)   # return DashboardPage



