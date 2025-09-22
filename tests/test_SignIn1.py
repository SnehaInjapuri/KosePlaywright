import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://test.koseapp.com/")
    page.locator("div").filter(has_text=re.compile(r"^BuyRentHome loansSign In$")).locator("div").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("sneha.injapuri@koseapp.com")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Sneha@1234")
    page.get_by_role("button", name="Access Your Account").click()
