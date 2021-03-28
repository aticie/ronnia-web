<script>
  import TwitchLogo from "./Logo/TwitchLogo.svelte";
  import anime from "animejs/lib/anime.es.js";

  function mouseEnterAnimate() {
    anime({
      targets: ["#twitchlogo", "#twitchtext"],
      translateX: "-=100",
      easing: "easeOutExpo",
    });
    anime({
      targets: "#twitchimg",
      translateY: 0,
      easing: "easeOutExpo",
    });
  }

  function mouseLeaveAnimate() {
    anime({
      targets: ["#twitchlogo", "#twitchtext"],
      translateX: 0,
      easing: "easeOutExpo",
    });
    anime({
      targets: "#twitchimg",
      translateY: 200,
      easing: "easeOutExpo",
    });
  }
</script>

<button
  on:click={(_) => {
    window.location.href = "/twitch_authorize";
  }}
  on:mouseenter={mouseEnterAnimate}
  on:mouseleave={mouseLeaveAnimate}
  >
  <div class="img" id="twitchimg" style="transform: translateY(200px);">
    <!-- <img src="https://twitch.ppy.sh/assets/images/button.16de7c2c.svg" alt=""/> -->
    <img src="https://osu.ppy.sh/assets/images/button.16de7c2c.svg" alt=""/>
  </div>
  <div class="logo" id="twitchlogo">
    <TwitchLogo />
  </div>
  <div class="text" id="twitchtext">Twitch</div>
</button>

<style>
  button {
    position: relative;

    width: 316px;
    height: 62px;
    background-color: #e84545;
    border: none;
    border-radius: 10px;
    margin-top: 5px;
    margin-left: 5px;
    margin-right: 5px;

    color: white;
    font-family: "Roboto", sans-serif;
    font-size: 16pt;

    display: flex;
    justify-content: center;
    align-items: center;
    flex-grow: 1;

    overflow: hidden;
  }
  .img {
    position: absolute;
    width: 100%;
  }
  .img img {
    width: 100%;
  }
  .logo {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .text {
    flex-grow: 1;
  }
</style>
