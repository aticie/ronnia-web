<template>
  <button
    class="
      flex items-center gap-2
      bg-red hover:bg-neutral-800 transition-colors
      p-4 py-2 rounded
      text-sm select-none
    ">
    <div v-if="$slots.icon" class="h-7 aspect-square">
      <slot name="icon"></slot>
    </div>
    <slot></slot>
  </button>
</template>
