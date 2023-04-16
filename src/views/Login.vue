<script setup lang="ts">
import BaseButton from '../components/BaseButton.vue';
import BaseIcon from '../components/BaseIcon.vue';
import IconTwitch from "../components/icons/IconTwitch.vue";
import IconDiscord from '../components/icons/IconDiscord.vue';
import IconGithub from '../components/icons/IconGithub.vue';
import IconOsu from "../components/icons/IconOsu.vue";
import { useCookies } from '@vueuse/integrations/useCookies';

type SignupTypes = "twitch" | "osu";

const cookies = useCookies();
const signup = cookies.get<SignupTypes>("signup");

const twitchAuth = import.meta.env.VITE_TWITCH_AUTH;
const osuAuth = import.meta.env.VITE_OSU_AUTH;
</script>

<template>
  <div class="grid gap-8 w-full max-w-sm rounded">
    <div class="flex flex-col gap-20">
      <div class="flex justify-center items-end -ml-8">
        <img src="/favicon.png" class="h-10 -mr-1 -mb-0.5" />
        <h1 class="font-bold text-center">onnia Dashboard</h1>
      </div>

      <div class="grid gap-2">
        <div class="ml-0.5 font-semibold">
          <p v-if="!signup">Log in with:</p>
          <p v-else>Complete your sign-up to Ronnia with</p>
        </div>

        <a v-if="!signup || signup === 'osu'" :href="twitchAuth">
          <BaseButton class="w-full">
            <template #icon>
              <IconTwitch />
            </template>
            <p>Twitch</p>
          </BaseButton>
        </a>

        <a v-if="!signup || signup === 'twitch'" :href="osuAuth">
          <BaseButton class="w-full">
            <template #icon>
              <IconOsu />
            </template>
            <p>osu!</p>
          </BaseButton>
        </a>
      </div>
    </div>

    <div class="flex flex-col items-start">
      <p class="text-xs text-neutral-500 font-bold ml-0.5 mb-1">Links</p>
      <div class="flex rounded overflow-hidden bg-neutral-900 divide-x divide-neutral-950">
        <a href="https://discord.gg/J4WPJsceFc">
          <BaseIcon>
            <IconDiscord />
          </BaseIcon>
        </a>
        <a href="https://github.com/aticie/ronnia-web">
          <BaseIcon>
            <IconGithub />
          </BaseIcon>
        </a>
      </div>
    </div>
  </div>
</template>
