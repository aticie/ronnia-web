<script setup lang="ts">
import BaseRange from "../components/BaseRange.vue";
import BaseButton from "../components/BaseButton.vue";
import IconLogout from "../components/icons/IconLogout.vue";
import IconRefresh from "../components/icons/IconRefresh.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingBase from "../components/settings/SettingBase.vue";

import { useCookies } from '@vueuse/integrations/useCookies';
import { useFetch } from "@vueuse/core";
import { useRouter } from 'vue-router';
import { ref } from "vue";
import SettingsRange from "../components/settings/SettingsRange.vue";

const router = useRouter();
const cookies = useCookies();
const token = cookies.get<string>('token');
if (!token && !import.meta.env.DEV) router.replace("/login");

const { data, error, execute, isFetching } = await useFetch<UserDetails>(
  `${import.meta.env.VITE_API_BASE}/user_details?${new URLSearchParams({
    jwt_token: token
  })}`
);



data.value = {
  "command": "signup",
  "osu_username": "Sibyl",
  "osu_id": 10440852,
  "twitch_username": "sibyl000",
  "twitch_id": "170818624",
  "avatar_url": "https://a.ppy.sh/10440852?1675107108.jpeg",
  "user_id": 3165,
  "username": "Sibyl",
  "exp": 1682544959,
  "excluded_users": [],
  "settings": [
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
}

const settings = ref(data.value.settings);
</script>

<template>
  <div v-if="error || !data" class="flex flex-col text-center">
    <BaseButton @click="execute">
      <template #icon>
        <IconRefresh :class="{ 'animate-spin': isFetching }" />
      </template>
      <p>Refetch</p>
    </BaseButton>
  </div>

  <div class="grid gap-8 w-full max-w-lg">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img :src="data?.avatar_url" class="h-12 aspect-square rounded" />
        <p>{{ data?.osu_username }}</p>
      </div>
      <BaseButton>
        <template #icon>
          <IconLogout />
        </template>
        <p>Logout</p>
      </BaseButton>
    </div>

    <div class="flex flex-col gap-2 rounded overflow-hidden">
      <template v-for="setting in settings">
        <SettingToggle v-if="setting.type === 'toggle'" :data="setting" />
        <SettingsRange v-if="setting.type === 'range'" :data="setting" />
      </template>
    </div>
  </div>
</template>
