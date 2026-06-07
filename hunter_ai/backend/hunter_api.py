import sys
import subprocess
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Ścieżka do skryptu scrapującego (w tym samym folderze)
SCRAPER_SCRIPT = os.path.join(os.path.dirname(__file__), 'hunter_rwdz.py')

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    data = request.json or {}
    city = data.get('city', 'Gliwice')
    year = data.get('year', '2024')
    trace_id = data.get('traceId', request.headers.get('x-trace-id', 'unknown'))
    
    print(f"[Trace ID: {trace_id}] Sygnał: Uruchomienie scrapingu dla miasta: {city}, rok: {year}")

    try:
        # ARCHITEKT: Przekazujemy parametry jako argumenty linii komend
        # subprocess.Popen nie blokuje wykonania - Fire-and-Forget
        subprocess.Popen([
            sys.executable, 
            SCRAPER_SCRIPT, 
            "--city", city, 
            "--year", str(year),
            "--trace", trace_id
        ])
        
        print(f"[Trace ID: {trace_id}] Proces {SCRAPER_SCRIPT} został uruchomiony w tle.")
        
        return jsonify({
            "status": "accepted",
            "message": "Scraper started in background",
            "traceId": trace_id
        }), 202

    except Exception as e:
        print(f"[Trace ID: {trace_id}] BŁĄD podczas uruchamiania procesu: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "traceId": trace_id
        }), 500

if __name__ == '__main__':
    print("--- Hunter AI: Mikro-serwer Wyzwalacza ---")
    print("Słucham na: http://127.0.0.1:5000")
    app.run(port=5000, debug=False)
