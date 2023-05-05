<script setup lang="ts">
import axios from "axios";

const response = await axios.get("/live", {
  withCredentials: false,
  params: { limit: 1000 },
});

const domain = window.location.hostname;
</script>

<template>
  <div class="lg:absolute inset-0 flex justify-end items-end overflow-hidden">
    <div
      class="surface mask grid grid-cols-4 gap-4 max-w-7xl h-[70%] overflow-y-auto"
    >
      <img
        v-for="streamer in response.data"
        :src="`https://static-cdn.jtvnw.net/previews-ttv/live_user_${streamer}.jpg`"
        class="w-full aspect-video object-cover"
      />
      <img
        v-for="streamer in response.data"
        :src="`https://static-cdn.jtvnw.net/previews-ttv/live_user_${streamer}.jpg`"
        class="w-80 aspect-video object-cover"
      />
      <img
        v-for="streamer in response.data"
        :src="`https://static-cdn.jtvnw.net/previews-ttv/live_user_${streamer}.jpg`"
        class="w-80 aspect-video object-cover"
      />
    </div>
  </div>
</template>
