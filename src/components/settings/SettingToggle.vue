<script setup lang="ts">
import SettingBase from "./SettingBase.vue";
import BaseCheckbox from '../BaseCheckbox.vue';

defineProps<{
  data: SettingToggle
}>();
</script>

<template>
  <SettingBase>
    <label :for="data.id.toString()" class="select-none w-full">{{ data.description }}</label>
    <BaseCheckbox :id="data.id" v-model="data.value" />
  </SettingBase>
</template>
