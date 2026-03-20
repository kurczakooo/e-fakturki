<script setup lang="ts">
import { RouterView } from "vue-router";
import LeftMenu from "./components/LeftMenu.vue";
import TopBar from "./components/TopBar.vue";
import LoginDialog from "./components/dialogs/LoginDialog.vue";
import { Toast } from "primevue";
</script>

<template>
  <div class="app-container">
    <TopBar />
    <div class="main-container">
      <LeftMenu />
      <!-- Main content area -->
      <div class="content-area">
        <Toast />
        <RouterView />
        <!-- <LoginDialog /> -->
      </div>
    </div>
  </div>
</template>
