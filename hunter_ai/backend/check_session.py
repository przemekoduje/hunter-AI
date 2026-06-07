import os
import requests
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

def check_session_persistence():
    captcha_key = os.getenv("TWOCAPTCHA_API_KEY")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/")
        page.fill("#city", "Gliwice")
        
        # Solve first captcha
        page.locator("img#sec_code_captcha").screenshot(path="temp_captcha.png")
        with open("temp_captcha.png", "rb") as f:
            res = requests.post("http://2captcha.com/in.php", data={"key": captcha_key, "method": "post"}, files={"file": f})
        cid = res.text.split("|")[1]
        solved = None
        for _ in range(12):
            time.sleep(5)
            res = requests.get("http://2captcha.com/res.php", params={"key": captcha_key, "action": "get", "id": cid})
            if res.text.startswith("OK|"):
                solved = res.text.split("|")[1]
                break
        
        if solved:
            page.fill("#sec_code", solved)
            page.click("button.search")
            page.wait_for_selector("table.table")
            
            # Click first "pokaż"
            page.locator("a[href*='/wniosek/']").first.click()
            time.sleep(3)
            
            content = page.content()
            if "Wpisz kod" in content:
                print("SESSION PERSISTENCE FAILED: Second captcha required.")
            else:
                print("SESSION PERSISTENCE SUCCESS: Detail page visible.")
                print(f"Detail Text Snippet: {page.locator('body').inner_text()[:200]}")
                
        browser.close()

if __name__ == "__main__":
    check_session_persistence()
