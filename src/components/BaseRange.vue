<script setup lang="ts" generic="T">
import { ref, watch } from 'vue';
import { useMouseInElement, useMousePressed } from '@vueuse/core';

const props = defineProps<{
  modelValue?: any,
  min: number,
  max: number,
  pipStep: number
}>();

const emit = defineEmits(["update:modelValue"]);

const dragging = ref(false);
const track = ref(null);

const leftOffset = ref(0);

const { elementX, elementWidth, isOutside } = useMouseInElement(track)
const { pressed } = useMousePressed({ target: track })

watch([elementX, pressed], () => {
  if (!dragging.value && !isOutside.value && pressed.value) {
    dragging.value = true;
    return;
  }

  if (dragging.value && isOutside.value, !pressed.value) {
    dragging.value = false;
    return;
  }

  let percent = elementX.value * 100 / elementWidth.value;
  leftOffset.value = Math.max(0, Math.min(percent, 100));

  let x = props.max * leftOffset.value / 100;
  emit("update:modelValue", x);

  console.log(props.modelValue);
})
</script>

<template>
  <div class="w-full">
    <div ref="track" class="
      flex items-center grow rounded-full
      bg-neutral-950 h-2.5
    ">
      <div class="flex items-center w-full h-full mr-4 relative inset-0">
        <div class="absolute w-5 h-5 bg-red rounded-full" :style="{
          left: `${leftOffset}%`
        }" />

        <div class="absolute h-full bg-red rounded-full" :style="{
          width: `${leftOffset + 1}%`
        }" />
      </div>
    </div>

    <div>
      <div class="flex p-2 pb-0 justify-between">
        <p v-for="i in pipStep">{{ i * pipStep }}</p>
      </div>
    </div>
  </div>
</template>
