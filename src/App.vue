<script setup lang="ts">
import Development from "./components/TheDevRouter.vue";
import BaseSuspense from "./components/base/BaseSuspense.vue";

const isDev = import.meta.env.DEV;
</script>

<template>
  <div class="p-2 min-h-screen flex flex-col justify-center items-center">
    <RouterView v-slot="{ Component }">
      <BaseSuspense>
        <component :is="Component" />
      </BaseSuspense>
    </RouterView>

    <Development v-if="isDev" />
  </div>
</template>
