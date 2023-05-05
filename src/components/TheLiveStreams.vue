<script setup lang="ts">
import axios from "axios";
import { ref, onMounted, onUnmounted } from "vue";
import { useInfiniteScroll } from "@vueuse/core";

const response = await axios.get<string[]>("/live", {
  withCredentials: false,
  params: { limit: 1000 },
});

const streamers = ref(response.data);
const target = ref<HTMLElement | null>(null);

let interval: number;
onMounted(() => {
  interval = setInterval(() => {
    target.value?.scrollTo({ top: target.value.scrollTop + 1, behavior: "smooth" });
  }, 40)
})

onUnmounted(() => clearInterval(interval))

useInfiniteScroll(target, () => {
  streamers.value.push(...streamers.value);
}, { distance: 50 })
</script>

<template>
  <div class="lg:absolute inset-0 flex justify-end items-end overflow-hidden">
    <div class="surface max-w-7xl h-[70%]">
      <p class="text-neutral-800 font-bold text-center">Some cool streamers that use Ronnia!</p>
      <div
        ref="target"
        class="mask grid grid-cols-4 gap-4 overflow-y-auto h-full"
      >
        <img
          v-for="streamer in streamers"
          :src="`https://static-cdn.jtvnw.net/previews-ttv/live_user_${streamer}.jpg`"
          class="w-full aspect-video object-cover hover:scale-110 transition-transform"
        />
      </div>
    </div>
  </div>
</template>
