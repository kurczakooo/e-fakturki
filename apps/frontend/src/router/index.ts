import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
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
      path: "/",
      redirect: "/login",
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
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
