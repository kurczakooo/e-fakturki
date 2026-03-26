export interface AddressCreationRequest {
  companyId: number;
  street_and_number: string;
  zipcode: string;
  city: string;
}

export interface AddressCreationResponse {
  companyId: number;
  addressId: number;
}
