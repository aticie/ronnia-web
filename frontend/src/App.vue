<script setup lang="ts">
import Footer from './components/Footer.vue';
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <main>
      <RouterView />
    </main>

    <Footer />
  </div>
</template>
