"use client";

import React, { useState } from 'react';

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
  const [isScraping, setIsScraping] = useState(false);
  const [scrapeMessage, setScrapeMessage] = useState<{ text: string, type: 'success' | 'error' } | null>(null);

  const handleScrape = async () => {
    setIsScraping(true);
    setScrapeMessage(null);

    try {
      const response = await fetch('/api/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city, year }),
      });

      const data = await response.json();

      if (response.ok) {
        setScrapeMessage({ 
          text: '✅ Proces scrapingu rozpoczęty w tle. Odśwież listę za kilka minut.', 
          type: 'success' 
        });
      } else {
        throw new Error(data.error || 'Błąd serwera');
      }
    } catch (err: any) {
      setScrapeMessage({ 
        text: `❌ Błąd: ${err.message}`, 
        type: 'error' 
      });
    } finally {
      setIsScraping(false);
      // Ukryj komunikat po 10 sekundach
      setTimeout(() => setScrapeMessage(null), 10000);
    }
  };

  return (
    <div className="space-y-4 mb-8">
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 flex flex-col md:flex-row items-end gap-4 shadow-sm">
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

        <div className="flex gap-2 w-full md:w-auto">
          <button
            onClick={onSearch}
            disabled={loading || isScraping}
            className="flex-1 md:flex-none bg-[#1a73e8] hover:bg-blue-700 text-white font-medium py-2 px-8 rounded shadow-sm transition-colors disabled:opacity-50"
          >
            {loading ? 'Szukanie...' : 'Szukaj'}
          </button>

          <button
            onClick={handleScrape}
            disabled={isScraping || loading}
            className="flex-1 md:flex-none bg-white hover:bg-gray-100 text-[#1a73e8] border border-[#1a73e8] font-medium py-2 px-6 rounded shadow-sm transition-colors disabled:opacity-50"
            title="Uruchamia pobieranie nowych danych w tle przez n8n"
          >
            {isScraping ? 'Uruchamianie...' : 'Pobierz nowe'}
          </button>
        </div>
      </div>

      {scrapeMessage && (
        <div className={`p-4 rounded-md text-sm border ${
          scrapeMessage.type === 'success' 
            ? 'bg-green-50 text-green-700 border-green-200' 
            : 'bg-red-50 text-red-700 border-red-200'
        } transition-all animate-fade-in`}>
          {scrapeMessage.text}
        </div>
      )}
    </div>
  );
};

export default SearchFilters;
