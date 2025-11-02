import re
from playwright.sync_api import Page, expect


class FooterPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto_home(self):
        """Navigate to homepage and verify it's loaded."""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator("text=Buy").first).to_be_visible(timeout=30000)