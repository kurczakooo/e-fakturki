import { defineStore } from "pinia";

export const useCurrentUserStore = defineStore("currentUser", {
  state: () => {
    return {
      userId: "" as string,
      name: null as string | null,
      lastname: null as string | null,
      email: null as string | null,
      token: null as string | null,

      companyId: null as string | null,
      companyName: null as string | null,
      companyNip: null as string | null,
      companyCountryCode: null as string | null,
      companyAddressL1: null as string | null,
      companyAddressL2: null as string | null,
      companyEmail: null as string | null,
      companyPhoneNumber: null as string | null,
      companyKsefAuthorized: false as boolean | null,
    };
  },
  getters: {
    getUserId: (state) => state.userId,
    getName: (state) => state.name,
    getLastname: (state) => state.lastname,
    getFullName: (state) => {
      if (state.name && state.lastname) {
        return `${state.name} ${state.lastname}`;
      }
      return null;
    },
    getToken: (state) => state.token,
    getEmail: (state) => state.email,
    getCompanyId: (state) => state.companyId,
    getCompanyName: (state) => state.companyName,
    getCompanyNip: (state) => state.companyNip,
    getCompanyCountryCode: (state) => state.companyCountryCode,
    getCompanyAddressL1: (state) => state.companyAddressL1,
    getCompanyAddressL2: (state) => state.companyAddressL2,
    getCompanyEmail: (state) => state.companyEmail,
    getCompanyPhoneNumber: (state) => state.companyPhoneNumber,

    getUserCompanyListEntry: (state) => {
      return {
        id: state.companyId,
        owner_id: state.userId,
        name: state.companyName,
        nip: state.companyNip,
        country_code: state.companyCountryCode,
        address_l1: state.companyAddressL1,
        address_l2: state.companyAddressL2,
        email: state.companyEmail,
        phone_number: state.companyPhoneNumber,
      };
    },

    isCompanyKsefAuthorized: (state) => state.companyKsefAuthorized,
  },
  actions: {
    setToken(token: string) {
      this.token = token;
    },
    setUserData(userId: string, name: string, lastname: string, email: string, token: string) {
      this.userId = userId;
      this.name = name;
      this.lastname = lastname;
      this.email = email;
      this.token = token;
    },
    setCompanyData(
      companyId: string,
      companyName: string,
      companyNip: string,
      companyCountryCode: string,
      companyAddressL1: string,
      companyAddressL2: string,
      companyEmail: string,
      companyPhoneNumber: string,
      companyKsefAuthorized: boolean,
    ) {
      this.companyId = companyId;
      this.companyName = companyName;
      this.companyNip = companyNip;
      this.companyCountryCode = companyCountryCode;
      this.companyAddressL1 = companyAddressL1;
      this.companyAddressL2 = companyAddressL2;
      this.companyEmail = companyEmail;
      this.companyPhoneNumber = companyPhoneNumber;
      this.companyKsefAuthorized = companyKsefAuthorized;
    },
    setCompanyKsefAuthorizationStatus(status: boolean) {
      this.companyKsefAuthorized = status;
    },
    toString() {
      return `CurrentUserStore: { userId: ${this.userId}, name: ${this.name}, lastname: ${this.lastname}, email: ${this.email}, token: ${this.token}, companyId: ${this.companyId}, companyName: ${this.companyName}, companyKsefAuthorized: ${this.companyKsefAuthorized} }`;
    },
  },
});
