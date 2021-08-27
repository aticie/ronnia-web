<script>
  import { Router, Route, Link, navigate } from "svelte-navigator";
  import { tokenStore } from "./store.js";
  import Cookies from "js-cookie";
  import axios from "axios";

  import Settings from "./routes/settings.svelte";
  import Signup from "./routes/signup.svelte";
  import Login from "./routes/login.svelte";

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
        user_name = res.data["username"];
        user_avatar_url = res.data["avatar_url"];
        user_id_db = res.data["user_id"];
        user_settings = res.data["settings"];
        navigate('/settings');
      })
      .catch(function (e) {
        // JWT token expired, clearing token...
        tokenStore.setToken(0);
        navigate('/');
      });
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

<Router>
  <html lang="en">
    <body>
      <div class="container">
        <div class="header">
          <h1>Ronnia Dashboard</h1>
        </div>
        <div class="navigation" />
        <div class="content">
          <Route path="/">
            {#if $tokenStore == 0}
              {navigate("/login")}
            {:else}
              {navigate("/settings")}
            {/if}
          </Route>
          <Route path="login">
            <Login />
          </Route>
          
          <Route path="signup">
            <Signup />
          </Route>
          <Route path="about">
            <h3>About</h3>
            <p>That's what it's all about!</p>
          </Route>
          <Route path="settings">
            <Settings />
          </Route>
        </div>
      </div>

      <footer>
        Thanks to Sibyl#3838 and bora#5130 for website and frontend design.
      </footer>
    </body>
  </html>

  <main />
</Router>

<!--
        

        {#if $tokenStore == 0}
          {#if error}
            <div class="errortext">
              You are not registered to ronnia<br />
              Add heyronii#9925 on discord for registration.<br />
              <a href="https://github.com/aticie/ronnia"
                >Check out project page for more details.</a
              >
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
-->
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
  .content {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  footer {
    margin: 1% 1%;
  }
</style>
