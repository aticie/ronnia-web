<script>
  import { tokenStore } from "../store.js";
</script>

<button on:click={_ => tokenStore.delToken()}>
  Logout
</button>
