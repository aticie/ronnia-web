<script>
    import Button from "../components/Button.svelte";
</script>

<p>Log in to Ronnia with</p>
<div class="login_buttons">
    <div>
        <Button
            text="Login"
            onClick={() => {
                window.location.href = "/osu_authorize";
            }}
            logo="./public/Logo/OsuLogo.svg"
            identifier="osuLoginButton"
        />
    </div>
    <div>
        <Button
            text="Login"
            onClick={() => {
                window.location.href = "/twitch_authorize";
            }}
            logo="./public/Logo/TwitchLogo.svg"
            identifier="twitchLoginButton"
        />
    </div>
</div>
