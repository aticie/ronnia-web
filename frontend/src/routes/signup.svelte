<script>
  import Cookies from "js-cookie";
  import {toOsuAuth, toTwitchAuth} from "../utils";

  let signupCookie = Cookies.get("signup");
</script>

<div class="page-content items-center">
  <p class="text-center font-semibold">Complete your sign-up to Ronnia with</p>

  {#if signupCookie == "twitch"}
    <button class="button b-with-icon w-1/2" on:click={toTwitchAuth}>
      <img src="/public/osu!LogoWhite.svg" alt="osu icon" />
      osu! 
    </button>
  {:else}
    <button class="button b-with-icon w-1/2" on:click={toOsuAuth}>
      <img src="/public/twitchGlitchWhite.svg" alt="twitch icon" />
      Twitch
    </button>
  {/if}

</div>
