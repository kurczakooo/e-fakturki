import type { pageInfo } from "../types/ksef";

export interface CategoryListItem {
  id: string;
  default_unit: string | null;
  default_tax_rate: number | null;
  name: string;
}

export interface GetProductsListRequest {
  search_string: string | null;
  category: string | null;
  page_size: number;
  page_offset: number;
}

export interface ProductListItem {
  id: string;
  name: string;
  category: string | null;
  categoryId: string | null;
  description: string | null;
  gtin: string | null;
  unit: string | null;
  net_price: number | null;
  tax_rate: number | null;
  gross_price: number | null;
}

export interface GetProductsListResponse {
  companies: ProductListItem[];
  page_info: pageInfo;
}
