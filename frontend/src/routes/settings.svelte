<script>
    import {navigate } from "svelte-navigator";
    import SettingsCheckbox from "../components/SettingsCheckbox.svelte";
    import TinyButton from "../components/TinyButton.svelte";
    import SettingsSaveButton from "../components/SettingsSaveButton.svelte";
    import { tokenStore } from "../store.js";
    import InputBox from "../components/InputBox.svelte";
    import axios from "axios";

    let buttonDisabled = false;
    let errorText = "";
    let user_name;
    let user_avatar_url;
    let user_id_db;
    let user_settings = [];

    if ($tokenStore != 0) {
        axios
            .get("/user_details", { params: { jwt_token: $tokenStore } })
            .then((res) => {
                user_name = res.data["username"];
                user_avatar_url = res.data["avatar_url"];
                user_id_db = res.data["user_id"];
                user_settings = res.data["settings"];
            })
            .catch(function (e) {
                // JWT token expired, clearing token...
                tokenStore.setToken(0);
                navigate('/');
            });
    }
    else{
        navigate('/');
    }

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

<div class="userbox">
    <div
        alt="Avatar"
        class="rounded-circle avatar"
        crossorigin="anonymous"
        style="background-image: url('{user_avatar_url
            ? user_avatar_url
            : ''}')"
    />
    <div class="profile-info">
        {user_name}
    </div>
    <TinyButton
        text="Logout"
        identifier="logoutButton"
        onClick={() => {
            tokenStore.delToken();
            navigate('/');
        }}
    />
</div>
<div class="settings">
    {#each user_settings as setting}
        {#if setting.key !== "test"}
            <div class="setting">
                {#if setting.type === "toggle"}
                    <div class="checkbox">
                        <SettingsCheckbox bind:checked={setting.value} />
                    </div>
                {:else}
                    <div class="inputbox">
                        <InputBox
                            key={setting.key}
                            bind:min_value={setting.range_start}
                            bind:max_value={setting.range_end}
                            on:message={handleInputBoxMessage}
                        />
                    </div>
                {/if}
                <div class="command">
                    {setting.key == "sr" ? "min sr\nmax sr" : setting.key}
                </div>
                <div class="description">
                    {setting.description}
                </div>
            </div>
        {/if}
    {/each}
</div>
<div class="errortext">{errorText}</div>
<div class="savebutton">
    <SettingsSaveButton
        bind:disabled={buttonDisabled}
        settings={user_settings}
        jwt_token={$tokenStore}
        timeout_secs="2000"
    />
</div>

<style>
    .settings {
        display: flex;
        flex-direction: column;
        text-align: left;
        margin-top: 20px;
    }
    .setting {
        margin-top: 5px;
        margin-bottom: 5px;

        font-size: 26px;
        display: grid;
        grid-template-columns: 70px 120px auto;
        align-items: center;
    }
    .checkbox {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .rounded-circle {
        height: 64px;
        width: 64px;
        border-radius: 50%;
    }
    .avatar {
        background-size: cover;
    }
    .profile-info {
        font-size: x-large;
        margin-left: 10px;
        margin-right: 5px;
    }
    .userbox {
        display: flex;
        align-items: center;
    }
    .inputbox {
        display: flex;
        flex-direction: column;
    }
    .errortext {
        color: #e84545;
        margin: 30px 10px;
    }
</style>
