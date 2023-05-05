<script setup lang="ts">
import axios from "axios";

const response = await axios.get("/live", {
  withCredentials: false,
  params: { limit: 1000 },
});

const domain = window.location.hostname;
</script>

<template>
  <div class="lg:absolute w-full flex items-end inset-0 overflow-hidden">
    <!-- <div class="lg:surface flex flex-col overflow-hidden lg:w-[150%]"> -->
      <!-- <p class="lg:text-xl text-neutral-800 text-center font-bold">
        Some Cool Streamers that use Ronnia!
      </p> -->

      <div class="h-1/2">
        <div
          class="surface mx-auto mask grid grid-cols-5 gap-4"
        >
          <!-- class="lg:mask flex flex-wrap justify-center lg:justify-normal gap-4" -->
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
          <img
            v-for="streamer in response.data"
            :src="`https://static-cdn.jtvnw.net/previews-ttv/live_user_${streamer}.jpg`"
            class="w-80 aspect-video object-cover"
          />
        </div>

      </div>
  </div>
</template>
