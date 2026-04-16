import axios from "axios";
import type { CompanyCreationRequest, CompanyCreationResponse } from "../types/company";
import { apiConfig } from "../../config";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.companies;

export const createCompany = async (
  data: CompanyCreationRequest,
): Promise<CompanyCreationResponse> => {
  try {
    const response = await axios.post<CompanyCreationResponse>(baseUrl, data);
    return response.data;
  } catch (error: any) {
    console.log(error.response?.data?.detail);
    throw error;
  }
};
