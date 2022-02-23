<script>
import { toast } from '@zerodevx/svelte-toast'
import axios from "axios";

  export let settings;
  export let jwt_token;
  export let timeout_secs;
  export let disabled;
  let onClick = async () => {
    disabled = true;
    await axios.post('/save_user_settings', {jwt_token, settings});
    toast.push('Saved your settings!');
    setTimeout(() => { disabled = false }, timeout_secs);
  };
</script>

<button {disabled}
  on:click={onClick}
  >
  <div class="text">SAVE</div>  
</button>

<style>
  button {
    position: relative;

    width: 12rem;
    height: 4rem;
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

    transition: background-color 300ms;
  }
  button:hover:not([disabled]) {
    background-color:#fd6a61;
  }
  button:disabled{
    background-color: #aaaaaa;
  }
  .text {
    font-size: 14pt;
  }
</style>
