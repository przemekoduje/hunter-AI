from playwright.sync_api import sync_playwright

def test_robust_get_val():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page.goto("https://wyszukiwarka.gunb.gov.pl/wniosek/320cafed-4b92-497b-9a11-fe2ed2fa12fc/")
        
        # We might get a captcha here if we are not in a session, but let's see.
        if "Wpisz kod" in page.content():
             print("Captcha detected - test failed to see data.")
             browser.close()
             return

        def get_val_robust(labels):
            if isinstance(labels, str): labels = [labels]
            rows = page.locator("div.row").all()
            for row in rows:
                cols = row.locator("div").all()
                if len(cols) >= 2:
                    label_text = cols[0].inner_text().strip()
                    for l in labels:
                        if l.lower() in label_text.lower():
                            return cols[1].inner_text().strip()
            return ""

        print(f"Nr dzialki: {get_val_robust(['Nr działki ew', 'Numer działki'])}")
        print(f"Inwestor: {get_val_robust(['Inwestor', 'Nazwa'])}")
        
        browser.close()

if __name__ == "__main__":
    test_robust_get_val()
