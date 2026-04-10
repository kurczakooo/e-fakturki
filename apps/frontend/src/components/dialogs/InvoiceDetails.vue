<script setup lang="ts">
import { Button, Dialog, Card, Tag, DataTable, Column, Divider, Select, DataView } from "primevue";
import invoiceXml from "../../assets/mock_xml";

const props = defineProps<{
  visible: boolean;
  invoice: any;
}>();

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

function onGetInvoice() {}

function collectAddress(address: any) {
  return (
    address.street +
    " " +
    address.building_number +
    ", " +
    address.postal_code +
    " " +
    address.city +
    ", " +
    address.country
  );
}

function createFileName(invoice: any) {
  return invoice.invoice_number.trim().replace(/\s+/g, "_");
}

function onDownloadXml(fileName: string) {
  // call API to get the XML
  const xml = invoiceXml;

  const blob = new Blob([xml], { type: "application/xml" });
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = fileName;

  document.body.appendChild(a);
  a.click();

  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

function onDownloadPdf() {}

function onPrintPdf() {}

const emit = defineEmits(["update:visible"]);
</script>

<template>
  <Dialog
    :visible="visible"
    position="bottom"
    @update:visible="emit('update:visible', $event)"
    modal
    maximizable
    :style="{ width: '60%' }"
  >
    <!-- header -->
    <template #header>
      <div class="flex-1 flex gap-4 items-center">
        <Tag v-if="invoice.is_new" value="Nowa"></Tag>
        <span class="text-xl font-bold">
          {{ "Faktura nr " + invoice.invoice_number }}
        </span>
        <Tag
          :value="ksefStatusHint[invoice.ksef_status]"
          :severity="ksefStatusSeverity[invoice.ksef_status]"
        ></Tag>
        <Button
          v-if="invoice.ksef_status === 'accepted' || invoice.ksef_status === 'rejected'"
          icon="pi pi-info-circle"
          outlined
          v-tooltip.top="'Szczegóły'"
        ></Button>
        <Button
          v-if="invoice.ksef_status === 'not_sent' || invoice.ksef_status === 'rejected'"
          icon="pi pi-send"
          outlined
          v-tooltip.top="'Wyślij do KSeF'"
        ></Button>
      </div>
    </template>

    <!-- content -->
    <div class="mr-4 ml-4">
      <!-- issue date and place -->
      <div class="flex-1 flex flex-col text-end">
        <span>Miejsce i data wystawienia: </span>
        <span class="font-semibold">
          {{ invoice.issue_place + ", " + new Date(invoice.issue_date).toLocaleDateString() }}
        </span>
        <span>Data dostarczenia towaru / Wykonania usługi: </span>
        <span class="font-semibold">
          {{ new Date(invoice.exec_date).toLocaleDateString() }}
        </span>
      </div>
      <!-- companies info -->
      <div class="flex-1 flex justify-between mt-4 mb-8">
        <Card>
          <template #title>Sprzedawca</template>
          <template #content>
            <p class="m-0">{{ invoice.seller_name }}</p>
            <p class="m-0">NIP {{ invoice.seller_nip }}</p>
            <p class="m-0">{{ collectAddress(invoice.seller_address) }}</p>
          </template>
        </Card>
        <Card>
          <template #title>Nabywca</template>
          <template #content>
            <p class="m-0">{{ invoice.buyer_name }}</p>
            <p class="m-0">NIP {{ invoice.buyer_nip }}</p>
            <p class="m-0">{{ collectAddress(invoice.buyer_addrees) }}</p>
          </template>
        </Card>
      </div>
      <!-- invoice items -->
      <DataTable :value="invoice.items">
        <Column field="record_nr" header="Lp." style="width: 2%"></Column>
        <Column field="name" header="Nazwa towaru lub usługi" style="width: 25%"></Column>
        <Column field="amount" header="Ilość + J.m." style="width: 12%">
          <template #body="slotProps">
            <span>{{ slotProps.data.amount + " " + slotProps.data.unit }}</span>
          </template>
        </Column>
        <!-- <Column field="unit" header="J.m." style="width: 8%"></Column> -->
        <Column field="price_net" header="Cena netto (zł)" style="width: 10%">
          <template #body="slotProps">
            <span>{{ Math.floor(slotProps.data.price_net).toFixed(2) }}</span>
          </template>
          <template #footer>
            <span class="font-semibold"> SUMA: </span>
          </template>
        </Column>
        <Column field="net_total" header="Wartość netto (zł)" style="width: 10%">
          <template #body="slotProps">
            <span>{{ Math.floor(slotProps.data.net_total).toFixed(2) }}</span>
          </template>
          <template #footer>
            <span class="font-semibold">
              {{ Math.floor(invoice.net_total).toFixed(2) }}
            </span>
          </template>
        </Column>
        <Column field="tax_rate" header="Stawka VAT" style="width: 7%">
          <template #body="slotProps">
            <span>{{ slotProps.data.tax_rate + "%" }}</span>
          </template>
        </Column>
        <Column field="tax_total" header="Wartość VAT (zł)" style="width: 10%">
          <template #body="slotProps">
            <span>{{ Math.floor(slotProps.data.tax_total).toFixed(2) }}</span>
          </template>
          <template #footer>
            <span class="font-semibold">
              {{ Math.floor(invoice.tax_total).toFixed(2) }}
            </span>
          </template>
        </Column>
        <Column field="gross_total" header="Wartość brutto (zł)" style="width: 10%">
          <template #body="slotProps">
            <span>{{ Math.floor(slotProps.data.gross_total).toFixed(2) }}</span>
          </template>
          <template #footer>
            <span class="font-semibold">
              {{ Math.floor(invoice.gross_total).toFixed(2) }}
            </span>
          </template>
        </Column>
      </DataTable>
      <!-- summary -->
      <div class="mt-4">
        <Card>
          <template #title>Do zapłaty:&nbsp;&nbsp;{{ invoice.gross_total }} zł</template>
          <template #content>
            <!-- <span>{{ "słownie: " }}</span> -->
          </template>
        </Card>
      </div>

      <!-- payment info -->
      <Divider />
      <div class="flex mt-4">
        <!-- left info -->
        <div class="flex-1 flex flex-col text-start">
          <span>Rodzaj płatności: </span>
          <span class="font-semibold">
            {{ paymentType[invoice.payment_type] }}
          </span>
          <span>Termin płatności: </span>
          <span class="font-semibold">
            {{ new Date(invoice.payment_due_date).toLocaleDateString() }}
          </span>
          <div class="mt-2">
            <span>Dane płatności: </span>
            <div>
              <span>Numer konta: </span>
              <span class="font-semibold">
                {{ invoice.payment_details.iban }}
              </span>
            </div>
            <div>
              <span>Bank: </span>
              <span class="font-semibold">
                {{ invoice.payment_details.bank_name }}
              </span>
            </div>
            <div>
              <span>Tytuł przelewu: </span>
              <span class="font-semibold">
                {{ invoice.payment_details.transfer_title || "-" }}
              </span>
            </div>
          </div>
        </div>
        <!-- right status -->
        <div class="flex-1 flex justify-end items-start gap-4">
          <div class="flex gap-4 items-center">
            <Select
              v-model="invoice.payment_status"
              :options="paymentOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Wybierz status płatności"
            >
              <template #option="slotProps">
                <Tag
                  :value="slotProps.option.label"
                  :severity="paymentStatusSeverity[slotProps.option.value]"
                />
              </template>

              <template #value="slotProps">
                <Tag
                  v-if="slotProps.value"
                  :value="paymentOptions.find((o) => o.value === slotProps.value)?.label"
                  :severity="paymentStatusSeverity[slotProps.value]"
                />
                <span v-else class="text-gray-400"> Wybierz status płatności </span>
              </template>
            </Select>
          </div>
        </div>
      </div>
      <Divider />

      <!-- additional info -->
      <div class="flex-1 flex flex-col">
        <span>Uwagi: </span>
        <span class="font-semibold">
          {{ invoice.additional_info || "-" }}
        </span>
      </div>
    </div>

    <template #footer>
      <Button
        label="Pobierz XML"
        icon="pi pi-download"
        outlined
        @click="() => onDownloadXml(createFileName(invoice))"
      ></Button>
      <Button
        disabled
        label="Pobierz PDF"
        icon="pi pi-file-pdf"
        outlined
        @click="onDownloadPdf"
      ></Button>
      <Button disabled label="Drukuj" icon="pi pi-print" outlined @click="onPrintPdf"></Button>
    </template>
  </Dialog>
</template>
