<script setup lang="ts">
import axios from "axios";

const response = await axios.get("/live", { withCredentials: false });
const domain = window.location.hostname;
</script>

<template>
  <div class="lg:absolute w-full inset-0 overflow-hidden">
    <div
      class="lg:surface flex flex-col overflow-hidden lg:w-[150%]"
    >
      <p class="lg:text-xl text-neutral-800 text-center font-bold">Some Cool Streamers that use Ronnia!</p>

      <div class="lg:mask flex flex-wrap justify-center lg:justify-normal gap-4">
        <iframe
          v-for="(streamer, index) in response.data"
          :key="streamer"
          :src="`https://player.twitch.tv/?channel=${streamer}&parent=${domain}`"
          class="w-80 aspect-video rounded border border-neutral-600 bg-neutral-950 shadow shadow-neutral-500 hover:scale-125 transition-transform"
          allowfullscreen>
        </iframe>

        <div
          v-for="i in (20 - response.data.length)"
          class="w-80 aspect-video rounded border border-neutral-600 bg-neutral-950 shadow shadow-neutral-500 hover:scale-125 transition-transform"
        />
      </div>
    </div>
  </div>
</template>
