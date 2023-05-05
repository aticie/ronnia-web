<script setup lang="ts">
import { ref } from "vue";
import { useVModel } from "@vueuse/core";
import { useBus } from "../../composables";
import axios from "axios";

import SettingBase from './SettingBase.vue';
import BaseButton from "../base/BaseButton.vue";
import IconDelete from "../icons/IconDelete.vue";
import IconAdd from "../icons/IconAdd.vue";

const props = defineProps<{
  modelValue: string[]
}>();
const emit = defineEmits<{
  (event: "update:modelValue", payload: string[]): void
}>();

const bus = useBus();
const users = useVModel(props, "modelValue", emit);
const user = ref();

const response = await axios.get<string[]>("/user/exclude");
users.value = response.data;

const addExcluded = async () => {
  if (!user.value) return;

  if (users.value.includes(user.value)) {
    bus.emit({
      title: "Error while adding user!",
      description: "User already exists."
    })

    return;
  }

  await axios.post<string[]>("/user/exclude", {}, {
    params: {
      excluded_user: user.value
    }
  });

  users.value.unshift(user.value);

  bus.emit({
    title: `Added ${user.value} to excluded users!`
  })
}

const removeExcluded = async (user: string) => {
  await axios.delete("/user/exclude", {
    params: {
      excluded_user: user
    }
  });

  bus.emit({ title: `Removed ${user} from excluded users!` });

  let index = users.value.findIndex(x => x === user);
  users.value.splice(index, 1);
}
</script>

<template>
  <SettingBase class="flex-col gap-2">
    <p class="text-neutral-500 font-bold text-left w-full text-sm ml-2">
      User to be excluded
    </p>

    <div class="flex flex-wrap gap-2 w-full">
      <input
        v-model="user"
        @keyup.enter="addExcluded"
        class="bg-neutral-950 rounded p-2 grow"
      />
      <BaseButton @click="addExcluded" class="px-2">
        <template #icon>
          <IconAdd />
        </template>
      </BaseButton>
    </div>

    <p class="text-neutral-500 font-bold text-left w-full text-sm ml-2 mt-2">
      Users
    </p>
    <ul
      class="bg-neutral-950 max-h-60 overflow-y-auto w-full relative rounded divide-y divide-neutral-800 overflow-hidden"
    >
      <p
        v-if="users.length === 0"
        class="p-2 text-center text-neutral-700 text-sm"
      >
        You can add users that should be excluded here!
      </p>
      <li
        v-for="user in users"
        :key="user"
        class="flex items-center justify-between p-1 group"
      >
        <p class="ml-2">{{ user }}</p>
        <BaseButton @click="removeExcluded(user)" class="px-2">
          <template #icon>
            <IconDelete />
          </template>
        </BaseButton>
      </li>
    </ul>
  </SettingBase>
</template>
