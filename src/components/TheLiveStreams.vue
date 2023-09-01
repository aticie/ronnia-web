<script setup lang="ts">
import axios from "axios";
import { ref, onMounted } from "vue";

const response = await axios.get<string[]>("/live/users", {
  withCredentials: false,
  params: { limit: 1000 },
});

const animationDuration = response.data.length * 1.38;
document.documentElement.style.setProperty("--duration", `${animationDuration}s`);

let popCount = response.data.length % 4;
response.data.splice(response.data.length - popCount, popCount);

const streamers = ref<Array<string>>([...response.data, ...response.data]);
const target = ref<HTMLElement | null>(null);

onMounted(() => {
  if (!target.value) return;

  let rowCount = response.data.length / 4;
  // the height of first half of the elements, required for it to feel like infinite loop
  target.value.style.setProperty("--row", `${-209 * rowCount}px`);
});
</script>

<template>
  <div class="absolute flex items-end bottom-0 inset-x-0 w-full pt-10 h-[70%] overflow-hidden">
    <div class="surface mx-auto">
      <p
        class="text-neutral-400 text-center text-3xl select-none"
        style="font-family: 'Bebas Neue', cursive"
      >
        Some cool streamers that use Ronnia!
      </p>

      <div
        class="mask h-[612px] overflow-hidden flex flex-col items-center -z-10"
      >
        <div
          ref="target"
          class="animate-scroll max-w-7xl grid grid-cols-4 gap-2"
        >
          <a
            v-for="streamer in streamers"
            :href="`https://twitch.tv/${streamer}`"
            class="group"
          >
            <div class="group-hover:bg-rose-700 transition-colors rounded-xl">
              <img
                :src="`https://static-cdn.jtvnw.net/previews-ttv/live_user_${streamer}-484x268.jpg`"
                class="border border-neutral-700 rounded-lg aspect-video object-cover group-hover:-translate-x-4 group-hover:-translate-y-4 transition-transform"
              />
            </div>
            <p class="ml-4" style="font-family: 'Bebas Neue', cursive">
              {{ streamer }}
            </p>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
