<script setup lang="ts">
import { Dialog, Button, InputText, Message, Password, FloatLabel } from "primevue";
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
    details: z.string().min(1, { message: "Details is required via Form Resolver." }),
  }),
);

const zodUserNameResolver = zodResolver(z.string().min(1, { message: "Username is required." }));
const zodFirstNameResolver = zodResolver(z.string().min(1, { message: "Name is required." }));
const zodNameResolver = zodResolver(z.string().min(1, { message: "Last name is required." }));
const zodPasswordResolver = zodResolver(z.string().min(1, { message: "Password is required." }));

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
    <span class="block mb-8">{{ "Stwórz użytkownika w systemie" }}</span>
    <div class="card flex justify-center">
      <Form
        :initialValues
        :resolver
        @submit="onFormSubmit"
        class="flex flex-col gap-4 w-full sm:w-80"
      >
        <FormField
          v-slot="$field"
          name="firstname"
          initialValue=""
          :resolver="zodFirstNameResolver"
          class="flex flex-col gap-1"
        >
          <FloatLabel variant="on">
            <InputText id="imie_input" type="text" fluid />
            <label for="imie_input">Imię</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField
          v-slot="$field"
          name="lastname"
          initialValue=""
          :resolver="zodNameResolver"
          class="flex flex-col gap-1"
        >
          <FloatLabel variant="on">
            <InputText id="nazwisko_input" type="text" fluid />
            <label for="nazwisko_input">Nazwisko</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField
          v-slot="$field"
          name="email"
          initialValue=""
          :resolver="zodUserNameResolver"
          class="flex flex-col gap-1"
        >
          <FloatLabel variant="on">
            <InputText id="email_input" type="text" fluid />
            <label for="email_input">E-mail</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField
          v-slot="$field"
          name="password"
          initialValue=""
          :resolver="zodPasswordResolver"
          class="flex flex-col gap-1"
        >
          <FloatLabel variant="on">
            <Password id="password_input" type="text" :feedback="false" toggleMask fluid />
            <label for="password_input">Hasło</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <Button type="submit" severity="secondary" label="Submit" />
      </Form>
    </div>
  </Dialog>
</template>
