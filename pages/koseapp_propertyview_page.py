import re
from asyncio import timeout

import page
from playwright.sync_api import Page, expect


class KoseappPropertyViewPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto_home(self):
        """Navigate to homepage and verify it's loaded."""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator("text=Buy").first).to_be_visible(timeout=30000)


    # ✅ City Search

    def search_city(self, city: str):
        # Click search input
        search_box = self.page.locator(".flex-grow.flex .location-search input").first
        expect(search_box).to_be_visible(timeout=15000)
        search_box.click()
        search_box.fill(city)

        # Select suggestion from dropdown
        option = self.page.get_by_role("option").filter(has_text=city).first
        expect(option).to_be_visible(timeout=20000)
        option.click()

        # ✅ Wait for property search API using context event listener
        self.page.context.wait_for_event(
            "response",
            predicate=lambda r: re.search(r"propertysearch", r.url) and r.status == 200,
            timeout=45000
        )

        # ✅ Ensure property cards are loaded
        property_cards = self.page.locator("div.cursor-pointer.font-poppins")
        expect(property_cards.first).to_be_visible(timeout=45000)

    # ✅ Dynamic First Property Card

    def open_first_property_card(self):
        # Wait until at least one property card is available in DOM
        self.page.wait_for_selector("div.p-2.xs\\:p-3.sm\\:p-4.md\\:p-5.h-auto.flex.flex-col", timeout=30000)

        # Select the first property card
        first_card = self.page.locator("div.p-2.xs\\:p-3.sm\\:p-4.md\\:p-5.h-auto.flex.flex-col").first

        # Ensure it is visible and clickable
        expect(first_card).to_be_visible(timeout=30000)

        # Click to open the property details page
        first_card.click(timeout=20000)

    def click_back_button(self):
        back_button = self.page.locator("svg.lucide-arrow-left")
        back_button.wait_for(state="visible", timeout=30000)
        back_button.click()

    def click_first_property_on_map(self, timeout: int = 40000):
        first_marker = self.page.locator("(//div[contains(@class,'price-marker')])[1]")

        # Wait until marker is visible & interactable
        first_marker.wait_for(state="visible", timeout=timeout)

        # Ensure the marker isn't behind the header / other elements
        first_marker.scroll_into_view_if_needed(timeout=timeout)

        # Force-click in case it’s partially overlapped by another marker
        first_marker.click(force=True, timeout=timeout)

        # ✅ View Switching

    def switch_view(self, view_name: str):
        btn = self.page.get_by_role("button", name=re.compile(view_name, re.I))
        expect(btn).to_be_visible(timeout=20000)
        btn.click()
        self.page.wait_for_timeout(4000)  # slight UI react delay

