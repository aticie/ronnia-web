<script setup lang="ts">
import SettingBase from "./SettingBase.vue";
import BaseRange from "../BaseRange.vue";
import { SettingRange } from "../../types";
import { ref, toRef } from "vue";

const props = defineProps<{
  data: SettingRange;
}>();

const values = ref<[number, number]>([props.data.range_start, props.data.range_end]);
</script>

<template>
  <SettingBase>
    <BaseRange
      v-model="values"
      :min="0"
      :max="100"
      :pipStep="10"
      range
    />
  </SettingBase>
</template>
