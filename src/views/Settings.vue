<script setup lang="ts">
import { ref } from "vue";
import { Settings } from "../types";
import { watchDebounced } from "@vueuse/core";
import { useBus, useMinuteFormat, useCooldown } from "../composables";
import { useRouter } from "vue-router";
import axios from "axios";

import IconDone from "../components/icons/IconDone.vue";
import TheUser from "../components/TheUser.vue";
import SettingExcluded from "../components/settings/SettingExcluded.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingBase from "../components/settings/SettingBase.vue";
import BaseSuspense from "../components/base/BaseSuspense.vue";
import BaseButton from "../components/base/BaseButton.vue";
import BaseRange from "../components/base/BaseRange.vue";

const bus = useBus();
const router = useRouter();
const { onCooldown, resetCooldown } = useCooldown(5);

const settings = ref<Settings>();
const isFetching = ref(false);
const excludedUsers = ref([]);

try {
  const response = await axios.get<Settings>("/user/settings");
  settings.value = response.data;
} catch {
  router.replace("/login");
}

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

    bus.emit({
      title: "Saved your settings!",
    });
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

watchDebounced(settings, saveSettings, {
  debounce: 1500,
  deep: true,
});
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
            v-slot="{ values }"
          >
            <p>{{ useMinuteFormat(values) }}</p>
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
          >
            <template #default="{ values }">
              <p>{{ values[1] === 10 ? "∞" : values[1].toFixed(1) }}</p>
            </template>
            <template #left="{ values }">
              <p>{{ values[0].toFixed(1) }}</p>
            </template>
          </BaseRange>
        </SettingBase>
      </template>

      <BaseSuspense>
        <SettingExcluded v-model="excludedUsers" />
      </BaseSuspense>

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
