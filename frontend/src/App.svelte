<script>
  import { tokenStore } from "./store.js";
  import Cookies from "js-cookie";
  import axios from "axios";
  import Logout from "./components/Logout.svelte";

  let cookieToken = Cookies.get("token");
  if (cookieToken) {
    tokenStore.setToken(cookieToken);
    Cookies.remove("token");
  }

  if ($tokenStore != 0) {
    let user_name;
    axios
      .get("/user_details", { params: { jwt_token: $tokenStore } })
      .then((res) => {
        user_name = res["username"];
      });
  }
</script>

<html lang="en">
  <body>
    <div>
      <center>
        {#if $tokenStore != 0}
          logged in with token: {$tokenStore}.
          <Logout />
        {/if}

        {#if $tokenStore == 0}
          <h1>Login using the following links:</h1>
          <a
            href="https://osu.ppy.sh/oauth/authorize?response_type=code&client_id=2408&redirect_uri=http://localhost:8000/identify&scope=identify"
            >osu!</a
          >
        {/if}
      </center>
    </div>
  </body>
</html>

<style>
  body,
  html {
    background: #db9065;
  }
  div {
    padding: 8px;
  }
</style>
