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