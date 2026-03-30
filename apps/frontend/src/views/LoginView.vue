<script setup lang="ts">
import { computed, watch } from "vue";
import { useRouter } from "vue-router";

import { useCurrentUserStore } from "../stores/currentUserStore";
import AddCompanyDialog from "../components/dialogs/AddCompanyDialog.vue";
import AddKsefCredentials from "../components/dialogs/AddKsefCredentials.vue";
import LoginDialog from "../components/dialogs/LoginDialog.vue";

const router = useRouter();
const currentUserStore = useCurrentUserStore();

const isLoggedIn = computed(() => (currentUserStore.getFullName ? true : false));
const isCompanySelected = computed(() => (currentUserStore.getCompanyId ? true : false));
const isKsefAuthenticated = computed(() => currentUserStore.isCompanyKsefAuthorized);

watch(
  [isLoggedIn, isCompanySelected, isKsefAuthenticated],
  ([loggedIn, companySelected, ksefAuth]) => {
    if (loggedIn && companySelected && ksefAuth) {
      router.push("/sales");
    }
  },
  { immediate: true },
);
</script>

<template>
  <div>
    <LoginDialog v-if="!isLoggedIn" />
    <AddCompanyDialog v-if="!isCompanySelected && isLoggedIn" />
    <AddKsefCredentials v-if="!isKsefAuthenticated && isCompanySelected" />
  </div>
</template>
