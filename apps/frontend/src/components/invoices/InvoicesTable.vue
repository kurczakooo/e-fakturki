<script setup lang="ts">
import { ref, onMounted } from "vue";

import { DataTable, Column, Button, Tag, Select } from "primevue";
import InvoiceDetails from "../dialogs/InvoiceDetails.vue";
import items from "../../assets/mock_invoices";
import PaymentStatusColumnField from "./paymentStatusColumnField.vue";

// Invoice status
const statusIcon = {
  draft: "pi pi-clipboard",
  issued: "pi pi-check-circle",
};
const statusSeverity = {
  draft: "secondary",
  issued: "success",
};
const statusHint = {
  draft: "Szkic faktury",
  issued: "Faktura wystawiona",
};
// Invoice in KSeF status
const ksefStatusIcon = {
  not_sent: "pi pi-hourglass",
  sent: "pi pi-send",
  rejected: "pi pi-times",
  accepted: "pi pi-check-circle",
};
const ksefStatusSeverity = {
  not_sent: "warn",
  sent: "info",
  rejected: "danger",
  accepted: "success",
};
const ksefStatusHint = {
  not_sent: "Nie wysłano do KSeF",
  sent: "W trakcie wysyłania do KSeF",
  rejected: "Faktura odrzucona przez KSeF",
  accepted: "Faktura obecna w systemie KSeF",
};
// Invoice payment status
const paymentType = {
  bank_transfer: "Przelew",
  cash: "Gotówka",
};
const paymentStatus = {
  paid: "Opłacono",
  partial: "Częściowo opłacono",
  unpaid: "Nie opłacono",
};
const paymentStatusSeverity = {
  paid: "success",
  partial: "warn",
  unpaid: "danger",
};
const paymentOptions = [
  { label: "Nie opłacono", value: "unpaid" },
  { label: "Opłacono", value: "paid" },
  { label: "Częściowo opłacono", value: "partial" },
];

const loading = ref<boolean>(false);
const tableType = "Faktury sprzedażowe";
const selectedInvoice = ref(null);
const selectedInvoiceData = ref<any>(null);
const dialogVisible = ref(false);
const sortedInvoices = ref([]);
const editRows = ref([]);
const isEditing = ref(false);

function onInvoiceSelect(event: any) {
  // dont allow for selection when editing
  if (isEditing.value) return;

  selectedInvoiceData.value = event.data;
  dialogVisible.value = true;
}

function onInvoiceUnselect() {
  selectedInvoice.value = null;
  selectedInvoiceData.value = null;
}

function OnChoosePaymentStatus(event: any) {
  const { newData, index } = event;

  sortedInvoices.value[index] = newData;

  isEditing.value = false;
}

onMounted(() => {
  sortedInvoices.value = items.sort((a, b) => Number(b.is_new) - Number(a.is_new));
});
</script>

<template>
  <DataTable
    :value="sortedInvoices"
    :loading="loading"
    v-model:editingRows="editRows"
    edit-mode="row"
    dataKey="inv_nr"
    @row-edit-init="isEditing = true"
    @row-edit-save="OnChoosePaymentStatus"
    @row-edit-cancel="isEditing = false"
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
    :pt="{
      table: { style: 'min-width: 50rem' },
      column: {
        bodycell: ({ state }) => ({
          style: state['d_editing'],
        }),
      },
    }"
  >
    <template #header>
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-xl font-bold">{{ tableType }}</span>
        <Button icon="pi pi-refresh" rounded raised />
      </div>
    </template>
    <Column field="inv_nr" sortable header="Numer faktury" style="width: 10%">
      <template #body="slotProps">
        <Tag v-if="slotProps.data.is_new" value="Nowa"></Tag>
        <span>{{ " " + slotProps.data.inv_nr }}</span>
      </template>
    </Column>
    <Column field="status" sortable header="Status" style="width: 5%">
      <template #body="slotProps">
        <Tag
          :icon="statusIcon[slotProps.data.status]"
          :severity="statusSeverity[slotProps.data.status]"
          v-tooltip.bottom="{ value: statusHint[slotProps.data.status] }"
        ></Tag>
      </template>
    </Column>
    <Column field="ksef" sortable header="Status KSeF" style="width: 5%">
      <template #body="slotProps">
        <Tag
          :icon="ksefStatusIcon[slotProps.data.ksef]"
          :severity="ksefStatusSeverity[slotProps.data.ksef]"
          v-tooltip.bottom="{ value: ksefStatusHint[slotProps.data.ksef] }"
        ></Tag>
      </template>
    </Column>
    <Column field="date" sortable header="Data wystawienia" style="width: 10%"> </Column>
    <Column field="buyer" sortable header="Kontrahent" style="width: 15%"> </Column>
    <Column field="sum_gross" sortable header="Suma brutto" style="width: 10%">
      <template #body="slotProps">
        <span class="inline-flex gap-1 items-baseline">
          <span>PLN</span>
          <span class="font-semibold">{{ slotProps.data.sum_gross.toFixed(2) }}</span>
        </span>
      </template>
    </Column>
    <Column field="pay_type" sortable header="Rodzaj płatności" style="width: 10%">
      <template #body="slotProps">
        <span class="font-semibold">{{ paymentType[slotProps.data.pay_type] }}</span>
      </template>
    </Column>
    <Column field="pay_status" sortable header="Status płatności" style="width: 15%">
      <!-- default value -->
      <template #body="slotProps">
        <Tag
          :value="paymentStatus[slotProps.data.pay_status]"
          :severity="paymentStatusSeverity[slotProps.data.pay_status]"
        />
      </template>
      <!-- selection drawer -->
      <template #editor="{ data, field }">
        <Select
          v-model="data[field]"
          :options="paymentOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Select a Status"
          float
        >
          <template #option="slotProps">
            <Tag
              :value="slotProps.option.label"
              :severity="paymentStatusSeverity[slotProps.option.value]"
            />
          </template>
        </Select>
      </template>
    </Column>
    <Column :rowEditor="true" bodyStyle="text-align:left" style="width: 10%"></Column>
  </DataTable>
  <!-- Invoice details dialog -->
  <InvoiceDetails v-model:visible="dialogVisible" :invoice="selectedInvoiceData" />
</template>
