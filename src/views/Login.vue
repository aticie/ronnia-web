<script setup lang="ts">
import BaseSuspense from "../components/base/BaseSuspense.vue";
import BaseButton from "../components/base/BaseButton.vue";
import BaseIcon from "../components/base/BaseIcon.vue";
import TheLiveStreams from "../components/TheLiveStreams.vue";
import IconDiscord from "../components/icons/IconDiscord.vue";
import IconTwitch from "../components/icons/IconTwitch.vue";
import IconGithub from "../components/icons/IconGithub.vue";
import IconOsu from "../components/icons/IconOsu.vue";

import { ref } from "vue";
import { useWindowSize } from "@vueuse/core";
import { useRouter } from "vue-router";
import { useUserStore } from "../store";

const { width } = useWindowSize();
const router = useRouter();
const userStore = useUserStore();
const signup = ref<SignupTypes>();

type SignupTypes = "osu" | "twitch";

try {
  const isSignup = await userStore.getUser();
  if (isSignup) signup.value = isSignup;

  router.replace("/settings");
} catch {}

const twitchAuth = import.meta.env.VITE_TWITCH_AUTH;
const osuAuth = import.meta.env.VITE_OSU_AUTH;
</script>

<template>
  <div class="w-full snap-center">
    <div class="h-screen max-w-sm mx-auto flex flex-col pt-32 gap-10">
      <div class="flex justify-center items-end -ml-8">
        <h1 class="font-bold text-center text-xl">
          <span
            class="text-rose-700 text-2xl translate-y-[0.450px] translate-x-[3px] inline-block"
            >R</span
          >
          onnia Dashboard
        </h1>
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

      <div class="flex flex-col items-start">
        <p class="text-xs text-neutral-500 font-bold ml-0.5 mb-1">Links</p>
        <div
          class="flex rounded overflow-hidden bg-neutral-900 divide-x divide-neutral-950"
        >
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

      <BaseSuspense v-if="width > 1024">
        <TheLiveStreams />
      </BaseSuspense>
    </div>
  </div>

  <div class="h-screen bg-green-500 snap-center">
    <p>hey</p>
  </div>
</template>
