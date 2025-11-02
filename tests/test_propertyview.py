from pages.koseapp_propertyview_page import KoseappPropertyViewPage


def test_property_view(logged_in_page, base_url):
    page = logged_in_page
    propertyview_page = KoseappPropertyViewPage(logged_in_page, base_url)

    #propertyview_page.goto_home()
    propertyview_page.search_city("Dallas, TX")

    propertyview_page.switch_view("Grid")
    propertyview_page.open_first_property_card()
    propertyview_page.click_back_button()

    propertyview_page.switch_view("Map")
    propertyview_page.click_first_property_on_map()

    propertyview_page.switch_view("Split")
    propertyview_page.open_first_property_card()
    propertyview_page.click_back_button()
