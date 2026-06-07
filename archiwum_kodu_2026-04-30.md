# Archiwum Projektu: Hunter AI (2026-04-30)

## Struktura plików:
```
Hunter AI
├── Instrukcja_Systemowa_Antigravity.md
├── diff_ostatni_krok.md
├── hunter_ai
│   └── backend
│       ├── hunter_rwdz.py
│       └── requirements.txt
└── plan_kroku.md
```

## Zawartość plików:

### Plik: Instrukcja_Systemowa_Antigravity.md
```
# Reguły Pracy Antigravity (Koder)

## Obieg Pracy (Workflow)
Krok 1: Otrzymujesz zadanie do wykonania.
Krok 2: Generujesz tekstowy plik `plan_kroku.md`.
Krok 3: BEZWZGLĘDNIE zatrzymujesz pracę. Nie piszesz i nie modyfikujesz żadnego kodu.
Krok 4: Czekasz na dokładną komendę akceptacyjną: "Dalej".
Krok 5: Po otrzymaniu komendy "Dalej" wdrażasz kod i modyfikujesz pliki.
Krok 6: Natychmiast po wdrożeniu generujesz plik `diff_ostatni_krok.md` z listą zmienionych linii i opisem zmian.

## Komendy Specjalne
* Komenda "Dalej": Jedyny sygnał autoryzujący wykonanie edycji kodu według planu z kroku 2.
* Komenda "Archiwum": Na ten sygnał musisz wygenerować plik tekstowy o stałej nazwie `archiwum_kodu_2026-04-28.md` i ZAWSZE zapisać go (nadpisując poprzedni) w katalogu: `/Users/przemyslawrakotny/Library/CloudStorage/GoogleDrive-przemek.rakotny@gmail.com/Mój dysk/### Projekty AI ###/AI (12 miesiecy z AI)/#   mamToSprawdzone/n8n_testy (do # mam to sprawdzone)/Hunter AI DG`. Plik ten będzie zawierał:
  1. Drzewo struktury plików projektu.
  2. Pełną zawartość (kod źródłowy) wszystkich stworzonych i zmodyfikowanych plików w projekcie.
  3. BEZWZGLĘDNE WYKLUCZENIA: Omijaj pliki środowiskowe, zależności i buildy. Nie dołączaj: `node_modules`, `venv`, `__pycache__`, `.env`, `.git`, folderów `dist`/`build` ani plików blokad (np. `package-lock.json`).

## Struktura pliku plan_kroku.md
Wymagane sekcje planu to:
* Cel: Krótkie podsumowanie zadania.
* Pliki: Lista plików do edycji lub stworzenia.
* Logika: Opis działania i użytych pakietów.
* Koszty: Szacunkowe koszty wywołania kodu (np. zapytania API, zużycie procesora).

## Standardy Kodowania
* Krokowe wdrażanie: Pisz wyłącznie małe, izolowane funkcje.
* Zmienne: Całkowity zakaz hardkodowania haseł i tokenów (używaj zmiennych środowiskowych ENV).
* Logowanie: Każda funkcja musi posiadać logi (INFO/ERROR) z unikalnym identyfikatorem `Trace ID`.
* Bezpieczeństwo: Przed każdą edycją istniejącego pliku twórz jego kopię z rozszerzeniem `.bak`.
```

### Plik: diff_ostatni_krok.md
```
# Raport Zmian (Diff) - Ostatni Krok

Poniżej znajduje się kod źródłowy z ostatniego wdrożenia (Zadanie 6: Integracja z n8n - uścisk dłoni), wygenerowany w formacie `git diff`:

## Modyfikacje w pliku: `hunter_ai/backend/hunter_rwdz.py`

```diff
--- hunter_rwdz.py.bak	2026-04-28 22:21:29
+++ hunter_rwdz.py	2026-04-28 22:21:45
@@ -238,10 +238,30 @@
     if check_environment():
         logger.info(f"[Trace ID: {trace_id}] Środowisko gotowe do działania.")
         data = run_scraper(trace_id)
-        if data is not None:
+        if data:
             logger.info(f"[Trace ID: {trace_id}] Zakończono proces sukcesem. Zwrócono {len(data)} rekordów.")
+            
+            webhook_url = os.getenv("N8N_WEBHOOK_URL")
+            if not webhook_url:
+                logger.error(f"[Trace ID: {trace_id}] Brak zdefiniowanego N8N_WEBHOOK_URL. Przerywam wysyłkę.")
+                return
+            
+            logger.info(f"[Trace ID: {trace_id}] Rozpoczynam wysyłkę danych do n8n (Webhook)...")
+            for attempt in range(1, 4):
+                try:
+                    response = requests.post(webhook_url, json=data, timeout=10)
+                    response.raise_for_status()
+                    logger.info(f"[Trace ID: {trace_id}] Sukces! Dane przesłane do n8n (Status: {response.status_code}).")
+                    break
+                except requests.RequestException as e:
+                    logger.warning(f"[Trace ID: {trace_id}] Próba {attempt}/3 wysyłki do n8n nie powiodła się: {str(e)}")
+                    if attempt < 3:
+                        time.sleep(2)
+            else:
+                logger.error(f"[Trace ID: {trace_id}] Uścisk dłoni z n8n NIE POWIÓDŁ SIĘ po 3 próbach.")
+                
         else:
-            logger.error(f"[Trace ID: {trace_id}] Proces zakończył się niepowodzeniem (brak danych).")
+            logger.error(f"[Trace ID: {trace_id}] Proces zakończył się niepowodzeniem (brak danych lub błąd krytyczny).")
     else:
         logger.warning(f"[Trace ID: {trace_id}] Skrypt zatrzymany z powodu błędnej konfiguracji środowiska.")
 
```

```

### Plik: plan_kroku.md
```
# Plan Kroku: Zadanie 6

## Cel
Wdrożenie mechanizmu "uścisku dłoni" (Handshake) między przygotowanym skryptem a systemem orkiestracji n8n. Zebrane, przefiltrowane dane zostaną przekazane na odpowiedni webhook za pomocą żądania POST z zaimplementowanym systemem ponawiania prób (Retry Pattern) dla podniesienia stabilności.

## Pliki
* `hunter_ai/backend/hunter_rwdz.py` (Modyfikacja)

## Logika
1. **Weryfikacja danych i URL:**
   - W bloku `main()` po odebraniu `data`, weryfikacja czy zmienna nie jest pusta (`if data:`).
   - Załadowanie zmiennej docelowej `webhook_url = os.getenv("N8N_WEBHOOK_URL")`.
   - Przypadek brzegowy: Zalogowanie absolutnego błędu `ERROR` i przedwczesne zakończenie skryptu, jeżeli webhook nie został zdefiniowany w `.env`.
2. **Mechanizm Ponawiania Prób (Retry Pattern):**
   - Budowa pętli `for attempt in range(1, 4):` dającej maksymalnie 3 szanse na komunikację.
   - Wywołanie wewnątrz `try`: `requests.post(webhook_url, json=data, timeout=10)`.
   - Weryfikacja kodów HTTP poprzez `response.raise_for_status()`. W razie 200/201 – logger odnotuje sukces (Trace ID) i instrukcja `break` przerwie pętlę.
3. **Obsługa Ostrzeżeń i Przerw:**
   - Jeżeli `requests` zgłosi `RequestException`, zostanie to przechwycone blokiem `except`.
   - Moduł zgłosi `WARNING` (np. "Próba X nie powiodła się") i wymusi uśpienie algorytmu na 2 sekundy (`time.sleep(2)`) przed ponownym uderzeniem.
4. **Logika Błędu Krytycznego:**
   - Wykorzystanie mało znanej, acz wydajnej instrukcji języka Python – `else:` dla pętli `for`. Kod ten wykona się tylko w sytuacji, gdy pętla wyczerpie wszystkie iteracje bez natrafienia na `break`. Zostanie w niej wygenerowany ostateczny komunikat `ERROR` informujący, że integracja z n8n nie powiodła się pomimo prób.

## Koszty
Podobnie jak poprzednio, sama operacja logistyczna nic nie kosztuje (chyba że środowisko docelowe w chmurze n8n będzie generować własne opłaty, co jest całkowicie poza rygorem tego skryptu). Stanowi natomiast kluczową bramkę dla przesyłu wartości do dalszego potoku N8N.

```

### Plik: hunter_ai/backend/hunter_rwdz.py
```
import os
import logging
import uuid
import time
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Wczytanie zmiennych środowiskowych z pliku .env (jeśli istnieje)
load_dotenv()

# Konfiguracja głównego loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("HunterAI")

def check_environment():
    """Funkcja walidująca konfigurację środowiska."""
    trace_id = str(uuid.uuid4())
    logger.info(f"[Trace ID: {trace_id}] Rozpoczęto inicjalizację środowiska...")

    gunb_url = os.getenv("GUNB_URL")
    n8n_url = os.getenv("N8N_WEBHOOK_URL")
    captcha_key = os.getenv("TWOCAPTCHA_API_KEY")

    missing_keys = []
    if not gunb_url:
        missing_keys.append("GUNB_URL")
    if not n8n_url:
        missing_keys.append("N8N_WEBHOOK_URL")
    if not captcha_key:
        missing_keys.append("TWOCAPTCHA_API_KEY")

    if missing_keys:
        logger.error(f"[Trace ID: {trace_id}] Braki w konfiguracji środowiska: {', '.join(missing_keys)}")
        return False
    
    logger.info(f"[Trace ID: {trace_id}] Konfiguracja środowiska poprawna.")
    return True

def run_scraper(trace_id: str):
    """Główna logika scrape'owania z użyciem Playwright."""
    logger.info(f"[Trace ID: {trace_id}] Inicjalizacja środowiska Playwright...")
    
    gunb_url = os.getenv("GUNB_URL")
    playwright = None
    browser = None
    
    try:
        playwright = sync_playwright().start()
        # Można zmienić headless=False do celów debugowania
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        logger.info(f"[Trace ID: {trace_id}] Przechodzenie pod adres URL: {gunb_url}")
        page.goto(gunb_url, timeout=30000)
        
        # Opcjonalna obsługa okien zgód cookies/RODO
        try:
            logger.info(f"[Trace ID: {trace_id}] Sprawdzanie obecności popupów z cookies...")
            # Przykładowy selektor, do dostosowania pod konkretną stronę
            accept_btn = page.wait_for_selector("button:has-text('Akceptuj'), button:has-text('Zgadzam się')", timeout=3000)
            if accept_btn:
                accept_btn.click()
                logger.info(f"[Trace ID: {trace_id}] Kliknięto przycisk akceptacji cookies.")
        except PlaywrightTimeoutError:
            logger.info(f"[Trace ID: {trace_id}] Nie wykryto popupa z cookies w zadanym czasie.")
            
        # Zrzut ekranu jako dowód poprawnego załadowania interfejsu
        screenshot_path = "debug_start.png"
        page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"[Trace ID: {trace_id}] Wykonano zrzut ekranu do pliku: {screenshot_path}")

        # Precyzyjna interakcja z formularzem RWDZ
        logger.info(f"[Trace ID: {trace_id}] Rozpoczęto wypełnianie formularza...")

        # 1. Rodzaj wyszukiwania
        # DO ZMIANY: Selektor radio buttona
        radio_wyszukiwanie = "input[type='radio']:near(:text('Wyszukiwanie pozwoleń na budowę'))"
        page.locator(radio_wyszukiwanie).first.check()
        logger.info(f"[Trace ID: {trace_id}] Zaznaczono 'Wyszukiwanie pozwoleń na budowę'.")

        # 2. Typ dokumentu
        # DO ZMIANY: Selektor typu dokumentu
        select_typ_dok = "select:near(:text('Typ dokumentu'))"
        page.locator(select_typ_dok).first.select_option(label="decyzja pozytywna")
        logger.info(f"[Trace ID: {trace_id}] Wybrano Typ dokumentu: 'decyzja pozytywna'.")

        # 3. Data wydania decyzji (od / do)
        # DO ZMIANY: Selektory dat
        input_data_od = "input[placeholder*='RRRR-MM-DD']:near(:text('od'))"
        input_data_do = "input[placeholder*='RRRR-MM-DD']:near(:text('do'))"
        page.locator(input_data_od).first.type("2024-01-01", delay=100)
        page.locator(input_data_do).first.type("2024-12-31", delay=100)
        logger.info(f"[Trace ID: {trace_id}] Uzupełniono daty wydania decyzji (2024-01-01 - 2024-12-31).")

        # 4. Województwo
        # DO ZMIANY: Selektor województwa w 'Informacje o obiekcie'
        select_woj = "select:near(:text('Województwo'))"
        page.locator(select_woj).first.select_option(label="śląskie")
        logger.info(f"[Trace ID: {trace_id}] Wybrano Województwo: 'śląskie'.")

        # 5. Miejscowość
        # DO ZMIANY: Selektor miejscowości
        input_miasto = "input:near(:text('Miejscowość'))"
        page.locator(input_miasto).first.type("Gliwice", delay=100)
        logger.info(f"[Trace ID: {trace_id}] Wpisano Miejscowość: 'Gliwice'.")

        # 6. Rodzaj zamierzenia
        # DO ZMIANY: Selektor rodzaju zamierzenia
        select_rodzaj = "select:near(:text('Rodzaj zamierzenia budowlanego'))"
        page.locator(select_rodzaj).first.select_option(label="budowa nowego obiektu budowlanego")
        logger.info(f"[Trace ID: {trace_id}] Wybrano Rodzaj zamierzenia: 'budowa nowego obiektu budowlanego'.")

        # 7. Kategoria obiektu
        # DO ZMIANY: Selektor kategorii obiektu
        select_kat = "select:near(:text('Kategoria obiektu'))"
        page.locator(select_kat).first.select_option(label="I")
        logger.info(f"[Trace ID: {trace_id}] Wybrano Kategorię obiektu: 'I'.")

        # Obsługa obrazkowego CAPTCHA
        logger.info(f"[Trace ID: {trace_id}] Lokalizacja obrazka CAPTCHA...")
        # DO ZMIANY: Selektor obrazka captcha
        img_captcha = "img[src*='captcha']"
        captcha_path = "captcha.png"
        page.locator(img_captcha).first.screenshot(path=captcha_path)
        logger.info(f"[Trace ID: {trace_id}] Wykonano zrzut CAPTCHA do pliku: {captcha_path}")

        logger.info(f"[Trace ID: {trace_id}] Przesyłanie CAPTCHA do 2Captcha...")
        captcha_key = os.getenv("TWOCAPTCHA_API_KEY")
        
        try:
            with open(captcha_path, "rb") as f:
                response = requests.post(
                    "http://2captcha.com/in.php",
                    data={"key": captcha_key, "method": "post"},
                    files={"file": f},
                    timeout=15
                )
            
            in_result = response.text
            if not in_result.startswith("OK|"):
                logger.error(f"[Trace ID: {trace_id}] Błąd 2Captcha IN: {in_result}")
                raise Exception(f"Błąd wysyłki do 2Captcha: {in_result}")
            
            captcha_id = in_result.split("|")[1]
            logger.info(f"[Trace ID: {trace_id}] CAPTCHA wysłana pomyślnie. Otrzymano ID: {captcha_id}")
            
            logger.info(f"[Trace ID: {trace_id}] Oczekiwanie na rozwiązanie (polling)...")
            solved_text = None
            max_retries = 12  # max 60s (12 * 5s)
            
            for _ in range(max_retries):
                time.sleep(5)
                res_response = requests.get(
                    "http://2captcha.com/res.php",
                    params={"key": captcha_key, "action": "get", "id": captcha_id},
                    timeout=15
                )
                res_result = res_response.text
                
                if res_result == "CAPCHA_NOT_READY":
                    logger.info(f"[Trace ID: {trace_id}] CAPTCHA jeszcze niegotowa, czekam...")
                    continue
                elif res_result.startswith("OK|"):
                    solved_text = res_result.split("|")[1]
                    logger.info(f"[Trace ID: {trace_id}] Otrzymano rozwiązanie CAPTCHA: {solved_text}")
                    break
                else:
                    logger.error(f"[Trace ID: {trace_id}] Błąd 2Captcha RES: {res_result}")
                    raise Exception(f"Błąd weryfikacji 2Captcha: {res_result}")
                    
            if not solved_text:
                logger.error(f"[Trace ID: {trace_id}] Timeout - nie rozwiązano CAPTCHA w przewidzianym czasie (60s).")
                raise Exception("CAPTCHA timeout")
                
            # Wpisanie otrzymanego kodu
            # DO ZMIANY: Selektor pola tekstowego captcha
            input_captcha = "input:near(:text('Wpisz kod'))"
            logger.info(f"[Trace ID: {trace_id}] Wpisywanie rozwiązania CAPTCHA w pole: {input_captcha}")
            page.locator(input_captcha).first.type(solved_text, delay=100)
            
            # Wysłanie formularza
            # DO ZMIANY: Selektor przycisku wyszukiwania
            btn_wyszukaj = "button:has-text('Wyszukaj'), button:has-text('Szukaj')"
            logger.info(f"[Trace ID: {trace_id}] Klikanie przycisku wyszukiwania: {btn_wyszukaj}")
            page.locator(btn_wyszukaj).first.click()
            
            logger.info(f"[Trace ID: {trace_id}] Oczekiwanie na tabelę wyników...")
            # DO ZMIANY: Selektor tabeli wyników
            page.wait_for_selector("table", timeout=30000)
            
            logger.info(f"[Trace ID: {trace_id}] Tabela załadowana. Rozpoczynam ekstrakcję danych...")
            # DO ZMIANY: Selektor wierszy tabeli
            rows = page.locator("table tbody tr").all()
            
            extracted_data = []
            
            for row in rows[:50]:
                try:
                    td = row.locator("td").all_inner_texts()
                    record = {
                        # DO ZMIANY: Dopasować indeksy tablicy do rzeczywistych kolumn
                        "numer_decyzji": td[0] if len(td) > 0 else "",
                        "inwestor": td[1] if len(td) > 1 else "",
                        "zamierzenie": td[2] if len(td) > 2 else ""
                    }
                    extracted_data.append(record)
                except Exception as ex_row:
                    logger.warning(f"[Trace ID: {trace_id}] Błąd podczas ekstrakcji wiersza: {str(ex_row)}")
                    
            logger.info(f"[Trace ID: {trace_id}] Ekstrakcja zakończona. Pobrane rekordy: {len(extracted_data)}")
            
            return extracted_data

        except Exception as e_api:
            logger.error(f"[Trace ID: {trace_id}] Wystąpił błąd podczas obsługi API 2Captcha/Requests: {str(e_api)}")
            raise e_api

    except Exception as e:
        logger.error(f"[Trace ID: {trace_id}] Wystąpił błąd podczas pracy Playwright: {str(e)}")
        return None
    finally:
        logger.info(f"[Trace ID: {trace_id}] Rozpoczęto zamykanie sesji przeglądarki.")
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
        logger.info(f"[Trace ID: {trace_id}] Zamknięto środowisko Playwright i sesję przeglądarki.")

def main():
    trace_id = str(uuid.uuid4())
    logger.info(f"[Trace ID: {trace_id}] Uruchomienie skryptu hunter_rwdz.py")
    
    if check_environment():
        logger.info(f"[Trace ID: {trace_id}] Środowisko gotowe do działania.")
        data = run_scraper(trace_id)
        if data:
            logger.info(f"[Trace ID: {trace_id}] Zakończono proces sukcesem. Zwrócono {len(data)} rekordów.")
            
            webhook_url = os.getenv("N8N_WEBHOOK_URL")
            if not webhook_url:
                logger.error(f"[Trace ID: {trace_id}] Brak zdefiniowanego N8N_WEBHOOK_URL. Przerywam wysyłkę.")
                return
            
            logger.info(f"[Trace ID: {trace_id}] Rozpoczynam wysyłkę danych do n8n (Webhook)...")
            for attempt in range(1, 4):
                try:
                    response = requests.post(webhook_url, json=data, timeout=10)
                    response.raise_for_status()
                    logger.info(f"[Trace ID: {trace_id}] Sukces! Dane przesłane do n8n (Status: {response.status_code}).")
                    break
                except requests.RequestException as e:
                    logger.warning(f"[Trace ID: {trace_id}] Próba {attempt}/3 wysyłki do n8n nie powiodła się: {str(e)}")
                    if attempt < 3:
                        time.sleep(2)
            else:
                logger.error(f"[Trace ID: {trace_id}] Uścisk dłoni z n8n NIE POWIÓDŁ SIĘ po 3 próbach.")
                
        else:
            logger.error(f"[Trace ID: {trace_id}] Proces zakończył się niepowodzeniem (brak danych lub błąd krytyczny).")
    else:
        logger.warning(f"[Trace ID: {trace_id}] Skrypt zatrzymany z powodu błędnej konfiguracji środowiska.")

if __name__ == "__main__":
    main()

```

### Plik: hunter_ai/backend/requirements.txt
```
playwright
requests
python-dotenv

```

