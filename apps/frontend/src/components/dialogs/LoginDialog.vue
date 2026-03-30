<script setup lang="ts">
import { Dialog, Button, InputText, Message, Password, FloatLabel } from "primevue";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";
import { useMutation } from "@tanstack/vue-query";
import { useToast } from "primevue/usetoast";
import { reactive, ref } from "vue";
import { z } from "zod";

import AppLogo from "../AppLogo.vue";
import { useCurrentUserStore } from "../../stores/currentUserStore";

const toast = useToast();
const currentUserStore = useCurrentUserStore();

const initialValues = reactive({
  firstname: "",
  lastname: "",
  email: "",
  password: "",
});

const registerResolver = zodResolver(
  z.object({
    firstname: z.string().min(1, { message: "Imię jest wymagane." }),
    lastname: z.string().min(1, { message: "Nazwisko jest wymagane." }),
    email: z
      .string()
      .min(1, { message: "E-mail jest wymagany." })
      .regex(/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/, {
        message: "Wpisz poprawny e-mail.",
      }),
    password: z.string().min(1, { message: "Hasło jest wymagane." }),
  }),
);

const loginResolver = zodResolver(
  z.object({
    email: z
      .string()
      .min(1, { message: "E-mail jest wymagany." })
      .regex(/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/, {
        message: "Wpisz poprawny e-mail.",
      }),
    password: z.string().min(1, { message: "Hasło jest wymagane." }),
  }),
);

const loginMutation = useMutation({
  mutationFn: async (values: any) => {
    const loginResp = { user_id: 2, name: "Damian", lastname: "Karwat", email: values.email };

    const checkCompanyResp = {
      user_id: 2,
      company_id: 1,
      company_name: "Lukpol Warszawa",
      ksef_auth: true,
    };
    return { loginResp, checkCompanyResp };
  },
  onSuccess: (data, variables) => {
    toast.add({ severity: "info", summary: "Zalogowano pomyślnie", life: 3000 });
    currentUserStore.setUserData(
      data.loginResp.user_id,
      data.loginResp.name,
      data.loginResp.lastname,
      data.loginResp.email,
    );
    currentUserStore.setCompanyData(
      data.checkCompanyResp.company_id,
      data.checkCompanyResp.company_name,
      data.checkCompanyResp.ksef_auth,
    );
  },

  onError: () => {
    toast.add({ severity: "error", summary: "Coś poszło nie tak", life: 3000 });
  },
});

const registerMutation = useMutation({
  mutationFn: async (values: any) => {
    const loginResp = { user_id: 2, name: "Damian", lastname: "Karwat", email: values.email };
    return loginResp;
  },
  onSuccess: (data, variables) => {
    toast.add({ severity: "info", summary: "Zarejestrowano pomyślnie", life: 3000 });
    currentUserStore.setUserData(data.user_id, data.name, data.lastname, data.email);
  },

  onError: () => {
    toast.add({ severity: "error", summary: "Coś poszło nie tak", life: 3000 });
  },
});

const onFormSubmit = async (loggingIn: boolean, event: FormSubmitEvent) => {
  const { valid } = event;
  if (!valid) return;

  if (loggingIn) loginMutation.mutate(event.values);
  else registerMutation.mutate(event.values);
};

const login = ref(true);
</script>

<template>
  <Dialog :visible="true" modal :closable="false" :draggable="false" :style="{ width: '40rem' }">
    <template #header>
      <div class="flex flex-1 justify-between">
        <AppLogo />
        <Button
          text
          :label="login ? 'Zamiast tego zarejestruj się' : 'Wróć do logowania'"
          @click="() => (login = !login)"
        />
      </div>
    </template>
    <span class="block mb-8 font-semibold">{{
      login ? "Zaloguj się do systemu" : "Zarejestruj się w systemie"
    }}</span>
    <div class="card flex justify-center">
      <!-- LOGIN FORM -->
      <Form
        v-if="login"
        :initialValues
        :resolver="loginResolver"
        @submit="(event) => onFormSubmit(true, event)"
        class="flex flex-col gap-4 w-full sm:w-80"
      >
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
        <Button
          type="submit"
          severity="secondary"
          label="Zaloguj"
          :loading="loginMutation.isPending.value"
          :disabled="loginMutation.isPending.value"
        />
      </Form>
      <!-- REGISTER FORM -->
      <Form
        v-if="!login"
        :initialValues
        :resolver="registerResolver"
        @submit="(event) => onFormSubmit(false, event)"
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
        <Button
          type="submit"
          severity="secondary"
          label="Zarejestruj się"
          :loading="registerMutation.isPending.value"
          :disabled="registerMutation.isPending.value"
        />
      </Form>
    </div>
  </Dialog>
</template>
