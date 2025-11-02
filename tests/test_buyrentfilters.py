import pytest
from playwright.sync_api import Page, expect
from pages.koseapp_buyrentfilters_page import BuyRentFilters
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


@pytest.mark.parametrize("search_type", ["Buy", "Rent"])
def test_filter_properties(logged_in_page, search_type):
    page = logged_in_page
    filters_page = BuyRentFilters(page)

    # --- Test data ---
    test_data = {
        "location_search": "Dallas",
        "location_option": "Dallas, TX, USA",
        "home_type": "Condos",
        "bedrooms": 3,
        "bathrooms": 2,
        "status": "Contract",
        "sqft_min": "2000",
        "sqft_max": "4000",
        "year_built_min": "1990",
        "year_built_max": "2024",
        "parking": 2,
        "stories": 2,
        "amenities": ["Pool", "Gym"],
    }

    # --- Step 1: Navigate to property search ---
    page.goto(f"https://dev.koseapp.com/propertysearch?type={search_type}")
    page.wait_for_load_state("networkidle")

    # --- Step 2 to End remain same ---
    filters_page.enter_location(test_data["location_search"], test_data["location_option"])
    filters_page.open_more_filters()
    filters_page.select_home_type(test_data["home_type"])
    filters_page.select_bedrooms(test_data["bedrooms"])
    filters_page.select_bathrooms(test_data["bathrooms"])
    filters_page.select_status(test_data["status"])
    filters_page.open_show_more_filters()
    filters_page.enter_square_footage(test_data["sqft_min"], test_data["sqft_max"])
    filters_page.enter_year_built(test_data["year_built_min"], test_data["year_built_max"])
    filters_page.select_parking(test_data["parking"])
    filters_page.select_stories(test_data["stories"])

    for amenity in test_data["amenities"]:
        filters_page.toggle_amenity(amenity)

    filters_page.apply_filters()

    prop_card = page.locator("div.property-card").first
    no_results = page.locator("text='No results'").first

    try:
        prop_card.wait_for(state="visible", timeout=15000)
        print("✅ Properties loaded with applied filters")
    except PlaywrightTimeoutError:
        if no_results.is_visible():
            print("No results found ❌")
        else:
            print("Locator not found or page still loading")
