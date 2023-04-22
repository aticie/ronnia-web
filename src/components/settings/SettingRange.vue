<script setup lang="ts">
import SettingBase from "./SettingBase.vue";
import BaseRange from "../BaseRange.vue";
import { SettingRange } from "../../types";
import { ref, toRef } from "vue";

const props = defineProps<{
  data: SettingRange;
}>();

let start = props.data.range_start === -1 ? 0 : props.data.range_start;
let end = props.data.range_end === -1 ? 10 : props.data.range_end;

const values = ref<[number, number]>([start, end]);
</script>

<template>
  <SettingBase>
    <BaseRange
      v-model="values"
      :min="0"
      :max="10"
      range
    />
  </SettingBase>
</template>
