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

const invoiceTypes = ["purchase", "sales"] as const;
export type InvoiceType = (typeof invoiceTypes)[number];
export interface getInvoicesListRequest {
  company_id: number;
  date_from: string;
  date_to: string;
  page_size: number;
  page_offset: number;
}

export interface invoiceListItem {
  id: string;
  invoice_number: string;
  issued_date: string;
  is_new: boolean;
  seller_name: string;
  buyer_name: string;
  gross_total: number;
  currency: string;
  payment_type: string | null;
  payment_status: string | null;
  ksef_number: string | null;
  ksef_status: string;
}

interface pageInfo {
  current_page: number;
  page_size: number;
  total_items: number;
  has_next_page: boolean;
  has_previous_page: boolean;
}

export interface getInvoicesListResponse {
  invoices: invoiceListItem[];
  page_info: pageInfo;
}
