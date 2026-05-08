<script setup lang="ts">
import { useToast } from "primevue";
import { Message, FloatLabel, InputText, Dialog, Button, Select } from "primevue";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";

import { useCurrentUserStore } from "../../stores/currentUserStore";
import { reactive, ref, watch } from "vue";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { useMutation } from "@tanstack/vue-query";
import { updateCompany, getIsoCountries, createCompany } from "../../lib/services/companyService";
import z from "zod";
import type {
  CompanyDetails,
  CompanyListItem,
  CreateOrUpdate,
  IsoCountries,
} from "../../lib/types/company";

const props = withDefaults(
  defineProps<{
    visible: boolean;
    createOrUpdate: CreateOrUpdate;
    userCompany: boolean;
    companyBrief: CompanyListItem | null;
    companyDetails: CompanyDetails | null;
    loading?: boolean;
  }>(),
  {
    companyBrief: null,
    companyDetails: null,
  },
);
const emit = defineEmits(["update:visible", "success", "cancel"]);
const toast = useToast();
const currentUserStore = useCurrentUserStore();
const countries = ref<IsoCountries[]>([]);
const selectedCountry = ref<IsoCountries>();
const dialogClosable = !(props.userCompany && props.createOrUpdate === "create");

const initialValues = reactive({
  name: "",
  nip: "",
  krs: "",
  regon: "",
  addressL1: "",
  addressL2: "",
  addressCorrespondanceL1: "",
  addressCorrespondanceL2: "",
  email: "",
  phoneNumber: "",
  additionalInfo: "",
});

function resetInitialValues() {
  initialValues.name = props.companyBrief?.name ?? "";
  initialValues.nip = props.companyBrief?.nip ?? "";
  initialValues.krs = props.companyDetails?.krs ?? "";
  initialValues.regon = props.companyDetails?.regon ?? "";
  initialValues.addressL1 = props.companyBrief?.address_l1 ?? "";
  initialValues.addressL2 = props.companyBrief?.address_l2 ?? "";
  initialValues.addressCorrespondanceL1 = props.companyDetails?.address_correspondance_l1 ?? "";
  initialValues.addressCorrespondanceL2 = props.companyDetails?.address_correspondance_l2 ?? "";
  initialValues.email = props.companyBrief?.email ?? "";
  initialValues.phoneNumber = props.companyBrief?.phone_number ?? "";
  initialValues.additionalInfo = props.companyDetails?.additional_info ?? "";
}

watch(
  [() => props.companyBrief, () => props.companyDetails],
  () => {
    if (props.createOrUpdate === "update") resetInitialValues();
  },
  { immediate: true },
);

const resolver = zodResolver(
  z.object({
    name: z
      .string()
      .min(1, { message: "Nazwa firmy jest wymagana." })
      .min(3, { message: "Nazwa musi mieć min. 3 znaki." }),
    nip: z
      .string()
      .min(1, { message: "NIP jest wymagany." })
      .max(10, { message: "NIP może zawierać maksymalnie 10 cyfr." })
      .refine((val) => /^[1-9]((\d[1-9])|([1-9]\d))\d{7}$/.test(val), {
        message: "NIP musi być poprawny.",
      }),
    krs: z.string().refine((val) => val === "" || /^\d{10}$/.test(val), {
      message: "KRS musi mieć dokładnie 10 cyfr lub pozostać pusty",
    }),
    regon: z.string().refine((val) => val === "" || /^(\d{14})$/.test(val), {
      message: "REGON musi mieć 14 cyfr lub pozostać pusty",
    }),
    addressL1: z.string().max(512, { message: "Adres przekracza maksymalny rozmiar." }),
    addressL2: z.string().max(512, { message: "Adres przekracza maksymalny rozmiar." }),
    addressCorrespondanceL1: z
      .string()
      .max(512, { message: "Adres przekracza maksymalny rozmiar." }),
    addressCorrespondanceL2: z
      .string()
      .max(512, { message: "Adres przekracza maksymalny rozmiar." }),
    email: z
      .string()
      .refine(
        (val) =>
          val === "" ||
          /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/.test(
            val,
          ),
        {
          message: "Wpisz poprawny e-mail lub pozostaw puste pole.",
        },
      ),
    phoneNumber: z.string().max(16, {
      message: "Numer telefonu może zawierać maksymalnie 16 znaków. (Wpisuj bez spacji)",
    }),
    additionalInfo: z
      .string()
      .max(2048, { message: "Informacja dodatkowa przekracza maksymalny rozmiar." }),
  }),
);

const createCompanyMutation = useMutation({
  mutationFn: async (values: any) => {
    const companyResp = await createCompany({
      owner_id: props.userCompany ? currentUserStore.getUserId : null,
      name: values.name,
      nip: values.nip,
      krs: values.krs ?? null,
      regon: values.regon ?? null,
      country_code: selectedCountry.value?.code,
      address_l1: values.addressL1 ?? null,
      address_l2: values.addressL2 ?? null,
      address_correspondance_l1: values.addressCorrespondanceL1 ?? null,
      address_correspondance_l2: values.addressCorrespondanceL2 ?? null,
      email: values.email ?? null,
      phone_number: values.phoneNumber ?? null,
      additional_info: values.additionalInfo ?? null,
    });

    return companyResp;
  },

  onSuccess: (data, variables) => {
    if (props.userCompany && props.createOrUpdate === "create") {
      currentUserStore.setCompanyData(
        data.company_id,
        variables.name,
        variables.nip,
        selectedCountry.value?.code,
        variables.address_l1,
        variables.address_l2,
        variables.email,
        variables.phone_number,
        false,
      );
    }
    toast.add({ severity: "success", summary: "Firma dodana pomyślnie!", life: 3000 });
    emit("success");
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 5000 });
  },
});

const updateCompanyMutation = useMutation({
  mutationFn: async (values: any) => {
    const companyResp = await updateCompany({
      id: props.companyBrief?.id,
      name: values.name,
      nip: values.nip,
      krs: values.krs ?? null,
      regon: values.regon ?? null,
      country_code: selectedCountry.value?.code,
      address_l1: values.addressL1 ?? null,
      address_l2: values.addressL2 ?? null,
      address_correspondance_l1: values.addressCorrespondanceL1 ?? null,
      address_correspondance_l2: values.addressCorrespondanceL2 ?? null,
      email: values.email ?? null,
      phone_number: values.phoneNumber ?? null,
      additional_info: values.additionalInfo ?? null,
    });

    return companyResp;
  },

  onSuccess: (data, variables) => {
    if (props.userCompany && props.createOrUpdate === "update") {
      currentUserStore.setCompanyData(
        data,
        variables.name,
        variables.nip,
        variables.country_code,
        variables.address_l1,
        variables.address_l2,
        variables.email,
        variables.phone_number,
        true,
      );
    }
    toast.add({
      severity: "success",
      summary: "Dane firmy zaaktualizowane pomyślnie!",
      life: 3000,
    });
    emit("success");
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 5000 });
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
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 5000 });
  },
});

const onFormSubmit = async (event: FormSubmitEvent) => {
  const { valid } = event;
  if (!valid) return;

  if (props.createOrUpdate === "update") updateCompanyMutation.mutate(event.values);
  if (props.createOrUpdate === "create") createCompanyMutation.mutate(event.values);
};

watch(
  () => props.visible,
  async (visible) => {
    if (visible) {
      await getCountryCodesMutation.mutateAsync();
      if (props.createOrUpdate === "update") {
        selectedCountry.value = countries.value.find(
          (c) => c.code === props.companyBrief?.country_code,
        );
      } else {
        selectedCountry.value = countries.value.find((c) => c.code === "PL");
      }
    }
  },
);
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="emit('update:visible', $event)"
    :closable="dialogClosable"
    modal
    :draggable="false"
    :style="{ width: '40rem' }"
  >
    <template #header>
      <div v-if="props.createOrUpdate === 'update'" class="flex flex-col text-xl font-semibold">
        <span v-if="userCompany">
          Edytuj dane firmy użytkownika {{ currentUserStore.getFullName }}:
        </span>
        <span v-else> Edytuj dane firmy: </span>
        <span class="font-semibold text-xl">
          {{ initialValues.name }}
        </span>
      </div>
      <div v-if="props.createOrUpdate === 'create'" class="flex flex-col text-xl font-semibold">
        <span v-if="userCompany">
          Dodaj firmę użytkownika: {{ currentUserStore.getFullName }}
        </span>
        <span v-else> Dodaj nową firmę </span>
      </div>
    </template>
    <span v-if="props.createOrUpdate === 'create'" class="flex pb-4"
      >Pola opcjonalne i dodatkowe informacje o firmie można zmienić później.</span
    >
    <div class="card flex justify-center pt-2">
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
            <FormField v-slot="$field" name="email" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="email_input" type="text" fluid />
                <label for="email_input">E-mail (Opcjonalnie)</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="phoneNumber" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="phoneNumber_input" type="text" fluid />
                <label for="phoneNumber_input">Telefon (Opcjonalnie)</label>
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
              :disabled="userCompany"
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
            <FormField v-slot="$field" name="addressCorrespondanceL1" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText
                  v-bind="$field.props"
                  id="addressCorrespondanceL1_input"
                  type="text"
                  fluid
                />
                <label for="addressCorrespondanceL1_input"
                  >Adres korespondencyjny linia 1 (Opcjonalnie)</label
                >
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="addressCorrespondanceL2" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText
                  v-bind="$field.props"
                  id="addressCorrespondanceL1_input"
                  type="text"
                  fluid
                />
                <label for="addressCorrespondanceL1_input"
                  >Adres korespondencyjny linia 2 (Opcjonalnie)</label
                >
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="additionalInfo" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="additionalInfo_input" type="text" fluid />
                <label for="additionalInfo_input">Dodatkowe informacje (Opcjonalnie)</label>
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
          :label="props.createOrUpdate === 'update' ? 'Zmień dane firmy' : 'Dodaj firmę'"
          :loading="updateCompanyMutation.isPending.value || createCompanyMutation.isPending.value"
          :disabled="updateCompanyMutation.isPending.value || createCompanyMutation.isPending.value"
          class="sm:w-100"
        />
      </Form>
    </div>
  </Dialog>
</template>
