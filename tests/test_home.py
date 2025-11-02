from pages.koseapp_home_page import HomePage

def test_homepage_after_login(logged_in_page):
    # ✅ Reuse the logged-in page and load HomePage object
    home_page = HomePage(logged_in_page)

    # ✅ Now use HomePage actions
    home_page.click_buy_button()
    home_page.click_rent_button()
    home_page.is_homeloans_button_visible()