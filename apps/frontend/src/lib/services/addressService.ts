import axios from "axios";
import type { AddressCreationRequest, AddressCreationResponse } from "../types/address";
import { apiConfig } from "../../config";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.addresses;

export const createAddress = async (
  data: AddressCreationRequest,
): Promise<AddressCreationResponse> => {
  try {
    const response = await axios.post<AddressCreationResponse>(baseUrl, data);
    return response.data;
  } catch (error) {
    throw error;
  }
};
