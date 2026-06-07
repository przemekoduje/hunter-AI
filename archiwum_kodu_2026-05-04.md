--- FILE: Instrukcja_Systemowa_Antigravity.md ---
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
--- FILE: plan_kroku.md ---
# Plan Kroku: Interaktywny Panel Filtrów "Premium" (Zadanie 18)

## Cel
Wdrożenie nowoczesnego, estetycznego interfejsu wyszukiwania na froncie, który pozwoli użytkownikowi wybrać miasto oraz rok. Zmiana ma na celu nie tylko poprawę użyteczności (filtrowanie danych), ale również podniesienie standardu wizualnego aplikacji (Premium Look & Feel).

## Pliki
* `[NEW] hunter_ai/frontend/components/SearchFilters.tsx`: Nowy komponent formularza z selektorami.
* `[MODIFY] hunter_ai/frontend/app/page.tsx`: Integracja filtrów i obsługa stanów.
* `[MODIFY] hunter_ai/frontend/app/api/leads/route.ts`: Obsługa parametrów zapytania (query params) i filtrowanie w Prisma.
* `[MODIFY] hunter_ai/frontend/app/globals.css`: Dodanie tokenów wizualnych dla stylu "Premium".

## Logika
1.  **Komponent Filtrowania**: Stworzę elegancki panel (prawdopodobnie w formie karty z lekkim gradientem/szkłem), zawierający:
    *   `Select` dla miasta (domyślnie "Gliwice").
    *   `Select` dla roku (2024, 2025).
    *   Przycisk "Szukaj / Odśwież" z animacją hover.
2.  **API Route**: Rozbuduję funkcję `GET` o wyciąganie `city` i `year` z URL. Prisma wykona filtrowanie po stronie bazy:
    *   `miejscowosc: { contains: city, mode: 'insensitive' }`
    *   `data_wydania_decyzji: { contains: year }` (ponieważ data to string).
3.  **Frontend State**: `fetchLeads` będzie teraz budować URL z parametrami, np. `/api/leads?city=Gliwice&year=2024`.

## Koszty
* **Baza Danych**: Zapytania do MongoDB są darmowe w ramach obecnego klastra (limit operacji odczytu).
* **Vercel/Hosting**: Brak dodatkowych kosztów (operacje po stronie klienta i lekkie API).

## Otwarty punkt (Pytanie do użytkownika)
1.  **Dynamiczny Scraper?** Czy po kliknięciu "Szukaj", jeśli danych nie ma w bazie, bot powinien automatycznie odpalić scraping w tle (wymagałoby to dodatkowej logiki kolejkowania), czy na razie skupiamy się wyłącznie na filtrowaniu tego, co już mamy pobrane?
2.  **Stylistyka**: Czy preferujesz styl "Google Clean" (biały, czysty), czy "Modern Dark SaaS" (ciemny, neonowe akcenty, glassmorphism)?

---
Proces planowania został ukończony. **STOP.** Nie modyfikuję kodu. Czekam na Twoją akceptację tego planu (komenda "Dalej").

--- FILE: diff_ostatni_krok.md ---
# Diff Ostatni Krok: Panel Filtrów RWDZ (Zadanie 18)

## Opis zmian
Zaimplementowano system filtrowania leadów po stronie frontendu i backendu, zgodnie z wytycznymi stylu "Google Clean" (Material Design).

### 1. Warstwa Prezentacji (Frontend)
*   **[NEW] `SearchFilters.tsx`**: Stworzono minimalistyczny panel wyszukiwania (Miasto, Rok) z wykorzystaniem płaskich komponentów, whitespace i koloru akcji Google Blue (#1a73e8).
*   **[MODIFY] `page.tsx`**: 
    *   Dodano stany `city` i `year`.
    *   Zintegrowano `SearchFilters`.
    *   Zaktualizowano `fetchLeads` do obsługi `URLSearchParams`.
    *   Wprowadzono mechanizm generowania unikalnego `Trace ID` przy każdej zmianie parametrów wyszukiwania (Traceability).
    *   Zastosowano twarde kopie bezpieczeństwa `.bak`.

### 2. Warstwa Logiki (Backend API)
*   **[MODIFY] `route.ts`**: 
    *   Dodano przechwytywanie parametrów `city` i `year`.
    *   Zaimplementowano dynamiczne budowanie obiektu `where` dla Prisma ORM.
    *   Zastosowano filtrowanie `contains` z flagą `mode: 'insensitive'` dla miast.
    *   Filtrowanie dat odbywa się poprzez dopasowanie fragmentu stringa (roku).

## Zmiany w kodzie (Diff)

### API Route (`route.ts`)
```diff
 export async function GET(request: NextRequest) {
+  const { searchParams } = new URL(request.url);
+  const city = searchParams.get('city');
+  const year = searchParams.get('year');
+  
   const traceId = request.headers.get('x-trace-id') || undefined;
-  logInfo('Otrzymano żądanie pobrania leadów...', traceId);
+  logInfo(`Zapytanie o leady (API) - Filtry: miasto=${city || 'brak'}, rok=${year || 'brak'}`, traceId);
 
   try {
+    const where: any = {};
+    if (city) where.miejscowosc = { contains: city, mode: 'insensitive' };
+    if (year) where.data_wydania_decyzji = { contains: year };
+
     const leads = await prisma.lead.findMany({
+      where,
       orderBy: { id: 'desc' }
     });
```

### Main Page (`page.tsx`)
```diff
-  const fetchLeads = async () => {
-    const traceId = getTraceId();
+  const fetchLeads = async (isInitial = false) => {
+    const traceId = getTraceId(); 
     logInfo(`Inicjacja pobierania (miasto: ${city}, rok: ${year})`, traceId);
+    const params = new URLSearchParams({ city, year });
-    const response = await fetch('/api/leads', {
+    const response = await fetch(`/api/leads?${params.toString()}`, {
```

## Status weryfikacji
*   [x] Generowanie Trace ID dla każdego zapytania.
*   [x] Filtrowanie Prisma (contains/insensitive).
*   [x] Estetyka Google Clean (Brak gradientów, płaskie UI).
*   [x] Kopia .bak plików źródłowych.

--- FILE: hunter_ai/backend/hunter_rwdz.py ---
import os
import logging
import uuid
import time
import requests
import random
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

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
            return False
        
        logger.info(f"[Trace ID: {trace_id}] CAPTCHA rozwiązana: {solved_text}")
        page.locator("input#sec_code").fill(solved_text)
        # Przycisk wyszukaj ma różne klasy zależnie od strony
        search_btn = page.locator("button.search, button[type='submit']")
        search_btn.first.click()
        return True
    except Exception as e:
        logger.error(f"Błąd solve_captcha: {str(e)}")
        return False

def run_scraper(trace_id: str):
    """Główna logika scrape'owania."""
    gunb_url = os.getenv("GUNB_URL", "https://wyszukiwarka.gunb.gov.pl/")
    captcha_key = os.getenv("TWOCAPTCHA_API_KEY")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Rotacja prostych User-Agentów
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        context = browser.new_context(user_agent=random.choice(user_agents))
        page = context.new_page()
        
        try:
            logger.info(f"[Trace ID: {trace_id}] Start: {gunb_url}")
            time.sleep(random.uniform(2, 5)) # Losowa przerwa na start
            page.goto(gunb_url, timeout=30000)
            
            # Formularz
            page.locator("input#city").fill("Gliwice")
            page.select_option("select#rwd_document_type", "Decyzja pozytywna")
            page.locator("input#decision_date_min").fill("2024-01-01")
            page.locator("input#decision_date_max").fill("2024-12-31")
            
            if not solve_captcha(page, captcha_key, trace_id):
                raise Exception("Nie udało się rozwiązać pierwszej CAPTCHA")
            
            page.wait_for_selector("table.table", timeout=30000)
            rows_count = page.locator("table.table tbody tr").count()
            logger.info(f"[Trace ID: {trace_id}] Znaleziono {rows_count} rekordów w tabeli.")

            extracted_data = []
            process_limit = 30
            
            # Pobieramy linki (z obsługą paginacji)
            detail_urls = []
            logger.info(f"[Trace ID: {trace_id}] Zbieranie linków (limit: {process_limit})...")
            
            while len(detail_urls) < process_limit:
                page.wait_for_selector("table.table", timeout=30000)
                # Znajdź wszystkie unikalne linki do wniosków
                links = page.locator("table.table tbody tr td a").all()
                for link in links:
                    href = link.get_attribute("href")
                    if href and "/wniosek/" in href:
                        full_url = f"https://wyszukiwarka.gunb.gov.pl{href}" if href.startswith("/") else href
                        if full_url not in detail_urls:
                            detail_urls.append(full_url)
                    if len(detail_urls) >= process_limit: break
                
                if len(detail_urls) >= process_limit: break
                
                # Paginacja - obsługa różnych wariantów przycisku 'Następna'
                next_btn = page.locator("a[aria-label='Następna'], .pagination a:has-text('Następna'), .pagination a:has-text('>')").first
                if next_btn.is_visible():
                    current_page = len(detail_urls) // 10
                    logger.info(f"[Trace ID: {trace_id}] Klikam 'Następna' (strona {current_page}, zebrano: {len(detail_urls)})...")
                    next_btn.click()
                    time.sleep(2)
                    page.wait_for_load_state("networkidle")
                else:
                    break

            logger.info(f"[Trace ID: {trace_id}] Zebrano łącznie {len(detail_urls)} linków do przetworzenia.")

            for url in detail_urls:
                try:
                    logger.info(f"[Trace ID: {trace_id}] Szczegóły: {url}")
                    page.goto(url, timeout=20000)
                    time.sleep(1) # Czas na renderowanie
                    
                    # Budujemy mapę wszystkich pól na stronie (Key-Value)
                    fields = {}
                    try:
                        rows = page.locator("div.row").all()
                        for row in rows:
                            cols = row.locator("div").all()
                            if len(cols) >= 2:
                                lbl = cols[0].inner_text().strip().lower().rstrip(":")
                                val = cols[1].inner_text().strip()
                                if lbl and val:
                                    fields[lbl] = val
                    except Exception as e:
                        logger.warning(f"Błąd skanowania pól: {e}")

                    # 1. Czyszczenie numeru działki
                    raw_dzialka = fields.get("nr działki ew.", fields.get("numer działki", ""))
                    clean_dzialka = raw_dzialka
                    if "działka nr" in raw_dzialka.lower():
                        clean_dzialka = raw_dzialka.lower().split("działka nr")[-1].strip().upper()
                    elif not clean_dzialka and "dzialka" in str(fields):
                        # Próba ratunkowa jeśli label był inny
                        for k, v in fields.items():
                            if "działka" in k: clean_dzialka = v.split("nr")[-1].strip().upper()

                    # 2 & 3. Inwestor (Imię + Nazwisko lub Nazwa firmy)
                    imie = fields.get("imię", "")
                    nazwisko = fields.get("nazwisko", "")
                    # "nazwa" to często nazwa firmy inwestora, "inwestor" to etykieta zbiorcza
                    nazwa_firmy = fields.get("nazwa", "") 
                    inwestor_label = fields.get("inwestor", "")
                    
                    if imie or nazwisko:
                        inwestor_final = f"{imie} {nazwisko}".strip()
                    elif nazwa_firmy and len(nazwa_firmy) < 150: # Unikamy długich opisów projektów
                        inwestor_final = nazwa_firmy
                    else:
                        inwestor_final = inwestor_label if inwestor_label else "Nie znaleziono"

                    record = {
                        "miejscowosc": "Gliwice",
                        "inwestor": inwestor_final,
                        "nr_dzialki_ewid": clean_dzialka,
                        "obreb_ewid": fields.get("obręb ew.", fields.get("obręb", "-")),
                        "jednostka_ew": fields.get("jednostka ew.", fields.get("jednostka ewidencyjna", "-")),
                        "data_wydania_decyzji": fields.get("numer i data wydania decyzji", fields.get("data wydania decyzji", "-")),
                        "trace_id": trace_id
                    }
                    
                    # Czyszczenie daty (jeśli jest format "Decyzja nr ... z dnia 2024-01-01")
                    if " z dnia " in record["data_wydania_decyzji"]:
                        record["data_wydania_decyzji"] = record["data_wydania_decyzji"].split(" z dnia ")[-1]
                    elif record["data_wydania_decyzji"] == "-":
                        record["data_wydania_decyzji"] = "Brak (W trakcie)"

                    if record["nr_dzialki_ewid"]:
                        extracted_data.append(record)
                        logger.info(f"[Trace ID: {trace_id}] Zapisano: {record['nr_dzialki_ewid']}")
                    else:
                        logger.warning(f"[Trace ID: {trace_id}] Brak danych działki dla {url}")
                        
                except Exception as e_row:
                    logger.warning(f"Błąd wiersza {url}: {str(e_row)}")

            return extracted_data

        except Exception as e:
            logger.error(f"Błąd krytyczny: {str(e)}")
            page.screenshot(path="error_fatal.png")
            return None
        finally:
            browser.close()

def main():
    trace_id = "550e8400-e29b-41d4-a716-446655440000"
    logger.info(f"BIEG PRODUKCYJNY START (Trace: {trace_id})")
    
    data = run_scraper(trace_id)
    if data:
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        logger.info(f"Wysyłka {len(data)} rekordów do n8n pod adres {webhook_url}...")
        
        # Diagnostyka: czy n8n w ogóle żyje?
        try:
            requests.get("http://localhost:5678/", timeout=2)
            logger.info("Serwer n8n odpowiada na localhost:5678.")
        except Exception as e:
            logger.error(f"BRAK KONTAKTU z n8n na localhost:5678: {e}")

        try:
            response = requests.post(webhook_url, json=data, timeout=20)
            logger.info(f"STATUS n8n: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"Treść błędu n8n (prawdopodobnie workflow nie jest Active): {response.text}")
            print(f"DONE: {len(data)} records sent.")
        except Exception as e:
            logger.error(f"Błąd wysyłki do n8n: {str(e)}")
    else:
        logger.error("Brak danych do wysłania.")

if __name__ == "__main__":
    main()

--- FILE: hunter_ai/frontend/app/page.tsx ---
"use client";

import { useState, useEffect } from 'react';
import { getTraceId, logInfo, logError } from '@/utils/logger';
import { RwdzLead } from '@/types';
import LeadsTable from '@/components/LeadsTable';
import SearchFilters from '@/components/SearchFilters';

export default function Home() {
  const [leads, setLeads] = useState<RwdzLead[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Stany filtrów
  const [city, setCity] = useState('Gliwice');
  const [year, setYear] = useState('2024');

  const fetchLeads = async (isInitial = false) => {
    // Generujemy nowe Trace ID dla każdej akcji użytkownika (chyba że to start strony)
    const traceId = getTraceId(); 
    setLoading(true);
    setError(null);
    logInfo(`Inicjacja pobierania (miasto: ${city}, rok: ${year})`, traceId);

    try {
      const params = new URLSearchParams({
        city,
        year
      });

      const response = await fetch(`/api/leads?${params.toString()}`, {
        method: 'GET',
        headers: {
          'x-trace-id': traceId
        }
      });
      
      if (!response.ok) {
        throw new Error(`API zwróciło status: ${response.status}`);
      }
      
      const data: RwdzLead[] = await response.json();
      
      setLeads(data);
      logInfo(`Pobrano pomyślnie ${data.length} rekordów`, traceId);
    } catch (err: any) {
      logError('Błąd pobierania danych', err, traceId);
      setError('Wystąpił błąd podczas pobierania danych z bazy.');
    } finally {
      setLoading(false);
    }
  };

  // Pobierz dane na start (opcjonalnie, wg preferencji architekta)
  useEffect(() => {
    fetchLeads(true);
  }, []);

  return (
    <div className="min-h-screen bg-white text-[#202124] p-4 md:p-8 lg:p-12 font-sans">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Header Section - Minimalist Google Style */}
        <header className="pb-4">
          <h1 className="text-2xl font-normal text-gray-900">Eksplorator Leadów RWDZ</h1>
          <p className="text-sm text-gray-600 mt-1">System analityczny pozwoleń na budowę (GUNB)</p>
        </header>

        {/* Search Panel */}
        <SearchFilters 
          city={city} 
          setCity={setCity} 
          year={year} 
          setYear={setYear} 
          onSearch={() => fetchLeads()} 
          loading={loading}
        />

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 text-red-700 p-4 rounded shadow-sm">
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Results Counter */}
        <div className="flex justify-between items-center px-1">
          <span className="text-sm text-gray-500">
            Znaleziono: <span className="font-medium text-gray-900">{leads.length}</span> rekordów
          </span>
        </div>

        {/* Data Table Section */}
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
          <LeadsTable leads={leads} />
        </div>

      </div>
    </div>
  );
}

--- FILE: hunter_ai/frontend/app/api/leads/route.ts ---
import { NextRequest, NextResponse } from 'next/server';
import { logInfo, logError } from '@/utils/logger';
import prisma from '@/lib/prisma';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const city = searchParams.get('city');
  const year = searchParams.get('year');
  
  // Przechwycenie Trace ID z nagłówków
  const traceId = request.headers.get('x-trace-id') || undefined;
  
  logInfo(`Zapytanie o leady (API) - Filtry: miasto=${city || 'brak'}, rok=${year || 'brak'}`, traceId);

  try {
    const where: any = {};
    
    if (city) {
      where.OR = [
        { miejscowosc: { contains: city, mode: 'insensitive' } },
        { display_name: { contains: city, mode: 'insensitive' } }
      ];
    }

    // Pobranie rekordów z bazy przez Prisma ORM
    const leads = await prisma.lead.findMany({
      where,
      orderBy: {
        id: 'desc'
      }
    });

    logInfo(`Pomyślnie pobrano ${leads.length} rekordów z MongoDB pasujących do filtrów`, traceId);

    // Mapowanie i parsowanie display_name dla frontendu
    const parsedLeads = leads.map(lead => {
      let street = '';
      let houseNumber = '';
      let cityParsed = lead.miejscowosc || '';

      if (lead.display_name) {
        const parts = lead.display_name.split(',').map(p => p.trim());
        
        // Logika parsująca: szukamy elementu z numerem (ma cyfry) i elementu z ulicą
        // Zazwyczaj numer jest blisko początku
        for (let i = 0; i < Math.min(parts.length, 4); i++) {
          const part = parts[i];
          const hasDigits = /\d/.test(part);
          const isOnlyDigits = /^\d+[a-zA-Z]?$/.test(part);

          if (hasDigits && !houseNumber) {
            houseNumber = part;
          } else if (!hasDigits && !street && part.length > 3) {
            street = part;
          }
        }

        // Szukamy miasta w całym ciągu
        const cityIndex = parts.findIndex(p => 
          p.toLowerCase().includes('gliwice') || 
          (city && p.toLowerCase().includes(city.toLowerCase()))
        );
        if (cityIndex !== -1) cityParsed = parts[cityIndex];
      }

      return {
        ...lead,
        street: street || 'Brak danych',
        houseNumber: houseNumber || 'n/a',
        city: cityParsed || 'Nieznane',
        miejscowosc: cityParsed || lead.miejscowosc,
        zamierzenie: lead.display_name
      };
    });

    return NextResponse.json(parsedLeads, {
      headers: {
        'x-trace-id': traceId || ''
      }
    });

  } catch (error) {
    logError('Błąd podczas filtrowania bazy danych MongoDB', error, traceId);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}

--- FILE: hunter_ai/frontend/components/LeadsTable.tsx ---
import { RwdzLead } from '@/types';

interface LeadsTableProps {
  leads: RwdzLead[];
}

export default function LeadsTable({ leads }: LeadsTableProps) {
  return (
    <div className="bg-gray-50 rounded shadow-sm border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-200 text-sm font-medium text-gray-500">
              <th className="p-4">Inwestor</th>
              <th className="p-4">Ulica</th>
              <th className="p-4">Numer</th>
              <th className="p-4">Miasto</th>
              <th className="p-4">Pełny Adres</th>
            </tr>
          </thead>
          <tbody className="text-sm text-[#202124]">
            {leads.length > 0 ? (
              leads.map((lead, idx) => (
                <tr key={idx} className="border-b border-gray-200 bg-white hover:bg-gray-50 transition-colors">
                  <td className="p-4 font-medium">{lead.inwestor}</td>
                  <td className="p-4">{lead.street}</td>
                  <td className="p-4">{lead.houseNumber}</td>
                  <td className="p-4">{lead.city}</td>
                  <td className="p-4 text-xs text-gray-500 max-w-xs truncate" title={lead.display_name || ''}>
                    {lead.display_name}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="p-8 text-center text-gray-500 bg-white">
                  Brak danych do wyświetlenia. Spróbuj zmienić filtry lub wyszukać ponownie.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

--- FILE: hunter_ai/frontend/components/SearchFilters.tsx ---
"use client";

import React from 'react';

interface SearchFiltersProps {
  city: string;
  setCity: (city: string) => void;
  year: string;
  setYear: (year: string) => void;
  onSearch: () => void;
  loading: boolean;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({ 
  city, 
  setCity, 
  year, 
  setYear, 
  onSearch, 
  loading 
}) => {
  return (
    <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-8 flex flex-col md:flex-row items-end gap-4">
      <div className="flex-1 w-full space-y-2">
        <label htmlFor="city" className="block text-sm font-medium text-gray-700">Miasto</label>
        <input
          id="city"
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="np. Gliwice"
          className="w-full bg-white border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#1a73e8] focus:border-[#1a73e8]"
        />
      </div>
      
      <div className="w-full md:w-32 space-y-2">
        <label htmlFor="year" className="block text-sm font-medium text-gray-700">Rok</label>
        <select
          id="year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          className="w-full bg-white border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[#1a73e8] focus:border-[#1a73e8]"
        >
          <option value="2024">2024</option>
          <option value="2025">2025</option>
          <option value="2023">2023</option>
        </select>
      </div>

      <button
        onClick={onSearch}
        disabled={loading}
        className="w-full md:w-auto bg-[#1a73e8] hover:bg-blue-700 text-white font-medium py-2 px-8 rounded shadow-sm transition-colors disabled:opacity-50"
      >
        {loading ? 'Szukanie...' : 'Szukaj'}
      </button>
    </div>
  );
};

export default SearchFilters;

--- FILE: hunter_ai/frontend/prisma/schema.prisma ---
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "mongodb"
  url      = env("DATABASE_URL")
}

model Lead {
  id           String  @id @default(auto()) @map("_id") @db.ObjectId
  inwestor     String
  display_name String?

  // Pola opcjonalne (starsza struktura lub inne rekordy)
  miejscowosc          String?
  data_wydania_decyzji String?
  nr_dzialki_ewid      String?
  obreb_ewid           String?
  jednostka_ew         String?
  trace_id             String?

  @@map("leads")
}

--- FILE: hunter_ai/frontend/types/index.ts ---
export interface RwdzLead {
  inwestor: string;
  street: string;
  houseNumber: string;
  city: string;
  display_name?: string;
  
  // Pola opcjonalne dla kompatybilności
  data_wydania_decyzji?: string;
  miejscowosc?: string;
  nr_dzialki_ewid?: string;
  obreb_ewid?: string;
  jednostka_ew?: string;
}

--- FILE: hunter_ai/frontend/utils/logger.ts ---
export const getTraceId = (): string => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  // Fallback for environments where crypto.randomUUID is not available
  return 'xxxx-xxxx-xxxx-xxxx'.replace(/[x]/g, () =>
    (Math.random() * 16 | 0).toString(16)
  );
};

export const logError = (message: string, error?: any, traceId?: string) => {
  const currentTraceId = traceId || getTraceId();
  console.error(`[Trace ID: ${currentTraceId}] ${message}`, error || '');
  // Docelowo: wysyłka błędu do zewnętrznego systemu (Sentry, n8n webhook logów)
};

export const logInfo = (message: string, traceId?: string) => {
  const currentTraceId = traceId || getTraceId();
  console.info(`[Trace ID: ${currentTraceId}] ${message}`);
};

