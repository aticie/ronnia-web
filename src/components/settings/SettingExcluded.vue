<script setup lang="ts">
import BaseButton from "../base/BaseButton.vue";
import SettingBase from "./SettingBase.vue";
import IconAdd from "../icons/IconAdd.vue";
import IconDelete from "../icons/IconDelete.vue";
import {ref} from "vue";
import {useFetch, useVModel} from "@vueuse/core";
import {useBus} from "../../composables";

const props = defineProps<{
  modelValue: string[];
}>();
const emit = defineEmits(["update:modelValue"]);
const ids = useVModel(props, "modelValue", emit);
const bus = useBus();

const userId = ref("");

const excludeBaseUrl = `${import.meta.env.VITE_API_BASE}/user/exclude`;

const {data} = await useFetch(
    excludeBaseUrl,
    {credentials: "include"}
).json();
ids.value = data.value;

const addUser = async () => {
  if (!userId.value) return;
  if (userId.value in ids.value) {
    bus.emit({
      title: "Error while adding user!",
      description: "User already exists!",
    });
    return;
  }

  let user = userId.value
  const params = new URLSearchParams({
    excluded_user: user
  });
  const addUserUrl = `${excludeBaseUrl}?` + params.toString()
  const {statusCode, error, data} = await useFetch(
      addUserUrl,
      {
        credentials: "include",
      }
  ).post().text();

  if (statusCode.value !== 200) {
    bus.emit({
      title: "Error while adding user!",
      description: error.value,
    });
  } else {
    bus.emit({title: `Added ${data.value} to excluded users!`});
    ids.value.unshift(user);
    userId.value = "";
  }
};

const removeUser = async (index: number) => {
  let user = ids.value[index];
  const params = new URLSearchParams({
    excluded_user: user
  });
  const url = `${import.meta.env.VITE_API_BASE}/user/exclude?` + params.toString()
  const {statusCode, error, data} = await useFetch(
      url,
      {
        credentials: "include",
      }
  ).delete().text();

  if (statusCode.value !== 200) {
    bus.emit({
      title: "Error while removing user!",
      description: error.value,
    });
  } else {
    bus.emit({title: `Removed ${data.value} from excluded users!`});
    ids.value.splice(index, 1);
  }
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
          <IconAdd/>
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
            <IconDelete/>
          </template>
          <p>Delete</p>
        </BaseButton>
      </li>
    </ul>
  </SettingBase>
</template>
