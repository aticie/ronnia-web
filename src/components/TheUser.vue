<script setup lang="ts">
import { useFetch } from "@vueuse/core";
import { useCookies } from "@vueuse/integrations/useCookies";
import { useRouter } from "vue-router";
import { UserDetails } from "../types";

import IconOsu from "./icons/IconOsu.vue";
import IconTwitch from "./icons/IconTwitch.vue";
import IconLogout from "./icons/IconLogout.vue";
import BaseButton from "./base/BaseButton.vue";

const router = useRouter();
const cookies = useCookies();

if (!cookies.get("token")) {
  router.replace("/login");
}

const { data } = await useFetch(`${import.meta.env.VITE_API_BASE}/user/me`, {
  credentials: "include",
}).json<UserDetails>();

const logout = () => {
  useFetch(`${import.meta.env.VITE_API_BASE}/user/me`, {
    credentials: "include",
  }).delete();

  cookies.remove("signup");
  router.replace("/login");
};
</script>

<template>
  <div v-if="data" class="grid gap-2">
    <div class="flex gap-2">
      <div class="bg-neutral-900 p-2 rounded flex-1 relative">
        <IconOsu class="h-6 mb-2 absolute right-2 opacity-40" />
        <div class="flex items-center gap-2">
          <img :src="data.osuAvatarUrl" class="w-14 aspect-square rounded" />
          <p>{{ data.osuUsername }}</p>
        </div>
      </div>

      <div class="bg-neutral-900 p-2 rounded flex-1 relative">
        <IconTwitch class="h-6 mb-2 absolute right-2 opacity-40" />
        <div class="flex items-center gap-2">
          <img :src="data.twitchAvatarUrl" class="w-14 aspect-square rounded" />
          <p>{{ data.twitchUsername }}</p>
        </div>
      </div>
    </div>

    <BaseButton @click="logout">
      <template #icon>
        <IconLogout />
      </template>
      <p>Logout</p>
    </BaseButton>
  </div>
</template>
