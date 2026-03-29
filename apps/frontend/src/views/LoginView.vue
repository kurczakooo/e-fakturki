<script setup lang="ts">
import { ref } from "vue";

import AddCompanyDialog from "../components/dialogs/AddCompanyDialog.vue";
import AddKsefCredentials from "../components/dialogs/addKsefCredentials.vue";
import LoginDialog from "../components/dialogs/LoginDialog.vue";

const isLoggedIn = ref(false);
const isCompanySelected = ref(false);
const isKsefAuthenticated = ref(false);
</script>

<template>
  <LoginDialog />
  <!-- <AddCompanyDialog :visible="true" /> -->
  <!-- <AddKsefCredentials :visible="true" company-name="Lukpol Warszawa" /> -->
</template>
