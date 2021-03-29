<script>
  import anime from "animejs/lib/anime.es.js";

  export let text;
  export let logo;
  export let onClick = () => {};
  export let identifier;
  let logoidentifier = `${identifier}logo`;

  function mouseEnterAnimate() {
    anime({
      targets: [`#${logoidentifier}`, `#${identifier}`],
      translateX: -100,
      easing: "easeOutExpo",
      duration: 500
    });
  }

  function mouseLeaveAnimate() {
    anime({
      targets: [`#${logoidentifier}`, `#${identifier}`],
      translateX: 0,
      easing: "easeOutExpo",
      duration: 500
    });
  }
</script>

<button
  on:click={onClick}
  on:mouseenter={mouseEnterAnimate} 
  on:mouseleave={mouseLeaveAnimate}
  >

  {#if logo}
    <div class="logo" id={logoidentifier}>
      <img src={logo} alt="">
    </div>
  {/if}
  
  <div class="text" id={identifier}>{text}</div>  
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
    outline: none;
    overflow: hidden;

    background-image: url("https://osu.ppy.sh/assets/images/button.16de7c2c.svg");
    background-size: cover;
    background-position: 0% 10%;
    transition-duration: 300ms;
  }
  button:hover {
    background-position: 0% 50%;
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
