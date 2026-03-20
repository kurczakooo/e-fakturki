<script setup lang="ts">
import Dialog from "primevue/dialog";

const props = defineProps<{
  visible: boolean;
  invoice: any;
}>();

const emit = defineEmits(["update:visible"]);
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="emit('update:visible', $event)"
    modal
    header="Invoice"
  >
    <div v-if="invoice">
      <p>Numer faktury: {{ invoice.inv_nr }}</p>
      <p>Status: {{ invoice.status }}</p>
      <p>Status KSeF: {{ invoice.ksef }}</p>
      <p>Data: {{ invoice.date }}</p>
      <p>Kontrahent: {{ invoice.buyer }}</p>
      <p>Suma brutto: {{ invoice.sum_gross }}</p>
      <p>Status płatności: {{ invoice.pay_status }}</p>
    </div>
  </Dialog>
</template>
