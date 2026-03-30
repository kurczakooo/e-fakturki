import { defineStore } from "pinia";

export const useCurrentUserStore = defineStore("currentUser", {
  state: () => {
    return {
      userId: null as number | null,
      name: null as string | null,
      lastname: null as string | null,
      email: null as string | null,

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
    getEmail: (state) => state.email,
    getCompanyId: (state) => state.companyId,
    getCompanyName: (state) => state.companyName,
    isCompanyKsefAuthorized: (state) => state.companyKsefAuthorized,
  },
  actions: {
    setUserData(userId: number, name: string, lastname: string, email: string) {
      this.userId = userId;
      this.name = name;
      this.lastname = lastname;
      this.email = email;
    },
    setCompanyData(companyId: number, companyName: string, companyKsefAuthorized: boolean) {
      this.companyId = companyId;
      this.companyName = companyName;
      this.companyKsefAuthorized = companyKsefAuthorized;
    },
    setCompanyKsefAuthorizationStatus(status: boolean) {
      this.companyKsefAuthorized = status;
    },
  },
});
