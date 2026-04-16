<script setup lang="ts">
import { Dialog, Button, InputText, Message, FloatLabel } from "primevue";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { useMutation } from "@tanstack/vue-query";
import { useToast } from "primevue/usetoast";
import { computed, reactive } from "vue";
import { z } from "zod";

import AppLogo from "../AppLogo.vue";
import { createCompany } from "../../lib/services/companyService";
import { createAddress } from "../../lib/services/addressService";
import { useCurrentUserStore } from "../../stores/currentUserStore";

const toast = useToast();
const currentUserStore = useCurrentUserStore();

const initialValues = reactive({
  name: "",
  nip: "",
  krs: "",
  regon: "",
  street: "",
  number: "",
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
    street: z.string().min(4, { message: "Ulica jest wymagana." }),
    number: z
      .string()
      .min(1, { message: "Numer jest wymagany." })
      .max(10, { message: "Numer może mieć maksymalnie 10 znaków." })
      .regex(/^[0-9A-Za-z\/]+$/, {
        message: "Numer może zawierać tylko cyfry, litery i znak '/'.",
      }),
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

const createCompanyWithAddressMutation = useMutation({
  mutationFn: async (values: any) => {
    const companyResp = await createCompany({
      user_id: currentUserStore.getUserId,
      name: values.name,
      nip: values.nip,
      krs: values.krs == "" ? null : values.krs,
      regon: values.regon == "" ? null : values.regon,
    });

    const addressResp = await createAddress({
      company_id: companyResp.company_id,
      type: "registered",
      country: "Poland",
      city: values.city,
      postal_code: values.zipcode,
      street: values.street,
      building_number: values.number,
    });
    return { companyResp, addressResp };
  },

  onSuccess: (data, variables) => {
    toast.add({ severity: "success", summary: "Firma i adres dodane pomyślnie!", life: 3000 });
    currentUserStore.setCompanyData(data.companyResp.company_id, variables.name, false);
  },

  onError: () => {
    toast.add({ severity: "error", summary: "Coś poszło nie tak", life: 3000 });
  },
});

const onFormSubmit = async (event: FormSubmitEvent) => {
  const { valid } = event;
  if (!valid) return;

  createCompanyWithAddressMutation.mutate(event.values);
};

const userName = computed(() => currentUserStore.getFullName);
</script>

<template>
  <Dialog :visible="true" modal :closable="false" :draggable="false" :style="{ width: '40rem' }">
    <template #header>
      <AppLogo />
    </template>
    <span class="block mb-5 font-semibold"> Dodaj firmę użytkownika: {{ userName }} </span>
    <div class="card flex justify-center">
      <Form
        :initialValues
        :resolver
        @submit="onFormSubmit"
        class="flex flex-col gap-4 w-full items-center sm:w-150"
      >
        <div class="flex gap-4 w-full">
          <div class="flex flex-col gap-4 w-full">
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
          </div>
          <div class="flex flex-col gap-4 w-full">
            <FormField v-slot="$field" name="street" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="street_input" type="text" fluid />
                <label for="street_input">Ulica</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="number" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="building_number_input" type="text" fluid />
                <label for="building_number_input">Numer budynku</label>
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
                <InputText
                  v-bind="$field.props"
                  id="city_input"
                  type="text"
                  :feedback="false"
                  fluid
                />
                <label for="city_input">Miasto</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
          </div>
        </div>
        <Button
          type="submit"
          severity="secondary"
          label="Dodaj firmę"
          :loading="createCompanyWithAddressMutation.isPending.value"
          :disabled="createCompanyWithAddressMutation.isPending.value"
          class="sm:w-100"
        />
      </Form>
    </div>
  </Dialog>
</template>
