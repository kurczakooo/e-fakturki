import axios from "axios";
import type { getInvoicesListRequest, getInvoicesListResponse, InvoiceType } from "../types/ksef";
import { apiConfig } from "../../config";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.invoices;

export const getInvoicesList = async (
  data: getInvoicesListRequest,
  invoiceType: InvoiceType,
): Promise<getInvoicesListResponse> => {
  try {
    const response = await axios.post<getInvoicesListResponse>(baseUrl, data, {
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

export const updateInvoiceIsNew = async (invoice_id: string, is_new: boolean): Promise<number> => {
  try {
    const response = await axios.patch(`${baseUrl}/${invoice_id}/is-new`, {
      is_new: is_new,
    });
    return response.status;
  } catch (error) {
    console.log(error.response?.data?.detail);
    throw error;
  }
};
