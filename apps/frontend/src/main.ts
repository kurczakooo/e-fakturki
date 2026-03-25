import "./style.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import { ToastService } from "primevue";
import { VueQueryPlugin } from "@tanstack/vue-query";

import PrimeVue from "primevue/config";
import Aura from "@primeuix/themes/aura";
import Tooltip from "primevue/tooltip";
import { definePreset } from "@primeuix/themes";

const customPreset = definePreset(Aura, {
  //https://primevue.org/theming/styled/
  semantic: {
    primary: {
      50: "{sky.50}",
      100: "{sky.100}",
      200: "{sky.200}",
      300: "{sky.300}",
      400: "{sky.400}",
      500: "{sky.500}",
      600: "{sky.600}",
      700: "{sky.700}",
      800: "{sky.800}",
      900: "{sky.900}",
      950: "{sky.950}",
    },
    colorScheme: {
      light: {},
      dark: {},
    },
  },
});

const app = createApp(App);
app.use(router);
app.use(ToastService);
app.use(VueQueryPlugin);
app.use(PrimeVue, {
  theme: {
    preset: customPreset,
    options: {
      prefix: "prime",
      darkModeSelector: ".prime-dark-mode",
      //   darkModeSelector: "system",
    },
  },
  ripple: true, // Enable ripple effect for buttons globally
  inputVariant: "filled", // Set default input variant
});
app.directive("tooltip", Tooltip);

app.mount("#app");
