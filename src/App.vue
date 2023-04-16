<script setup lang="ts">
import { useCookies } from "@vueuse/integrations/useCookies";
import { useRouter } from 'vue-router';

const router = useRouter();
const cookies = useCookies();

if (!cookies.get("token") && import.meta.env.DEV) {
  router.replace("/login");
} else {
  router.replace("/settings");
}
</script>

<template>
  <div class="min-h-screen flex flex-col justify-center items-center">
    <RouterView v-slot="{ Component }">
      <Suspense :timeout="0">
        <component :is="Component" />
        <template #fallback>
          Loading...
        </template>
      </Suspense>
    </RouterView>
  </div>
</template>
