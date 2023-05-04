<script setup lang="ts">
import { ref } from "vue";
import { Settings } from "../types";
import { useBus, useMinuteFormat, useCooldown } from "../composables";
import axios from "axios";

import IconDone from "../components/icons/IconDone.vue";
import TheUser from "../components/TheUser.vue";
import SettingExcluded from "../components/settings/SettingExcluded.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingBase from "../components/settings/SettingBase.vue";
import BaseSuspense from "../components/base/BaseSuspense.vue";
import BaseButton from "../components/base/BaseButton.vue";
import BaseRange from "../components/base/BaseRange.vue";

const data = (await axios.get<Settings>("/user/settings")).data;

const settings = ref(data);
const isFetching = ref(false);
const excludedUsers = ref([]);

const bus = useBus();
const { onCooldown, resetCooldown } = useCooldown(5);

const saveSettings = async () => {
  if (!settings.value) return;
  isFetching.value = true;
  resetCooldown();

  const values: { [key: string]: any } = {};
  for (const setting of settings.value) {
    values[setting.name] = setting.value;
  }

  try {
    await axios.post("/user/settings", values);
    isFetching.value = false;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      bus.emit({
        title: "Error while saving!",
        description: error.response?.data || error.message,
      });
    }
  } finally {
    isFetching.value = false;
  }
};
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
            <p>{{ useMinuteFormat(value) }}</p>
          </BaseRange>
        </SettingBase>
        <SettingBase v-if="setting.type === 'range'" class="flex-col">
          <p class="text-left w-full mb-2">{{ setting.description }}</p>
          <BaseRange
            v-model="setting.value"
            :min="0"
            :max="10"
            :pipStep="1"
            range
            v-slot="{ value }"
          >
            <p>{{ value === 10 ? "∞" : value.toFixed(2) }}</p>
          </BaseRange>
        </SettingBase>
      </template>

      <SettingExcluded v-model="excludedUsers" />

      <BaseButton
        @click="saveSettings"
        :isLoading="isFetching"
        :disabled="onCooldown"
      >
        <template #icon>
          <IconDone />
        </template>
        <p>Save Changes</p>
      </BaseButton>
    </div>
  </div>
</template>
