import re

from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page:Page): # constructor
        self.page = page
        self.signin_button = page.locator("div").filter(has_text=re.compile(r"^BuyRentHome loansSign In$")).locator("div")
        self.email_input = page.get_by_placeholder("Email")
        self.password_input = page.get_by_placeholder("Password")
        self.accessyouraccount_button = page.get_by_role("button", name="Access Your Account")

    def goto(self):
        self.page.goto("https://test.koseapp.com/signin")
        self.page.wait_for_load_state("domcontentloaded")


    def click_signin(self):
        self.signin_button.click()

    def enter_email(self, email:str): #function
        self.email_input.fill(email)

    def enter_password(self, password:str): #function
        self.password_input.fill(password)

    def click_accessaccount(self):  #Method
        self.accessyouraccount_button.click()

    def login(self, email: str, password: str):
            """
            Complete login flow: click Sign In, enter credentials, click Access Your Account.
            """
            self.click_signin()
            self.enter_email(email)
            self.enter_password(password)
            self.click_accessaccount()
            # Wait for navigation or page load after login
            self.page.wait_for_load_state("networkidle")




