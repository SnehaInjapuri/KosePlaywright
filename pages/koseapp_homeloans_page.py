import re
from playwright.sync_api import Page, expect


class HomeLoansPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto_home(self):
        """Navigate to homepage and verify it's loaded."""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator("text=Buy").first).to_be_visible(timeout=30000)


    # ✅ Enhanced with proper waits + validations
    def explore_home_loans(self):
        print("🏠 Navigating to Home Loans section...")

        self.page.get_by_role("link", name="Home loans").click()
        expect(self.page).to_have_url(re.compile(r".*/home-loans"))

        # ✅ Ensure page load
        self.page.wait_for_timeout(1500)

        # ✅ Click first tile → See more
        first_see_more = self.page.locator("span", has_text="See more").first
        expect(first_see_more).to_be_visible(timeout=15000)
        first_see_more.click()

        # ✅ Verify slide panel present
        panel = self.page.locator("div.fixed").filter(has_text="Mortgages")
        expect(panel).to_be_visible(timeout=20000)

        loan_sections = [
            "Adjustable Rate Mortgages",
            "Fixed Rate Mortgages",
            "FHA Loan",
            "VA Home Loan",
            "Jumbo Loan",
            "Non-QM Loans"
        ]

        for loan in loan_sections:
            print(f"\n📌 Checking loan type inside panel: {loan}")

            left_nav_item = self.page.locator("div.cursor-pointer").filter(has_text=loan).first
            expect(left_nav_item).to_be_visible(timeout=20000)

            left_nav_item.scroll_into_view_if_needed()

            # ✅ JS Click to bypass overlay blocking interactions
            self.page.evaluate("(el) => el.click()", left_nav_item.element_handle())

            # ✅ Wait for heading to appear
            detail_header = self.page.get_by_role("heading", name=re.compile(loan, re.I)).first
            expect(detail_header).to_be_visible(timeout=20000)

            print(f"✅ Verified: {loan}")

        print("\n🎯 All loan sections validated successfully ✅")

        # ✅ Close button after validation
        close_btn = self.page.get_by_role("button", name="Close").first
        expect(close_btn).to_be_visible(timeout=15000)
        close_btn.click()

        # ✅ Apply Now opens popup tab
        with self.page.expect_popup() as popup:
            apply_btn = self.page.get_by_role("button", name="Apply Now")
            expect(apply_btn).to_be_visible(timeout=20000)
            apply_btn.click()

        popup_page = popup.value
        popup_page.wait_for_load_state("domcontentloaded")
        expect(popup_page).to_have_url(re.compile("apply", re.I))
        print("✅ Apply popup opened & URL verified!")