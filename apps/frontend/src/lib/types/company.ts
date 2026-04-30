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

export interface UserCompanyRequest {
  user_id: string;
}

export interface UserCompanyResponse {
  company_id: number;
  name: string;
  ksef_authorized: boolean;
}
