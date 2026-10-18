<script setup lang="ts">
import { ref } from "vue";
import { Toolbar, Button } from "primevue";

const props = defineProps<{
  selectedYear: number;
}>();

const emit = defineEmits<{
  (e: "update:selectedYear", year: number): void;
}>();

const selectedYear = ref(props.selectedYear);

function previousYear() {
  selectedYear.value--;
  emit("update:selectedYear", selectedYear.value);
}

function nextYear() {
  selectedYear.value++;
  emit("update:selectedYear", selectedYear.value);
}
</script>

<template>
  <Toolbar>
    <template #start>
      <Button
        icon="pi pi-chevron-left"
        raised
        rounded
        @click="previousYear"
        :disabled="selectedYear === 2000"
      />
    </template>

    <template #center>
      <span class="text-lg font-semibold">{{ selectedYear }}</span>
    </template>

    <template #end>
      <Button
        icon="pi pi-chevron-right"
        raised
        rounded
        @click="nextYear"
        :disabled="selectedYear === new Date().getFullYear()"
      />
    </template>
  </Toolbar>
</template>
