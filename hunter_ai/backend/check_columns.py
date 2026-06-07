import os
import requests
import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

def check_hidden_columns():
    captcha_key = os.getenv("TWOCAPTCHA_API_KEY")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://wyszukiwarka.gunb.gov.pl/")
        page.fill("#city", "Gliwice")
        
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
            
            # Check all column headers
            headers = page.locator("table.table thead th").all_inner_texts()
            print(f"Headers: {headers}")
            
            # Check row 1 cells (including hidden ones)
            row1_cells = page.locator("table.table tbody tr:first-child td").all()
            for i, cell in enumerate(row1_cells):
                visible = cell.is_visible()
                text = cell.inner_text()
                html = cell.inner_html()
                print(f"Cell {i}: visible={visible}, text='{text}', html='{html[:50]}...'")
                
        browser.close()

if __name__ == "__main__":
    check_hidden_columns()
