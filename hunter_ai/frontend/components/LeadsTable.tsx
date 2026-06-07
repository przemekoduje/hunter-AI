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
