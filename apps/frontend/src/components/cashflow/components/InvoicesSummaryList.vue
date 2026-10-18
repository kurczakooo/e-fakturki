<script setup lang="ts">
import { computed, ref } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { formatPLN } from "../../../lib/utils";

import items from "../../../assets/mock_invoices";

const props = defineProps<{
  selectedYear: number;
  selectedMonth: number | null;
  type: "sales" | "purchases";
}>();

const selectedInvoice = ref(null);

function onInvoiceSelect(event: any) {
  selectedInvoice.value = event.data;
}

function onInvoiceUnselect() {
  selectedInvoice.value = null;
}

// Randomly generated cashflow values for demonstration purposes
const cashflow = Math.floor(Math.random() * 10000);
const previousCashflow = Math.floor(cashflow * 0.9);

const calculateAgainstPreviousMonth = computed(() => {
  // Calculate the percentage difference with a + or - sign
  const difference = ((cashflow - previousCashflow) / previousCashflow) * 100;
  return (difference >= 0 ? "+" : "") + difference.toFixed(2);
});
</script>

<template>
  <div class="p-div-white flex flex-1 flex-col gap-2">
    <!-- CASHFLOW SUMMARY -->
    <div class="flex flex-1 flex-col gap-2">
      <h1 class="text-xl font-bold">
        {{ type === "sales" ? "Przychód netto" : "Koszty netto" }} {{ formatPLN(cashflow) }}
      </h1>
      <div class="flex flex-1 gap-1">
        <h3 class="text-gray-600">vs poprzedni miesiąc:</h3>
        <h3
          :class="
            (calculateAgainstPreviousMonth.startsWith('+') && props.type === 'sales') ||
            (calculateAgainstPreviousMonth.startsWith('-') && props.type === 'purchases')
              ? 'text-green-600'
              : 'text-red-600'
          "
        >
          {{ calculateAgainstPreviousMonth }}%
        </h3>
      </div>
    </div>
    <!-- INVOICES BRIEF TABLE -->
    <div class="p-div-white flex flex-1 flex-col gap-2">
      <DataTable
        :value="items"
        dataKey="inv_nr"
        stripedRows
        v-model:selection="selectedInvoice"
        selection-mode="single"
        @row-select="onInvoiceSelect"
        @row-unselect="onInvoiceUnselect"
        removableSort
        scrollable
        scrollHeight="400px"
      >
        <Column field="date" header="Data" sortable></Column>
        <Column
          field="buyer"
          :header="props.type === 'sales' ? 'Klient' : 'Dostawca'"
          sortable
        ></Column>
        <Column field="sum_gross" header="Suma brutto" sortable>
          <template #body="slotProps">
            {{ formatPLN(slotProps.data.sum_gross) }}
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>
