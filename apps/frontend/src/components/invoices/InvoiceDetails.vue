<script setup lang="ts">
import {
  Button,
  Dialog,
  Card,
  Tag,
  Popover,
  DataTable,
  Column,
  Divider,
  Select,
  useToast,
} from "primevue";
import invoiceXml from "../../assets/mock_xml";
import { emptyToNull } from "../../lib/utils";
import { ref, watch } from "vue";
import { useMutation } from "@tanstack/vue-query";
import { getInvoiceDetails, postInvoiceToKsef } from "../../lib/services/ksefService";
import type { InvoiceCompanyData, InvoiceObject } from "../../lib/types/invoices";
import {
  ksefStatusHint,
  ksefStatusSeverity,
  paymentType,
  paymentStatusSeverity,
  paymentOptions,
} from "../../lib/types/invoices";
import type { invoiceTableType } from "../../lib/types/invoices";
import { useCurrentUserStore } from "../../stores/currentUserStore";
import { createCompany } from "../../lib/services/companyService";

const props = defineProps<{
  visible: boolean;
  invoice_type: invoiceTableType;
  invoice: any;
}>();

const toast = useToast();
const currentUserStore = useCurrentUserStore();
const ksefPopup = ref();
const toggleKsefPopup = (event: any) => {
  ksefPopup.value.toggle(event);
};
const emit = defineEmits(["update:visible"]);
const invoice = ref<InvoiceObject>();
const postInvoiceToKsefError = ref<string>("");

const getInvoiceDetailsMutation = useMutation({
  mutationFn: async (values: any) => {
    const list_data = await getInvoiceDetails(values.company_id, values.invoice_id);
    return list_data;
  },

  onSuccess: (data) => {
    invoice.value = structuredClone(data);
  },

  onError: (data) => {
    toast.add({ severity: "error", summary: "Błąd w danych faktury." + data, life: 3000 });
  },
});

const postInvoiceToKsefMutation = useMutation({
  mutationFn: async (values: any) => {
    const status = await postInvoiceToKsef(values.company_id, values.invoice_id);
    return status;
  },

  onSuccess: (data) => {
    if (invoice.value) {
      invoice.value.ksef_number = data.ksef_number;
      invoice.value.invoicing_date = data.invoicing_date;
      invoice.value.acquisition_date = data.acquisition_date;
      invoice.value.permanent_storage_date = data.permanent_storage_date;
    }
    toast.add({ severity: "info", summary: "Pomyślnie wysłano fakturę do KSeF.", life: 3000 });
  },

  onError: (data) => {
    toast.add({
      severity: "error",
      summary: "Błąd podczas wysyłania faktury do KSeF." + data,
      life: 3000,
    });
    postInvoiceToKsefError.value = data.message;
  },
});

const saveCompanyMutation = useMutation({
  mutationFn: async () => {
    const company =
      props.invoice_type === "sales" ? invoice.value?.buyer_info : invoice.value?.seller_info;

    const companyResp = await createCompany({
      owner_id: null,
      name: company?.name,
      nip: company?.nip,
      krs: null,
      regon: null,
      country_code: "PL",
      address_l1: emptyToNull(company?.address_l1),
      address_l2: emptyToNull(company?.address_l2),
      address_correspondance_l1: null,
      address_correspondance_l2: null,
      email: emptyToNull(company?.email),
      phone_number: emptyToNull(company?.phone),
      additional_info: null,
    });

    return companyResp;
  },

  onSuccess: () => {
    toast.add({ severity: "success", summary: "Firma dodana pomyślnie!", life: 3000 });
  },

  onError: (error) => {
    toast.add({
      severity: "info",
      summary: error?.response?.data?.detail,
      life: 5000,
    });
  },
});

function collectAddress(companyInfo: InvoiceCompanyData) {
  return [companyInfo.address_l1, companyInfo.address_l2].filter(Boolean).join(", ");
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

watch(
  () => props.visible,
  async (visible) => {
    if (visible && props.invoice?.id) {
      await getInvoiceDetailsMutation.mutateAsync({
        company_id: currentUserStore.getCompanyId,
        invoice_id: props.invoice.id,
      });
    }
  },
);
</script>

<template>
  <Dialog
    :visible="visible"
    position="bottom"
    @update:visible="emit('update:visible', $event)"
    @hide="
      () => {
        invoice.value = null;
      }
    "
    modal
    maximizable
    :style="{ width: '60%' }"
    :loading="getInvoiceDetailsMutation.isPending.value"
  >
    <!-- header -->
    <template #header>
      <div v-if="invoice" class="flex-1 flex gap-4 items-center">
        <Tag v-if="invoice.is_new" value="Nowa"></Tag>
        <span class="text-xl font-bold">
          {{ `Faktura ${invoice.invoice_type.toUpperCase()} nr ${invoice.invoice_number}` }}
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
          @click="toggleKsefPopup"
          :loading="postInvoiceToKsefMutation.isPending.value"
          :disabled="postInvoiceToKsefMutation.isPending.value"
        ></Button>
        <Button
          v-if="invoice.ksef_status === 'not_sent' || invoice.ksef_status === 'rejected'"
          icon="pi pi-send"
          outlined
          v-tooltip.top="'Wyślij do KSeF'"
          @click="postInvoiceToKsefMutation.mutate"
          :loading="postInvoiceToKsefMutation.isPending.value"
          :disabled="postInvoiceToKsefMutation.isPending.value"
        ></Button>
      </div>
    </template>

    <!-- content -->
    <div v-if="invoice" class="mr-4 ml-4">
      <!-- issue date and place -->
      <div class="flex-1 flex flex-col text-end">
        <span>Miejsce i data wystawienia: </span>
        <div>
          <span class="font-semibold">
            {{ invoice.issue_place ? `${invoice.issue_place}, ` : "-, " }}
          </span>
          <span class="font-semibold">
            {{ new Date(invoice.issue_date).toLocaleDateString() }}
          </span>
        </div>
      </div>
      <!-- companies info -->
      <div class="flex-1 flex justify-between mt-4 mb-8">
        <Card>
          <template #title>Sprzedawca</template>
          <template #content>
            <p class="m-0">{{ invoice.seller_info.name }}</p>
            <p class="m-0">NIP {{ invoice.seller_info.nip }}</p>
            <p class="m-0">{{ collectAddress(invoice.seller_info) }}</p>
          </template>
        </Card>
        <div
          class="flex flex-1 items-start"
          :class="props.invoice_type === 'sales' ? 'justify-end pr-2' : 'justify-start pl-2'"
        >
          <Button
            icon="pi pi-save"
            outlined
            v-tooltip.top="'Zapisz firmę w bazie danych'"
            @click="saveCompanyMutation.mutate"
            :loading="saveCompanyMutation.isPending.value"
            :disabled="saveCompanyMutation.isPending.value"
          ></Button>
        </div>
        <Card>
          <template #title>Nabywca</template>
          <template #content>
            <p class="m-0">{{ invoice.buyer_info.name }}</p>
            <p class="m-0">NIP {{ invoice.buyer_info.nip }}</p>
            <p class="m-0">{{ collectAddress(invoice.buyer_info) }}</p>
          </template>
        </Card>
      </div>
      <!-- invoice items -->
      <DataTable :value="invoice.entries || []">
        <Column field="row_number" header="Lp." style="width: 2%"></Column>
        <Column field="name" header="Nazwa towaru lub usługi" style="width: 25%"></Column>
        <Column field="amount" header="Ilość + J.m." style="width: 12%">
          <template #body="slotProps">
            <span>{{ slotProps.data.amount + " " + slotProps.data.unit }}</span>
          </template>
        </Column>
        <Column field="net_price" header="Cena netto (zł)" style="width: 10%">
          <template #body="slotProps">
            <span v-if="slotProps.data.net_price">{{ slotProps.data.net_price.toFixed(2) }}</span>
            <span v-else>-</span>
          </template>
          <template #footer>
            <span class="font-semibold"> SUMA: </span>
          </template>
        </Column>
        <Column field="net_total" header="Wartość netto (zł)" style="width: 10%">
          <template #body="slotProps">
            <span v-if="slotProps.data.net_total">{{ slotProps.data.net_total.toFixed(2) }}</span>
            <span v-else>-</span>
          </template>
          <template #footer>
            <span class="font-semibold">
              {{ invoice.net_total.toFixed(2) }}
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
            <span v-if="slotProps.data.tax_total">{{ slotProps.data.tax_total.toFixed(2) }}</span>
            <span v-else>-</span>
          </template>
          <template #footer>
            <span v-if="invoice.tax_total" class="font-semibold">
              {{ invoice.tax_total.toFixed(2) }}
            </span>
            <span v-else>-</span>
          </template>
        </Column>
        <Column
          v-if="invoice.entries[0]?.gross_price"
          field="gross_price"
          header="Cena brutto (zł)"
          style="width: 10%"
        >
          <template #body="slotProps">
            <span v-if="slotProps.data.gross_price">{{
              slotProps.data.gross_price.toFixed(2)
            }}</span>
            <span v-else>-</span>
          </template>
        </Column>
        <Column field="gross_total" header="Wartość brutto (zł)" style="width: 10%">
          <template #body="slotProps">
            <span v-if="slotProps.data.gross_total">{{
              slotProps.data.gross_total.toFixed(2)
            }}</span>
            <span v-else>-</span>
          </template>
          <template #footer>
            <span class="font-semibold">
              {{ invoice.gross_total.toFixed(2) }}
            </span>
          </template>
        </Column>
      </DataTable>
      <!-- summary -->
      <div class="mt-4">
        <Card>
          <template #title>Do zapłaty:&nbsp;&nbsp;{{ invoice.gross_total.toFixed(2) }} zł</template>
          <template #content>
            <!-- <span>{{ "słownie: " }}</span> -->
          </template>
        </Card>
      </div>

      <!-- payment info -->
      <Divider />
      <div v-if="invoice.payment" class="flex mt-4">
        <!-- left info -->
        <div class="flex-1 flex flex-col text-start">
          <span>Rodzaj płatności: </span>
          <span class="font-semibold">
            {{ paymentType[invoice.payment.payment_type] }}
          </span>
          <span>Termin płatności: </span>
          <span class="font-semibold">
            {{ new Date(invoice.payment.payment_due_date).toLocaleDateString() }}
          </span>
          <div class="mt-2">
            <span>Dane płatności: </span>
            <div v-if="invoice.payment.seller_bank_account_number">
              <span>Numer konta: </span>
              <span class="font-semibold">
                {{ invoice.payment.seller_bank_account_number }}
              </span>
            </div>
            <div v-if="invoice.payment.seller_bank_name">
              <span>Bank: </span>
              <span class="font-semibold">
                {{ invoice.payment.seller_bank_name }}
              </span>
            </div>
          </div>
        </div>
        <!-- right status -->
        <div class="flex-1 flex justify-end items-start gap-4">
          <div class="flex gap-4 items-center">
            <Select
              v-model="invoice.payment.payment_status"
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
      <div class="flex-1 flex flex-col gap-4">
        <div class="flex-1 flex flex-col">
          <span>Adnotacje: </span>
          <span class="font-semibold">
            {{ invoice.annotations || "-" }}
          </span>
        </div>
        <div class="flex-1 flex flex-col">
          <span>Rejestry: </span>
          <span class="font-semibold">
            {{ invoice.footer_registers || "-" }}
          </span>
        </div>
        <div class="flex-1 flex flex-col">
          <span>Dodatkowe informacje: </span>
          <span class="font-semibold">
            {{ invoice.additional_info || "-" }}
          </span>
          <span class="font-semibold">
            {{ invoice.footer_info || "-" }}
          </span>
        </div>
      </div>
    </div>

    <template #footer v-if="invoice">
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

  <!-- ksef popup -->
  <Popover ref="ksefPopup">
    <div v-if="invoice?.ksef_status === 'accepted'" class="flex flex-col w-130">
      <div>
        <span>Numer KSeF: </span>
        <span class="font-semibold">{{ invoice?.ksef_number }}</span>
      </div>
      <div>
        <span>Data przyjęcia faktury w systemie KSeF: </span>
        <span class="font-semibold">{{
          new Date(invoice?.invoicing_date).toLocaleString("pl-PL", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
          })
        }}</span>
      </div>
      <div>
        <span>Data nadania numeru KSeF: </span>
        <span class="font-semibold">{{
          new Date(invoice?.acquisition_date).toLocaleString("pl-PL", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
          })
        }}</span>
      </div>
      <div>
        <span>Data trwałego zapisu faktury w KSeF: </span>
        <span class="font-semibold">{{
          new Date(invoice?.permanent_storage_date).toLocaleString("pl-PL", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
          })
        }}</span>
      </div>
    </div>
    <div v-if="invoice?.ksef_status === 'rejected'" class="flex flex-col w-130">
      <span>Szczegóły odrzucenia faktury przez KSeF: </span>
      <span class="font-semibold">{{ postInvoiceToKsefError }}</span>
    </div>
  </Popover>
</template>
