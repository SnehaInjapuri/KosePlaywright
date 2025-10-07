import re
from playwright.sync_api import Page, expect


class BuyRentFilters:
    def __init__(self, page: Page):
        self.page = page

        # --- Location ---
        self.location_input = page.locator("input[aria-autocomplete='list']")
        self.location_option = lambda name: page.get_by_role("option", name=name, exact=True)

        # --- More Filters ---
        self.more_filters_button = page.get_by_role("button", name="More Filters")

        # --- Home Type (dropdown) ---
        self.home_type_dropdown = page.locator("select").first

        # --- Beds / Baths ---
        self.bed_button = lambda count: page.get_by_role("button", name=f"{count}+").nth(0)
        self.bath_button = lambda count: page.get_by_role("button", name=f"{count}+").nth(1)

        # --- Status ---
        self.status_button = lambda status: page.get_by_role("button", name=status)

        # --- Show More Filters ---
        self.show_more_filters_button = page.get_by_role("button", name="Show More Filters")

        # --- Price Range ---
        # ✅ FIX: Use labels or placeholder text visible in the DOM, not hardcoded 100000
        #self.min_price_input = page.locator("label:text('Price Range') + div input[placeholder='Min']")
        #self.max_price_input = page.locator("label:text('Price Range') + div input[placeholder='Max']")

        # --- Area (sq ft) ---
        self.square_footage_min = page.get_by_placeholder("Min Area").or_(page.locator("input[name='areaMin']"))
        self.square_footage_max = page.get_by_placeholder("Max Area").or_(page.locator("input[name='areaMax']"))

        # --- Year Built ---
        self.year_built_input_min = page.locator("label:has-text('Year Built') + div input[placeholder='Min']")
        self.year_built_input_max = page.locator("label:has-text('Year Built') + div input[placeholder='Max']")

        # --- Parking Spots ---
        self.parking_button = lambda count: page.get_by_role("button", name=f"{count}+").nth(2)

        # --- Stories ---
        self.stories_button = lambda count: page.get_by_role("button", name=f"{count}+").nth(3)

        # --- Amenities ---
        self.amenity_checkbox = lambda label: page.get_by_label(label)

        # --- Apply / Reset ---
        self.apply_filters_button = page.get_by_role("button", name=re.compile("Search|Apply Filters", re.I))
        self.reset_filters_button = page.get_by_role("button", name=re.compile("Clear|Reset", re.I))

    # --- Methods ---

    def enter_location(self, location: str, option_text: str = None):
        self.location_input.click()
        self.location_input.fill("")
        self.location_input.type(location, delay=100)

        # ✅ Wait for at least one visible suggestion option (using retry)
        self.page.wait_for_selector("role=option", timeout=10000)

        options = self.page.get_by_role("option")
        count = options.count()
        print(f"Found {count} location options")

        if count == 0:
            raise AssertionError(f"No autocomplete options found for location: {location}")

        for i in range(min(count, 5)):
            try:
                print("Option:", options.nth(i).inner_text())
            except Exception:
                pass

        if option_text:
            option = options.filter(has_text=option_text)
            if option.count() > 0:
                option.first.click()
            else:
                print(f"Option '{option_text}' not found, selecting first available")
                options.first.click()
        else:
            options.first.click()

        # ✅ Wait for map / property list to reload
        self.page.wait_for_timeout(1000)

    def open_more_filters(self):
        self.more_filters_button.scroll_into_view_if_needed()
        self.more_filters_button.click()
        self.page.wait_for_timeout(1500)  # allow animation to finish

        # ✅ Look for multiple possible markers
        possible_markers = [
            "text=/Price/i",
            "text=/Filters/i",
            "text=/Bedrooms/i",
            "select",  # fallback: any dropdown appears
        ]

        for selector in possible_markers:
            try:
                self.page.wait_for_selector(selector, timeout=4000)
                print(f"✅ Found filter section marker: {selector}")
                return
            except:
                pass

        # ❌ If still not visible, take screenshot for debugging
        print("❌ DEBUG: No expected filter markers found after clicking 'More Filters'")
        self.page.screenshot(path="filters_debug.png", full_page=True)
        raise TimeoutError("Filter panel did not open — check filters_debug.png for actual DOM.")

    def select_home_type(self, home_type: str):
        self.home_type_dropdown.select_option(label=home_type)
        expect(self.home_type_dropdown).to_have_value(home_type, timeout=3000)

    def select_bedrooms(self, count: int):
        btn = self.bed_button(count)
        btn.click()
        expect(btn).to_have_class(re.compile(".*bg-\\[#122F37\\].*"), timeout=3000)

    def select_bathrooms(self, count: int):
        btn = self.bath_button(count)
        btn.click()
        expect(btn).to_have_class(re.compile(".*bg-\\[#122F37\\].*"), timeout=3000)

    def select_status(self, status: str):
        btn = self.status_button(status)
        btn.click()
        expect(btn).to_have_class(re.compile(".*bg-\\[#122F37\\].*"), timeout=3000)

    def open_show_more_filters(self):
        self.show_more_filters_button.scroll_into_view_if_needed()
        self.show_more_filters_button.click()
        self.page.wait_for_timeout(1500)

        possible_markers = [
            "text=/Area/i",
            "text=/Year/i",
            "text=/Parking/i",
            "text=/Stories/i",
        ]

        for selector in possible_markers:
            try:
                self.page.wait_for_selector(selector, timeout=4000)
                print(f"✅ Found advanced filter marker: {selector}")
                return
            except:
                pass

        print("❌ DEBUG: No advanced filter markers found after clicking 'Show More Filters'")
        self.page.screenshot(path="showmore_debug.png", full_page=True)
        raise TimeoutError("Advanced filter panel did not open — check showmore_debug.png for actual DOM.")

    #def enter_price_range(self, min_price: str, max_price: str):
     #   """Fill the Price Range inputs (Min and Max)."""
      #  min_input = self.page.locator("label:text('Price Range') + div input[placeholder='Min']")
       # max_input = self.page.locator("label:text('Price Range') + div input[placeholder='Max']")

        #min_input.fill(min_price)
        #max_input.fill(max_price)

    def enter_square_footage(self, min_sqft: str, max_sqft: str):
        min_input = self.page.locator("label:has-text('Area (sq ft)') + div input[placeholder='Min']")
        max_input = self.page.locator("label:has-text('Area (sq ft)') + div input[placeholder='Max']")

        min_input.scroll_into_view_if_needed()
        min_input.fill(min_sqft)
        max_input.fill(max_sqft)

        expect(min_input).to_have_value(min_sqft, timeout=3000)
        expect(max_input).to_have_value(max_sqft, timeout=3000)

    def enter_year_built(self, min_year: str, max_year: str):
        # Scroll into view to avoid hidden element errors
        self.year_built_input_min.scroll_into_view_if_needed()
        self.year_built_input_min.fill(min_year)
        self.year_built_input_max.fill(max_year)

        # Validate values
        expect(self.year_built_input_min).to_have_value(min_year, timeout=3000)
        expect(self.year_built_input_max).to_have_value(max_year, timeout=3000)

    def select_parking(self, count: int):
        btn = self.parking_button(count)
        btn.click()
        expect(btn).to_have_class(re.compile(".*bg-\\[#122F37\\].*"), timeout=3000)

    def select_stories(self, count: int):
        btn = self.stories_button(count)
        btn.click()
        expect(btn).to_have_class(re.compile(".*bg-\\[#122F37\\].*"), timeout=3000)

    def toggle_amenity(self, amenity: str):
        if not amenity:
            return
        checkbox = self.amenity_checkbox(amenity)
        checkbox.check()
        expect(checkbox).to_be_checked(timeout=3000)

    def apply_filters(self):
        self.apply_filters_button.click()
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass
        self.page.wait_for_timeout(1000)

    def reset_filters(self):
        self.reset_filters_button.click()
        self.page.wait_for_timeout(500)


