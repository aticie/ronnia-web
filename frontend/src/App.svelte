<script>
  import { Router, Route, navigate } from "svelte-navigator";
  import { tokenStore } from "./store";
  import Cookies from "js-cookie";

  import { SvelteToast } from "@zerodevx/svelte-toast";
  import Login from "./routes/login.svelte";
  import Settings from "./routes/settings.svelte";
  import Signup from "./routes/signup.svelte";

  import urls from "./urls.json";
  
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

<main class="w-full max-w-xl flex flex-col gap-4">
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
  
  <div class="flex justify-end items-center footer">
    <p class="hidden md:block md:mr-auto">Thanks to Sibyl#3838 and bora#5130 for website and frontend design.</p>
  
    <div class="flex gap-2">
      <a href={urls.discordUrl}>
        <img src="/public/discordLogo.svg" class="icon h-10 w-10" alt="discord icon" />
      </a>
      <a href={urls.githubUrl}>
        <img src="/public/githubMark.svg" class="icon h-10 w-10" alt="github icon" />
      </a>
    </div>
  </div>
</main>
