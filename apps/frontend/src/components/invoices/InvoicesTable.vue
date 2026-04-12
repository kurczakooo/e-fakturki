<script setup lang="ts">
import { ref, onMounted } from "vue";

import { DataTable, Column, Button, Tag, Select, DatePicker, useToast, FloatLabel } from "primevue";
import InvoiceDetails from "../dialogs/InvoiceDetails.vue";
import { getInvoicesList } from "../../lib/services/invoiceService";
import { useMutation } from "@tanstack/vue-query";
import { useCurrentUserStore } from "../../stores/currentUserStore";
import type { invoiceListItem } from "../../lib/types/ksef";
import { useInvoicesStore } from "../../stores/invoicesStore";
import { formatLocalDate } from "../../lib/utils";
import { refreshInvoiceListFromKsef } from "../../lib/services/ksefService";
// import items from "../../assets/mock_invoices";

const props = defineProps<{
  invoice_type: string;
}>();

const toast = useToast();
const currentUserStore = useCurrentUserStore();
const invoicesStore = useInvoicesStore();

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

const tableType = props.invoice_type == "sales" ? "Faktury sprzedażowe" : "Faktury zakupowe";
const dateRange = ref<Date[]>([new Date(2026, 0, 1), new Date()]);
const selectedInvoice = ref(null);
const selectedInvoiceData = ref<any>(null);
const dialogVisible = ref(false);
const sortedInvoices = ref<invoiceListItem[]>([]);
const editRows = ref([]);
const isEditing = ref(false);
const pageSize = ref(10);
const first = ref(0);
const totalRecords = ref(0);

const getInvoicesMutation = useMutation({
  mutationFn: async (values: any) => {
    const invoice_ksef_ids = await refreshInvoiceListFromKsef(
      {
        company_id: values.company_id,
        date_from: values.date_from,
        date_to: values.date_to,
        page_size: values.page_size,
        page_offset: values.page_offset,
      },
      values.invoice_type,
    );

    const list_data = await getInvoicesList(
      {
        company_id: values.company_id,
        date_from: values.date_from,
        date_to: values.date_to,
        page_size: values.page_size,
        page_offset: values.page_offset,
      },
      values.invoice_type,
    );
    return list_data;
  },

  onSuccess: (data) => {
    sortedInvoices.value = data.invoices.sort((a, b) => Number(b.is_new) - Number(a.is_new));
    totalRecords.value = data.page_info.total_items;

    if (props.invoice_type === "sales") {
      invoicesStore.setSalesInvoicesCount(data.invoices.filter((inv) => inv.is_new).length);
      console.log(sortedInvoices.value);
    } else {
      invoicesStore.setPurchaseInvoicesCount(data.invoices.filter((inv) => inv.is_new).length);
    }

    toast.add({ severity: "info", summary: "Pomyślnie pobrano faktury.", life: 3000 });
  },

  onError: (data) => {
    toast.add({ severity: "error", summary: "Błąd w pobieraniu faktur." + data, life: 3000 });
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

function onPageChange(event: any) {
  first.value = event.first;
  pageSize.value = event.rows;

  getInvoicesMutation.mutate({
    company_id: currentUserStore.getCompanyId,
    date_from: formatLocalDate(dateRange.value[0]),
    date_to: formatLocalDate(dateRange.value[1]),
    page_size: pageSize.value,
    page_offset: event.first,
    invoice_type: props.invoice_type,
  });
}

function refreshInvoices() {
  first.value = 0;

  getInvoicesMutation.mutate({
    company_id: currentUserStore.getCompanyId,
    date_from: formatLocalDate(dateRange.value[0]),
    date_to: formatLocalDate(dateRange.value[1]),
    page_size: pageSize.value,
    page_offset: 0,
    invoice_type: props.invoice_type,
  });
}

function setCustomDateRange(range: string) {
  const now = new Date();
  const startDate = new Date();

  switch (range) {
    case "week":
      startDate.setDate(now.getDate() - 7);
      break;
    case "month":
      startDate.setMonth(now.getMonth() - 1);
      break;
    case "year":
      startDate.setFullYear(now.getFullYear() - 1);
      break;
    case "full":
      startDate.setFullYear(2026, 0, 1);
      break;
  }

  dateRange.value = [startDate, now];
  refreshInvoices();
}

// function onLocalSort(event: any) {
//   const { sortField, sortOrder } = event;

//   sortedInvoices.value.sort((a, b) => {
//     const aValue = a[sortField];
//     const bValue = b[sortField];

//     if (aValue == null) return -1 * sortOrder;
//     if (bValue == null) return 1 * sortOrder;

//     if (typeof aValue === "number" && typeof bValue === "number") {
//       return (aValue - bValue) * sortOrder;
//     }

//     if (sortField === "issue_date") {
//       return (new Date(aValue).getTime() - new Date(bValue).getTime()) * sortOrder;
//     }

//     // default string sorting
//     return String(aValue).localeCompare(String(bValue)) * sortOrder;
//   });
// }

onMounted(() => {
  refreshInvoices();
});
</script>

<template>
  <DataTable
    :value="sortedInvoices"
    :loading="getInvoicesMutation.isPending.value"
    v-model:editingRows="editRows"
    edit-mode="row"
    dataKey="invoice_number"
    @row-edit-init="isEditing = true"
    @row-edit-save="OnChoosePaymentStatus"
    @row-edit-cancel="isEditing = false"
    v-model:selection="selectedInvoice"
    selection-mode="single"
    @row-select="onInvoiceSelect"
    @row-unselect="onInvoiceUnselect"
    paginator
    paginator-position="bottom"
    :rows="pageSize"
    :first="first"
    :rows-per-page-options="[5, 10, 15, 25, 50]"
    :total-records="totalRecords"
    @page="onPageChange"
    lazy
    removableSort
    scroll-height="flex"
    scrollable
    scroll-direction="both"
    striped-rows
    :pt="{
      table: { style: 'min-width: 50rem;' },
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
        <div class="flex flex-1 justify-end gap-4">
          <FloatLabel variant="on">
            <DatePicker
              v-model="dateRange"
              selection-mode="range"
              :manual-input="false"
              showIcon
              show-button-bar
              iconDisplay="input"
              date-format="yy/mm/dd"
            >
              <template #buttonbar>
                <div class="flex gap-2 w-full">
                  <Button
                    size="small"
                    label="Ostatni tydzień"
                    outlined
                    @click="() => setCustomDateRange('week')"
                  />
                  <Button
                    size="small"
                    label="Ostatni miesiąc"
                    outlined
                    @click="() => setCustomDateRange('month')"
                  />
                  <Button
                    size="small"
                    label="Ostatni rok"
                    outlined
                    @click="() => setCustomDateRange('year')"
                  />
                  <Button
                    size="small"
                    label="Cały zakres"
                    outlined
                    @click="() => setCustomDateRange('full')"
                  />
                </div>
              </template>
            </DatePicker>
            <label for="on_label">Zakres dat</label>
          </FloatLabel>
          <Button
            icon="pi pi-refresh"
            rounded
            raised
            :disabled="getInvoicesMutation.isPending.value"
            @click="refreshInvoices"
          />
        </div>
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
    <Column field="issue_date" sortable header="Data wystawienia" style="width: 10%">
      <template #body="slotProps">
        <span>{{ new Date(slotProps.data.issue_date).toLocaleDateString() }}</span>
      </template>
    </Column>
    <Column sortable header="Kontrahent" style="width: 20%">
      <template #body="slotProps">
        <span>{{
          props.invoice_type === "sales" ? slotProps.data.buyer_name : slotProps.data.seller_name
        }}</span>
      </template>
    </Column>
    <Column field="gross_total" sortable header="Suma brutto" style="width: 10%">
      <template #body="slotProps">
        <span class="inline-flex gap-1 items-baseline">
          <span>PLN</span>
          <span class="font-semibold">{{ slotProps.data.gross_total }}</span>
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
