<script>
  import axios from "axios";
  import Settings from "../components/Settings.svelte";
  import { navigate } from "svelte-navigator";
  import { tokenStore } from "../store";
  import { toast } from "@zerodevx/svelte-toast";

  let userId;
  let username;
  let userAvatarUrl;

  let userSettings = [];
  let userExcludes = [];

  const getUser = async () => {
    try {
      const response = await axios.get("/user_details", {
        params: { jwt_token: $tokenStore },
      });

      userId = response.data["user_id"];
      username = response.data["username"];
      userAvatarUrl = response.data["avatar_url"];
      userSettings = response.data["settings"];
      userExcludes = response.data["excluded_users"];
    } catch {
      tokenStore.setToken(0);
      navigate("/");
    }
  };

  getUser();

  let disabled = false;
  const saveSettings = async () => {
    disabled = true;

    await axios.post("/save_user_settings", {
      jwt_token: $tokenStore,
      settings: userSettings,
      excluded_users: userExcludes,
    });

    setTimeout(() => disabled = false, 4000)
    toast.push("Saved your settings!");
  };
</script>

<div class="flex flex-col gap-4">
  <div class="flex justify-between items-center gap-4">
    <div class="flex items-center gap-2">
      <img src={userAvatarUrl} class="rounded-md w-12 h-12" alt="user avatar" />
      <p>{username}</p>
    </div>

    <button class="button b-with-icon"><img src="/public/logout.svg" alt="logout icon" style="width: 1.75rem; height: 1.75rem;" />Logout</button>
  </div>

  <Settings settings={userSettings} {userExcludes} />

  <button class="button disabled:bg-neutral-800" {disabled} on:click={saveSettings}>Save</button>
</div>
