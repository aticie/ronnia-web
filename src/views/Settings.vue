<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Settings } from "../types";
import { watchDebounced } from "@vueuse/core";
import { useBus, useMinuteFormat } from "../composables";
import { api, apiErrorMessage } from "../api";

import IconDone from "../components/icons/IconDone.vue";
import TheUser from "../components/TheUser.vue";
import SettingExcluded from "../components/settings/SettingExcluded.vue";
import SettingToggle from "../components/settings/SettingToggle.vue";
import SettingBase from "../components/settings/SettingBase.vue";
import BaseSuspense from "../components/base/BaseSuspense.vue";
import BaseButton from "../components/base/BaseButton.vue";
import BaseRange from "../components/base/BaseRange.vue";

const bus = useBus();

const settings = ref<Settings>();
const isFetching = ref(false);
const excludedUsers = ref<string[]>([]);
const loadError = ref("");

const loadSettings = async () => {
  loadError.value = "";
  try {
    const response = await api.get<Settings>("/user/settings");
    settings.value = response.data;
  } catch (error) {
    loadError.value = apiErrorMessage(error);
    bus.emit({ title: "Could not load settings", description: loadError.value, type: "error" });
  }
};
await loadSettings();

type SettingsValues = Record<string, boolean | number | [number, number]>;
const saveError = ref("");
let pendingValues: SettingsValues | undefined;

const snapshotSettings = (): SettingsValues | undefined => {
  if (!settings.value) return;
  // The Rust endpoint replaces Settings, so each queued snapshot contains all
  // fields and owns its range tuple independently of subsequent UI edits.
  const values: SettingsValues = {};
  for (const setting of settings.value) {
    values[setting.name] = setting.type === "range"
      ? [setting.value[0], setting.value[1] >= 10 ? -1 : setting.value[1]]
      : setting.value;
  }
  return values;
};
const savedSnapshot = ref(JSON.stringify(snapshotSettings()));
const hasUnsavedChanges = computed(() => JSON.stringify(snapshotSettings()) !== savedSnapshot.value);
const saveStatus = computed(() => {
  if (isFetching.value) return "Saving…";
  if (saveError.value) return "Save failed";
  return hasUnsavedChanges.value ? "Unsaved changes" : "All changes saved";
});

const saveSettings = async () => {
  const values = snapshotSettings();
  if (!values) return;
  if (!isFetching.value && JSON.stringify(values) === savedSnapshot.value && !saveError.value) return;
  pendingValues = values;
  if (isFetching.value) return;
  isFetching.value = true;
  saveError.value = "";

  try {
    // Manual saves, debounced saves, and edits during a request share this
    // single writer. Coalesce waiting edits, never overlap full replacements.
    while (pendingValues) {
      const current = pendingValues;
      pendingValues = undefined;
      const snapshot = JSON.stringify(current);
      if (snapshot === savedSnapshot.value) continue;
      await api.post("/user/settings", current);
      savedSnapshot.value = snapshot;
    }
    bus.emit({
      title: "Saved your settings!",
      description: "Your settings are saved every time you make a change.",
      type: "success"
    });
  } catch (error) {
    // Keep the form and its latest pending snapshot intact for an explicit
    // retry. A failed write must not produce a success notification.
    pendingValues = snapshotSettings();
    saveError.value = apiErrorMessage(error);
    // A failed response can leave the server outcome uncertain; retry must
    // write the current form even when it matches the last acknowledged state.
    savedSnapshot.value = "";
    bus.emit({
      title: "Error while saving!",
      description: saveError.value,
      type: "error"
    });
  } finally {
    isFetching.value = false;
  }
};

// Queue edits immediately while a save is running, rather than waiting for the
// debounce timer: a completing older request must flush the latest form state.
watch(settings, (current, previous) => {
  if (current && previous && isFetching.value) pendingValues = snapshotSettings();
}, { deep: true, flush: "sync" });

watchDebounced(settings, (current, previous) => {
  if (current && previous) void saveSettings();
}, {
  debounce: 1500,
  deep: true,
});
</script>

<template>
  <div class="w-full max-w-lg p-2">
    <BaseSuspense>
      <TheUser />
    </BaseSuspense>

    <div v-if="loadError" role="alert" class="mt-6 text-red-400">
      <p>{{ loadError }}</p>
      <button class="underline" @click="loadSettings">Retry loading settings</button>
    </div>

    <p v-if="saveError" role="alert" class="mt-3 text-red-400">
      {{ saveError }} Your changes are still in the form. Use Save Changes to retry.
    </p>

    <div v-if="settings" class="flex flex-col gap-2 mt-10">
      <template v-for="setting in settings" :key="setting.name">
        <SettingToggle v-if="setting.type === 'toggle'" :data="setting" />
        <SettingBase v-if="setting.type === 'value'" class="flex-col">
          <p class="text-left w-full mb-2">{{ setting.description }}</p>
          <BaseRange
            v-model="setting.value"
            :min="0"
            :max="15 * 60"
            :pipStep="60"
            round
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
            round
            range
          >
            <template #default="{ values }">
              <p>{{ values[1] === -1 || values[1] >= 10 ? "∞" : values[1].toFixed(1) }}</p>
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

      <div class="flex flex-wrap items-center gap-3">
        <BaseButton
          @click="saveSettings"
          :isLoading="isFetching"
          :disabled="isFetching || (!hasUnsavedChanges && !saveError)"
          aria-describedby="settings-save-status"
        >
          <template #icon>
            <IconDone />
          </template>
          <p>Save Changes</p>
        </BaseButton>
        <p id="settings-save-status" role="status" class="text-sm text-neutral-300">
          {{ saveStatus }}
        </p>
      </div>
    </div>
  </div>
</template>
