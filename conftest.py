import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def logged_in_page(page: Page):
    """Stable Login Fixture"""

    page.set_viewport_size({"width": 1500, "height": 900})
    page.goto("https://dev.koseapp.com/")
    page.wait_for_load_state("domcontentloaded")

    # ✅ Click Sign In from menu cluster (proven working locator)
    menu_signin = page.locator("div").filter(
        has_text=re.compile(r"^BuyRentHome loansSign In$")
    ).locator("div")
    expect(menu_signin).to_be_visible(timeout=40000)
    menu_signin.click()

    # ✅ Wait for login fields using TEXT fallback (more reliable)
    email_input = page.get_by_placeholder("Email")
    password_input = page.get_by_placeholder("Password")

    expect(email_input).to_be_visible(timeout=40000)

    # ✅ Perform login
    email_input.fill("sneha.injapuri@koseapp.com")
    password_input.fill("Sneha@12345")

    access_btn = page.get_by_role("button", name="Access Your Account")
    expect(access_btn).to_be_enabled(timeout=20000)
    access_btn.click()

    # ✅ Verify success
    expect(page.get_by_text("Find your dream home")).to_be_visible(timeout=60000)

    return page

