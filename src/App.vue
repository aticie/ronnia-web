<script setup lang="ts">
import { useCookies } from "@vueuse/integrations/useCookies";
import { useRouter } from 'vue-router';
import Footer from './components/Footer.vue';

const router = useRouter();
const cookies = useCookies();

if (!cookies.get("token")) {
  router.replace("/login");
} else {
  router.replace("/settings");
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <main class="grow flex flex-col max-w-2xl w-full mx-auto lg:p-8 gap-4">
      <h1 class="text-center text-4xl font-bold">Ronnia Dashboard</h1>
      
      <RouterView v-slot="{ Component }">
        <Suspense :timeout="0">
          <component :is="Component" />

          <template #fallback>
            <p>loading</p>
          </template>
        </Suspense>
      </RouterView>
    </main>

    <Footer />
  </div>
</template>
