<script setup lang="ts">
import ky from "ky";
import BaseButton from "../components/BaseButton.vue";
import { useCookies } from '@vueuse/integrations/useCookies';
import { useRouter } from 'vue-router';
import { ref } from "vue";

const router = useRouter();
const cookies = useCookies();
const token = cookies.get<string>('token');
if (!token && !import.meta.env.DEV) router.replace("/login");

const userDetails = ref<UserDetails>();
const error = ref<unknown>();

const fetchUser = async () => {
  try {
    userDetails.value = await ky.get("user_details", {
      prefixUrl: import.meta.env.VITE_API_BASE,
      searchParams: {
        jwt_token: token
      }
    }).json();

    error.value = null;
  } catch (e) {
    if (!import.meta.env.DEV) {
      cookies.remove("token");
      router.replace("/login");
    }

    error.value = e;
  }
}

await fetchUser();
</script>

<template>
  <BaseButton v-if="error" @click="fetchUser">Refetch</BaseButton>
  <div v-else>
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <img :src="userDetails?.avatar_url" class="h-12 aspect-square rounded" />
        <p>{{ userDetails?.osu_username }}</p>
      </div>
      <BaseButton>Logout</BaseButton>
    </div>
  </div>
</template>
