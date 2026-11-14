<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import Development from "./components/TheDevRouter.vue";
import TheMigrationBanner from "./components/TheMigrationBanner.vue";
import TheToaster from "./components/TheToaster.vue";
import BaseSuspense from "./components/base/BaseSuspense.vue";
import { fetchMigrationStatus } from "./api";
import { useBus } from "./composables/useBus";

const isDev = import.meta.env.DEV;
const migrationActive = ref(false);
const migrationCutoffAt = ref<string | null>(null);

const route = useRoute();
const router = useRouter();
const bus = useBus();

// Subscribe after the toaster mounts, and consume the marker so reloads stay quiet.
onMounted(() => {
  watch(
    () => route.query.login_error,
    (error) => {
      if (error !== "1") return;
      bus.emit({ type: "error", title: "Login failed" });
      const { login_error, ...query } = route.query;
      void router.replace({ path: route.path, query, hash: route.hash });
    },
    { immediate: true }
  );
});

// Public rollout status is optional configuration: a missing or failing
// endpoint must never prevent the dashboard from rendering.
const loadMigrationStatus = async () => {
  try {
    const status = await fetchMigrationStatus();
    migrationActive.value = status.active === true;
    migrationCutoffAt.value =
      typeof status.cutoffAt === "string" ? status.cutoffAt : null;
  } catch {
    migrationActive.value = false;
    migrationCutoffAt.value = null;
  }
};
void loadMigrationStatus();
</script>

<template>
  <div class="min-h-[100dvh] flex flex-col items-center">
    <TheMigrationBanner
      v-if="migrationActive"
      :cutoff-at="migrationCutoffAt"
    />
    <TheToaster />

    <RouterView v-slot="{ Component }">
      <BaseSuspense>
        <component :is="Component" />
      </BaseSuspense>
    </RouterView>

    <Development v-if="isDev" />
  </div>
</template>
