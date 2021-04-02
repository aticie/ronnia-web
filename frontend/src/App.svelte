<script>
  import { tokenStore } from "./store.js";
  import Cookies from "js-cookie";
  import axios from "axios";
  import SettingsCheckbox from "./components/SettingsCheckbox.svelte";
  import Button from "./components/Button.svelte";

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
    <div class="container">
      <div class="header">
        <h1>Ronnia Dashboard</h1>
      </div>
      <div class="content">
        {#if $tokenStore != 0}
          logged in as: {user_name}.
          <Button
            text="Logout"
            identifier="logoutButton"
            onClick={() => {
              tokenStore.delToken();
            }}
          />

          <div class="settings">
            {#each settings as { id, key, default_value, description }}
              <div class="setting">
                <div class="checkbox">
                  <SettingsCheckbox
                    checked={default_value == "1" ? true : false}
                    onClick={(checked) => {
                      console.log(checked);
                    }}
                  />
                </div>
                <div class="command">
                  {key}
                </div>
                <div class="description">
                  {description}
                </div>
              </div>
            {/each}
          </div>
        {/if}

        {#if $tokenStore == 0}
          <p>Log in to Ronnia with</p>
          <div class="login_buttons">
            <div>
              <Button
                text="Login"
                onClick={() => {
                  window.location.href = "/osu_authorize";
                }}
                logo="./Logo/OsuLogo.svg"
                identifier="osuLoginButton"
              />
            </div>
            <div>
              <Button
                text="Login"
                onClick={() => {
                  window.location.href = "/twitch_authorize";
                }}
                logo="./Logo/TwitchLogo.svg"
                identifier="twitchLoginButton"
              />
            </div>
          </div>
        {/if}
      </div>
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
    margin-top: 50px;
  }
  .header h1 {
    color: #e84545;
  }
  .login_buttons {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
  }
  .content {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .settings {
    display: flex;
    flex-direction: column;
    text-align: left;
    margin-top: 20px;
  }
  .setting {
    margin-top: 5px;
    margin-bottom: 5px;

    font-size: 26px;
    display: grid;
    grid-template-columns: 70px 120px auto;
    align-items: center;
  }
  .checkbox {
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
