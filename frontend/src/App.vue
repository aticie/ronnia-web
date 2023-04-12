<script setup lang="ts">
import Footer from './components/Footer.vue';
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <main class="grow flex flex-col items-center p-4 gap-4">
      <h1 class="text-center text-4xl font-bold">Ronnia Dashboard</h1>
      <RouterView />
    </main>

    <Footer />
  </div>
</template>
