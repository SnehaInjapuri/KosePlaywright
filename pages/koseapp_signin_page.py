from playwright.sync_api import Page

class SignInPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        """Navigate to the login page."""
        self.page.goto("https://dev.koseapp.com/signin")
        self.page.wait_for_load_state("domcontentloaded")
