<script setup lang="ts">
import BaseButton from "../components/BaseButton.vue";
import IconLogout from "../components/icons/IconLogout.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import { useCookies } from '@vueuse/integrations/useCookies';
import { useFetch } from "@vueuse/core";
import { useRouter } from 'vue-router';

const router = useRouter();
const cookies = useCookies();
const token = cookies.get<string>('token');
if (!token && !import.meta.env.DEV) router.replace("/login");

const { data, error, execute, isFetching } = await useFetch<UserDetails>(
  `${import.meta.env.VITE_API_BASE}/user_details?${new URLSearchParams({
    jwt_token: token
  })}`
);
</script>

<template>
  <div v-if="error || !data" class="flex flex-col text-center">
    <BaseButton @click="execute">Refetch</BaseButton>
  </div>

  <div v-else class="flex flex-col gap-2">
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
      <template v-for="setting in data?.settings">
        <SettingToggle v-if="setting.type === 'toggle'" :data="setting" />
      </template>
    </div>
  </div>
</template>
