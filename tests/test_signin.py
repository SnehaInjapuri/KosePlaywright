from playwright.sync_api import expect
from pages.koseapp_signin_page import SignInPage

def test_signin_flow(logged_in_page):
    page = logged_in_page

    signin_page = SignInPage(page)
   # signin_page.open_profile_menu()

    # ✅ Assert post-login UI
    #expect(page.get_by_text("Your Profile")).to_be_visible(timeout=30000)
