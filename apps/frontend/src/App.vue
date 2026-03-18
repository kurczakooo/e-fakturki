<script setup lang="ts">
import LeftMenu from "./components/LeftMenu.vue";
import { RouterView } from "vue-router";
import TopBar from "./components/TopBar.vue";
</script>

<template>
  <div class="app-container">
    <TopBar />
    <div class="main-container">
      <LeftMenu />
      <!-- Main content area -->
      <div class="content-area">
        <RouterView />
      </div>
    </div>
  </div>
</template>
