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
    target.value?.scrollTo({
      top: target.value.scrollTop + 1,
      behavior: "smooth",
    });
  }, 40);
});

onUnmounted(() => clearInterval(interval));

useInfiniteScroll(
  target,
  () => {
    streamers.value.push(...streamers.value);
  },
  { distance: 50 }
);
</script>

<template>
  <div class="lg:absolute inset-0 flex justify-end items-end overflow-hidden">
    <div class="surface max-w-7xl h-[70%] overlfow-x-visible">
      <p
        class="text-neutral-800 font-bold text-center text-2xl select-none"
        style="font-family: 'Bebas Neue', cursive"
      >
        Some cool streamers that use Ronnia!
      </p>
      <div
        ref="target"
        class="mask grid grid-cols-4 gap-2 px-10 overflow-y-auto h-full"
      >
        <a
          v-for="streamer in streamers"
          :href="`https://twitch.tv/${streamer}`"
        >
          <img
            :src="`https://static-cdn.jtvnw.net/previews-ttv/live_user_${streamer}.jpg`"
            class="w-full rounded-lg border border-neutral-800 aspect-video object-cover hover:-translate-x-4 hover:-translate-y-4 transition-transform"
          />
          <p class="ml-4" style="font-family: 'Bebas Neue', cursive">{{ streamer }}</p>
        </a>
      </div>
    </div>
  </div>
</template>
