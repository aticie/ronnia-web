<script setup lang="ts">
import BaseButton from '../components/BaseButton.vue';
import BaseIcon from '../components/BaseIcon.vue';
import IconTwitch from "../components/icons/IconTwitch.vue";
import IconOsu from "../components/icons/IconOsu.vue";
import { useCookies } from '@vueuse/integrations/useCookies';

type SignupTypes = "twitch" | "osu";

const cookies = useCookies();
const signup = cookies.get<SignupTypes>("signup");

const twitchAuth = import.meta.env.VITE_TWITCH_AUTH;
const osuAuth = import.meta.env.VITE_OSU_AUTH;
</script>

<template>
  <div>
    <p v-if="!signup" class="text-neutral-500 font-bold mb-1">Log in Ronnia with:</p>
    <p v-else class="text-neutral-500 font-bold mb-1">Complete your sign-up to Ronnia with</p>

    <div class="flex gap-2">
      <a v-if="!signup || signup === 'osu'" :href="twitchAuth" class="flex w-full">
        <BaseButton>
          <BaseIcon>
            <IconTwitch />
          </BaseIcon>
          <p>Twitch</p>
        </BaseButton>
      </a>

      <a v-if="!signup || signup === 'twitch'" :href="osuAuth" class="flex w-full">
        <BaseButton>
          <BaseIcon>
            <IconOsu />
          </BaseIcon>
          <p>osu!</p>
        </BaseButton>
      </a>
    </div>
  </div>
</template>
