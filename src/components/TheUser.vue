<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { UserDetails } from "../types";
import axios from "axios";

import IconOsu from "./icons/IconOsu.vue";
import IconTwitch from "./icons/IconTwitch.vue";
import IconLogout from "./icons/IconLogout.vue";
import BaseButton from "./base/BaseButton.vue";
import IconDelete from "./icons/IconDelete.vue";

const router = useRouter();
const data = ref();

try {
  const response = await axios.get<UserDetails>("/user/me");
  data.value = response.data;
} catch {
  router.replace("/login");
}

const removeUser = async () => {
  try {
    await axios.delete("/user/me");
  } finally {
    router.replace("/login");
  }
};

const logout = async () => {
  try {
    await axios.get("/user/logout");
  } finally {
    router.replace("/login");
  }
};
</script>

<template>
  <div v-if="data" class="grid gap-2">
    <div class="flex gap-2">
      <div class="flex items-end bg-neutral-900 p-2 rounded flex-1 relative">
        <IconOsu class="h-6 mb-2 absolute right-2 opacity-40" />
        <div class="flex items-center gap-2">
          <img :src="data.osuAvatarUrl" class="w-14 aspect-square rounded" />
          <p>{{ data.osuUsername }}</p>
        </div>
      </div>

      <div class="bg-neutral-900 p-2 rounded flex-1 relative" :class="{ 'border-2 border-green-500': data.isLive }">
        <div class="flex items-center gap-2 pb-2">
          <div class="w-2.5 h-2.5 bg-neutral-500 rounded-full" :class="{ 'bg-green-500': data.isLive }" />
          <p class="text-sm">{{ data.isLive ? 'Online' : 'Offline' }}</p>
        </div>

        <IconTwitch class="h-6 mb-2 absolute right-2 opacity-40" />
        <div class="flex items-center gap-2">
          <img :src="data.twitchAvatarUrl" class="w-14 aspect-square rounded" />
          <p>{{ data.twitchUsername }}</p>
        </div>
      </div>
    </div>

    <div class="flex gap-2">
      <BaseButton @click="logout" class="basis-44">
        <template #icon>
          <IconLogout />
        </template>
        <p>Logout</p>
      </BaseButton>

      <BaseButton @click="removeUser" class="basis-44">
        <template #icon>
          <IconDelete />
        </template>
        <p>Delete Account</p>
      </BaseButton>
    </div>
  </div>
</template>
