<script setup lang="ts">
import ky from "ky";
import { useCookies } from '@vueuse/integrations/useCookies';
import { useRouter } from 'vue-router';

const router = useRouter();
const cookies = useCookies();
const token = cookies.get<string>('token');
if (!token && !import.meta.env.DEV) router.replace("/login");

try {
  const userDetails: UserDetails = await ky.get("user_details", {
    prefixUrl: import.meta.env.VITE_API_BASE,
    searchParams: {
      jwt_token: token
    }
  }).json();


} catch {
  if (!import.meta.env.DEV) {
    cookies.remove("token");
    router.replace("/login");
  }
}
</script>

<template>
  <div>
    <p>settings</p>
  </div>
</template>
