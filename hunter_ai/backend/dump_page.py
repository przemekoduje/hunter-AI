from playwright.sync_api import sync_playwright

def dump_html():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/")
        # Wait for any image to be sure the page is loading
        page.wait_for_load_state("networkidle")
        html = page.content()
        with open("page_dump.html", "w") as f:
            f.write(html)
        page.screenshot(path="page_debug.png")
        browser.close()

if __name__ == "__main__":
    dump_html()
