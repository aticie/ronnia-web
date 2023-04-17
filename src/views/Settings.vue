<script setup lang="ts">
import BaseButton from "../components/BaseButton.vue";
import IconLogout from "../components/icons/IconLogout.vue";
import IconRefresh from "../components/icons/IconRefresh.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingsRange from "../components/settings/SettingRange.vue";

import { useCookies } from '@vueuse/integrations/useCookies';
import { useFetch } from "@vueuse/core";
import { useRouter } from 'vue-router';
import { UserDetails, SettingType } from "../types";
import { ref } from "vue";

const router = useRouter();
const cookies = useCookies();
const token = cookies.get<string>('token');
if (!token && !import.meta.env.DEV) router.replace("/login");

const { data, error, execute, isFetching } = await useFetch<UserDetails>(
  `${import.meta.env.VITE_API_BASE}/user_details?${new URLSearchParams({
    jwt_token: token
  })}`
);

const settings = ref<SettingType[] | undefined>(data.value?.settings);

settings.value =
  [
    {
      "id": 1,
      "key": "echo",
      "default_value": 1,
      "description": "Enables Twitch chat acknowledge message.",
      "type": "toggle",
      "value": 1
    },
    {
      "id": 2,
      "key": "enable",
      "default_value": 1,
      "description": "Enables the bot.",
      "type": "toggle",
      "value": 1
    },
    {
      "id": 3,
      "key": "sub-only",
      "default_value": 0,
      "description": "Subscribers only request mode.",
      "type": "toggle",
      "value": 0
    },
    {
      "id": 4,
      "key": "cp-only",
      "default_value": 0,
      "description": "Channel Points only request mode.",
      "type": "toggle",
      "value": 0
    },
    {
      "id": 5,
      "key": "test",
      "default_value": 0,
      "description": "Enables test mode.",
      "type": "toggle",
      "value": 0
    },
    {
      "id": 1,
      "key": "sr",
      "default_low": -1.0,
      "default_high": -1.0,
      "description": "Set star rating limit for requests.",
      "type": "range",
      "range_start": -1.0,
      "range_end": -1.0
    },
    {
      "id": 6,
      "key": "cooldown",
      "default_value": 30,
      "description": "Cooldown for requests.",
      "type": "value",
      "value": 30
    }
  ]


const logout = () => {
  cookies.remove("token");
  router.replace("/login");
}
</script>

<template>
  <div v-if="error || !data" class="grid gap-4 p-4 bg-rose-800 rounded">
    <p>{{ error }}</p>
    <BaseButton @click="execute">
      <template #icon>
        <IconRefresh :class="{ 'animate-spin': isFetching }" />
      </template>
      <p>Refetch</p>
    </BaseButton>
  </div>

  <div class="grid gap-2 w-full max-w-lg">
    <p class="font-bold text-lg text-white bg-rose-700 w-fit p-2 rounded mb-10">
      Dashboard
    </p>

    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img :src="data?.avatar_url" class="h-12 aspect-square rounded" />
        <p>{{ data?.osu_username }}</p>
      </div>
      <BaseButton @click="logout">
        <template #icon>
          <IconLogout />
        </template>
        <p>Logout</p>
      </BaseButton>
    </div>

    <div class="grid gap-2">
      <template v-for="setting in settings">
        <SettingToggle v-if="setting.type === 'toggle'" :data="setting" />
        <SettingsRange v-if="setting.type === 'range'" :data="setting" />
      </template>
    </div>
  </div>
</template>
