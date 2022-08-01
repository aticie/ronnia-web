<script>
  import axios from "axios";
  import Settings from "../components/Settings.svelte";
  import { navigate } from "svelte-navigator";
  import { tokenStore } from "../store";

  let userId;
  let username = "Sibyl";
  let userAvatarUrl =
    "https://static-cdn.jtvnw.net/jtv_user_pictures/0dd8274f-e21a-42cf-b020-40463e5519f6-profile_image-300x300.png";

  let userSettings = [
    {
      id: 1,
      key: "echo",
      default_value: 1,
      description: "Enables Twitch chat acknowledge message.",
      type: "toggle",
      value: 1,
    },
    {
      id: 2,
      key: "enable",
      default_value: 1,
      description: "Enables the bot.",
      type: "toggle",
      value: 1,
    },
    {
      id: 3,
      key: "sub-only",
      default_value: 0,
      description: "Subscribers only request mode.",
      type: "toggle",
      value: 0,
    },
    {
      id: 4,
      key: "cp-only",
      default_value: 0,
      description: "Channel Points only request mode.",
      type: "toggle",
      value: 0,
    },
    {
      id: 5,
      key: "test",
      default_value: 0,
      description: "Enables test mode.",
      type: "toggle",
      value: 0,
    },
    {
      id: 1,
      key: "sr",
      default_low: -1.0,
      default_high: -1.0,
      description: "Set star rating limit for requests.",
      type: "range",
      range_start: -1.0,
      range_end: -1.0,
    },
    {
      id: 6,
      key: "cooldown",
      default_value: 30,
      description: "Cooldown for requests.",
      type: "value",
      value: 30,
    },
  ];
  let userExcludes = [123];

  const getUser = async () => {
    try {
      const response = await axios.get("/user_details", {
        params: { jwt_token: $tokenStore },
      });

      userId = response.data["user_id"];
      username = response.data["username"];
      userAvatarUrl = response.data["avatar_url"];
      userSettings = response.data["settings"].filter(x => x.key != "test");
      userExcludes = response.data["excluded_users"];
    } catch {
      tokenStore.setToken(0);
      if (!import.meta.env.DEV) {
        navigate("/");
      }
    }
  };

  getUser();
</script>

<div class="flex flex-col gap-4">
  <div class="flex justify-between items-center gap-4">
    <div class="flex items-center gap-2">
      <img src={userAvatarUrl} class="rounded-md w-12 h-12" alt="user avatar" />
      <p>{username}</p>
    </div>

    <button class="button b-with-icon"><img src="/logout.svg" alt="logout icon" />Logout</button>
  </div>
  
  <Settings settings={userSettings} userExcludes={userExcludes} />
</div>
