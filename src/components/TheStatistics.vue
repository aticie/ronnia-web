<script setup lang="ts">
import axios from "axios";
import { ref } from "vue";
import { Beatmap } from "../types";

const response = await axios.get<Beatmap[]>("/requests/beatmaps/top", {
  params: {
    daysAgo: 30,
  },
  withCredentials: false,
});

const beatmaps = ref<Beatmap[]>(response.data);
</script>

<template>
  <div class="grid gap-4 max-w-2xl mx-auto">
    <p class="w-fit p-2 px-4 rounded bg-neutral-950 mb-4">Most Requested Beatmaps</p>
    <ol class="grid gap-2">
      <li
        v-for="map in beatmaps"
        :key="map.id"
        class="p-2 rounded relative"
        :style="{
          background: `url(${map.beatmapset.covers.cover})`,
          backgroundPosition: 'center',
        }"
      >
        <a :href="map.url" class="relative z-10 break-all">
          <p class="text-lg font-semibold h-14">
            {{ map.beatmapset.title }}
          </p>

          <div class="flex justify-between text-shadow">
            <p class="text-sm">{{ map.beatmapset.artist }}</p>
            <p>Requested {{ map.count }} times</p>
          </div>
        </a>

        <div class="bg-black/75 absolute inset-0" />
      </li>
    </ol>
  </div>
</template>
