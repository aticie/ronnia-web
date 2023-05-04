<script setup lang="ts">
import axios from "axios";
import { watch, ref } from "vue";
import { useMousePressed, useMouseInElement } from "@vueuse/core";

const response = await axios.get("/live", { withCredentials: false });
const domain = window.location.hostname;

const target = ref<HTMLElement | null>(null);

const { pressed } = useMousePressed();
const { elementX } = useMouseInElement(target);

watch(elementX, (newVal, oldVal) => {
  if (!pressed.value || !target.value) {
    return;
  }
  
  let difference = newVal - oldVal;
  target.value.scrollBy({ left: -difference });
})
</script>

<template>
  <div 
    ref="target" 
    class="flex gap-2 max-w-7xl overflow-x-auto rounded-xl overflow-hidden pointer-events-none mask"
  >
    <iframe
      v-for="streamer in response.data"
      :key="streamer"
      :src="`https://player.twitch.tv/?channel=${streamer}&parent=${domain}`"
      class="h-60 aspect-video"
      allowfullscreen>
    </iframe>
  </div>
</template>
