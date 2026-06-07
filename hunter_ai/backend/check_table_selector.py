from playwright.sync_api import sync_playwright

def get_results_selector():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/")
        page.fill("#city", "Gliwice")
        page.fill("#decision_date_min", "2024-01-01")
        page.fill("#decision_date_max", "2024-12-31")
        
        # We need to solve captcha here manually or just see if there is a table class on the page even if empty
        # Actually, let's just look for any table in the whole page after some time
        page.wait_for_timeout(2000)
        html = page.content()
        with open("search_page_initial.html", "w") as f:
            f.write(html)
        browser.close()

if __name__ == "__main__":
    get_results_selector()
