from playwright.sync_api import expect
from pages.koseapp_likedislike_property_page import LikedislikePropertyPage

def test_like_dislike_properties(logged_in_page):
    page = logged_in_page
    likedislike_page = LikedislikePropertyPage(page)

    likedislike_page.open_recommended_listings()
    likedislike_page.like_first_property()
    likedislike_page.like_second_property()
    likedislike_page.dislike_third_property()

    likedislike_page.open_profile()
    expect(page.get_by_role("menuitem", name="My Profile")).to_be_visible()

    likedislike_page.open_liked_listings()
    expect(page.locator(".property-card")).to_be_visible()

    likedislike_page.open_disliked_listings()
    expect(page.locator(".property-card")).to_be_visible()
