<script setup lang="ts">
import { ref } from "vue";
import { useFetch } from "@vueuse/core";
import { Settings } from "../types";

import IconDone from "../components/icons/IconDone.vue";
import TheUser from "../components/TheUser.vue";
import SettingExcluded from "../components/settings/SettingExcluded.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingBase from "../components/settings/SettingBase.vue";
import BaseSuspense from "../components/base/BaseSuspense.vue";
import BaseRange from "../components/base/BaseRange.vue";
import BaseButton from "../components/base/BaseButton.vue";

const { data } = await useFetch(
  `${import.meta.env.VITE_API_BASE}/user/settings`,
  { credentials: "include" }
).json<Settings>();

const settings = ref(data.value);
const excludedUsers = ref([]);
const isFetching = ref(false);
const cooldown = ref(false);

const saveSettings = async () => {
  if (!settings.value) return;
  isFetching.value = true;
  cooldown.value = true;

  const values: { [key: string]: any } = {};
  for (const setting of settings.value) {
    values[setting.name] = setting.value;
  }

  const { error } = await useFetch(
    `${import.meta.env.VITE_API_BASE}/user/settings`,
    {
      credentials: "include",
    }
  ).post(values);

  isFetching.value = false;
  setTimeout(() => cooldown.value = false, 2000);
};

const thumbValue = (val: number) => {
  let rounded = Math.round(val);

  if (val < 60) return `${rounded}s`
  if (val % 60 === 0) return `${Math.round(val/60)}m`
  return `${Math.floor(rounded / 60)}m${rounded % 60}s`
}
</script>

<template>
  <div class="w-full max-w-lg p-2">
    <BaseSuspense>
      <TheUser />
    </BaseSuspense>

    <div v-if="settings" class="flex flex-col gap-2 mt-10">
      <template v-for="setting in settings">
        <SettingToggle v-if="setting.type === 'toggle'" :data="setting" />
        <SettingBase v-if="setting.type === 'value'" class="flex-col">
          <p class="text-left w-full mb-2">{{ setting.description }}</p>
          <BaseRange
            v-model="setting.value"
            :min="0"
            :max="15 * 60"
            :pipStep="60"
            v-slot="{ value }"
          >
            <p>{{ thumbValue(value) }}</p>
          </BaseRange>
        </SettingBase>
        <SettingBase v-if="setting.type === 'range'" class="flex-col">
          <p class="text-left w-full mb-2">{{ setting.description }}</p>
          <BaseRange
            v-model="setting.value"
            :min="0"
            :max="10"
            :pipStep="1"
            range v-slot="{ value }"
          >
            <p>{{ value === 10 ? "∞" : value.toFixed(2) }}</p>
          </BaseRange>
        </SettingBase>
      </template>

      <SettingExcluded v-model="excludedUsers" />

      <BaseButton @click="saveSettings" :isLoading="isFetching" :disabled="cooldown">
        <template #icon>
          <IconDone />
        </template>
        <p>Save Changes</p>
      </BaseButton>
    </div>
  </div>
</template>
