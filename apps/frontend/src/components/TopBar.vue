<script setup lang="ts">
import { ref, onMounted } from "vue";

import AppLogo from "./AppLogo.vue";

import { Toolbar, Select, Button } from "primevue";

const User = ref<string>("Łukasz Kowalski");
const companiesOptions = ["Lukpol Warszawa", "Lukpol Kielce", "Lukpol Radom"];
const selectedCompany = ref<string | undefined>("");

onMounted(() => {
  selectedCompany.value = companiesOptions[0];
});
</script>

<template>
  <Toolbar>
    <template #start>
      <AppLogo />
    </template>

    <template #end>
      <div class="flex items-center gap-4">
        <Select
          v-model="selectedCompany"
          :options="companiesOptions"
          :placeholder="selectedCompany"
        />
        <p>{{ User }}</p>
        <Button icon="pi pi-user" raised rounded />
        <Button icon="pi pi-cog" raised rounded />
      </div>
    </template>
  </Toolbar>
</template>
