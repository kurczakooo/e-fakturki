<script setup lang="ts">
import { useToast } from "primevue";
import { Message, FloatLabel, InputText, Dialog, Button, Select } from "primevue";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";

import { useCurrentUserStore } from "../../stores/currentUserStore";
import { reactive, ref, watch } from "vue";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { useMutation } from "@tanstack/vue-query";
import z from "zod";
import type { CreateOrUpdate } from "../../lib/types/company";
import type { CategoryListItem, ProductListItem } from "../../lib/types/products";
import {
  createProduct,
  getCategoriesByCompanyId,
  updateProduct,
} from "../../lib/services/productService";

const props = withDefaults(
  defineProps<{
    visible: boolean;
    createOrUpdate: CreateOrUpdate;
    productInfo: ProductListItem | null;
    loading?: boolean;
  }>(),
  {
    productInfo: null,
  },
);
const emit = defineEmits(["update:visible", "success", "cancel"]);
const toast = useToast();
const currentUserStore = useCurrentUserStore();
const categories = ref<CategoryListItem[]>([]);
const selectedCategory = ref<CategoryListItem | null>(null);

const initialValues = reactive({
  name: props.productInfo?.name ?? "",
  category: props.productInfo?.category ?? "",
  categoryId: props.productInfo?.categoryId ?? null,
  description: props.productInfo?.description ?? "",
  gtin: props.productInfo?.gtin ?? "",
  unit: props.productInfo?.unit ?? "",
  netPrice: props.productInfo?.net_price ?? null,
  taxRate: props.productInfo?.tax_rate ?? null,
  grossPrice: props.productInfo?.gross_price ?? null,
});
// const initialValues = reactive({
//   name: "",
//   category: "",
//   categoryId: null,
//   description: "",
//   gtin: "",
//   unit: "",
//   net_price: null,
//   tax_rate: null,
//   gross_price: null,
// });

// function resetInitialValues() {
//   initialValues.name = props.productInfo?.name ?? "";
//   initialValues.category = props.productInfo?.category ?? "";
//   initialValues.categoryId = props.productInfo?.categoryId ?? "";
//   initialValues.description = props.productInfo?.description ?? "";
//   initialValues.gtin = props.productInfo?.gtin ?? "";
//   initialValues.unit = props.productInfo?.unit ?? "";
//   initialValues.net_price = props.productInfo?.net_price ?? null;
//   initialValues.tax_rate = props.productInfo?.tax_rate ?? null;
//   initialValues.gross_price = props.productInfo?.gross_price ?? null;
// }

// watch(
//   () => props.productInfo,
//   () => {
//     if (props.createOrUpdate === "update") resetInitialValues();
//   },
//   { immediate: true },
// );

const resolver = zodResolver(
  z.object({
    name: z.string().min(1, { message: "Nazwa produktu jest wymagana." }),
    description: z.string().max(2048, { message: "Opis przekracza maksymalny rozmiar." }),
    gtin: z.string().max(20, { message: "GTIN może zawierać maksymalnie 20 cyfr." }),
    unit: z
      .string()
      .min(1, { message: "Jednostka miary jest wymagana." })
      .refine((val) => val === "" || /^[a-z0-9. ]{1,256}$/.test(val), {
        message: "Jednostka miary musi zawierać wyłącznie małe litery, cyfry, spacje i kropki.",
      })
      .min(1, { message: "Jednostka miary jest wymagana." }),
    netPrice: z.number().min(0, { message: "Cena netto musi być nieujemna." }),
    taxRate: z.number().min(0, { message: "Stawka VAT musi być nieujemna." }),
    grossPrice: z.number().min(0, { message: "Cena brutto musi być nieujemna." }),
  }),
);

const createProductMutation = useMutation({
  mutationFn: async (values: any) => {
    const productResp = await createProduct({
      name: values.name,
      description: values.description,
      gtin: values.gtin,
      unit: values.unit,
      net_price: values.netPrice,
      tax_rate: values.taxRate,
      gross_price: values.grossPrice,
      category_id: selectedCategory.value?.id,
    });

    return productResp;
  },

  onSuccess: () => {
    toast.add({ severity: "success", summary: "Produkt dodany pomyślnie!", life: 3000 });
    emit("success");
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 5000 });
  },
});

const updateProductMutation = useMutation({
  mutationFn: async (values: any) => {
    const productResp = await updateProduct({
      product_id: props.productInfo?.id,
      name: values.name,
      description: values.description,
      gtin: values.gtin,
      unit: values.unit,
      net_price: values.netPrice,
      tax_rate: values.taxRate,
      gross_price: values.grossPrice,
      category_id: selectedCategory.value?.id,
    });

    return productResp;
  },

  onSuccess: () => {
    toast.add({
      severity: "success",
      summary: "Produkt zaaktualizowany pomyślnie!",
      life: 3000,
    });
    emit("success");
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 5000 });
  },
});

const getCategoriesMutation = useMutation({
  mutationFn: async () => {
    return await getCategoriesByCompanyId(currentUserStore.getCompanyId);
  },

  onSuccess: (data) => {
    categories.value = data;
  },

  onError: (error) => {
    toast.add({ severity: "error", summary: error.response?.data?.detail, life: 5000 });
  },
});

const onFormSubmit = async (event: FormSubmitEvent) => {
  const { valid } = event;
  if (!valid) return;

  if (props.createOrUpdate === "update") updateProductMutation.mutate(event.values);
  if (props.createOrUpdate === "create") createProductMutation.mutate(event.values);
};

watch(
  () => props.visible,
  async (visible) => {
    if (visible) {
      await getCategoriesMutation.mutateAsync();
      if (props.createOrUpdate === "update") {
        selectedCategory.value = categories.value.find(
          (c) => c.name === props.productInfo?.category,
        );
      } else {
        selectedCategory.value = null;
      }
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
    :style="{ width: '40rem' }"
  >
    <template #header>
      <div v-if="props.createOrUpdate === 'update'" class="flex flex-col text-xl font-semibold">
        <span> Edytuj dane produktu firmy {{ currentUserStore.getCompanyName }}: </span>
      </div>
      <div v-if="props.createOrUpdate === 'create'" class="flex flex-col text-xl font-semibold">
        <span> Dodaj nowy produkt dla firmy: {{ currentUserStore.getCompanyName }} </span>
      </div>
    </template>
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
                <label for="name_input">Nazwa produktu</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <Select
              v-model="selectedCategory"
              :options="categories"
              optionLabel="name"
              placeholder="Kategoria"
              fluid
            >
              <template #value="slotProps">
                <div v-if="slotProps.value" class="flex items-center gap-2">
                  <div>{{ slotProps.value.name }}</div>
                </div>
                <span v-else>
                  {{ slotProps.placeholder }}
                </span>
              </template>
              <template #option="slotProps">
                <div class="flex items-center gap-2">
                  <div>{{ slotProps.option.name }}</div>
                </div>
              </template>
              <template #dropdownicon>
                <i class="pi pi-folder" />
              </template>
            </Select>
            <FormField v-slot="$field" name="gtin" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="gtin_input" type="text" fluid />
                <label for="gtin_input">GTIN (Opcjonalnie)</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="description" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="description_input" type="text" fluid />
                <label for="description_input">Opis produktu (Opcjonalnie)</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
          </div>
          <div class="flex flex-col gap-4 w-full">
            <FormField v-slot="$field" name="unit" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="unit_input" type="text" fluid />
                <label for="unit_input">Jednostka miary</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="netPrice" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="netPrice_input" type="text" fluid />
                <label for="netPrice_input">Cena netto</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="taxRate" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="taxRate_input" type="text" fluid />
                <label for="taxRate_input">Stawka VAT</label>
              </FloatLabel>
              <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
                $field.error?.message
              }}</Message>
            </FormField>
            <FormField v-slot="$field" name="grossPrice" class="flex flex-col gap-1">
              <FloatLabel variant="on">
                <InputText v-bind="$field.props" id="grossPrice_input" type="text" fluid />
                <label for="grossPrice_input">Cena brutto</label>
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
          :label="props.createOrUpdate === 'update' ? 'Zmień dane produktu' : 'Dodaj produkt'"
          :loading="updateProductMutation.isPending.value || createProductMutation.isPending.value"
          :disabled="updateProductMutation.isPending.value || createProductMutation.isPending.value"
          class="sm:w-100"
        />
      </Form>
    </div>
  </Dialog>
</template>
