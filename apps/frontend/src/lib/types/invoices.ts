// type representing invoice

export interface InvoiceEntry {
  row_number: number;
  delivery_date: string | null;
  name: string;
  amount: number;
  unit: string;
  net_price: number;
  gross_price: number | null;
  net_total: number;
  tax_rate: number;
  tax_total: number | null;
  gross_total: number;
}

export interface InvoiceCompanyData {
  name: string;
  nip: string;
  address_l1: string;
  address_l2: string;
  email: string | null;
  phone: string | null;
}

export interface InvoicePayment {
  payment_status: string;
  payment_type: string;
  payment_date: string | null;
  payment_due_date: string | null;
  partial_payments: string | null;
  seller_bank_account_number: string | null;
  seller_bank_name: string | null;
}

export interface InvoiceResponse {
  id: string;
  invoice_number: string;
  invoice_type: string;
  ksef_number: string | null;
  invoicing_date: string | null;
  acquisition_date: string | null;
  permanent_storage_date: string | null;
  ksef_status: string;
  is_new: boolean;
  issue_date: string;
  issue_place: string;
  seller_info: InvoiceCompanyData;
  buyer_info: InvoiceCompanyData;
  entries: InvoiceEntry[];
  currency: string;
  net_total: number;
  tax_total: number;
  gross_total: number;
  payment: InvoicePayment;
  annotations: string | null;
  additional_info: string | null;
  footer_info: string | null;
  footer_registers: string | null;
}
