import pytest
from playwright.sync_api import Page, expect
from pages.koseapp_likedislike_property_page import LikedislikePropertyPage


def test_like_dislike_properties(page: Page):
    # Go to property recommendations page
    page.goto("https://test.koseapp.com/")

    # Create Page Object
    likedislike_page = LikedislikePropertyPage(page)

    # Step 1: Open recommended list
    likedislike_page.open_recommended_listings()

    # Step 2: Like first property
    likedislike_page.like_first_property()

    # Step 3: Like second property
    likedislike_page.like_second_property()

    # Step 4: Dislike third property
    likedislike_page.dislike_third_property()

    # Step 5: Open profile menu
    likedislike_page.open_profile()
    expect(page.get_by_role("menuitem", name="My Profile")).to_be_visible()

    # Step 6: Open Liked Listings
    likedislike_page.open_liked_listings()
    expect(page.locator(".property-card")).to_be_visible()

    # Step 7: Open Disliked Listings
    likedislike_page.open_disliked_listings()
    expect(page.locator(".property-card")).to_be_visible()
