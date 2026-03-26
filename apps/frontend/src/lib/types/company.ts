export interface CompanyCreationRequest {
  userId: number;
  name: string;
  nip: string;
  krs?: string;
  regon?: string;
}

export interface CompanyCreationResponse {
  companyId: number;
}
