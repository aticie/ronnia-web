<script>
  import Cookies from "js-cookie";

  let signupCookie = Cookies.get("signup");
</script>

<div class="page-content items-center">
  <p class="text-center font-semibold">Complete your sign-up to Ronnia with</p>

  {#if signupCookie == "twitch"}
    <button class="button b-with-icon w-1/2">
      <img src="/public/osu!LogoWhite.svg" alt="osu icon" />
      osu! 
    </button>
  {:else}
    <button class="button b-with-icon w-1/2">
      <img src="/public/TwitchGlitchWhite.svg" alt="twitch icon" />
      Twitch
    </button>
  {/if}

</div>
