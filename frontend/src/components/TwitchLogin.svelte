<button
  on:click={(_) => {
    window.location.href = "/twitch_authorize";
  }}
>
</button>

<style>
  button{
    transition: ease-in-out 0.2s;
    background-image: url('/images/twitch-logo.svg');
    background-color: transparent;
    border:none;
    outline:none;
    width: 90px;
    height: 90px;
    margin: 15px;
    margin-top: 30px;
  }
  button:hover{
    filter: brightness(0.5);
  }
</style>
