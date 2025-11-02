import pytest
from pages.koseapp_home_page import HomePage
from pages.koseapp_scheduletour_page import KoseappScheduleTourPage

def test_schedule_tour(logged_in_page, base_url):
    """End-to-end: schedule a tour with existing login fixture"""

    #home_page = HomePage(logged_in_page)

    # ✅ User already logged in → Go to Buy page
    #home_page.click_buy_button()

    # ✅ Create tour page instance
    tour_page = KoseappScheduleTourPage(logged_in_page, base_url)

    # ✅ Start scheduling flow
    tour_page.search_city("Dallas, TX")
    tour_page.open_first_property_card()
    tour_page.select_date_and_time("Thu 06 Nov 2025", "09:00 AM")
    tour_page.choose_tour_type("In-Person")
    tour_page.confirm_schedule()
