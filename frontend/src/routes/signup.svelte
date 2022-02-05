<script>
    import Button from "../components/Button.svelte";
    import Cookies from "js-cookie";

    let signupCookie = Cookies.get("signup");
</script>

<p>Complete your sign-up to Ronnia with</p>
<div class="signup_button">
    <div>
        {#if signupCookie == 'twitch'}
        <Button
            text="Login"
            onClick={() => {
                window.location.href = "/osu_authorize";
            }}
            logo="./public/Logo/OsuLogo.svg"
            identifier="osuSignupButton"
        />
        {:else if signupCookie == 'osu'}
        <Button
            text="Login"
            onClick={() => {
                window.location.href = "/twitch_authorize";
            }}
            logo="./public/Logo/TwitchLogo.svg"
            identifier="twitchSignupButton"
        />
        {/if}
    </div>
</div>

<style>
    p {
        font-size: 16pt;
    }
    .signup_button {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }
</style>
