import { defineStore } from "pinia";

export const useCurrentUserStore = defineStore("currentUser", {
  state: () => {
    return {
      userId: "" as string,
      name: null as string | null,
      lastname: null as string | null,
      email: null as string | null,
      token: null as string | null,

      companyId: null as number | null,
      companyName: null as string | null,
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
    isCompanyKsefAuthorized: (state) => state.companyKsefAuthorized,
  },
  actions: {
    setToken(token: string) {
      this.token = token;
    },
    setUserData(userId: number, name: string, lastname: string, email: string, token: string) {
      this.userId = userId;
      this.name = name;
      this.lastname = lastname;
      this.email = email;
      this.token = token;
    },
    setCompanyData(companyId: number, companyName: string, companyKsefAuthorized: boolean) {
      this.companyId = companyId;
      this.companyName = companyName;
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
