<template>
  <button
    class="
      flex items-center gap-2
      bg-rose-800 hover:bg-rose-700 transition-colors
      p-4 py-2 rounded
      text-sm select-none
    ">
    <div v-if="$slots.icon" class="h-6 aspect-square">
      <slot name="icon"></slot>
    </div>
    <slot></slot>
  </button>
</template>
