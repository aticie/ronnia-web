<script>
  import { toOsuAuth, toTwitchAuth } from "../utils";
</script>

<div class="page-content">
  <p class="text-neutral-500 font-semibold">Log in to Ronnia with</p>
  <div class="flex flex-1 flex-col md:flex-row gap-2">
    <button class="button b-with-icon flex-1" on:click={toTwitchAuth}>
      <img src="/public/twitchGlitchWhite.svg" alt="twitch icon" />
      Twitch
    </button>
    <button class="button b-with-icon flex-1" on:click={toOsuAuth}>
      <img src="/public/osu!LogoWhite.svg" alt="twitch icon" />
      osu!
    </button>
  </div>
</div>
