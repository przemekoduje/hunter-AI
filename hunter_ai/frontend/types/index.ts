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
