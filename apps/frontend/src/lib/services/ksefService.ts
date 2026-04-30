import axios from "axios";
import type {
  InvoiceType,
  KsefCredentialsCreationRequest,
  KsefCredentialsCreationResponse,
  getInvoicesListRequest,
} from "../types/ksef";
import { apiConfig } from "../../config";
import type { InvoiceResponse } from "../types/invoices";

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

export const refreshInvoiceListFromKsef = async (
  data: getInvoicesListRequest,
  invoiceType: InvoiceType,
): Promise<string[]> => {
  try {
    const response = await axios.post<string[]>(baseUrl + "/invoices", data, {
      params: {
        invoice_type: invoiceType,
      },
    });

    return response.data;
  } catch (error) {
    console.log(error.response?.data?.detail);

    throw error;
  }
};

export const getInvoiceDetails = async (
  company_id: number,
  invoice_id: string,
): Promise<InvoiceResponse> => {
  try {
    const response = await axios.post<InvoiceResponse>(
      `${baseUrl}/single_invoice_download/${company_id}/${invoice_id}`,
    );
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error.response?.data?.detail);

    throw error;
  }
};
