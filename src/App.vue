<script setup lang="ts">
import Development from "./components/TheDevRouter.vue";
import { useCookies } from "@vueuse/integrations/useCookies";
import { useRouter } from 'vue-router';

const router = useRouter();
const cookies = useCookies();

const isDev = import.meta.env.DEV;

if (!cookies.get("token")) {
  router.replace("/login");
} else {
  router.replace("/settings");
}
</script>

<template>
  <div class="p-2 min-h-screen flex flex-col justify-center items-center">
    <RouterView v-slot="{ Component }">
      <Suspense :timeout="0">
        <component :is="Component" />
        <template #fallback>
          Loading...
        </template>
      </Suspense>
    </RouterView>

    <Development v-if="isDev" />
  </div>
</template>
