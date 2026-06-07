# Podsumowanie Zmian: Zadanie 20 (Dynamiczny Scraper i Filtrowanie)

System został w pełni udynamiczniony. Przycisk **"Pobierz nowe"** reaguje teraz na wybrane przez Ciebie miasto i rok, a Dashboard poprawnie filtruje wyniki z bazy danych.

## Zrealizowane działania:

1.  **Frontend**: Zaktualizowano [SearchFilters.tsx](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/frontend/components/SearchFilters.tsx). Przycisk "Pobierz nowe" wysyła teraz wybrane miasto i rok do API.
2.  **Next.js API (Trigger)**: Zaktualizowano [api/scrape/route.ts](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/frontend/app/api/scrape/route.ts). Endpoint odbiera parametry i przekazuje je do mikro-serwera Flask.
3.  **Next.js API (Leads)**: Zaktualizowano [api/leads/route.ts](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/frontend/app/api/leads/route.ts). Wdrożono poprawne filtrowanie po **Roku** w bazie MongoDB.
4.  **Mikro-serwer Python**: Zaktualizowano [hunter_api.py](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/backend/hunter_api.py). Serwer przekazuje miasto i rok jako argumenty do skryptu scrapera.
5.  **Scraper RWDZ**: Zaktualizowano [hunter_rwdz.py](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/backend/hunter_rwdz.py). 
    *   Wprowadzono obsługę argumentów `--city` i `--year`.
    *   Zakres dat wyszukiwania jest teraz obliczany dynamicznie (np. dla roku 2025: od 2025-01-01 do 2025-12-31).

## Jak przetestować:
1. Zmień miasto na **"Zabrze"** lub rok na **"2025"**.
2. Kliknij **"Pobierz nowe"**.
3. Obserwuj logi serwera `hunter_api.py` – zobaczysz, że scraper szuka danych dla nowych parametrów.
4. Po zakończeniu kliknij **"Szukaj"**, aby odświeżyć tabelę (widok będzie filtrowany po nowym mieście/roku).

---
**Status**: System jest w pełni dynamiczny. Rozwiązano problem "braku nowych danych" wynikający z sztywnej konfiguracji.
