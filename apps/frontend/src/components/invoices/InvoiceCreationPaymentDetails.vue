<script setup lang="ts">
import { Form, FormField } from "@primevue/forms";
import {
  Toolbar,
  Panel,
  InputText,
  Button,
  FloatLabel,
  Message,
  DatePicker,
  Select,
  Tag,
} from "primevue";
import { ref } from "vue";
import {
  paymentOptions,
  paymentStatus,
  paymentStatusSeverity,
  paymentType,
} from "../../lib/types/invoices";

const emits = defineEmits(["completed"])

const selectedPaymentStatus = ref("unpaid");
const paymentTypes = Object.entries(paymentType).map(([key, value]) => ({
  label: value,
  value: Number(key),
}));
const selectedPaymentType = ref(1);
const payDueDate = ref(new Date());
const payDate = ref(new Date());
</script>

<template>
  <Panel>
    <template #header>
      <span class="text-xl font-bold">Płatność</span>
    </template>
    <Form class="flex flex-col gap-2 w-full sm:w-100 pb-2">
      <FormField v-slot="$field" name="payment_status" class="flex flex-col gap-1">
        <FloatLabel variant="on">
          <Select
            v-model="selectedPaymentStatus"
            :options="paymentOptions"
            optionLabel="label"
            optionValue="value"
            fluid
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
            </template>
          </Select>
          <label for="name_input">Status płatności</label>
        </FloatLabel>
        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <FormField v-slot="$field" name="payment_type" class="flex flex-col gap-1">
        <FloatLabel variant="on">
          <Select
            v-model="selectedPaymentType"
            :options="paymentTypes"
            optionLabel="label"
            optionValue="value"
            fluid
          >
          </Select>
          <label for="name_input">Rodzaj płatności</label>
        </FloatLabel>
        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
          $field.error?.message
        }}</Message>
      </FormField>
      <Panel
        v-if="[2, 3, 4, 5, 6, 7].includes(selectedPaymentType)"
        header="Dane płatności"
        toggleable
        collapsed
      >
        <div class="flex flex-col gap-2">
          <FormField v-slot="$field" name="iban" class="flex flex-col gap-1">
            <FloatLabel variant="on">
              <InputText v-bind="$field.props" id="iban_input" type="text" fluid />
              <label for="iban_input">Numer rachunku bankowego (IBAN)</label>
            </FloatLabel>
            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
              $field.error?.message
            }}</Message>
          </FormField>
          <FormField v-slot="$field" name="bankName" class="flex flex-col gap-1">
            <FloatLabel variant="on">
              <InputText v-bind="$field.props" id="bankName_input" type="text" fluid />
              <label for="bankName_input">Nazwa Banku</label>
            </FloatLabel>
            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
              $field.error?.message
            }}</Message>
          </FormField>
        </div>
      </Panel>
      <FormField
        v-if="selectedPaymentStatus !== 'paid'"
        v-slot="$field"
        name="pay_due_date"
        class="flex flex-col gap-1"
      >
        <FloatLabel variant="on">
          <DatePicker
            v-model="payDueDate"
            inputId="payDueDate"
            dateFormat="yy/mm/dd"
            fluid
            showIcon
            iconDisplay="input"
          />
          <label for="payDueDate">Termin płatności</label>
        </FloatLabel>
        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>
      <FormField v-else v-slot="$field" name="krs" class="flex flex-col gap-1">
        <FloatLabel variant="on">
          <DatePicker
            v-model="payDate"
            inputId="payDate"
            dateFormat="yy/mm/dd"
            fluid
            showIcon
            iconDisplay="input"
          />
          <label for="payDate">Data płatności</label>
        </FloatLabel>
        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
          $field.error?.message
        }}</Message>
      </FormField>
    </Form>
  </Panel>
</template>
