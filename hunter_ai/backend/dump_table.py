import os
import logging
import uuid
import time
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def dump_table_structure():
    captcha_key = os.getenv("TWOCAPTCHA_API_KEY")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/")
        page.fill("#city", "Gliwice")
        page.fill("#decision_date_min", "2024-01-01")
        page.fill("#decision_date_max", "2024-12-31")
        
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
            
            rows = page.locator("table.table tbody tr").all()
            with open("table_structure.txt", "w") as f:
                for i, row in enumerate(rows[:5]):
                    texts = row.locator("td").all_inner_texts()
                    f.write(f"Row {i}: {texts}\n")
            
            page.screenshot(path="table_debug.png")
        browser.close()

if __name__ == "__main__":
    dump_table_structure()
