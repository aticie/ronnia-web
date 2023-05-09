<script setup lang="ts">
import { useRouter } from "vue-router";
import { useUserStore } from "../store";

import IconOsu from "./icons/IconOsu.vue";
import IconTwitch from "./icons/IconTwitch.vue";
import IconLogout from "./icons/IconLogout.vue";
import IconDelete from "./icons/IconDelete.vue";
import BaseButton from "./base/BaseButton.vue";

const userStore = useUserStore();
const router = useRouter();

const removeUser = async () => {
  try {
    await userStore.deleteUser();
  } finally {
    router.replace("/login");
  }
};

const logout = async () => {
  try {
    await userStore.logoutUser();
  } finally {
    router.replace("/login");
  }
};
</script>

<template>
  <div v-if="userStore.user" class="grid gap-2">
    <div class="flex gap-2">
      <div class="bg-neutral-900 p-2 rounded flex-1 relative">
        <IconOsu class="h-6 mb-2 absolute right-2 opacity-40" />
        <div class="flex items-center gap-2">
          <img
            :src="userStore.user.osuAvatarUrl"
            class="w-14 aspect-square rounded"
          />
          <p>{{ userStore.user.osuUsername }}</p>
        </div>
      </div>

      <div
        class="bg-neutral-900 p-2 rounded flex-1 relative"
        :class="{ 'outline outline-2 outline-green-500': userStore.user.isLive }"
      >
        <IconTwitch class="h-6 absolute right-2 opacity-40" />
        <div class="flex items-center gap-2">
          <img
            :src="userStore.user.twitchAvatarUrl"
            class="w-14 aspect-square rounded"
          />
          <p>{{ userStore.user.twitchUsername }}</p>
        </div>

        <div class="flex items-center gap-2 mt-2">
          <div
            class="w-2.5 h-2.5 bg-neutral-500 rounded-full"
            :class="{ '!bg-green-500': userStore.user.isLive }"
          />
          <p class="text-sm">
            {{ userStore.user.isLive ? "Online" : "Offline" }}
          </p>
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
