// type for holding KSeF credentials
export interface KsefCredentials {
  certFile: File | null;
  keyFile: File | null;
  certPassword: string;
}

export interface KsefCredentialsCreationRequest {
  company_id: number;
  certificates_for_auth: boolean;
  certificate: File;
  private_key: File;
  password: string;
}

export interface KsefCredentialsCreationResponse {
  company_id: number;
  credentials_id: number;
}
