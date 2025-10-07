from playwright.sync_api import expect, Page


class LikedislikePropertyPage:
    def __init__(self, page: Page):
        self.page = page
        self.recommended_list_link = page.get_by_role("link", name="See all recommended listings")

        # Target buttons inside recommendation cards only
        self.first_like_button = page.locator("div.flex.absolute.top-2 .mr-2").first
        self.second_like_button = page.locator("div.flex.absolute.top-2 .mr-2").nth(1)
        self.third_dislike_button = page.locator("div.flex.absolute.top-2 .mr-2").nth(2)

        # Profile button - stable selector (avoid dynamic radix IDs)
        self.profile_logo = page.locator("button[aria-haspopup='menu']")

        self.my_profile_item = page.get_by_role("menuitem", name="My Profile")
        self.liked_listings_link = page.get_by_role("link", name="Liked Listings", exact=True)
        self.disliked_listings_link = page.get_by_role("link", name="Disliked Listings")

    def open_recommended_listings(self):
        expect(self.recommended_list_link).to_be_visible(timeout=10000)
        self.recommended_list_link.click()
        self.page.wait_for_selector("div.relative img[alt^='Image of']", timeout=20000)

    def like_first_property(self):
        expect(self.first_like_button).to_be_visible(timeout=20000)
        self.first_like_button.click()
        self.page.wait_for_timeout(1000)

    def like_second_property(self):
        expect(self.second_like_button).to_be_visible(timeout=20000)
        self.second_like_button.click()
        self.page.wait_for_timeout(1000)

    def dislike_third_property(self):
        expect(self.third_dislike_button).to_be_visible(timeout=20000)
        self.third_dislike_button.click()
        self.page.wait_for_timeout(1000)

    def open_profile(self):
        expect(self.profile_logo).to_be_visible(timeout=10000)
        self.profile_logo.click()
        expect(self.my_profile_item).to_be_visible(timeout=10000)
        self.my_profile_item.click()

    def open_liked_listings(self):
        expect(self.liked_listings_link).to_be_visible(timeout=10000)
        self.liked_listings_link.click()
        expect(self.page.locator(".property-card").first).to_be_visible(timeout=10000)

    def open_disliked_listings(self):
        expect(self.disliked_listings_link).to_be_visible(timeout=10000)
        self.disliked_listings_link.click()
        expect(self.page.locator(".property-card").first).to_be_visible(timeout=10000)