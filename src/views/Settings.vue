<script setup lang="ts">
import BaseButton from "../components/BaseButton.vue";
import IconLogout from "../components/icons/IconLogout.vue";
import IconRefresh from "../components/icons/IconRefresh.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingsRange from "../components/settings/SettingRange.vue";

import { useCookies } from '@vueuse/integrations/useCookies';
import { useFetch } from "@vueuse/core";
import { useRouter } from 'vue-router';
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

const settings = ref(data.value?.settings);
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

  <div v-else class="grid gap-2 w-full max-w-lg">
    <p class="font-bold text-lg text-white bg-red w-fit p-2 rounded mb-10">
      Dashboard
    </p>

    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img :src="data.avatar_url" class="h-12 aspect-square rounded" />
        <p>{{ data.osu_username }}</p>
      </div>
      <BaseButton>
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