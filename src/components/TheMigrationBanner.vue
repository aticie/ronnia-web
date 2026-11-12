<script setup lang="ts">
import { computed } from "vue";
import { formatLocalDateTime } from "../utils";

const props = defineProps<{
  cutoffAt: string | null;
}>();

const formattedCutoff = computed(() =>
  props.cutoffAt ? formatLocalDateTime(props.cutoffAt) : undefined
);
</script>

<template>
  <section
    role="status"
    aria-live="polite"
    aria-atomic="true"
    data-testid="migration-banner"
    class="sticky top-0 z-50 w-full border-b border-rose-900/70 bg-rose-950/60 backdrop-blur"
  >
    <div
      class="mx-auto flex w-full max-w-2xl flex-col gap-3 px-4 py-3 text-sm sm:flex-row sm:items-center"
    >
      <div class="min-w-0 flex-1">
        <p class="font-semibold text-neutral-100">Ronnia has moved</p>
        <p class="mt-1 text-neutral-300">
          Accounts and settings now use the new dashboard. Sign in and
          re-authorize Twitch bot access to keep Ronnia responding in your
          channel.
        </p>
        <p v-if="formattedCutoff" class="mt-1 text-neutral-400">
          Migration cutoff:
          <time :datetime="cutoffAt ?? undefined">{{ formattedCutoff }}</time>
          (your local time).
        </p>
      </div>
    </div>
  </section>
</template>
