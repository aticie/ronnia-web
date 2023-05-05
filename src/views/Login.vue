<script setup lang="ts">
import BaseSuspense from "../components/base/BaseSuspense.vue";
import BaseButton from "../components/base/BaseButton.vue";
import BaseIcon from "../components/base/BaseIcon.vue";
import IconDiscord from "../components/icons/IconDiscord.vue";
import IconTwitch from "../components/icons/IconTwitch.vue";
import IconGithub from "../components/icons/IconGithub.vue";
import IconOsu from "../components/icons/IconOsu.vue";
import TheLiveStreams from "../components/TheLiveStreams.vue";
import { useCookies } from "@vueuse/integrations/useCookies";
import { useWindowSize } from "@vueuse/core";

type SignupTypes = "twitch" | "osu";

const { width } = useWindowSize();
const cookies = useCookies();
const signup = cookies.get<SignupTypes>("signup");

const twitchAuth = import.meta.env.VITE_TWITCH_AUTH;
const osuAuth = import.meta.env.VITE_OSU_AUTH;
</script>

<template>
  <div class="w-full pt-32 flex flex-col gap-8 justify-center min-h-full lg:min-h-0 max-w-sm rounded z-10">
    <div class="flex flex-col gap-10">
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
  </div>

  <BaseSuspense>
    <TheLiveStreams v-if="width > 1024" />
  </BaseSuspense>
</template>
