<script setup lang="ts">
import { Dialog, Button, InputText, Message, FloatLabel } from "primevue";
import { Form, FormField } from "@primevue/forms";

import { zodResolver } from "@primevue/forms/resolvers/zod";
import { z } from "zod";
import { useToast } from "primevue/usetoast";

import AppLogo from "../AppLogo.vue";
import { reactive } from "vue";

const toast = useToast();

const initialValues = reactive({
  details: "",
});

const resolver = zodResolver(
  z.object({
    name: z
      .string()
      .min(1, { message: "Nazwa firmy jest wymagana." })
      .min(3, { message: "Nazwa musi mieć min. 3 znaki." }),

    nip: z
      .string()
      .min(1, { message: "NIP jest wymagany." })
      .regex(/^\d{10}$/, { message: "NIP musi mieć dokładnie 10 cyfr." }),

    street_and_number: z
      .string()
      .min(1, { message: "Adres jest wymagany." })
      .min(5, { message: "Podaj pełny adres (ulica i numer)." }),

    zipcode: z
      .string()
      .min(1, { message: "Kod pocztowy jest wymagany." })
      .regex(/^\d{2}-\d{3}$/, {
        message: "Kod pocztowy musi być w formacie XX-XXX.",
      }),

    city: z
      .string()
      .min(1, { message: "Miasto jest wymagane." })
      .min(2, { message: "Miasto musi mieć min. 2 znaki." }),
  }),
);

const onFormSubmit = ({ valid }) => {
  if (valid) {
    toast.add({ severity: "success", summary: "Form is submitted.", life: 3000 });
  }
};

const emit = defineEmits(["update:visible"]);
</script>

<template>
  <Dialog
    :visible="true"
    @update:visible="emit('update:visible', $event)"
    modal
    :draggable="false"
    :style="{ width: '40%' }"
  >
    <template #header>
      <AppLogo />
    </template>
    <span class="block mb-8">{{ "Dodaj firmę do użytkownika: Łukasz Kowalski" }}</span>
    <div class="card flex justify-center">
      <Form
        :initialValues
        :resolver
        @submit="onFormSubmit"
        class="flex flex-col gap-4 w-full sm:w-80"
      >
        <FormField v-slot="$field" name="name" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="name_input" type="text" fluid />
            <label for="name_input">Nazwa firmy</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="nip" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="nip_input" type="text" fluid />
            <label for="nip_input">NIP Firmy</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="street_and_number" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="street_and_number_input" type="text" fluid />
            <label for="street_and_number_input">Ulica i nr</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="zipcode" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText
              v-bind="$field.props"
              id="zipcode_input"
              type="text"
              :feedback="false"
              fluid
            />
            <label for="zipcode_input">Kod pocztowy</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="city" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="city_input" type="text" :feedback="false" fluid />
            <label for="city_input">Miasto</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <Button type="submit" severity="secondary" label="Dodaj firmę" />
      </Form>
    </div>
  </Dialog>
</template>
