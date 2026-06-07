from playwright.sync_api import sync_playwright

def dump_detail():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/wniosek/320cafed-4b92-497b-9a11-fe2ed2fa12fc/")
        page.wait_for_load_state("networkidle")
        html = page.content()
        with open("detail_dump.html", "w") as f:
            f.write(html)
        browser.close()

if __name__ == "__main__":
    dump_detail()
