<script setup lang="ts">
import { ref } from "vue";

import { DataTable, Column, Button, Tag } from "primevue";
import InvoiceDetails from "./dialogs/InvoiceDetails.vue";
import items from "../assets/mock_invoices";

function getStatusSeverity(status: string) {
  switch (status) {
    case "draft":
      return "secondary";
    case "sent":
      return "success";
    case "new":
      return "info";
    default:
      return null;
  }
}

const statusLabel = {
  draft: "Szkic",
  sent: "Wysłana",
  new: "Nowa",
};

const loading = ref<boolean>(false);
const tableType = "Faktury sprzedażowe";
const selectedInvoice = ref(null);
const selectedInvoiceData = ref<any>(null);
const dialogVisible = ref(false);

function onInvoiceSelect(event: any) {
  selectedInvoiceData.value = event.data;
  dialogVisible.value = true;
}

function onInvoiceUnselect() {
  selectedInvoice.value = null;
  selectedInvoiceData.value = null;
}
</script>

<template>
  <DataTable
    :value="items"
    :loading="loading"
    v-model:selection="selectedInvoice"
    selection-mode="single"
    @row-select="onInvoiceSelect"
    @row-unselect="onInvoiceUnselect"
    paginator
    :rows="10"
    :rows-per-page-options="[5, 10, 15, 25, 50]"
    removableSort
    scrollable
    stripedRos
    tableStyle="min-width: 50rem"
  >
    <template #header>
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-xl font-bold">{{ tableType }}</span>
        <Button icon="pi pi-refresh" rounded raised />
      </div>
    </template>
    <Column field="inv_nr" sortable header="Numer faktury"></Column>
    <Column field="status" sortable header="Status">
      <template #body="slotProps">
        <Tag
          :value="statusLabel[slotProps.data.status]"
          :severity="getStatusSeverity(slotProps.data.status)"
        ></Tag>
      </template>
    </Column>
    <Column field="ksef" sortable header="Status KSeF"></Column>
    <Column field="date" sortable header="Data wystawienia"></Column>
    <Column field="buyer" sortable header="Kontrahent"></Column>
    <Column field="sum_gross" sortable header="Suma brutto">
      <template #body="slotProps">
        {{ "PLN " + slotProps.data.sum_gross }}
      </template>
    </Column>
    <Column field="pay_status" sortable header="Status płatności"></Column>
  </DataTable>
  <!-- Invoice details dialog -->
  <InvoiceDetails v-model:visible="dialogVisible" :invoice="selectedInvoiceData" />
</template>
