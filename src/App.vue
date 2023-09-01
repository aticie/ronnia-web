<script setup lang="ts">
import Development from "./components/TheDevRouter.vue";
import TheToaster from "./components/TheToaster.vue";
import BaseSuspense from "./components/base/BaseSuspense.vue";
import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_API_BASE;

const isDev = import.meta.env.DEV;
</script>

<template>
  <div class="min-h-screen flex flex-col items-center">
    <TheToaster />

    <RouterView v-slot="{ Component }">
      <BaseSuspense>
        <component :is="Component" />
      </BaseSuspense>
    </RouterView>

    <Development v-if="isDev" />
  </div>
</template>
