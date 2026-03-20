<script setup lang="ts">
import type { display } from "@primeuix/themes/aura/inplace";
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
    position="bottom"
    @update:visible="emit('update:visible', $event)"
    modal
    :style="{ width: '80%' }"
  >
    <template #header>
      <div class="text-xl font-bold">
        {{ "Faktura nr " + invoice.inv_nr }}
      </div>
    </template>
    <div v-if="invoice">
      <p>Status: {{ invoice.status }}</p>
      <p>Status KSeF: {{ invoice.ksef }}</p>
      <p>Data: {{ invoice.date }}</p>
      <p>Kontrahent: {{ invoice.buyer }}</p>
      <p>Suma brutto: {{ invoice.sum_gross }}</p>
      <p>Status płatności: {{ invoice.pay_status }}</p>
    </div>
  </Dialog>
</template>
