<script>
  import { tokenStore } from "./store.js";
  import Cookies from "js-cookie";
  import axios from "axios";
  import SettingsCheckbox from "./components/SettingsCheckbox.svelte";
  import Button from "./components/Button.svelte";
  import TinyButton from "./components/TinyButton.svelte";
  import SettingsSaveButton from "./components/SettingsSaveButton.svelte";
  import InputBox from "./components/InputBox.svelte";

  tokenStore.useLocalStorage();
  let cookieToken = Cookies.get("token");
  let error = Cookies.get("error");
  let user_name;
  let user_avatar_url;
  let user_id_db;
  let user_settings = [];

  if (cookieToken) {
    tokenStore.setToken(cookieToken);
    Cookies.remove("token");
  }

  if (error) {
    Cookies.remove("error");
  }

  if ($tokenStore != 0) {
    axios
      .get("/user_details", { params: { jwt_token: $tokenStore } })
      .then((res) => {
        user_name = res.data["osu_username"];
        user_avatar_url = res.data["avatar_url"];
        //user_avatar_url = "https://a.ppy.sh/" + res.data["osu_id"];
        user_id_db = res.data["user_id"];
        axios
          .get("/get_user_settings", { params: { user_id: user_id_db } })
          .then((res) => {
            user_settings = res.data;
          });
      });
  }
  if ($tokenStore == 0) {
  }

  let buttonDisabled = false;
  let errorText = "";

  function handleInputBoxMessage(event) {
    let message = event.detail;
    if (message.error) {
      buttonDisabled = true;
      errorText = message.error;
    } else {
      buttonDisabled = false;
      errorText = "";
    }
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
          <div class="userbox">
            <div
              alt="Avatar"
              class="rounded-circle avatar"
              crossorigin="anonymous"
              style="background-image: url('{user_avatar_url}')"
            ></div>
            <div class="profile-info">
              {user_name}
            </div>
            <TinyButton
              text="Logout"
              identifier="logoutButton"
              onClick={() => {
                tokenStore.delToken();
              }}
            />
          </div>
          <div class="settings">
            {#each user_settings as setting}
              <div class="setting">
                {#if setting.type === "toggle"}
                  <div class="checkbox">
                    <SettingsCheckbox bind:checked={setting.value} />
                  </div>
                {:else}
                  <div class="inputbox">
                    <InputBox
                      key={setting.key}
                      bind:min_value={setting.range_start}
                      bind:max_value={setting.range_end}
                      on:message={handleInputBoxMessage}
                    />
                  </div>
                {/if}
                <div class="command">
                  {setting.key == "sr" ? "min sr\nmax sr" : setting.key}
                </div>
                <div class="description">
                  {setting.description}
                </div>
              </div>
            {/each}
          </div>
          <div class="errortext">{errorText}</div>
          <div class="savebutton">
            <SettingsSaveButton
              bind:disabled={buttonDisabled}
              settings={user_settings}
              user_id={user_id_db}
              timeout_secs="2000"
            />
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
          {#if error}
            <div class="errortext">
              You are not registered to ronnia<br>
              Add heyronii#9925 on discord for registration.<br>
              <a href=https://github.com/aticie/ronnia>Check out project page for more details.</a>
            </div>
          {/if}
        {/if}
      </div>
    </div>
    <footer>
      Thanks to Sibyl#3838 and bora#5130 for website and frontend design.
    </footer>
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
  .rounded-circle {
    height: 64px;
    width: 64px;
    border-radius: 50%;
  }
  .avatar {
    background-size: cover;
  }
  .profile-info {
    font-size: x-large;
    margin-left: 10px;
    margin-right: 5px;
  }
  .userbox {
    display: flex;
    align-items: center;
  }
  .inputbox {
    display: flex;
    flex-direction: column;
  }
  .errortext {
    color: #e84545;
    margin: 30px 10px;
  }
  footer{
    margin: 1% 1%;
  }
</style>
