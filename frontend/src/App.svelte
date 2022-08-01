<script>
  import { Router, Route, navigate } from "svelte-navigator";
  import { tokenStore } from "./store";
  import Cookies from "js-cookie";

  import { SvelteToast } from "@zerodevx/svelte-toast";
  import Login from "./routes/login.svelte";
  import Settings from "./routes/settings.svelte";
  import Signup from "./routes/signup.svelte";
  
  tokenStore.useLocalStorage();

  let cookieToken = Cookies.get("token");
  let error = Cookies.get("error");
  
  if (cookieToken) {
    tokenStore.setToken(cookieToken);
  }

  if (error) {
    Cookies.remove("error");
  }
</script>

<main class="w-full max-w-xl">
  <p class="font-semibold text-4xl text-center mt-10">Ronnia Dashboard</p>

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
    <Route path="/settings" component={Settings} />
  </Router>

  <p class="absolute left-2 bottom-2 text-neutral-500 font-semibold">Thanks to Sibyl#3838 and bora#5130 for website and frontend design.</p>
</main>
