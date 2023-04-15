<script setup lang="ts">
import SettingBase from "./SettingBase.vue";
import BaseRange from "../BaseRange.vue";

defineProps<{
  data: SettingRange
}>();
</script>

<template>
  <SettingBase>
    <BaseRange v-model="data.range_end" :min="0" :max="100" :pipStep="10" />
  </SettingBase>
</template>
