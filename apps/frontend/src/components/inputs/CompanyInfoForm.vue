<script setup lang="ts">
import { useToast } from "primevue";
import { Message, FloatLabel, InputText, Dialog, Button, Select } from "primevue";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";

import { useCurrentUserStore } from "../../stores/currentUserStore";
import { reactive, ref, watch } from "vue";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { useMutation } from "@tanstack/vue-query";
import { createCompany, getIsoCountries } from "../../lib/services/companyService";
import z from "zod";
import type { IsoCountries } from "../../lib/types/company";

const props = defineProps<{
  visible: boolean;
  userCompany: boolean;
  loading?: boolean;
}>();
const emit = defineEmits(["update:visible", "success", "cancel"]);
const toast = useToast();
const currentUserStore = useCurrentUserStore();
const countries = ref<IsoCountries[]>([]);
const selectedCountry = ref<IsoCountries>();

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
      owner_id: props.userCompany ? currentUserStore.getUserId : null,
      name: values.name,
      nip: values.nip,
      krs: values.krs == "" ? null : values.krs,
      regon: values.regon == "" ? null : values.regon,
      country_code: selectedCountry.value?.code,
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
    emit("success");
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 3000 });
  },
});

const getCountryCodesMutation = useMutation({
  mutationFn: async () => {
    return await getIsoCountries();
  },

  onSuccess: (data) => {
    countries.value = data;
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

const getHeader = () => {
  if (props.userCompany) {
    return "Dodaj firmę użytkownika: " + currentUserStore.getFullName;
  } else {
    return "Dodaj nową firmę";
  }
};

watch(
  () => props.visible,
  async (visible) => {
    if (visible) {
      await getCountryCodesMutation.mutateAsync();
      selectedCountry.value = countries.value.find((c) => c.code === "PL");
    }
  },
);
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="emit('update:visible', $event)"
    modal
    :draggable="false"
    :header="getHeader()"
    :style="{ width: '40rem' }"
  >
    <span class="flex pb-4"
      >Pola opcjonalne i dodatkowe informacje o firmie można zmienić później.</span
    >
    <div class="card flex justify-center">
      <Form
        :initialValues="initialValues"
        :resolver="resolver"
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
            <Select
              v-model="selectedCountry"
              :options="countries"
              :disabled="userCompany || getCountryCodesMutation.isPending.value"
              optionLabel="name"
              placeholder="Kraj"
              fluid
            >
              <template #value="slotProps">
                <div v-if="slotProps.value" class="flex items-center gap-2">
                  <img
                    :alt="slotProps.value.name"
                    :src="`https://flagcdn.com/${slotProps.value.code?.toLowerCase()}.svg`"
                    style="width: 24px"
                    loading="lazy"
                  />
                  <div>{{ slotProps.value.name }}</div>
                </div>
                <span v-else>
                  {{ slotProps.placeholder }}
                </span>
              </template>
              <template #option="slotProps">
                <div class="flex items-center gap-2">
                  <img
                    :alt="slotProps.option.label"
                    :src="`https://flagcdn.com/${slotProps.option.code?.toLowerCase()}.svg`"
                    style="width: 24px"
                    loading="lazy"
                  />
                  <div>{{ slotProps.option.name }}</div>
                </div>
              </template>
              <template #dropdownicon>
                <i class="pi pi-map" />
              </template>
            </Select>
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
