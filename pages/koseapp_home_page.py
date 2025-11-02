import re
from playwright.sync_api import Page, expect

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.buy_button = page.locator("nav a[href='/propertysearch?type=Buy']").first
        self.rent_button = page.locator("nav a[href='/propertysearch?type=Rent']").first
        self.homeloans_button = page.locator("nav a[href='/home-loans']").first

    def click_buy_button(self):
        self.page.wait_for_selector("nav", timeout=20000)
        self.buy_button.scroll_into_view_if_needed()
        expect(self.buy_button).to_be_visible(timeout=20000)
        expect(self.buy_button).to_be_enabled(timeout=20000)

        self.buy_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page).to_have_url(re.compile("type=Buy"), timeout=40000)

    def click_rent_button(self):
        self.page.wait_for_selector("nav", timeout=20000)
        self.rent_button.scroll_into_view_if_needed()
        expect(self.rent_button).to_be_visible(timeout=20000)
        expect(self.rent_button).to_be_enabled(timeout=20000)

        self.rent_button.click()
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page).to_have_url(re.compile("type=Rent"), timeout=40000)

    def is_homeloans_button_visible(self):
        self.page.wait_for_selector("nav", timeout=20000)
        self.homeloans_button.scroll_into_view_if_needed()
        expect(self.homeloans_button).to_be_visible(timeout=30000)
        expect(self.homeloans_button).to_be_enabled(timeout=20000)
