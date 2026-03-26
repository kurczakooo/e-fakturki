export const apiConfig = {
  apiBaseUrl: "http://localhost:8080/api/",

  endpoints: {
    ksef: "/ksef",
    companies: "/companies",
    addresses: "/addresses",
    bankAccounts: "/bank-accounts",
    invoices: "/invoices",
    users: "/users",
    products: "/products",
    categories: "/categories",
  },

  // Other application settings
  defaultPageSize: 10,
  tokenStorageKey: "user",
};
