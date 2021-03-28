<button on:click={_ => {window.location.href = '/osu_authorize'}}>
</button>

<style>
  button{
    transition: ease-in-out 0.2s;
    background-image: url('https://osu.ppy.sh/assets/images/osu-logo-white.59d385da.svg'), url('https://osu.ppy.sh/assets/images/osu-logo-triangles.b1e57c37.svg');
    background-size: auto;
    background-color: transparent;
    border-radius: 100%;
    border:none;
    outline:none;
    width: 100px;
    height: 100px;
    margin: 10px;
    margin-top: 25px;
  }
  button:hover{
    filter: brightness(0.5);
  }
</style>

