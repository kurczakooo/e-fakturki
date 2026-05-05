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
import { useCurrentUserStore } from "../../stores/currentUserStore";

const toast = useToast();
const currentUserStore = useCurrentUserStore();
const userName = computed(() => currentUserStore.getFullName);
const initialValues = reactive({
  name: "",
  nip: "",
  krs: "",
  regon: "",
  addressL1: "",
  addressL2: "",
  email: "",
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
    addressL1: z.string(),
    addressL2: z.string(),
    email: z.string(),
  }),
);

const createCompanyMutation = useMutation({
  mutationFn: async (values: any) => {
    const companyResp = await createCompany({
      owner_id: currentUserStore.getUserId,
      name: values.name,
      nip: values.nip,
      krs: values.krs == "" ? null : values.krs,
      regon: values.regon == "" ? null : values.regon,
      country_code: "PL",
      address_l1: values.addressL1 == "" ? null : values.addressL1,
      address_l2: values.addressL2 == "" ? null : values.addressL2,
      address_correspondance_l1: null,
      address_correspondance_l2: null,
      email: values.email == "" ? null : values.email,
      phone_number: null,
      additional_info: null,
    });

    return companyResp;
  },

  onSuccess: (data, variables) => {
    toast.add({ severity: "success", summary: "Firma dodana pomyślnie!", life: 3000 });
    currentUserStore.setCompanyData(
      data.company_id,
      variables.name,
      variables.nip,
      variables.country_code,
      variables.address_l1,
      variables.address_l2,
      variables.email,
      variables.phone_number,
      false,
    );
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 3000 });
  },
});

const onFormSubmit = async (event: FormSubmitEvent) => {
  const { valid } = event;
  if (!valid) return;

  createCompanyMutation.mutate(event.values);
};
</script>

<template>
  <Dialog modal :closable="false" :draggable="false" :style="{ width: '40rem' }">
    <template #header>
      <AppLogo />
    </template>
    <span class="block mb-2 font-semibold"> Dodaj firmę użytkownika: {{ userName }} </span>
    <span class="block mb-5 text-sm text-gray-500"
      >Pola opcjonalne i dodatkowe informacje o firmie można zmienić później.</span
    >
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
            <FormField v-slot="$field" name="addressL1" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="addresL1_input" type="text" fluid />
                <label for="addresL1_input">Adres linia 1 (Opcjonalnie)</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="addressL2" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="addresL2_input" type="text" fluid />
                <label for="addresL2_input">Adres linia 2 (Opcjonalnie)</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="email" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="email_input" type="text" fluid />
                <label for="email_input">E-mail (Opcjonalnie)</label>
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
          :loading="createCompanyMutation.isPending.value"
          :disabled="createCompanyMutation.isPending.value"
          class="sm:w-100"
        />
      </Form>
    </div>
  </Dialog>
</template>
