<script setup lang="ts">
import { Form, FormField } from "@primevue/forms";
import { Panel, InputText, FloatLabel, Message, Select, useToast } from "primevue";
import { reactive, ref, watch } from "vue";
import { useCurrentUserStore } from "../../stores/currentUserStore";
import type { IsoCountries } from "../../lib/types/company";
import { useMutation } from "@tanstack/vue-query";
import { getIsoCountries } from "../../lib/services/companyService";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import z from "zod";

const emit = defineEmits<{
  update: [data: any];
}>();
const props = defineProps<{
  seller: boolean;
}>();
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
  addressCorrespondanceL1: "",
  addressCorrespondanceL2: "",
  email: "",
  phoneNumber: "",
});

function resetInitialValues() {
  initialValues.name = currentUserStore.getCompanyName ?? "";
  initialValues.nip = currentUserStore.getCompanyNip ?? "";
  initialValues.krs = currentUserStore.getCompanyKrs ?? "";
  initialValues.regon = currentUserStore.getCompanyRegon ?? "";
  initialValues.addressL1 = currentUserStore.getCompanyAddressL1 ?? "";
  initialValues.addressL2 = currentUserStore.getCompanyAddressL2 ?? "";
  initialValues.addressCorrespondanceL1 = currentUserStore.getCompanyAddressCorrespondanceL1 ?? "";
  initialValues.addressCorrespondanceL2 = currentUserStore.getCompanyAddressCorrespondanceL2 ?? "";
  initialValues.email = currentUserStore.getCompanyEmail ?? "";
  initialValues.phoneNumber = currentUserStore.getCompanyPhoneNumber ?? "";
}

const resolver = zodResolver(
  z.object({
    name: z
      .string()
      .min(3, { message: "Nazwa musi mieć min. 3 znaki." })
      .max(256, { message: "Nazwa firmy może mieć maksymalnie 256 znaków." }),

    nip: z
      .string()
      .min(1, { message: "NIP jest wymagany." })
      .max(10, { message: "NIP może zawierać maksymalnie 10 cyfr." })
      .refine((val) => /^[1-9]((\d[1-9])|([1-9]\d))\d{7}$/.test(val), {
        message: "NIP musi być poprawny.",
      }),

    krs: z
      .string()
      .refine((val) => val === "" || /^\d{10}$/.test(val), {
        message: "KRS musi mieć dokładnie 10 cyfr lub pozostać pusty",
      })
      .optional(),

    regon: z
      .string()
      .refine((val) => val === "" || /^(\d{14})$/.test(val), {
        message: "REGON musi mieć 14 cyfr lub pozostać pusty",
      })
      .optional(),

    addressL1: z.string().max(512, { message: "Adres przekracza maksymalny rozmiar." }).optional(),

    addressL2: z.string().max(512, { message: "Adres przekracza maksymalny rozmiar." }).optional(),

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
      )
      .optional(),

    phoneNumber: z
      .string()
      .max(16, {
        message: "Numer telefonu może zawierać maksymalnie 16 znaków. (Wpisuj bez spacji)",
      })
      .optional(),

    addressCorrespondanceL2: z
      .string()
      .max(512, {
        message: "Adres przekracza maksymalny rozmiar.",
      })
      .optional(),

    addressCorrespondanceL2: z
      .string()
      .max(512, {
        message: "Adres przekracza maksymalny rozmiar.",
      })
      .optional(),
  }),
);

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

watch(
  () => props.seller,
  async () => {
    await getCountryCodesMutation.mutateAsync();
    if (props.seller) {
      resetInitialValues();
      selectedCountry.value = countries.value.find(
        (c) => c.code === currentUserStore.getCompanyCountryCode,
      );
    }
  },
  { immediate: true },
);
</script>

<template>
  <Panel>
    <template #header>
      <span class="text-xl font-bold">
        {{ props.seller ? "Dane sprzedawcy" : "Dane nabywcy" }}
      </span>
    </template>

    <Form
      :initialValues="initialValues"
      :resolver="resolver"
      class="flex flex-col gap-2 w-full sm:w-100 pb-2"
    >
      <!-- COMPANY NAME -->
      <FormField v-slot="$field" name="name" class="flex flex-col gap-1">
        <FloatLabel variant="on">
          <InputText
            :readonly="props.seller"
            v-bind="$field.props"
            v-model="initialValues.name"
            id="company_name_input"
            type="text"
            fluid
          />
          <label for="company_name_input">Nazwa firmy</label>
        </FloatLabel>

        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- NIP -->
      <FormField v-slot="$field" name="nip" class="flex flex-col gap-1">
        <FloatLabel variant="on">
          <InputText
            :readonly="props.seller"
            v-bind="$field.props"
            v-model="initialValues.nip"
            id="company_nip_input"
            type="text"
            fluid
          />
          <label for="company_nip_input">NIP firmy</label>
        </FloatLabel>

        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- KRS -->
      <FormField v-slot="$field" name="krs" class="flex flex-col gap-1">
        <FloatLabel variant="on">
          <InputText
            :readonly="props.seller"
            v-bind="$field.props"
            v-model="initialValues.krs"
            id="company_krs_input"
            type="text"
            fluid
          />
          <label for="company_krs_input"> KRS firmy (Opcjonalnie) </label>
        </FloatLabel>

        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- REGON -->
      <FormField v-slot="$field" name="regon" class="flex flex-col gap-1">
        <FloatLabel variant="on">
          <InputText
            :readonly="props.seller"
            v-bind="$field.props"
            v-model="initialValues.regon"
            id="company_regon_input"
            type="text"
            fluid
          />
          <label for="company_regon_input"> REGON firmy (Opcjonalnie) </label>
        </FloatLabel>

        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
          {{ $field.error?.message }}
        </Message>
      </FormField>

      <!-- ADDRESS -->
      <Panel :header="props.seller ? 'Adres sprzedawcy' : 'Adres nabywcy'" toggleable collapsed>
        <div class="flex flex-col gap-2">
          <Select
            :disabled="props.seller"
            v-model="selectedCountry"
            :options="countries"
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
                  :alt="slotProps.option.name"
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
              <InputText
                :readonly="props.seller"
                v-bind="$field.props"
                v-model="initialValues.addressL1"
                id="address_l1_input"
                type="text"
                fluid
              />
              <label for="address_l1_input"> Adres linia 1 (Opcjonalnie) </label>
            </FloatLabel>

            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
              {{ $field.error?.message }}
            </Message>
          </FormField>

          <FormField v-slot="$field" name="addressL2" class="flex flex-col gap-1">
            <FloatLabel variant="on">
              <InputText
                :readonly="props.seller"
                v-bind="$field.props"
                v-model="initialValues.addressL2"
                id="address_l2_input"
                type="text"
                fluid
              />
              <label for="address_l2_input"> Adres linia 2 (Opcjonalnie) </label>
            </FloatLabel>

            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
              {{ $field.error?.message }}
            </Message>
          </FormField>
        </div>
      </Panel>

      <!-- CONTACT -->
      <Panel :header="props.seller ? 'Kontakt sprzedawcy' : 'Kontakt nabywcy'" toggleable collapsed>
        <div class="flex flex-col gap-2">
          <FormField v-slot="$field" name="email" class="flex flex-col gap-1">
            <FloatLabel variant="on">
              <InputText
                :readonly="props.seller"
                v-bind="$field.props"
                v-model="initialValues.email"
                id="company_email_input"
                type="text"
                fluid
              />
              <label for="company_email_input"> E-mail (Opcjonalnie) </label>
            </FloatLabel>

            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
              {{ $field.error?.message }}
            </Message>
          </FormField>

          <FormField v-slot="$field" name="phoneNumber" class="flex flex-col gap-1">
            <FloatLabel variant="on">
              <InputText
                :readonly="props.seller"
                v-bind="$field.props"
                v-model="initialValues.phoneNumber"
                id="company_phone_input"
                type="text"
                fluid
              />
              <label for="company_phone_input"> Telefon (Opcjonalnie) </label>
            </FloatLabel>

            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
              {{ $field.error?.message }}
            </Message>
          </FormField>

          <FormField v-slot="$field" name="addressCorrespondanceL1" class="flex flex-col gap-1">
            <FloatLabel variant="on">
              <InputText
                :readonly="props.seller"
                v-bind="$field.props"
                v-model="initialValues.addressCorrespondanceL1"
                id="correspondence_address_l1_input"
                type="text"
                fluid
              />
              <label for="correspondence_address_l1_input">
                Adres korespondencyjny linia 1 (Opcjonalnie)
              </label>
            </FloatLabel>

            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
              {{ $field.error?.message }}
            </Message>
          </FormField>

          <FormField v-slot="$field" name="addressCorrespondanceL2" class="flex flex-col gap-1">
            <FloatLabel variant="on">
              <InputText
                :readonly="props.seller"
                v-bind="$field.props"
                v-model="initialValues.addressCorrespondanceL2"
                id="correspondence_address_l2_input"
                type="text"
                fluid
              />
              <label for="correspondence_address_l2_input">
                Adres korespondencyjny linia 2 (Opcjonalnie)
              </label>
            </FloatLabel>

            <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">
              {{ $field.error?.message }}
            </Message>
          </FormField>
        </div>
      </Panel>
    </Form>
  </Panel>
</template>
