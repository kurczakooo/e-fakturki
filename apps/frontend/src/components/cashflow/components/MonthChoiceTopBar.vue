<script setup lang="ts">
import Button from "primevue/button";
import { monthsDictionary } from "../../../lib/constants.ts";
import MonthTopBarSegment from "./MonthTopBarSegment.vue";

const props = defineProps<{
  selectedYear: number;
  selectedMonth: number | null;
}>();

const emit = defineEmits<{
  (e: "update:selectedMonth", monthNumber: number | null): void;
}>();

const monthNumbers = Object.keys(monthsDictionary).map(Number);
</script>

<template>
  <div class="flex justify-between items-center w-full pt-4 gap-4">
    <template v-for="monthNumber in monthNumbers" :key="monthNumber">
      <MonthTopBarSegment
        :monthNumber="monthNumber"
        :selectedYear="props.selectedYear"
        :selectedMonth="props.selectedMonth"
        @update:selectedMonth="emit('update:selectedMonth', $event)"
      />
    </template>
    <Button
      class="month-segment flex flex-1 items-center justify-center h-20"
      :class="{
        'font-semibold': props.selectedMonth === null,
        'month-segment-selected': props.selectedMonth === null,
      }"
      outlined
      @click="emit('update:selectedMonth', null)"
    >
      {{ `Cały rok ${props.selectedYear}` }}
    </Button>
  </div>
</template>
