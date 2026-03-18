import { createRouter, createWebHistory } from "vue-router";
import NewInvoiceView from "../views/NewInvoiceView.vue";
import SalesView from "../views/SalesView.vue";
import PurchasesView from "../views/PurchasesView.vue";
import ProductsView from "../views/ProductsView.vue";
import CompaniesView from "../views/CompaniesView.vue";
import SettingsView from "../views/SettingsView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/sales",
      name: "sales",
      component: SalesView,
    },
    {
      path: "/new-invoice",
      name: "new-invoice",
      component: NewInvoiceView,
    },
    {
      path: "/purchases",
      name: "purchases",
      component: PurchasesView,
    },
    {
      path: "/products",
      name: "products",
      component: ProductsView,
    },
    {
      path: "/companies",
      name: "companies",
      component: CompaniesView,
    },
    {
      path: "/settings",
      name: "settings",
      component: SettingsView,
    },
  ],
});

export default router;
