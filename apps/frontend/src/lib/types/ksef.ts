// type for holding KSeF credentials
export interface KsefCredentials {
  certFile: File | null;
  keyFile: File | null;
  certPassword: string;
}
