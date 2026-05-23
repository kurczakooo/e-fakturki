<script setup lang="ts">
import {
  DataTable,
  Column,
  Button,
  InputText,
  Select,
  DatePicker,
  Divider,
  useToast,
  Panel,
  InputNumber,
} from "primevue";

import { useCurrentUserStore } from "../stores/currentUserStore";
import { onMounted, ref } from "vue";
import type { InvoiceObject, InvoiceEntry } from "../lib/types/invoices";
import {
  calculateGrossPrice,
  calculateGrossTotal,
  calculateNetTotal,
  calculateTaxTotal,
  formatPLN,
  roundTo2,
  verifyNetVsGrossPrice,
} from "../lib/utils";
import { useMutation } from "@tanstack/vue-query";
import { getTaxRates } from "../lib/services/productService";
import type { TaxRate } from "../lib/types/products";
import InvoiceCreationFooter from "../components/invoices/InvoiceCreationFooter.vue";
import InvoiceCreationCompanyDataForm from "../components/invoices/InvoiceCreationCompanyDataForm.vue";
import InvoiceInfoForm from "../components/invoices/InvoiceInfoForm.vue";
import InvoiceDetails from "../components/invoices/InvoiceDetails.vue";
import InvoiceCreationPaymentDetails from "../components/invoices/InvoiceCreationPaymentDetails.vue";

const currentUserStore = useCurrentUserStore();
const toast = useToast();
const invoice = ref<InvoiceObject>({
  invoice_number: "",
  invoice_type: "VAT",
  ksef_status: "not_sent",
  is_new: true,
  issue_date: "",
  issue_place: "",
  seller_info: {
    name: currentUserStore.getCompanyName,
    nip: currentUserStore.getCompanyNip,
    address_l1: currentUserStore.getCompanyAddressL1,
    address_l2: currentUserStore.getCompanyAddressL2,
    email: currentUserStore.getCompanyEmail,
    phone: currentUserStore.getCompanyPhoneNumber,
  },
  buyer_info: {
    name: "",
    nip: "",
    address_l1: "",
    address_l2: "",
    email: null,
    phone: null,
  },
  entries: [],
  currency: "PLN",
  net_total: 0,
  tax_total: 0,
  gross_total: 0,
  payment: {
    payment_status: "unpaid",
    payment_type: "transfer",
    payment_date: null,
    payment_due_date: null,
    partial_payments: null,
    seller_bank_account_number: null,
    seller_bank_name: null,
  },
});
const invoiceEntryColumns = ref([
  { field: "delete_row", header: "", width: "width: 5%" },
  { field: "row_number", header: "Nr. wiersza", width: "width: 5%" },
  { field: "delivery_date", header: "Dostawa", width: "width: 8%" },
  { field: "name", header: "Nazwa", width: "width: 17%" },
  { field: "unit", header: "Jedn. Miary", width: "width: 6%" },
  { field: "amount", header: "Ilość", width: "width: 6%" },
  { field: "net_price", header: "Cena netto", width: "width: 8%" },
  { field: "tax_rate", header: "Stawka VAT", width: "width: 8%" },
  { field: "gross_price", header: "Cena brutto", width: "width: 8%" },
  { field: "net_total", header: "Wartość netto", width: "width: 8%" },
  { field: "tax_total", header: "Wartość VAT", width: "width: 8%" },
  { field: "gross_total", header: "Wartość brutto", width: "width: 8%" },
]);

const readonlyFields = [
  "delete_row",
  "row_number",
  "net_total",
  "tax_total",
  "gross_price",
  "gross_total",
];
const taxRates = ref<TaxRate[]>([]);
const taxRateMap = ref<Map<string, TaxRate>>(new Map());
const invoicePreviewDialog = ref(false);

const getTaxRatesMutation = useMutation({
  mutationFn: async () => {
    return await getTaxRates();
  },

  onSuccess: (data) => {
    taxRates.value = data;
    taxRateMap.value = new Map(data.map((tax) => [tax.str_repr, tax]));
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 5000 });
  },
});

function newEntry() {
  invoice.value?.entries.push({
    row_number: invoice.value?.entries.length + 1,
    delivery_date: new Date(),
    name: "",
    amount: 1,
    unit: "",
    net_price: 0,
    gross_price: 0,
    tax_rate: taxRates.value[0],
    net_total: 0,
    tax_total: 0,
    gross_total: 0,
  });
}

function recalculateInvoiceTotals() {
  invoice.value.net_total = roundTo2(
    invoice.value.entries.reduce((acc, entry) => acc + entry.net_total, 0),
  );
  invoice.value.tax_total = roundTo2(
    invoice.value.entries.reduce((acc, entry) => acc + entry.tax_total, 0),
  );
  invoice.value.gross_total = roundTo2(
    invoice.value.entries.reduce((acc, entry) => acc + entry.gross_total, 0),
  );
}

function onCellEditComplete(event: any) {
  const { data, newValue, field } = event;

  // optional validation
  if (newValue === null || newValue === undefined) {
    event.preventDefault();
    return;
  }

  // recalculate individual record prices and totals
  if (field === "net_price" && Number(newValue) > 0) {
    data[field] = roundTo2(Number(newValue));
    data.gross_price = calculateGrossPrice(data.net_price, data.tax_rate.value);
    data.net_total = calculateNetTotal(data.net_price, data.amount);
    data.tax_total = calculateTaxTotal(data.net_price, data.tax_rate.value, data.amount);
    data.gross_total = calculateGrossTotal(data.net_price, data.amount, data.tax_rate.value);
  }
  if (field === "amount" && Number(newValue) > 0) {
    data[field] = roundTo2(Number(newValue));
    data.net_total = calculateNetTotal(data.net_price, data.amount);
    data.tax_total = calculateTaxTotal(data.net_price, data.tax_rate.value, data.amount);
    data.gross_total = calculateGrossTotal(data.net_price, data.amount, data.tax_rate.value);
  }
  if (field === "tax_rate") {
    data[field] = newValue;
    data.gross_price = calculateGrossPrice(data.net_price, data.tax_rate.value);
    data.tax_total = calculateTaxTotal(data.net_price, data.tax_rate.value, data.amount);
    data.gross_total = calculateGrossTotal(data.net_price, data.amount, data.tax_rate.value);
  }

  data[field] = newValue;

  // recalculate invoice totals
  recalculateInvoiceTotals();
}

function removeInvoiceEntry(entry: InvoiceEntry) {
  invoice.value.entries = invoice.value?.entries.filter(
    (record) => record.row_number !== entry.row_number,
  );

  // move row numbers
  invoice.value.entries.forEach((e, index) => {
    e.row_number = index + 1;
  });

  // recalculate invoice totals
  recalculateInvoiceTotals();
}

function updateInvoiceInfo(event: any) {
  invoice.value.invoice_number = event.invoiceNumber;
  invoice.value.issue_place = event.issuePlace;
  invoice.value.issue_date = event.invoiceDate.toISOString();
  console.log(invoice.value);
}

onMounted(async () => {
  await getTaxRatesMutation.mutateAsync();
});
</script>

<template>
  <!-- header -->
  <div class="flex flex-col mt-5 mb-3 gap-1">
    <span class="text-xl font-bold pl-4 text-color">Tworzenie nowej faktury</span>
    <Divider />
  </div>
  <!-- invoice contents -->
  <Panel class="px-36 h-4/5 flex flex-1 flex-col overflow-y-scroll">
    <!-- <div class="gap-4 px-12 h-4/5 overflow-y-scroll"> -->
    <!-- companies info -->
    <div class="flex flex-1 pb-4 justify-center">
      <InvoiceInfoForm @update="updateInvoiceInfo" />
    </div>
    <div class="flex flex-1 justify-between pb-12">
      <InvoiceCreationCompanyDataForm
        :seller="true"
        v-tooltip.top="'Dane własnej firmy można zmienić w zakładce Firmy'"
      />
      <InvoiceCreationCompanyDataForm :seller="false" />
    </div>

    <!-- invoice entries table -->
    <DataTable
      :value="invoice?.entries"
      dataKey="row_number"
      editMode="cell"
      @cell-edit-complete="onCellEditComplete"
      :pt="{
        table: { style: 'table-layout: fixed;' },
        column: {
          bodycell: ({ state }) => ({
            class: [{ '!py-0': state['d_editing'] }],
          }),
        },
      }"
    >
      <template #header>
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="font-bold">Pozycje</span>
        </div>
      </template>
      <Column
        v-for="col of invoiceEntryColumns"
        :key="col.field"
        :field="col.field"
        :header="col.header"
        :editor="!readonlyFields.includes(col.field)"
        :style="col.width"
      >
        <!-- NORMAL DISPLAY -->
        <template #body="{ data, field }">
          <div v-if="['delete_row'].includes(field)" class="flex flex-1 justify-center">
            <Button
              icon="pi pi-trash"
              variant="outlined"
              severity="danger"
              rounded
              raised
              @click="removeInvoiceEntry(data)"
            />
          </div>

          <span v-else-if="['row_number'].includes(field)">
            {{ data[field] }}
          </span>

          <!-- monetary values -->
          <InputNumber
            v-else-if="['net_price', 'gross_price'].includes(field)"
            v-model="data[field]"
            mode="currency"
            currency="PLN"
            locale="pl-PL"
            autofocus
            fluid
          />

          <span v-else-if="['net_total', 'tax_total', 'gross_total'].includes(field)">
            {{ formatPLN(data[field]) }}
          </span>

          <!-- delivery date -->
          <span v-else-if="field === 'delivery_date'">
            <DatePicker
              v-model="data[field]"
              dateFormat="yy/mm/dd"
              fluid
              @click.stop
              @mousedown.stop
            />
          </span>

          <!-- tax rate -->
          <span
            v-else-if="field === 'tax_rate'"
            v-tooltip.bottom="taxRateMap.get(data[field].str_repr)?.hint_text"
            >{{ taxRateMap.get(data[field].str_repr)?.display_text || data[field] }}</span
          >

          <!-- default -->
          <InputText v-else v-model="data[field]" autofocus fluid />
        </template>

        <!-- EDIT MODE -->
        <template #editor="{ data, field }">
          <template
            v-if="readonlyFields.includes(field) && !['row_number', 'delete_row'].includes(field)"
          >
            <span>{{ data[field] }} zł</span>
          </template>
          <template v-else-if="field === 'row_number'">
            <span>{{ data[field] }}</span>
          </template>
          <template v-else-if="field === 'delete_row'">
            <div class="flex flex-1 justify-center">
              <Button
                icon="pi pi-trash"
                variant="outlined"
                severity="danger"
                rounded
                raised
                @click="removeInvoiceEntry(data)"
              />
            </div>
          </template>

          <!-- tax rate -->
          <template v-else-if="field === 'tax_rate'">
            <Select
              v-model="data[field]"
              :options="taxRates"
              class="h-10.5"
              emptyMessage="Brak opcji do wyboru"
              fluid
            >
              <template #value="slotProps">
                <div v-if="slotProps.value" class="flex items-center gap-2">
                  <div v-tooltip.bottom="slotProps.value.hint_text" class="flex flex-1">
                    {{ slotProps.value.display_text }}
                  </div>
                </div>
                <span v-else>
                  {{ slotProps.placeholder }}
                </span>
              </template>
              <template #option="slotProps">
                <div class="flex flex-1 items-center gap-2">
                  <div v-tooltip.bottom="slotProps.option.hint_text" class="flex flex-1">
                    {{ slotProps.option.display_text }}
                  </div>
                </div>
              </template>
            </Select>
          </template>

          <!-- delivery date -->
          <template v-else-if="field === 'delivery_date'">
            <DatePicker
              v-model="data[field]"
              dateFormat="yy/mm/dd"
              fluid
              @click.stop
              @mousedown.stop
            />
          </template>

          <!-- amount -->
          <template v-else-if="field === 'amount'">
            <InputNumber
              v-model="data[field]"
              locale="pl-PL"
              :minFractionDigits="0"
              :maxFractionDigits="3"
              autofocus
              fluid
            />
          </template>

          <!-- monetary values -->
          <template v-else-if="['net_price', 'gross_price'].includes(field)">
            <InputNumber
              v-model="data[field]"
              mode="currency"
              currency="PLN"
              locale="pl-PL"
              autofocus
              fluid
            />
          </template>

          <!-- default -->
          <template v-else>
            <InputText v-model="data[field]" autofocus fluid />
          </template>
        </template>

        <!-- FOOTER -->
        <template #footer>
          <Button
            v-if="col.field === 'delete_row'"
            class="ml-2"
            icon="pi pi-plus"
            rounded
            raised
            v-tooltip.bottom="'Dodaj kolejną pozycję'"
            @click="newEntry"
          ></Button>

          <span v-if="col.field === 'gross_price'" class="font-semibold"> SUMA: </span>
          <span v-else-if="col.field === 'net_total'" class="font-semibold">
            {{ formatPLN(invoice?.net_total || 0) }}
          </span>
          <span v-else-if="col.field === 'tax_total'" class="font-semibold">
            {{ formatPLN(invoice?.tax_total || 0) }}
          </span>
          <span v-else-if="col.field === 'gross_total'" class="font-semibold">
            {{ formatPLN(invoice?.gross_total || 0) }}
          </span>
        </template>
      </Column>
    </DataTable>

    <!-- payment details -->
    <div class="flex flex-1 justify-between pt-12">
      <InvoiceCreationPaymentDetails />
      <div>
        <span class="text-xl font-bold">Do zapłaty: </span>
        <span class="text-xl font-bold">{{ formatPLN(invoice?.gross_total || 0) }}</span>
      </div>
    </div>
    <!-- </div> -->
  </Panel>
  <!-- footer -->
  <div class="mt-3 relative">
    <InvoiceCreationFooter
      @preview="
        () => {
          invoicePreviewDialog = true;
        }
      "
    />
  </div>
  <!-- Invoice details dialog -->
  <InvoiceDetails v-model:visible="invoicePreviewDialog" :invoice="invoice" invoice_type="sales" />
</template>
