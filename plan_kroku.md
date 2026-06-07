# Plan Kroku: Zadanie C (Ścieżka 2 - Mikro-serwer Python)

Zgodnie z nowymi wytycznymi Architekta, wprowadzamy lokalny mikro-serwer w Pythonie, który będzie pełnił rolę asynchronicznego wyzwalacza (Trigger) dla skryptu scrapującego.

## Planowane działania:

1.  **Zależności Backendowe**:
    *   Dodanie `flask` do [requirements.txt](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/backend/requirements.txt).
    *   Instalacja `flask` w środowisku lokalnym.
2.  **Mikro-serwer Python**: Utworzenie [hunter_ai/backend/hunter_api.py](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/backend/hunter_api.py).
    *   Implementacja endpointu `POST /run-scraper`.
    *   Użycie `subprocess.Popen`, aby uruchomić `hunter_rwdz.py` w osobnym procesie systemowym (Fire-and-Forget).
    *   Obsługa błędów i logowanie (Trace ID).
3.  **Refaktoryzacja Next.js API**: Aktualizacja [app/api/scrape/route.ts](file:///Users/przemyslawrakotny/Documents/przemokoduje/n8n_testy/Hunter%20AI/hunter_ai/frontend/app/api/scrape/route.ts).
    *   Zmiana celu żądania na lokalny serwer Flask (`http://127.0.0.1:5000/run-scraper`).
    *   Wykorzystanie nowej zmiennej środowiskowej `SCRAPER_API_URL`.
4.  **Konfiguracja**:
    *   Backup i aktualizacja `.env.local` (ustawienie `SCRAPER_API_URL`).

## Otwarte pytania / Uwagi:
- **Środowisko Python**: Upewnię się, że używamy właściwego interpretera (np. `.venv`), jeśli jest skonfigurowany.
- **Port**: Domyślnie użyję portu 5000 dla Flaska, chyba że zostanie wskazany inny.

---
**Status**: Czekam na akceptację nowego planu (Ścieżka 2).
