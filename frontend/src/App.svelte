<script>
  import {navigate, Route, Router} from "svelte-navigator";
  import Cookies from "js-cookie";

  import {SvelteToast} from "@zerodevx/svelte-toast";
  import Login from "./routes/login.svelte";
  import Settings from "./routes/settings.svelte";
  import Signup from "./routes/signup.svelte";

  import urls from "./urls.json";
  import axios from "axios";

  axios.defaults.withCredentials = true;
</script>

<main class="w-full max-w-xl flex flex-col gap-4">
  <p class="font-semibold text-4xl text-center mt-10">Ronnia Dashboard</p>

  <SvelteToast/>

  <Router>
    <Route path="/">
      {#if !Cookies.get("token")}
        { navigate("/login") }
      {:else}
        { navigate("/settings") }
      {/if}
    </Route>
    <Route path="/login" component={Login}/>
    <Route path="/signup" component={Signup}/>
    <Route path="/settings" component={Settings}/>
  </Router>

  <div class="flex justify-between items-center gap-4 footer">
    <div class="flex gap-2">
      <a href={urls.discordUrl}>
        <img src="/public/discordLogo.svg" class="icon h-10 w-10" alt="discord icon"/>
      </a>
      <a href={urls.githubUrl}>
        <img src="/public/githubMark.svg" class="icon h-10 w-10" alt="github icon"/>
      </a>
    </div>

    <p class="hidden md:block">Thanks to Sibyl#3838 and bora#5130 for website and frontend design.</p>
  </div>
</main>
