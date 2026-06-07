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
