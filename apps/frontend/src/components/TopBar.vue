<script setup lang="ts">
import { computed } from "vue";

import { Toolbar, Select, Button } from "primevue";

import AppLogo from "./AppLogo.vue";
import { useCurrentUserStore } from "../stores/currentUserStore";

const currentUserStore = useCurrentUserStore();

const companyName = computed(() => currentUserStore.getCompanyName);
const userName = computed(() => currentUserStore.getFullName);
</script>

<template>
  <Toolbar>
    <template #start>
      <AppLogo />
    </template>

    <template #end>
      <div class="flex items-center gap-4">
        <Select
          :placeholder="companyName ? companyName : 'Wybierz firmę'"
          emptyMessage="Brak opcji do wyboru"
        />
        <p>{{ userName ? userName : "Zaloguj się" }}</p>
        <Button icon="pi pi-user" raised rounded />
        <Button icon="pi pi-cog" raised rounded />
      </div>
    </template>
  </Toolbar>
</template>
