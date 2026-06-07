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

    if (year) {
      // ARCHITEKT: Filtrowanie po roku z fallbackiem dla rekordów bez daty (aby były widoczne)
      where.OR = [
        ...(where.OR || []),
        { data_wydania_decyzji: { contains: year } },
        { data_wydania_decyzji: null },
        { data_wydania_decyzji: { isSet: false } }
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
      // ARCHITEKT: Priorytet dla twardych pól z bazy danych
      let street = lead.street || '';
      let houseNumber = lead.houseNumber || '';
      let cityParsed = lead.miejscowosc || '';

      // FALLBACK: Jeśli brakuje twardych pól, parsujemy display_name (dla starszych rekordów)
      if (!street || !houseNumber) {
        if (lead.display_name) {
          const parts = lead.display_name.split(',').map(p => p.trim());
          
          // Szukamy numeru (ma cyfry) i ulicy w pierwszych 4 segmentach
          for (let i = 0; i < Math.min(parts.length, 4); i++) {
            const part = parts[i];
            const hasDigits = /\d/.test(part);

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
      }

      return {
        ...lead,
        street: street || 'Brak danych',
        houseNumber: houseNumber || 'n/a',
        city: cityParsed || lead.miejscowosc || 'Nieznane',
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
