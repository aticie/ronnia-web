<script setup lang="ts">
import { useCookies } from "@vueuse/integrations/useCookies";
import { useRouter } from "vue-router";
import { UserDetails } from "../types";
import axios from "axios";

import IconOsu from "./icons/IconOsu.vue";
import IconTwitch from "./icons/IconTwitch.vue";
import IconLogout from "./icons/IconLogout.vue";
import BaseButton from "./base/BaseButton.vue";
import IconDelete from "./icons/IconDelete.vue";

const router = useRouter();
const cookies = useCookies();

if (!cookies.get("token")) {
  router.replace("/login");
}

const response = await axios.get<UserDetails>("/user/me");
const data = response.data;

const removeUser = async () => {
  await axios.delete("/user/me");
  cookies.remove("signup");
  router.replace("/login");
};

const logout = () => {
  cookies.remove("token");
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

    <div class="flex gap-2">
      <BaseButton @click="logout">
        <template #icon>
          <IconLogout />
        </template>
        <p>Logout</p>
      </BaseButton>

      <BaseButton @click="removeUser">
        <template #icon>
          <IconDelete />
        </template>
        <p>Delete Account</p>
      </BaseButton>
    </div>
  </div>
</template>
