<script>
  import { Router, Route, Link, navigate } from "svelte-navigator";
  import { tokenStore } from "./store";

  import { SvelteToast } from "@zerodevx/svelte-toast";
  import Login from "./routes/login.svelte";
  import Settings from "./routes/settings.svelte";
  import Signup from "./routes/signup.svelte";
  
  tokenStore.useLocalStorage();

  // import Cookies from "js-cookie";
  // import axios from "axios";

  // tokenStore.useLocalStorage();
  // let cookieToken = Cookies.get("token");
  // let error = Cookies.get("error");

  // if (cookieToken) {
  //   tokenStore.setToken(cookieToken);
  //   Cookies.remove("token");
  // }

  // if (error) {
  //   Cookies.remove("error");
  // }

  // if ($tokenStore !== 0) {
  //   navigate("/settings");
  // }
</script>

<main>
  <SvelteToast />

  <Router>
    <Route path="/">
      {#if $tokenStore === 0}
        { navigate("/login") }
      {:else}
        { navigate("/settings") }
      {/if}
    </Route>
    <Route path="/login" component={Login} />
    <Route path="/signup" component={Signup} />
  </Router>
</main>

<!-- <Router>
  <html lang="en">
    <body>
      <SvelteToast />
      <div class="container">
        <div class="header">
          <h1>Ronnia Dashboard</h1>
        </div>
        <div class="navigation" />
        <div class="content">
          <Route path="/">
            {#if $tokenStore === 0}
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

      <footer>Thanks to Sibyl#3838 and bora#5130 for website and frontend design.</footer>
    </body>
  </html>

  <main />
</Router> -->
