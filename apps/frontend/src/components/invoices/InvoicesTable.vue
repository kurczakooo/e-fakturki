<script setup lang="ts">
import { ref, onMounted } from "vue";

import { DataTable, Column, Button, Tag, Select, useToast } from "primevue";
import InvoiceDetails from "../dialogs/InvoiceDetails.vue";
import { getInvoicesList } from "../../lib/services/ksefService";
import { useMutation } from "@tanstack/vue-query";
import { useCurrentUserStore } from "../../stores/currentUserStore";
import type { getInvoicesListResponse } from "../../lib/types/ksef";
// import items from "../../assets/mock_invoices";

const props = defineProps<{
  invoice_type: string;
}>();

const toast = useToast();
const currentUserStore = useCurrentUserStore();

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

const tableType = "Faktury sprzedażowe";
const selectedInvoice = ref(null);
const selectedInvoiceData = ref<any>(null);
const dialogVisible = ref(false);
const sortedInvoices = ref<getInvoicesListResponse[]>([]);
const editRows = ref([]);
const isEditing = ref(false);

const getInvoicesMutation = useMutation({
  mutationFn: async (values: any) => {
    const invoice_list = await getInvoicesList(
      {
        company_id: 1,
        date_from: "01/02/2026",
        date_to: "07/04/2026",
        page_size: 100,
        page_offset: 0,
      },
      values.invoice_type,
    );
    return invoice_list;
  },

  onSuccess: (data) => {
    sortedInvoices.value = data.sort((a, b) => Number(b.is_new) - Number(a.is_new));
    toast.add({ severity: "info", summary: "Pomyślnie pobrano faktury.", life: 3000 });
  },

  onError: () => {
    toast.add({ severity: "error", summary: "Błąd w pobieraniu faktur.", life: 3000 });
  },
});

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
  getInvoicesMutation.mutate({
    invoice_type: props.invoice_type,
  });
});
</script>

<template>
  <DataTable
    :value="sortedInvoices"
    :loading="getInvoicesMutation.isPending.value"
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
    <Column field="invoice_number" sortable header="Numer faktury" style="width: 15%">
      <template #body="slotProps">
        <Tag v-if="slotProps.data.is_new" value="Nowa"></Tag>
        <span>{{ " " + slotProps.data.invoice_number }}</span>
      </template>
    </Column>
    <Column field="ksef_status" sortable header="Status KSeF" style="width: 10%">
      <template #body="slotProps">
        <Tag
          :icon="ksefStatusIcon[slotProps.data.ksef_status]"
          :severity="ksefStatusSeverity[slotProps.data.ksef_status]"
          v-tooltip.bottom="{ value: ksefStatusHint[slotProps.data.ksef_status] }"
        ></Tag>
      </template>
    </Column>
    <Column field="issue_date" sortable header="Data wystawienia" style="width: 10%"> </Column>
    <Column field="buyer_name" sortable header="Kontrahent" style="width: 15%"> </Column>
    <Column field="gross_total" sortable header="Suma brutto" style="width: 10%">
      <template #body="slotProps">
        <span class="inline-flex gap-1 items-baseline">
          <span>PLN</span>
          <span class="font-semibold">{{ slotProps.data.gross_total.toFixed(2) }}</span>
        </span>
      </template>
    </Column>
    <!-- <Column field="pay_type" sortable header="Rodzaj płatności" style="width: 10%">
      <template #body="slotProps">
        <span class="font-semibold">{{ paymentType[slotProps.data.pay_type] }}</span>
      </template>
    </Column> -->
    <Column field="payment_status" sortable header="Status płatności" style="width: 15%">
      <!-- default value -->
      <template #body="slotProps">
        <Tag
          :value="paymentStatus[slotProps.data.payment_status]"
          :severity="paymentStatusSeverity[slotProps.data.payment_status]"
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
