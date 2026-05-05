import axios from "axios";
import type {
  CompanyCreationRequest,
  CompanyCreationResponse,
  UserCompanyRequest,
  UserCompanyResponse,
  GetCompaniesListRequest,
  GetCompaniesListResponse,
  IsoCountries,
  CompanyDetails,
} from "../types/company";
import { apiConfig } from "../../config";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.companies;

export const createCompany = async (
  data: CompanyCreationRequest,
): Promise<CompanyCreationResponse> => {
  try {
    console.log(data);
    const response = await axios.post<CompanyCreationResponse>(baseUrl, data);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getUserCompany = async (data: UserCompanyRequest): Promise<UserCompanyResponse> => {
  try {
    const response = await axios.get<UserCompanyResponse>(
      `${baseUrl}/user?user_id=${data.user_id}`,
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getCompaniesList = async (
  data: GetCompaniesListRequest,
): Promise<GetCompaniesListResponse> => {
  try {
    const response = await axios.get<GetCompaniesListResponse>(
      `${baseUrl}?search_string=${data.search_string ? data.search_string : ""}&page_size=${data.page_size}&page_offset=${data.page_offset}`,
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

export const getCompanyDetails = async (company_id: string): Promise<CompanyDetails> => {
  try {
    const response = await axios.get<CompanyDetails>(`${baseUrl}/details?company_id=${company_id}`);
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
