import { NextResponse } from 'next/server';
import { getTraceId, logInfo, logError } from '@/utils/logger';

export async function POST(request: Request) {
  const traceId = getTraceId();
  const body = await request.json().catch(() => ({}));
  const { city, year } = body;

  logInfo(`Otrzymano żądanie wyzwalania scrapingu (API) - Miasto: ${city}, Rok: ${year}`, traceId);

  const scraperApiUrl = process.env.SCRAPER_API_URL;
// ... (reszta weryfikacji bez zmian)
  if (!scraperApiUrl) {
    const errorMsg = 'Brak skonfigurowanej zmiennej SCRAPER_API_URL w środowisku.';
    logError(errorMsg, new Error(errorMsg), traceId);
    return NextResponse.json(
      { error: 'Błąd konfiguracji serwera (brak SCRAPER_API_URL).', traceId },
      { status: 500 }
    );
  }

  try {
    // ARCHITEKT: Uderzamy w lokalny mikro-serwer Python (Flask) z parametrami
    fetch(scraperApiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-trace-id': traceId
      },
      body: JSON.stringify({
        action: 'start_scraping',
        city,
        year,
        traceId
      })
    }).catch(err => {
      // Logujemy błąd asynchronicznie, jeśli n8n nie odpowiedziało
      logError('Błąd podczas asynchronicznego wyzwalania n8n', err, traceId);
    });

    logInfo('Sygnał wyzwalający wysłany do n8n (Fire-and-Forget)', traceId);

    // Natychmiastowa odpowiedź dla Frontendu
    return NextResponse.json(
      { 
        message: 'Proces scrapingu został pomyślnie uruchomiony w tle.',
        traceId,
        status: 'accepted'
      }, 
      { 
        status: 202,
        headers: { 'x-trace-id': traceId }
      }
    );

  } catch (error) {
    logError('Błąd krytyczny podczas obsługi endpointu /api/scrape', error, traceId);
    return NextResponse.json(
      { error: 'Wystąpił błąd podczas próby uruchomienia procesu.', traceId },
      { status: 500 }
    );
  }
}
