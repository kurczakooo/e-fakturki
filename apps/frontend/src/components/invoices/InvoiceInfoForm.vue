<script setup lang="ts">
import { Form, FormField } from "@primevue/forms";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { Panel, InputText, FloatLabel, Message, DatePicker } from "primevue";
import { reactive, watch } from "vue";
import z from "zod";

const emit = defineEmits<{
  update: [
    {
      invoiceNumber: string;
      issuePlace: string;
      invoiceDate: Date | null;
    },
  ];
}>();

const initialValues = reactive({
  invoiceNumber: "",
  issuePlace: "",
  invoiceDate: new Date() as Date | null,
});

const resolver = zodResolver(
  z.object({
    invoiceNumber: z
      .string()
      .min(1, { message: "Numer faktury jest wymagany." })
      .max(256, { message: "Numer faktury może mieć maksymalnie 256 znaków." }),

    issuePlace: z.string().min(1, { message: "Miejsce wystawienia jest wymagane." }).max(256, {
      message: "Miejsce wystawienia może mieć maksymalnie 256 znaków.",
    }),
  }),
);

watch(
  initialValues,
  () => {
    emit("update", {
      invoiceNumber: initialValues.invoiceNumber,
      issuePlace: initialValues.issuePlace,
      invoiceDate: initialValues.invoiceDate,
    });
  },
  { deep: true },
);
</script>

<template>
  <Panel class="flex flex-1">
    <template #header>
      <span class="text-xl font-bold">Dane Faktury</span>
    </template>

    <Form :initialValues="initialValues" :resolver="resolver" class="flex flex-1 gap-2">
      <!-- invoice number -->
      <FormField v-slot="$field" name="invoiceNumber">
        <FloatLabel variant="on">
          <InputText
            v-bind="$field.props"
            v-model="initialValues.invoiceNumber"
            id="invoiceNumber_input"
            type="text"
            fluid
          />
          <label for="invoiceNumber_input">Numer Faktury</label>
        </FloatLabel>

        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- invoice date -->
      <FormField v-slot="$field" name="invoiceDate">
        <FloatLabel variant="on">
          <DatePicker
            v-model="initialValues.invoiceDate"
            inputId="invoiceDate"
            dateFormat="yy/mm/dd"
            fluid
            iconDisplay="input"
          />
          <label for="invoiceDate">Data wystawienia</label>
        </FloatLabel>
      </FormField>

      <!-- issue place -->
      <FormField v-slot="$field" name="issuePlace">
        <FloatLabel variant="on">
          <InputText
            v-bind="$field.props"
            v-model="initialValues.issuePlace"
            id="issuePlace_input"
            type="text"
            fluid
          />
          <label for="issuePlace_input">Miejsce wystawienia</label>
        </FloatLabel>

        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>
    </Form>
  </Panel>
</template>
