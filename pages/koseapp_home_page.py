from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page:Page):
        self.page = page
        self.buy_button = page.get_by_role("link", name="Buy")
        self.rent_button = page.get_by_role("link", name="Rent")
        self.homeloans_button = page.locator("text=Home Loans")

    def click_buy_button(self):
        self.buy_button.first.click()

    def click_rent_button(self):
        self.rent_button.first.click()

    def is_homeloans_button_visible(self):
        expect(self.homeloans_button).to_be_visible()

