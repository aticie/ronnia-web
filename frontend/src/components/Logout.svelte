<script>
  import OsuLogo from "./Logo/OsuLogo.svg";
  import anime from "animejs/lib/anime.es.js";
  import { tokenStore } from "../store.js"

  function mouseEnterAnimate() {
    anime({
      targets: ["#osulogo", "#osutext"],
      translateX: "-=100",
      easing: "easeOutExpo",
    });
    anime({
      targets: "#osuimg",
      translateY: 0,
      easing: "easeOutExpo",
    });
  }

  function mouseLeaveAnimate() {
    anime({
      targets: ["#osulogo", "#osutext"],
      translateX: 0,
      easing: "easeOutExpo",
    });
    anime({
      targets: "#osuimg",
      translateY: 200,
      easing: "easeOutExpo",
    });
  }
</script>

<button
  on:click={() => {
    tokenStore.delToken();
  }}
  on:mouseenter={mouseEnterAnimate}
  on:mouseleave={mouseLeaveAnimate}
  >
  <div class="img" id="osuimg" style="transform: translateY(200px);">
    <img src="https://osu.ppy.sh/assets/images/button.16de7c2c.svg" alt=""/>
  </div>
  <div class="text" id="osutext">Logout</div>
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
    outline: none;

    overflow: hidden;
  }
  .img {
    position: absolute;
    width: 100%;
  }
  .img img {
    width: 100%;
  }
  .text {
    flex-grow: 1;
  }
</style>
