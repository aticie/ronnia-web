<script setup lang="ts">
import BaseButton from "../BaseButton.vue";
import SettingBase from "./SettingBase.vue";
import IconAdd from "../icons/IconAdd.vue";
import { ref } from "vue";

const userId = ref<number>();
const userIds = ref<Array<number>>([]);

const addUser = () => {
  if (!userId.value) return;
  userIds.value.push(userId.value);

  userId.value = undefined;
};
</script>

<template>
  <SettingBase class="flex-col gap-2">
    <p class="text-neutral-500 font-bold text-left w-full text-sm ml-2 mt-2">
      User to be excluded
    </p>

    <div class="flex gap-2 w-full">
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
      class="bg-neutral-950 w-full rounded divide-y divide-neutral-800 overflow-hidden"
    >
      <p
        v-if="userIds.length === 0"
        class="p-2 text-center text-neutral-700 text-sm"
      >
        You can add users that should be excluded here!
      </p>
      <li
        v-for="id in userIds"
        :key="id"
        class="p-2 hover:bg-neutral-800 transition-colors"
      >
        {{ id }}
      </li>
    </ul>
  </SettingBase>
</template>
