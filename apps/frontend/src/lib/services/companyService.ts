import axios from "axios";
import type {
  UserCompanyResponse,
  IsoCountries,
  CompanyCreate,
  CompanyCreateResponse,
  CompanyReadUpdate,
  CompaniesListResponse,
} from "../types/company";
import { apiConfig } from "../../config";
import type { PaginationRequest } from "../types/common";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.companies;

export const createCompany = async (data: CompanyCreate): Promise<CompanyCreateResponse> => {
  console.log(baseUrl);
  try {
    const response = await axios.post<CompanyCreateResponse>(baseUrl, data);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateCompany = async (data: CompanyReadUpdate): Promise<CompanyCreateResponse> => {
  try {
    const response = await axios.put<CompanyCreateResponse>(baseUrl, data);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getUserCompany = async (): Promise<UserCompanyResponse> => {
  try {
    const response = await axios.get<UserCompanyResponse>(`${baseUrl}/me`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getCompaniesList = async (data: PaginationRequest): Promise<CompaniesListResponse> => {
  try {
    const response = await axios.get<CompaniesListResponse>(
      `${baseUrl}/list?search_string=${data.search_string ? data.search_string : ""}&page_size=${data.page_size}&page_offset=${data.page_offset}`,
    );

    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteCompany = async (company_id: string): Promise<string> => {
  try {
    const response = await axios.delete<string>(`${baseUrl}/${company_id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getIsoCountries = async (): Promise<IsoCountries[]> => {
  try {
    const response = await axios.get<IsoCountries[]>(`${baseUrl}/iso-countries`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
