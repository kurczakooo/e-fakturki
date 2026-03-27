export interface AddressCreationRequest {
  company_id: number;
  type: "registered" | "correspondence";
  country: string;
  city: string;
  postal_code: string;
  street: string;
  building_number: string;
}

export interface AddressCreationResponse {
  company_id: number;
  address_id: number;
}
