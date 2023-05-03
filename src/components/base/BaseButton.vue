<script setup lang="ts">
import IconSpinner from "../icons/IconSpinner.vue";

defineProps<{
  isLoading?: boolean;
}>();
</script>

<template>
  <button
    class="flex items-center gap-2 relative bg-rose-800 hover:bg-rose-700 transition-colors p-4 py-2 rounded overflow-hidden text-sm select-none"
  >
    <Transition
      enter-from-class="scale-0 opacity-0"
      enter-active-class="transition-all"
      leave-active-class="transition-all absolute"
      leave-to-class="scale-0 opacity-0"
    >
      <div v-if="isLoading" icon="spin">
        <IconSpinner />
      </div>
      <div v-else-if="$slots.icon" key="icon" class="h-6 aspect-square">
        <slot name="icon"></slot>
      </div>
    </Transition>
    <slot></slot>
  </button>
</template>
<style scoped>
.icon-leave-active,
.icon-enter-active {
  transition: all 350ms ease;
}

.icon-leave-to,
.icon-enter-from {
  opacity: 0;
  scale: 0;
}

.icon-leave-active {
  position: absolute;
}
</style>