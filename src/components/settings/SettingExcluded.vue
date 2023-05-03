<script setup lang="ts">
import BaseButton from "../base/BaseButton.vue";
import SettingBase from "./SettingBase.vue";
import IconAdd from "../icons/IconAdd.vue";
import IconDelete from "../icons/IconDelete.vue";
import { ref } from "vue";
import { useVModel } from "@vueuse/core";

const props = defineProps<{
  modelValue: string[];
}>();
const emit = defineEmits(["update:modelValue"]);
const ids = useVModel(props, "modelValue", emit);

const userId = ref("");
// const userIds = ref<Array<number>>([]);

const addUser = () => {
  if (!userId.value) return;
  ids.value.unshift(userId.value);
  userId.value = "";

  // userIds.value.unshift(userId.value);
  // userId.value = undefined;
};

const removeUser = (index: number) => {
  // userIds.value.splice(index, 1);
};
</script>

<template>
  <SettingBase class="flex-col gap-2">
    <p class="text-neutral-500 font-bold text-left w-full text-sm ml-2">
      User to be excluded
    </p>

    <div class="flex flex-wrap gap-2 w-full">
      <input
        v-model="userId"
        @keyup.enter="addUser"
        class="bg-neutral-950 rounded p-2 grow"
      />
      <BaseButton @click="addUser">
        <template #icon>
          <IconAdd />
        </template>
        <p>Add</p>
      </BaseButton>
    </div>

    <p class="text-neutral-500 font-bold text-left w-full text-sm ml-2 mt-2">
      Users
    </p>
    <ul
      class="bg-neutral-950 max-h-60 overflow-y-auto w-full relative rounded divide-y divide-neutral-800 overflow-hidden"
    >
      <p
        v-if="ids.length === 0"
        class="p-2 text-center text-neutral-700 text-sm"
      >
        You can add users that should be excluded here!
      </p>
      <li
        v-for="(id, index) in ids"
        :key="id"
        class="flex items-center justify-between p-1 group"
      >
        <p class="ml-2">{{ id }}</p>
        <BaseButton @click="removeUser(index)">
          <template #icon>
            <IconDelete />
          </template>
          <p>Delete</p>
        </BaseButton>
      </li>
    </ul>
  </SettingBase>
</template>
