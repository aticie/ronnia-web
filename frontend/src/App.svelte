<script>
  import { tokenStore } from "./store.js";
  import Cookies from "js-cookie";
  import axios from "axios";
  import Logout from "./components/Logout.svelte";
  import OsuLogin from "./components/OsuLogin.svelte";
  import TwitchLogin from "./components/TwitchLogin.svelte";

  tokenStore.useLocalStorage();
  let cookieToken = Cookies.get("token");
  let user_name;
  let settings = [];

  if (cookieToken) {
    tokenStore.setToken(cookieToken);
    Cookies.remove("token");
  }

  if ($tokenStore != 0) {
    axios
      .get("/user_details", { params: { jwt_token: $tokenStore } })
      .then((res) => {
        user_name = res.data["osu_username"];
      });
    axios.get("/get_all_settings").then((res) => {
      settings = res.data;
    });
  }
  if ($tokenStore == 0) {
  }
</script>

<html lang="en">
  <body>
    <div>
      <center>
        {#if $tokenStore != 0}
          logged in as: {user_name}.
          <Logout />
          {#each settings as { id, key, default_value, description }}
            {id}: {key} - {default_value} - {description} <br>
          {/each}
        {/if}

        {#if $tokenStore == 0}
          <div class="header">
            <h1>Ronnia Dashboard</h1>
            <p>Log in to Ronnia with</p>
            <div class="login_buttons">
              <div class="osu">
                <OsuLogin />
              </div>
              <div class="twitch">
                <TwitchLogin />
              </div>
            </div>
          </div>
        {/if}
      </center>
    </div>
  </body>
</html>

<style>
  h1 {
    font-size: 30pt;
  }
  p {
    font-size: 16pt;
  }
  .header {
    margin-top: 10%;
  }
  .login_buttons {
    display: flex;
    justify-content: center;
  }
</style>
