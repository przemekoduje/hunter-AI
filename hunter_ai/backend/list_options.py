from playwright.sync_api import sync_playwright

def list_options():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/")
        
        # Get all options for the document type select
        options = page.eval_on_selector("select#rwd_document_type", "el => Array.from(el.options).map(opt => ({text: opt.text, value: opt.value}))")
        print(f"Options: {options}")
        
        browser.close()

if __name__ == "__main__":
    list_options()
