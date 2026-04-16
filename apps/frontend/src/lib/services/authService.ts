import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { apiConfig } from "../../config";
import { useCurrentUserStore } from "../../stores/currentUserStore";
import type { LoginRequest, SignUpRequest, LoginResponse } from "../types/auth";

const baseUrl = apiConfig.apiBaseUrl + apiConfig.endpoints.auth;

// Axios interceptor to add the JWT token to all requests
axios.interceptors.request.use(
  (axiosConfig) => {
    const currentUserStore = useCurrentUserStore();
    const token = currentUserStore.getToken;
    if (!token) return axiosConfig;

    axiosConfig.headers["Authorization"] = "Bearer " + token;

    return axiosConfig;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export const decodeToken = (token: string): any => {
  try {
    return jwtDecode(token);
  } catch (error) {
    console.error("Invalid token:", error);
    return null;
  }
};

export const userLogin = async (data: LoginRequest): Promise<LoginResponse> => {
  try {
    const formData = new URLSearchParams();
    formData.append("grant_type", data.grant_type ?? "");
    formData.append("username", data.username);
    formData.append("password", data.password);
    formData.append("scope", data.scope ?? "");
    formData.append("client_id", data.client_id ?? "");
    formData.append("client_secret", data.client_secret ?? "");

    const response = await axios.post<LoginResponse>(baseUrl + "/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data;
  } catch (error: any) {
    throw error.response.status;
  }
};

export const userLogout = () => {
  const currentUserStore = useCurrentUserStore();
  currentUserStore.setToken("");
  currentUserStore.setUserData(null as any, null as any, null as any, null as any, null as any);
  currentUserStore.setCompanyData(null as any, null as any, false);
};

export const userSignUp = async (data: SignUpRequest): Promise<LoginResponse> => {
  try {
    const response = await axios.post<LoginResponse>(baseUrl + "/signup", data);
    return response.data;
  } catch (error: any) {
    throw error.response.status;
  }
};
