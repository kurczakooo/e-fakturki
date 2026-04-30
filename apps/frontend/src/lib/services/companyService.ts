import axios from "axios";
import type {
  CompanyCreationRequest,
  CompanyCreationResponse,
  UserCompanyRequest,
  UserCompanyResponse,
} from "../types/company";
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

export const getUserCompany = async (data: UserCompanyRequest): Promise<UserCompanyResponse> => {
  try {
    const response = await axios.get<UserCompanyResponse>(
      `${baseUrl}/user?user_id=${data.user_id}`,
    );
    return response.data;
  } catch (error: any) {
    console.log(error.response?.data?.detail);
    throw error;
  }
};
