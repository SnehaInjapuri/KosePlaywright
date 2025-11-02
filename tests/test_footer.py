from koseapp_footer_page import FooterPage

def test_footer(logged_in_page):
    page = logged_in_page

    footer = FooterPage(page)
    footer.goto_home()
    footer.verify_footer_links()
