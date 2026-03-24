<script setup lang="ts">
import { Dialog, Button, InputText, Message, FloatLabel, FileUpload, Password } from "primevue";
import { Form, FormField } from "@primevue/forms";

import { zodResolver } from "@primevue/forms/resolvers/zod";
import { z } from "zod";
import { useToast } from "primevue/usetoast";

import AppLogo from "../AppLogo.vue";
import { reactive, ref } from "vue";

const toast = useToast();

const initialValues = reactive({
  ksef_password: "",
});

const resolver = zodResolver(
  z.object({
    ksef_password: z.string().min(1, { message: "Hasło jest wymagane." }),
  }),
);

const onFormSubmit = ({ valid }) => {
  if (valid) {
    toast.add({ severity: "success", summary: "Form is submitted.", life: 3000 });
  }
};

const emit = defineEmits(["update:visible"]);

const companyName = ref("Lukpol Warszawa");
const isCertChosen = ref(false);
const isKeyChosen = ref(false);
</script>

<template>
  <Dialog
    :visible="true"
    @update:visible="emit('update:visible', $event)"
    modal
    :draggable="false"
    :style="{ width: '40rem' }"
  >
    <template #header>
      <AppLogo />
    </template>
    <span class="block mb-8 font-semibold">{{
      "Uwierzytelnij firmę " + companyName + " w systemie KSeF."
    }}</span>
    <div class="card flex justify-center">
      <Form
        :initialValues
        :resolver
        @submit="onFormSubmit"
        class="flex flex-col gap-4 w-full sm:w-100"
      >
        <FormField v-slot="$field" name="name" class="flex flex-col gap-1">
          <FileUpload
            name="ksef_certificate"
            :disabled="isCertChosen"
            withCredentials
            :showCancelButton="false"
            :showUploadButton="false"
            chooseLabel="Wybierz plik"
            :multiple="false"
            accept=".pfx,.crt,.cer"
            :maxFileSize="1000000"
            :fileLimit="1"
            invalidFileTypeMessage="Błędny typ pliku. (Akceptowalne: *.crt, *.pfx, *.cer)"
            @select="
              () => {
                isCertChosen = !isCertChosen;
              }
            "
          >
            <template #empty>
              <span class="font-semibold"
                >Przeciągnij i upuść certyfikat uwierzytelniający. (np. plik auth.crt)</span
              >
            </template>
            <template #content="{ files }">
              <div
                v-for="file in files"
                :key="file.name"
                class="flex justify-between items-center w-full"
              >
                <div class="flex items-center gap-2">
                  <i class="pi pi-file text-primary"></i>
                  <span class="font-medium">{{ file.name }}</span>
                </div>

                <!-- Status + przycisk usuń -->
                <div class="flex items-center gap-2">
                  <span class="text-sm text-gray-500">Gotowy</span>
                  <Button
                    icon="pi pi-times"
                    severity="danger"
                    text
                    @click="removeFileCallback(index)"
                  />
                </div>
              </div>
            </template>
          </FileUpload>
        </FormField>
        <FormField v-slot="$field" name="nip" class="flex flex-col gap-1">
          <FileUpload
            name="ksef_key"
            :disabled="isKeyChosen"
            withCredentials
            :showCancelButton="false"
            :showUploadButton="false"
            chooseLabel="Wybierz plik"
            :multiple="false"
            accept=".key"
            :maxFileSize="1000000"
            :fileLimit="1"
            invalidFileTypeMessage="Błędny typ pliku. (Akceptowalne: *.key)"
            @select="
              () => {
                isKeyChosen = !isKeyChosen;
              }
            "
          >
            <template #empty>
              <span class="font-semibold"
                >Przeciągnij i upuść klucz dla certyfikatu uwierzytelniającego. (np. plik
                auth.key)</span
              >
            </template>
            <template #content="{ files }">
              <div
                v-for="file in files"
                :key="file.name"
                class="flex justify-between items-center w-full"
              >
                <div class="flex items-center gap-2">
                  <i class="pi pi-file text-primary"></i>
                  <span class="font-medium">{{ file.name }}</span>
                </div>

                <!-- Status + przycisk usuń -->
                <div class="flex items-center gap-2">
                  <span class="text-sm text-gray-500">Gotowy</span>
                  <Button
                    icon="pi pi-times"
                    severity="danger"
                    text
                    @click="removeFileCallback(index)"
                  />
                </div>
              </div>
            </template>
          </FileUpload>
        </FormField>
        <FormField v-slot="$field" name="ksef_password" class="flex flex-col gap-1">
          <FloatLabel variant="on">
            <Password
              v-bind="$field.props"
              id="password_input"
              type="text"
              :feedback="false"
              toggleMask
              fluid
            />
            <label for="password_input">Hasło do klucza uwierzytelniającego KSeF</label>
          </FloatLabel>
          <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{
            $field.error?.message
          }}</Message>
        </FormField>
        <Button type="submit" severity="secondary" label="Dodaj firmę" />
      </Form>
    </div>
  </Dialog>
</template>
