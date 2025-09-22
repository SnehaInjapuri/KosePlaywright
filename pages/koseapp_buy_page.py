from playwright.sync_api import Page, expect

class BuyPage:
    def __init__(self, page: Page):
        self.page = page
        self.location_search_box = page.locator(".css-amejhk").first
        self.location_input = page.locator("#react-select-4-input")
        self.dallas_option = page.get_by_role("option", name="Dallas, TX, USA", exact=True)

    def click_location(self):
        self.location_search_box.click()

    def enter_location(self, location: str):
        expect(self.location_input).to_be_visible()
        self.location_input.type(location, delay=100)  # better than fill() for React-Select

    def select_location_option(self):
        expect(self.dallas_option).to_be_visible()
        self.dallas_option.click()
