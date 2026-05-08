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
  CompanyUpdate,
} from "../types/company";
import { apiConfig } from "../../config";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.products;

export const createProduct = async (
  data: CompanyCreationRequest,
): Promise<CompanyCreationResponse> => {
  try {
    const response = await axios.post<CompanyCreationResponse>(baseUrl, data);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateProduct = async (data: CompanyUpdate): Promise<CompanyUpdate> => {
  try {
    const response = await axios.put<CompanyUpdate>(baseUrl, data);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getProductList = async (
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

export const deleteProduct = async (company_id: string): Promise<string> => {
  try {
    const response = await axios.delete<string>(`${baseUrl}/${company_id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getCategoriesByCompanyId = async (): Promise<IsoCountries[]> => {
  try {
    const response = await axios.get<IsoCountries[]>(`${baseUrl}/iso-countries`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
