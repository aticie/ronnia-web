<script setup lang="ts">
import { Settings } from "../types";
import { useFetch } from "@vueuse/core";
import { ref } from "vue";

import TheUser from '../components/TheUser.vue';
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingBase from "../components/settings/SettingBase.vue";
import BaseRange from "../components/BaseRange.vue";

const { data } = await useFetch(
  `${import.meta.env.VITE_API_BASE}/user/settings`,
  { credentials: "include" }
).json<Settings>();

const settings = ref(data.value);
</script>

<template>
  <div class="w-full max-w-lg p-2">
    <Suspense :timeout="0">
      <TheUser />
      <template #fallback>
        <p>loading..</p>
      </template>
    </Suspense>

    <div v-if="settings" class="flex flex-col gap-2 mt-10">
      <template v-for="setting in settings">
        <SettingToggle v-if="setting.type === 'toggle'" :data="setting" />
        <SettingBase v-if="setting.type === 'value'" class="flex-col">
          <p class="text-left w-full mb-2">{{ setting.description }}</p>
          <BaseRange v-model="setting.value" :min="0" :max="15 * 60" :pipStep="60" />
        </SettingBase>
        <SettingBase v-if="setting.type === 'range'" class="flex-col">
          <p class="text-left w-full mb-2">{{ setting.description }}</p>
          <BaseRange v-model="setting.value" :min="0" :max="10" :pipStep="1" range />
        </SettingBase>
      </template>
    </div>
  </div>
</template>
