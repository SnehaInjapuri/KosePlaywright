# pages/koseapp_scheduletour_page.py
from datetime import datetime
import re
from playwright.sync_api import Page, expect


class KoseappScheduleTourPage:
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

    def select_date_and_time(self, date, time):
        # ✅ Convert provided date → extract parts (Thu 30 Oct 2025)
        date_obj = datetime.strptime(date, "%a %d %b %Y")
        day_abbr = date_obj.strftime("%a")  # Thu
        day_num = date_obj.strftime("%d")   # 30
        month_abbr = date_obj.strftime("%b")  # Oct

        print(f"📅 Selecting date: {day_abbr} {day_num} {month_abbr}")

        # ✅ Locator based on DOM structure (3 span children)
        date_button = self.page.locator(
            f"button:has(span:text-is('{day_abbr}'))"
            f":has(span:text-is('{int(day_num)}'))"  # remove leading zero for UI
            f":has(span:text-is('{month_abbr}'))"
        ).first

        # ✅ Scroll calendar until visible
        max_scrolls = 12
        for i in range(max_scrolls):
            if date_button.is_visible():
                date_button.scroll_into_view_if_needed()
                date_button.click()
                print("✅ Date clicked")
                break

            print(f"🔄 Scrolling calendar… ({i+1}/{max_scrolls})")
            next_btn = self.page.locator("button[aria-label='Next dates']").first

            # STOP if next button disabled (means no more scrolling)
            if not next_btn.is_enabled():
                raise Exception(f"❌ Date not available in calendar: {date}")
            next_btn.click()
            self.page.wait_for_timeout(400)
        else:
            raise Exception(f"❌ Could not locate date: {date}")

        # ✅ Open Time dropdown before waiting
        print("🕘 Clicking Select Time dropdown...")
        time_dropdown = self.page.locator(
            "label:text-is('Select Time') ~ div.flex.items-center.gap-1.cursor-pointer"
        )
        expect(time_dropdown).to_be_visible(timeout=15000)
        time_dropdown.click()

        # ✅ Wait until time options appear
        self.page.wait_for_selector("div.space-y-4 button", timeout=30000)

        # ✅ Select time
        self.select_time_slot(time)

    def select_time_slot(self, time: str):
        print(f"⏱ Selecting time slot (preferred): {time}")

        # ✅ Wait for time slots to appear
        time_buttons = self.page.locator("div.grid.grid-cols-3.gap-3 button")
        expect(time_buttons.first).to_be_visible(timeout=30000)

        # ✅ Read all visible times
        visible_slots = time_buttons.all_inner_texts()
        print(f"🎯 Visible Time Slots: {visible_slots}")

        # ✅ Prefer requested time if available
        preferred = time_buttons.filter(has_text=time)
        if preferred.count() > 0:
            preferred.first.scroll_into_view_if_needed()
            preferred.first.click()
            print(f"✅ Selected matching slot: {time}")
            return

        # ✅ fallback to first available valid time
        valid_slots = [slot for slot in visible_slots if ":" in slot]  # ensure it's a time
        if valid_slots:
            fallback = valid_slots[0]
            print(f"⚠️ Requested time unavailable → using fallback: {fallback}")
            time_buttons.filter(has_text=fallback).first.scroll_into_view_if_needed()
            time_buttons.filter(has_text=fallback).first.click()
            return

        raise AssertionError("❌ No valid time slot buttons found on this property")

    def choose_tour_type(self, tour_type: str = "In-Person"):
        """Choose a tour type dynamically."""
        tour_type_option = self.page.locator("label").filter(has_text=tour_type)
        expect(tour_type_option).to_be_visible(timeout=30000)
        tour_type_option.click()

    def confirm_schedule(self, success_message: str = "Tour scheduled successfully"):
        """Confirm the tour schedule and verify success message."""
        confirm_button = self.page.get_by_role("button", name="Schedule Tour")

        # ✅ Scroll and ensure it is clickable
        confirm_button.scroll_into_view_if_needed()
        expect(confirm_button).to_be_enabled(timeout=30000)
        confirm_button.click()

        # ✅ Wait for success confirmation UI
        self.page.wait_for_load_state("domcontentloaded")

        # ✅ Validate success popup/message exists somewhere
        success_locator = self.page.locator(f"text={success_message}")
        expect(success_locator).to_be_visible(timeout=45000)

        print("✅ Tour successfully scheduled!")


