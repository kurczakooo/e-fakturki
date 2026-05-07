import type { pageInfo } from "../types/ksef";

export interface IsoCountries {
  name: string;
  code: string;
}

export interface CompanyCreationRequest {
  owner_id: string | null;
  name: string;
  nip: string;
  krs: string | null;
  regon: string | null;
  country_code: string;
  address_l1: string | null;
  address_l2: string | null;
  address_correspondance_l1: string | null;
  address_correspondance_l2: string | null;
  email: string | null;
  phone_number: string | null;
  additional_info: string | null;
}

export interface CompanyCreationResponse {
  user_id: string;
  company_id: string;
}

export interface UserCompanyRequest {
  user_id: string;
}

export interface UserCompanyResponse {
  company_id: string;
  name: string;
  nip: string;
  country_code: string | null;
  address_l1: string | null;
  address_l2: string | null;
  email: string | null;
  phone_number: string | null;
  ksef_authorized: boolean;
}

export interface GetCompaniesListRequest {
  search_string: string | null;
  page_size: number;
  page_offset: number;
}

export interface CompanyListItem {
  id: string;
  owner_id: string | null;
  name: string;
  nip: string;
  country_code: string | null;
  address_l1: string | null;
  address_l2: string | null;
  email: string | null;
  phone_number: string | null;
}

export interface CompanyUpdate {
  id: string;
  name: string;
  nip: string;
  country_code: string | null;
  address_l1: string | null;
  address_l2: string | null;
  address_correspondance_l1: string | null;
  address_correspondance_l2: string | null;
  email: string | null;
  phone_number: string | null;
  additional_info: string | null;
}
export interface CompanyDetails {
  id: string;
  krs: string | null;
  regon: string | null;
  address_correspondance_l1: string | null;
  address_correspondance_l2: string | null;
  additional_info: string | null;
}

export interface GetCompaniesListResponse {
  companies: CompanyListItem[];
  page_info: pageInfo;
}

export type CreateOrUpdate = "create" | "update";
