from playwright.sync_api import sync_playwright

def inspect_detail():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/wniosek/320cafed-4b92-497b-9a11-fe2ed2fa12fc/")
        
        # We know there's a captcha on the detail page from detail_dump.html
        # Let's see if we can just see the labels WITHOUT solving it? 
        # No, detail_dump.html showed the captcha FORM.
        
        # WAIT! If the detail page needs a captcha, the bot MUST solve it for EVERY record.
        # This is very expensive.
        
        # Is there any other way? 
        # Let's check the search results page again.
        # Maybe the parcel number is in the HTML source but hidden?
        
        page.goto("https://wyszukiwarka.gunb.gov.pl/")
        # ... search logic ...
        # (I'll skip the full search here, I just want to know if I can bypass the detail captcha)
        
        browser.close()

if __name__ == "__main__":
    inspect_detail()
