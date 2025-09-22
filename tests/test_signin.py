import re
from idlelib.search import SearchDialog

from playwright.sync_api import Page, expect

from pages.koseapp_buy_page import BuyPage
from pages.koseapp_login_page import LoginPage
from pages.koseapp_home_page import HomePage


def test_example(page: Page) -> None:
    login_page = LoginPage(page)
    home_page = HomePage(page)
    buy_page = BuyPage(page)

#Navbar Click
    page.goto("https://test.koseapp.com/")
    login_page.signin_button.click()
    login_page.enter_email("sneha.injapuri@koseapp.com")
    login_page.enter_password("Sneha@1234")
    login_page.click_accessaccount()

#Buy Page Location Search

    home_page.click_buy_button()
    #buy_page.click_location()
   # buy_page.enter_location("Dallas")
  #  buy_page.select_location_option()

#Rent Page Location Search
    home_page.click_rent_button()
    #expect(home_page.is_homeloans_button_visible()).to.be.true()
    expect(home_page.homeloans_button).to_be_visible()




