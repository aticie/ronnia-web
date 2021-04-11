<script>
import axios from "axios";


  export let text;
  export let timeout_secs;
  let disabled = false;
  let onClick = () => {
    disabled = true;
    axios.post('/post_user_settings').then((res) => console.log(res));
    setTimeout(() => { disabled = false }, timeout_secs);
  };
</script>

<button {disabled}
  on:click={onClick}
  >
  <div class="text">{text}</div>  
</button>

<style>
  button {
    position: relative;

    width: 250px;
    height: 60px;
    background-color: #00adb5;
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

    transition: background-color 300ms;
  }
  button:hover:not([disabled]) {
    background-color:#00b8a9;
  }
  button:disabled{
    background-color: #aaaaaa;
  }
  .text {
    font-size: 14pt;
  }
</style>
