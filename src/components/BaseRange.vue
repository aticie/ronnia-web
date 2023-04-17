<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import { useMouseInElement, useMousePressed } from "@vueuse/core";

const props = defineProps<{
  modelValue?: any;
  min: number;
  max: number;
  pipStep: number;
  range?: boolean;
}>();

const emit = defineEmits(["update:modelValue"]);

const track = ref(null);
const thumbRightElement = ref(null);
const thumbLeftElement = ref(null);

const thumbRight = reactive({
  dragging: false,
  pressed: false,
  offset: 0,
});

const thumbLeft = reactive({
  dragging: false,
  pressed: false,
  offset: 0,
});

const { elementX, elementWidth, isOutside } = useMouseInElement(track);
const { pressed: rightPressed } = useMousePressed({ target: thumbRightElement, });
const { pressed: leftPressed } = useMousePressed({ target: thumbLeftElement });

const offset = computed(() => {
  return (elementX.value * 100) / elementWidth.value;
});

const shouldDrag = (isDragging: boolean, pressed: boolean) => {
  if (pressed) {
    isDragging = true;
    return false; // return early
  }

  if (isOutside.value || !pressed) {
    isDragging = false;
    return true; // don't return
  }
}

watch(offset, () => {
  if (shouldDrag(thumbRight.dragging, rightPressed.value)) {
    return;
  }

  thumbRight.offset = Math.max(offset.value, thumbLeft.offset);

  // let x = (props.max * thumbRight.offset) / 100;
  // emit("update:modelValue", x);
});

watch(offset, () => {
  if (shouldDrag(thumbLeft.dragging, leftPressed.value)) {
    return;
  }

  thumbLeft.offset = Math.min(offset.value, thumbRight.offset);

  // let percent = (elementX.value * 100) / elementWidth.value;
  // thumbLeft.offset = Math.max(0, Math.min(percent, 100));

  // let x = (props.max * thumbLeft.offset) / 100;
  // emit("update:modelValue", x);
});
</script>

<template>
  <div class="w-full relative">
    <div ref="track" class="flex items-center grow rounded-full relative bg-neutral-950 h-2.5">
      <div class="flex items-center w-full h-full mr-4 relative inset-0">
        <!-- left thumb -->
        <button
          ref="thumbLeftElement"
          v-if="range"
          class="absolute w-5 h-5 bg-rose-700 rounded-full"
          :style="{
            left: `${thumbLeft.offset}%`,
          }"
        />

        <!-- right thumb -->
        <button
          ref="thumbRightElement"
          class="absolute w-5 h-5 bg-rose-700 rounded-full"
          :style="{
            left: `${thumbRight.offset}%`,
          }"
        />

        <!-- track -->
        <div
          class="absolute h-full bg-rose-700 rounded-full pointer-events-none"
          :style="{
            width: `${thumbRight.offset - thumbLeft.offset + 1}%`,
            left: `${thumbLeft.offset}%`,
          }"
        />

        <p
          v-if="thumbRight.dragging"
          class="absolute bottom-6 text-xs rounded-full w-8 h-8 flex items-center justify-center bg-rose-700 select-none"
          :style="{
            left: `${thumbRight.offset}%`,
          }"
        >
          {{ modelValue.toFixed(1) }}
        </p>
      </div>
    </div>

    <div>
      <p>{{ range }}</p>
      <div class="flex p-2 pb-0 justify-between">
        <p v-for="i in pipStep" class="select-none text-xs text-neutral-500 font-bold">
          {{ i * pipStep }}
        </p>
      </div>
    </div>
  </div>
</template>
