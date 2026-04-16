<script setup lang="ts">
import { Dialog, Button, InputText, Message, Password, FloatLabel } from "primevue";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";
import { useMutation } from "@tanstack/vue-query";
import { useToast } from "primevue/usetoast";
import { reactive, ref } from "vue";
import { z } from "zod";

import AppLogo from "../AppLogo.vue";
import router from "../../router/router";
import { userLogin, userSignUp, decodeToken } from "../../lib/services/authService";
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

const loginDialog = ref(true);
const visible = ref(true);

const loginMutation = useMutation({
  mutationFn: async (values: any) => {
    const loginResp = await userLogin({
      grant_type: null,
      username: values.email,
      password: values.password,
      scope: null,
      client_id: null,
      client_secret: null,
    });

    const userData = decodeToken(loginResp.access_token);

    return { creds: userData, token: loginResp.access_token };
  },
  onSuccess: (data, variables) => {
    toast.add({ severity: "info", summary: "Zalogowano pomyślnie", life: 3000 });
    currentUserStore.setUserData(
      data.creds.sub,
      data.creds.name,
      data.creds.last_name,
      data.creds.email,
      data.token,
    );
    router.push("/sales");
  },

  onError: (error: number) => {
    if (error === 401) {
      toast.add({ severity: "error", summary: "Nieprawidłowy email lub hasło", life: 4000 });
    } else {
      toast.add({ severity: "error", summary: "Coś poszło nie tak", life: 4000 });
    }
  },
});

const registerMutation = useMutation({
  mutationFn: async (values: any) => {
    const registerResp = await userSignUp({
      name: values.firstname,
      last_name: values.lastname,
      email: values.email,
      password: values.password,
    });

    const userData = decodeToken(registerResp.access_token);

    return { creds: userData, token: registerResp.access_token };
  },
  onSuccess: (data, variables) => {
    toast.add({ severity: "info", summary: "Zarejestrowano pomyślnie", life: 3000 });

    currentUserStore.setUserData(
      data.creds.sub,
      data.creds.name,
      data.creds.last_name,
      data.creds.email,
      data.token,
    );

    console.log(currentUserStore.toString());
  },

  onError: (error: number) => {
    if (error === 401) {
      toast.add({
        severity: "error",
        summary: "Adres e-mail już zajęty!",
        life: 4000,
      });
    } else {
      setTimeout(() => {
        toast.add({ severity: "error", summary: "Coś poszło nie tak", life: 4000 });
      }, 100);
    }
  },
});

const onFormSubmit = async (loggingIn: boolean, event: FormSubmitEvent) => {
  const { valid } = event;
  if (!valid) return;

  if (loggingIn) loginMutation.mutate(event.values);
  else registerMutation.mutate(event.values);
};
</script>

<template>
  <Dialog :visible="visible" modal :closable="false" :draggable="false" :style="{ width: '40rem' }">
    <template #header>
      <div class="flex flex-1 justify-between">
        <AppLogo />
        <Button
          text
          :label="loginDialog ? 'Zamiast tego zarejestruj się' : 'Wróć do logowania'"
          @click="() => (loginDialog = !loginDialog)"
        />
      </div>
    </template>
    <span class="block mb-8 font-semibold">{{
      loginDialog ? "Zaloguj się do systemu" : "Zarejestruj się w systemie"
    }}</span>
    <div class="card flex justify-center">
      <!-- LOGIN FORM -->
      <Form
        v-if="loginDialog"
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
        v-if="!loginDialog"
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
