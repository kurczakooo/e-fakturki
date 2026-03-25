<script setup lang="ts">
import { ref } from "vue";
import { Menu, Badge } from "primevue";
import { toggleDarkMode } from "../lib/utils";

const items = ref([
  {
    label: "Faktury",
    items: [
      {
        label: "Nowa Faktura",
        icon: "pi pi-plus",
        route: "/new-invoice",
        disabled: true,
      },
      {
        label: "Sprzedaż",
        icon: "pi pi-shop",
        route: "/sales",
        disabled: false,
        badge: "2",
      },
      {
        label: "Zakup",
        icon: "pi pi-shopping-cart",
        route: "/purchases",
        disabled: false,
        badge: "2",
      },
    ],
  },
  {
    label: "Firma",
    items: [
      {
        label: "Produkty",
        icon: "pi pi-box",
        route: "/products",
        disabled: true,
      },
      {
        label: "Kontrahenci",
        icon: "pi pi-user",
        route: "/companies",
        disabled: true,
      },
    ],
  },
  {
    label: "Aplikacja",
    items: [
      {
        label: "Tryb",
        icon: "pi pi-sun",
        command: toggleDarkMode,
      },
      {
        label: "Ustawienia",
        icon: "pi pi-cog",
        route: "/settings",
        disabled: true,
      },
    ],
  },
]);
</script>

<template>
  <div class="card flex h-full">
    <Menu :model="items" class="w-full md:w-60 h-full">
      <!-- <template #start>
        <div class="inline-flex items-center gap-1 px-2 py-2">
          <Button label="Nowa faktura" icon="pi pi-plus" />
        </div>
      </template> -->

      <template #item="{ item, props }">
        <router-link
          v-if="item.route"
          v-slot="{ href, navigate }"
          :to="item.route"
          custom
          :disabled="item.disabled"
        >
          <a v-ripple :href="href" v-bind="props.action" @click="navigate">
            <span :class="item.icon" />
            <span class="ml-2">{{ item.label }}</span>
            <Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
          </a>
        </router-link>
        <a v-else v-ripple :href="item.url" :target="item.target" v-bind="props.action">
          <span :class="item.icon" />
          <span class="ml-2">{{ item.label }}</span>
        </a>
      </template>
    </Menu>
  </div>
</template>
