import pytest
from playwright.sync_api import sync_playwright, Page
from pages.koseapp_login_page import LoginPage

@pytest.fixture(scope="session")
def browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    yield browser
    browser.close()
    p.stop()

@pytest.fixture
def page(browser):
    context = browser.new_context(
        http_credentials={"username": "admin", "password": "Pa$$word"}
    )
    page = context.new_page()
    yield page
    context.close()

#Email = "sneha.injapuri@koseapp.com"
#Password = "Sneha@1234"
@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """
    Pytest fixture that returns a page already logged in.
    """
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("sneha.injapuri@koseapp.com", "Sneha@1234")
    return page
