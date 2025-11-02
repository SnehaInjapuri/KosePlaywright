import os
import pytest
from playwright.sync_api import Page
from pages.koseapp_homeloans_page import HomeLoansPage


def test_home_loan(logged_in_page, base_url):
    """End-to-end test: login and home loan view."""
    homeloans_page = HomeLoansPage(logged_in_page, base_url)


    # ✅ Step 1: Home Loans Method call
    homeloans_page.explore_home_loans()
