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
  firstname: "",
  lastname: "",
  email: "",
  password: "",
});

const resolver = zodResolver(
  z.object({
    firstname: z.string().min(1, { message: "Imię jest wymagane." }),

    lastname: z.string().min(1, { message: "Nazwisko jest wymagane." }),

    email: z.string().min(1, { message: "E-mail jest wymagany." }),

    password: z.string().min(1, { message: "Hasło jest wymagane." }),
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
    :style="{ width: '30rem' }"
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
        <FormField v-slot="$field" name="firstname" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="name_input" type="text" fluid />
            <label for="name_input">Imię</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="lastname" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="lastname_input" type="text" fluid />
            <label for="lastname_input">Nazwisko</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="email" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <InputText v-bind="$field.props" id="email_input" type="text" fluid />
            <label for="email_input">E-mail</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <FormField v-slot="$field" name="password" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <Password
              v-bind="$field.props"
              id="password_input"
              type="text"
              :feedback="false"
              toggleMask
              fluid
            />
            <label for="password_input">Hasło</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <Button type="submit" severity="secondary" label="Dodaj użytkownika" />
      </Form>
    </div>
  </Dialog>
</template>
