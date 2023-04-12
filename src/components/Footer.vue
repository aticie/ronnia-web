<script setup lang="ts">
import IconDiscord from './icons/IconDiscord.vue';
import IconGithub from './icons/IconGithub.vue';
import BaseIcon from './BaseIcon.vue';
</script>

<template>
  <footer class="sticky bottom-0 hidden sm:flex items-center justify-between p-2 bg-neutral-900">
    <p class="text-neutral-500 text-sm font-bold">Thanks to Sibyl#3838 and bora#5130 for website and frontend design.</p>
    
    <div class="flex gap-2">
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
  </footer>
</template>
