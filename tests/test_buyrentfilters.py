import pytest
from playwright.sync_api import Page, expect
from pages.koseapp_buyrentfilters_page import BuyRentFilters


@pytest.mark.parametrize("search_type", ["Buy", "Rent"])
def test_filter_properties(page: Page, logged_in_page, search_type):
    page = logged_in_page  # Already logged in
    filters_page = BuyRentFilters(page)

    # --- Test data ---
    test_data = {
        "location_search": "Dallas",
        "location_option": "Dallas, TX, USA",
        "home_type": "Condos",
        "bedrooms": 3,
        "bathrooms": 2,
        "status": "Contract",
      #  "price_min": "100000",
       # "price_max": "500000",
        "sqft_min": "2000",
        "sqft_max": "4000",
        "year_built_min": "1990",
        "year_built_max": "2024",
        "parking": 2,
        "stories": 2,
        "amenities": ["Pool", "Gym"],
    }

    # --- Step 1: Navigate to property search ---
    page.goto(f"https://test.koseapp.com/propertysearch?type={search_type}")

    # --- Step 2: Enter location ---
    filters_page.enter_location(test_data["location_search"], test_data["location_option"])

    # --- Step 3: Open More Filters section ---
    filters_page.open_more_filters()

    # --- Step 4: Apply filters ---
    filters_page.select_home_type(test_data["home_type"])
    filters_page.select_bedrooms(test_data["bedrooms"])
    filters_page.select_bathrooms(test_data["bathrooms"])
    filters_page.select_status(test_data["status"])
    #filters_page.enter_price_range(test_data["price_min"], test_data["price_max"])

    # --- Step 5: Open  Show More Filters section ---
    filters_page.open_show_more_filters()
    filters_page.enter_square_footage(test_data["sqft_min"], test_data["sqft_max"])
    filters_page.enter_year_built(test_data["year_built_min"], test_data["year_built_max"])
    filters_page.select_parking(test_data["parking"])
    filters_page.select_stories(test_data["stories"])

    for amenity in test_data["amenities"]:
        filters_page.toggle_amenity(amenity)

    # --- Step 6: Apply filters ---
    filters_page.apply_filters()

    # --- Step 7: Validate results ---
    prop_card = page.locator("div.property-card").first
    no_results = page.locator("text='No results'").first

    try:
        # Wait up to 15s for either to appear
        prop_card.wait_for(state="visible", timeout=15000)
        print("✅ Properties loaded with applied filters")
    except TimeoutError:
        try:
            no_results.wait_for(state="visible", timeout=5000)
            print("⚠️ No results found for applied filters")
        except TimeoutError:
            raise AssertionError("❌ Neither results nor 'No results' message appeared after waiting")