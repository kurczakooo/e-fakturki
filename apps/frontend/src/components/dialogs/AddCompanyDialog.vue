<script setup lang="ts">
import { Dialog, Button, InputText, Message, FloatLabel } from "primevue";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";

import { zodResolver } from "@primevue/forms/resolvers/zod";
import { z } from "zod";
import { useToast } from "primevue/usetoast";

import AppLogo from "../AppLogo.vue";
import { reactive } from "vue";

import { createCompany } from "../../lib/services/companyService";
import { createAddress } from "../../lib/services/addressService";

const props = defineProps<{
  user: string;
  visible: boolean;
}>();

const toast = useToast();

const initialValues = reactive({
  name: "",
  nip: "",
  krs: "",
  regon: "",
  street_and_number: "",
  zipcode: "",
  city: "",
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
    krs: z.string().refine((val) => val === "" || /^\d{10}$/.test(val), {
      message: "KRS musi mieć dokładnie 10 cyfr lub pozostać pusty",
    }),
    regon: z.string().refine((val) => val === "" || /^(\d{9}|\d{14})$/.test(val), {
      message: "REGON musi mieć 9 lub 14 cyfr lub pozostać pusty",
    }),
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

const onFormSubmit = async (event: FormSubmitEvent) => {
  const { valid } = event;
  if (!valid) return;

  try {
    const companyResp = await createCompany({
      userId: 1,
      name: event.values.name,
      nip: event.values.nip,
      krs: event.values.krs,
      regon: event.values.regon,
    });

    const addressResp = await createAddress({
      companyId: companyResp.companyId,
      street_and_number: event.values.street_and_number,
      zipcode: event.values.zipcode,
      city: event.values.city,
    });

    toast.add({ severity: "success", summary: "Firma i adres dodane pomyślnie!", life: 3000 });
  } catch (err) {
    toast.add({ severity: "error", summary: "Coś poszło nie tak", life: 3000 });
  }
};

const emit = defineEmits(["update:visible"]);
</script>

<template>
  <Dialog
    :visible="props.visible"
    @update:visible="emit('update:visible', $event)"
    modal
    :closable="false"
    :draggable="false"
    :style="{ width: '30rem' }"
  >
    <template #header>
      <AppLogo />
    </template>
    <span class="block mb-5 font-semibold"> Dodaj firmę użytkownika: {{ props.user }} </span>
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
        <FormField v-slot="$field" name="krs" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="krs_input" type="text" fluid />
            <label for="krs_input">KRS Firmy (Opcjonalnie)</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="regon" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="regon_input" type="text" fluid />
            <label for="regon_input">REGON Firmy (Opcjonalnie)</label>
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
