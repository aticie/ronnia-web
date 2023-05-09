<script setup lang="ts" generic="T extends [number, number] | number">
import { ref, computed, StyleValue, watch, onMounted } from "vue";
import { useMouseInElement, useMousePressed } from "@vueuse/core";
import { interpolate } from "../../utils";

interface Props {
  modelValue: T;
  min: number;
  max: number;
  range?: boolean;
  pipStep?: number;
}

interface Emits {
  (e: "update:modelValue", payload: [number, number] | number): void;
}

const emit = defineEmits<Emits>();
const xprops = defineProps<Props>();

// workaround until vue 3.3 lands
const props = xprops as unknown as Props;

type Element = HTMLElement | null;

const thumbRight = ref<Element>(null);
const thumbLeft = ref<Element>(null);
const track = ref<Element>(null);

const { elementWidth, elementX } = useMouseInElement(track, {
  handleOutside: false,
});
const { pressed: pressRight } = useMousePressed({ target: thumbRight });
const { pressed: pressLeft } = useMousePressed({ target: thumbLeft });

let right = Array.isArray(props.modelValue)
  ? props.modelValue[1]
  : props.modelValue;

const currentXRight = ref();
const currentXLeft = ref(0);

onMounted(() => {
  if (!track.value) return;

  // default values for position of thumbs, Updated on mouse event.
  let interpolatedRight = interpolate(
    right as number,
    props.min,
    0,
    props.max,
    track.value.clientWidth
  );
  currentXRight.value = interpolatedRight;

  // same for left thumb
  if (props.range && Array.isArray(props.modelValue)) {
    currentXLeft.value = interpolate(
      props.modelValue[0],
      props.min,
      0,
      props.max,
      track.value.clientWidth
    );
  }
});

const thumbRightStyle = computed<StyleValue>(() => {
  return {
    left: `${(currentXRight.value * 100) / elementWidth.value}%`,
    transform: "translateX(-50%)",
  };
});

const trackStyle = computed<StyleValue>(() => {
  // left offset of track should be zero if there is no left thumb, else
  // should be offset of left thumb
  let left = currentXLeft.value
    ? (currentXLeft.value * 100) / elementWidth.value
    : 0;

  return {
    width: `${(currentXRight.value * 100) / elementWidth.value - left}%`,
    left: `${left}%`,
  };
});

const thumbLeftStyle = computed<StyleValue>(() => {
  if (!currentXLeft.value) return {};

  return {
    left: `${(currentXLeft.value * 100) / elementWidth.value}%`,
    transform: "translateX(-50%)",
  };
});

const clamp = (x: number, x1: number, x2: number) => {
  return Math.max(x1, Math.min(x, x2));
};

// update thumb positions if they are pressed
watch(elementX, () => {
  if (!thumbRight.value) return;

  // clamp the x so it doesn't overflow from left or right
  let clampedX = clamp(elementX.value, 0, elementWidth.value);

  if (pressRight.value) {
    currentXRight.value = clampedX;

    // block right thumb from going more to the right than the left thumb
    if (currentXLeft.value && props.range) {
      currentXRight.value = Math.max(currentXRight.value, currentXLeft.value);
    }
  } else if (pressLeft.value && props.range) {
    // cap thumb value so it doesn't overflow
    currentXLeft.value = Math.min(currentXRight.value, clampedX);
  }

  // update the values that are given with v-model after interpolation.
  emit(
    "update:modelValue",
    Array.isArray(props.modelValue) && currentXLeft.value !== undefined
      ? [
          interpolate(
            currentXLeft.value,
            0,
            props.min,
            elementWidth.value,
            props.max
          ),
          interpolate(
            currentXRight.value,
            0,
            props.min,
            elementWidth.value,
            props.max
          ),
        ]
      : interpolate(
          currentXRight.value,
          0,
          props.min,
          elementWidth.value,
          props.max
        )
  );
});
</script>

<template>
  <div class="w-full">
    <div ref="track" class="w-full flex items-center relative h-8">
      <div class="absolute h-3 rounded-full w-full bg-neutral-950" />
      <div class="absolute h-3 rounded-full bg-rose-700" :style="trackStyle" />

      <button
        v-if="range"
        ref="thumbLeft"
        :style="thumbLeftStyle"
        class="absolute w-5 h-5 bg-rose-800 rounded-full"
      />
      <button
        ref="thumbRight"
        :style="thumbRightStyle"
        class="absolute w-5 h-5 bg-rose-800 rounded-full"
      />

      <p
        v-if="pressRight"
        class="absolute mb-16 bg-rose-700 text-xs rounded-lg p-1"
        :style="thumbRightStyle"
      >
        <slot :values="modelValue">{{ modelValue }}</slot>
      </p>

      <p
        v-if="pressLeft && range"
        class="absolute mb-16 bg-rose-700 text-xs rounded-lg p-1"
        :style="thumbLeftStyle"
      >
        <slot name="left" :values="modelValue">{{ modelValue }}</slot>
      </p>
    </div>

    <div v-if="pipStep" class="flex relative mb-4">
      <p
        v-for="i in max / pipStep + 1"
        class="absolute select-none text-xs text-neutral-500 font-bold"
        :style="{
          left: `${(100 / (max / pipStep)) * (i - 1)}%`,
          transform: 'translateX(-50%)',
        }"
      >
        {{ i - 1 }}
      </p>
    </div>
  </div>
</template>
