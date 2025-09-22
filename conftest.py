import pytest
from playwright.sync_api import sync_playwright

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
