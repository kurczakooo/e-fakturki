import axios from "axios";
import type {
  KsefCredentialsCreationRequest,
  KsefCredentialsCreationResponse,
} from "../types/ksef";
import { apiConfig } from "../../config";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.ksef;

export const createKsefCredentials = async (
  data: KsefCredentialsCreationRequest,
): Promise<KsefCredentialsCreationResponse> => {
  try {
    const formData = new FormData();

    formData.append("company_id", String(data.company_id));
    formData.append("certificates_for_auth", String(data.certificates_for_auth));
    formData.append("certificate", data.certificate);
    formData.append("private_key", data.private_key);
    formData.append("password", data.password);

    const response = await axios.post<KsefCredentialsCreationResponse>(
      baseUrl + "/certificates",
      formData,
    );

    return response.data;
  } catch (error) {
    throw error;
  }
};
