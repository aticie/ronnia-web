<script setup lang="ts" generic="T">
defineProps<{
  modelValue: T
}>();
defineEmits(["update:modelValue"]);
</script>

<template>
  <input 
    class="appearance-none w-5 h-5 bg-neutral-950 rounded-md checked:bg-red checked:bg-[url('/tick.svg')]"
    type="checkbox"
    :value="modelValue"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
  />
</template>
