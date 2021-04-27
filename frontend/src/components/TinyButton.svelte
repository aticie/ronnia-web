<script>
  export let text;
  export let logo;
  export let onClick = () => {};
</script>

<button
  on:click={onClick}
  >

  {#if logo}
    <div class="logo" >
      <img src={logo} alt="" crossorigin="anonymous">
    </div>
  {/if}
  
  <div class="text">{text}</div>  
</button>

<style>
  button {
    position: relative;

    width: 100px;
    height: 40px;
    background-color: #c43737;
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

    transition: background-position 300ms;
  }
  div {
    transition: transform 250ms;
  }
  button:hover {
    background-position: 0% 70%;
  }
  button:hover > div {
    transform: translateY(-2px);
  }
  .logo {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .text {
    font-size: 14pt;
  }
</style>
