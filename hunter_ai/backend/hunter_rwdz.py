import os
import logging
import uuid
import time
import requests
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import argparse

# Wczytanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HunterAI")

def solve_captcha(page, captcha_key, trace_id):
    """Pomocnicza funkcja do rozwiązywania CAPTCHA na stronie."""
    try:
        img_captcha = "img#sec_code_captcha"
        captcha_path = f"captcha_{int(time.time())}.png"
        
        # Czekamy na widoczność obrazka
        page.wait_for_selector(img_captcha, timeout=10000)
        page.locator(img_captcha).screenshot(path=captcha_path)
        
        logger.info(f"[Trace ID: {trace_id}] Przesyłanie CAPTCHA do 2Captcha...")
        with open(captcha_path, "rb") as f:
            response = requests.post(
                "http://2captcha.com/in.php",
                data={"key": captcha_key, "method": "post"},
                files={"file": f},
                timeout=15
            )
        
        if not response.text.startswith("OK|"):
            logger.error(f"Błąd 2Captcha IN: {response.text}")
            return False
        
        captcha_id = response.text.split("|")[1]
        solved_text = None
        for _ in range(12): # max 60s
            time.sleep(5)
            res = requests.get("http://2captcha.com/res.php", params={"key": captcha_key, "action": "get", "id": captcha_id})
            if res.text.startswith("OK|"):
                solved_text = res.text.split("|")[1]
                break
        
        if not solved_text:
            logger.error("Timeout podczas rozwiązywania CAPTCHA")
            return False
        
        logger.info(f"[Trace ID: {trace_id}] CAPTCHA rozwiązana: {solved_text}")
        page.locator("input#sec_code").fill(solved_text)
        
        # ARCHITEKT: Kliknięcie i czekanie na przeładowanie lub ukrycie loadera
        search_btn = page.locator("button.search, button[type='submit']").first
        search_btn.click()
        
        # Czekamy na ukrycie się loadera
        try:
            page.wait_for_selector("div#loading_results", state="hidden", timeout=15000)
        except:
            logger.warning("Loader div#loading_results nie zniknął w oczekiwanym czasie, kontynuuję...")
            
        return True
    except Exception as e:
        logger.error(f"Błąd solve_captcha: {str(e)}")
        return False

def extract_record_details_current(page, city, trace_id):
    """Pobiera dane z aktualnie otwartej strony szczegółów (Bardzo agresywna ekstrakcja)."""
    try:
        page.wait_for_timeout(2000) # Czekamy na renderowanie tabel
        # ARCHITEKT: Rygorystyczna logika ekstrakcji danych (Zadanie 21)
        # Zbieramy wszystkie pary klucz-wartość z każdej tabeli i div.row na stronie
        all_data = {}
        
        # 1. Przeszukaj wszystkie tabele
        tables = page.locator("table").all()
        for table in tables:
            try:
                rows = table.locator("tr").all()
                for row in rows:
                    cells = row.locator("td").all()
                    if len(cells) >= 2:
                        lbl = cells[0].inner_text().strip().lower().rstrip(":")
                        val = cells[1].inner_text().strip()
                        if lbl and val: all_data[lbl] = val
            except: continue
            
        # 2. Przeszukaj wszystkie wiersze typu div.row (fallback)
        rows = page.locator("div.row").all()
        for row in rows:
            try:
                cols = row.locator("div").all()
                # Szukamy par gdzie pierwsza kolumna to label, druga to value
                if len(cols) >= 2:
                    lbl = cols[0].inner_text().strip().lower().rstrip(":")
                    val = cols[1].inner_text().strip()
                    if lbl and val and len(lbl) < 50: # Rozsądna długość labela
                        if lbl not in all_data: all_data[lbl] = val
            except: continue

        # 3. Specyficzne szukanie "Danych inwestora" (User wspomniał o id=inwestor)
        # Próbujemy znaleźć tekst "IMIĘ" lub "NAZWA" blisko nagłówka Inwestor
        investor_name = "Nie znaleziono"
        
        # Logika dla Imię + Nazwisko
        imie = all_data.get("imię", "")
        nazwisko = all_data.get("nazwisko", "")
        if imie or nazwisko:
            investor_name = f"{imie} {nazwisko}".strip()
        else:
            # Logika dla firmy
            nazwa = all_data.get("nazwa", "")
            if nazwa:
                investor_name = nazwa

        # 4. Dane geodezyjne
        raw_dzialka = all_data.get("nr działki ew.", all_data.get("numer działki", "-"))
        clean_dzialka = raw_dzialka
        if "działka nr" in raw_dzialka.lower():
            clean_dzialka = raw_dzialka.lower().split("działka nr")[-1].strip().upper()

        return {
            "miejscowosc": city,
            "inwestor": investor_name,
            "nr_dzialki_ewid": clean_dzialka,
            "obreb_ewid": all_data.get("obręb ew.", "-"),
            "jednostka_ew": all_data.get("jednostka ew.", "-"),
            "data_wydania_decyzji": all_data.get("numer i data wydania decyzji", all_data.get("data wydania decyzji", "-")).split(" z dnia ")[-1],
            "trace_id": trace_id
        }
    except Exception as e:
        logger.error(f"Błąd ekstrakcji rekordu: {str(e)}")
        return None

def run_scraper(trace_id: str, city: str = "Gliwice", year: str = None, date_from: str = None, date_to: str = None):
    """Główna logika scrape'owania (Refaktoryzacja Strumieniowa)."""
    gunb_url = os.getenv("GUNB_URL", "https://wyszukiwarka.gunb.gov.pl/")
    captcha_key = os.getenv("TWOCAPTCHA_API_KEY")
    
    # ARCHITEKT: Dynamiczne daty (7 dni wstecz jeśli brak parametrów)
    if not date_from:
        if year:
            date_from = f"01.01.{year}"
            date_to = f"31.12.{year}"
        else:
            now = datetime.now()
            date_from = (now - timedelta(days=7)).strftime("%d.%m.%Y")
            date_to = now.strftime("%d.%m.%Y")
    
    logger.info(f"[Trace ID: {trace_id}] Konfiguracja zakresu: {date_from} - {date_to}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # ARCHITEKT: Bardziej realistyczne nagłówki, aby uniknąć "Forbidden"
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        page = context.new_page()
        
        try:
            page.goto(gunb_url, timeout=30000)
            
            # ARCHITEKT: Selektory oparte na VALUE
            logger.info(f"[Trace ID: {trace_id}] Wypełnianie formularza...")
            
            # Typ wyszukiwania (Radio)
            # Używamy click() zamiast check(), aby na pewno wywołać zdarzenia JS strony
            page.locator("input[name='document_type'][value='rwd']").click()
            
            # Czekamy aż pola staną się dostępne
            page.wait_for_selector("select#invest_purpose", state="visible", timeout=10000)
            
            page.locator("input#city").fill(city)
            
            # Typ dokumentu: Decyzja pozytywna
            page.select_option("select#rwd_document_type", value="Decyzja pozytywna")
            
            # Rodzaj zamierzenia: budowa nowych (Value=1)
            page.select_option("select#invest_purpose", value="1")
            
            # Kategoria obiektu: I (Value=2)
            page.select_option("select#invest", value="2")
            
            # Daty (format DD.MM.RRRR)
            page.locator("input#decision_date_min").fill(date_from)
            page.locator("input#decision_date_max").fill(date_to)
            
            if not solve_captcha(page, captcha_key, trace_id):
                raise Exception("Proces rozwiązywania CAPTCHA nie powiódł się.")
            
            # Czekamy na tabelę
            page.wait_for_selector("table.table", timeout=20000)
            
            extracted_data = []
            page_count = 1
            max_records = 50 # Bezpieczny limit dla jednego biegu
            
            # ARCHITEKT: Strumieniowe przetwarzanie strona po stronie
            while len(extracted_data) < max_records:
                logger.info(f"[Trace ID: {trace_id}] Przetwarzanie strony wyników nr {page_count}...")
                
                # Czekamy na wiersze tabeli
                page.wait_for_selector("table.table tbody tr", timeout=10000)
                rows_count = page.locator("table.table tbody tr").count()
                
                if rows_count == 0:
                    logger.info("Brak wyników na tej stronie.")
                    break

                for i in range(rows_count):
                    if len(extracted_data) >= max_records: break
                    
                    try:
                        # Pobieramy link z konkretnego wiersza
                        row = page.locator("table.table tbody tr").nth(i)
                        link = row.locator("td a").first
                        
                        if not link.is_visible(): continue
                        
                        logger.info(f"[Trace ID: {trace_id}] Otwieranie szczegółów rekordu {i+1}/{rows_count}...")
                        
                        # Klikamy w link zamiast goto(url), aby zachować sesję/referrer
                        link.click()
                        page.wait_for_load_state("networkidle")
                        
                        # Wyciągamy dane (teraz funkcja nie potrzebuje URL, bo jesteśmy już na stronie)
                        record = extract_record_details_current(page, city, trace_id)
                        if record:
                            extracted_data.append(record)
                            logger.info(f"[Trace ID: {trace_id}] Pobrano: {record['inwestor']}")
                        
                        # Wracamy do listy wyników
                        page.go_back()
                        page.wait_for_selector("table.table", timeout=10000)
                        time.sleep(random.uniform(1, 2)) # Krótka przerwa po powrocie
                        
                    except Exception as e:
                        logger.error(f"Błąd przy rekordzie {i+1}: {e}")
                        # Spróbujmy wrócić do tabeli na wszelki wypadek
                        try: 
                            page.goto(gunb_url) # Fallback jeśli go_back zawiedzie
                            # Tu musielibyśmy znowu wypełnić formularz, co jest skomplikowane.
                            # Lepiej po prostu logować błąd i kontynuować jeśli jesteśmy na dobrej stronie.
                        except: pass
                
                if len(extracted_data) >= max_records: break
                
                # Szukamy przycisku "Następna"
                next_btn = page.locator("a[aria-label='Następna'], .pagination a:has-text('Następna')").first
                if next_btn.is_visible() and next_btn.is_enabled():
                    next_btn.click()
                    time.sleep(2)
                    page.wait_for_load_state("networkidle")
                    page_count += 1
                else:
                    logger.info("Brak kolejnych stron wyników.")
                    break

            return extracted_data

        except Exception as e:
            logger.error(f"Błąd krytyczny skrapera: {str(e)}")
            return None
        finally:
            browser.close()

def main():
    parser = argparse.ArgumentParser(description='Hunter AI Scraper')
    parser.add_argument('--city', type=str, default='Gliwice')
    parser.add_argument('--year', type=str, default=None)
    parser.add_argument('--trace', type=str, default=str(uuid.uuid4()))
    args = parser.parse_args()

    logger.info(f"START BIEGU | City: {args.city} | Trace: {args.trace}")
    
    data = run_scraper(args.trace, city=args.city, year=args.year)
    if data:
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        logger.info(f"Przesyłanie {len(data)} rekordów do n8n...")
        try:
            response = requests.post(webhook_url, json=data, timeout=20)
            logger.info(f"Status n8n: {response.status_code}")
        except Exception as e:
            logger.error(f"Błąd wysyłki: {str(e)}")
    else:
        logger.error("Brak danych do wysłania.")

if __name__ == "__main__":
    main()
