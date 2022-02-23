<script>
    import {Router, Route, Link, navigate} from "svelte-navigator";
    import {tokenStore} from "./store.js";
    import Cookies from "js-cookie";
    import axios from "axios";

    import Settings from "./routes/settings.svelte";
    import Signup from "./routes/signup.svelte";
    import Login from "./routes/login.svelte";
    import {SvelteToast} from '@zerodevx/svelte-toast'

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

    if ($tokenStore !== 0) {
        navigate('/settings');
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
    <SvelteToast/>
    <div class="container">
        <div class="header">
            <h1>Ronnia Dashboard</h1>
        </div>
        <div class="navigation"/>
        <div class="content">
            <Route path="/">
                {#if $tokenStore === 0}
                    {navigate("/login")}
                {:else}
                    {navigate("/settings")}
                {/if}
            </Route>
            <Route path="login">
                <Login/>
            </Route>

            <Route path="signup">
                <Signup/>
            </Route>
            <Route path="about">
                <h3>About</h3>
                <p>That's what it's all about!</p>
            </Route>
            <Route path="settings">
                <Settings/>
            </Route>
        </div>
    </div>

    <footer>
        Thanks to Sibyl#3838 and bora#5130 for website and frontend design.
    </footer>
    </body>
    </html>

    <main/>
</Router>
<style>

    :root {
        --theme-main-color: #e84545;
        --theme-main-light: #ff5361;
        --theme-alt-color: #a71818;
        --theme-inactive-light: #646464;
        --theme-bg-color: #121212;
        --theme-inactive-color: #343434;
        --theme-text-color: #FFFFFF;
        --toastColor: var(--theme-text-color);
        --toastBarBackground: var(--theme-main-color);
    }

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
