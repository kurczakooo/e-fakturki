<script setup lang="ts">
import { Dialog, Button, Message, FloatLabel, Password } from "primevue";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";

import { zodResolver } from "@primevue/forms/resolvers/zod";
import { z } from "zod";
import { useToast } from "primevue/usetoast";

import AppLogo from "../AppLogo.vue";
import { ref } from "vue";
import FileInput from "../inputs/fileInput.vue";
import type { KsefCredentials } from "../../lib/types/ksef";

const props = defineProps<{
  visible: boolean;
  companyName: string;
}>();

const toast = useToast();

const resolver = zodResolver(
  z.object({
    ksef_password: z.string().min(1, { message: "Hasło jest wymagane." }),
  }),
);

const selectedCertFile = ref<File | null>(null);
const selectedKeyFile = ref<File | null>(null);

function handleSelectCert(file: File) {
  selectedCertFile.value = file;
}
function handleClearCert() {
  selectedCertFile.value = null;
}
function handleSelectKey(file: File) {
  selectedKeyFile.value = file;
}
function handleClearKey() {
  selectedKeyFile.value = null;
}

function areFilesSelected(): boolean {
  if (!selectedCertFile.value || !selectedKeyFile.value) {
    toast.add({
      severity: "error",
      summary: "Brak plików",
      detail: "Dodaj certyfikat i klucz",
      life: 3000,
    });
    return false;
  }
  return true;
}

const onFormSubmit = (event: FormSubmitEvent) => {
  const { valid, values } = event;
  if (!valid) return;
  if (!areFilesSelected()) return;

  const payload: KsefCredentials = {
    certFile: selectedCertFile.value,
    keyFile: selectedKeyFile.value,
    certPassword: (values as { ksef_password: string }).ksef_password,
  };

  console.log(payload);
};
</script>

<template>
  <Dialog
    :visible="props.visible"
    modal
    :closable="false"
    :draggable="false"
    :style="{ width: '40rem' }"
  >
    <template #header>
      <AppLogo />
    </template>
    <span class="block mb-2 font-semibold">
      Uwierzytelnij firmę {{ props.companyName }} w systemie KSeF.
    </span>
    <span class="block mb-5 text-sm text-gray-500">
      Upewnij się, że przesłane pliki służą do autoryzacji w KSeF, a nie do podpisu offline.
    </span>
    <div class="card flex justify-center">
      <Form :resolver @submit="onFormSubmit" class="flex flex-col gap-4 w-full sm:w-100">
        <FileInput
          acceptableFiles=".pfx,.crt,.cer"
          credentials
          :maxFileSize="1000000"
          invalidFileTypeMessage="Błędny typ pliku. (Akceptowalne: *.crt, *.pfx, *.cer)"
          dragAndDropMessage="Przeciągnij i upuść certyfikat uwierzytelniający. (np. plik auth.crt)"
          fileIcon="pi-file-check"
          @file-selected="handleSelectCert"
          @file-removed="handleClearCert"
        />
        <FileInput
          acceptableFiles=".key"
          credentials
          :maxFileSize="1000000"
          invalidFileTypeMessage="Błędny typ pliku. (Akceptowalne: *.key)"
          dragAndDropMessage="Przeciągnij i upuść klucz dla certyfikatu uwierzytelniającego. (np. plik
                auth.key)"
          fileIcon="pi-key"
          @file-selected="handleSelectKey"
          @file-removed="handleClearKey"
        />
        <FormField v-slot="$field" name="ksef_password" class="flex flex-col gap-1" initialValue="">
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
        <Button type="submit" severity="secondary" label="Uwierzytelnij firmę w KSeF" />
      </Form>
    </div>
  </Dialog>
</template>
