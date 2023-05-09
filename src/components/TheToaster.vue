<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import { useBus, Notification } from "../composables/useBus";
import IconDone from "./icons/IconDone.vue";

const notifications = ref<Notification[]>([]);
const bus = useBus();

const unsub = bus.on((notification) => {
  if (!notification.id) {
    notification.id = Math.random();
  }

  setTimeout(() => {
    let index = notifications.value.findIndex((x) => x.id);
    notifications.value.splice(index, 1);
  }, 5000);

  notifications.value.push(notification);
});

onUnmounted(unsub);
</script>

<template>
  <TransitionGroup
    tag="div"
    class="max-w-xs w-full fixed right-3 top-3 grid gap-2 z-10 text-sm"
    enter-from-class="-translate-y-full"
    leave-to-class="scale-0 opacity-0"
    enter-active-class="transition-all"
    leave-active-class="transition-all absolute"
    move-class="transition-all"
  >
    <div
      v-for="notif in notifications"
      :key="notif.id"
      class="flex gap-3 bg-neutral-950 border border-neutral-800 rounded-lg p-3"
    >
      <IconDone class="h-6 w-6 bg-neutral-900 p-1 rounded-full" />

      <div class="pt-0.5 w-full">
        <p>{{ notif.title }}</p>
        <p v-if="notif.description" class="text-xs mt-1 text-neutral-400">
          {{ notif.description }}
        </p>
      </div>
    </div>
  </TransitionGroup>
</template>
