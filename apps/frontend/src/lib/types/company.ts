export interface CompanyCreationRequest {
  user_id: number;
  name: string;
  nip: string;
  krs: string | null;
  regon: string | null;
}

export interface CompanyCreationResponse {
  user_id: number;
  company_id: number;
}
