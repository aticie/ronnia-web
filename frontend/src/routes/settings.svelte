<script>
    import {navigate} from "svelte-navigator";
    import SettingsCheckbox from "../components/SettingsCheckbox.svelte";
    import TinyButton from "../components/TinyButton.svelte";
    import SettingsSaveButton from "../components/SettingsSaveButton.svelte";
    import {tokenStore} from "../store.js";
    import RangeSlider from "svelte-range-slider-pips";
    import axios from "axios";

    let buttonDisabled = false;
    let errorText = "";
    let user_name;
    let user_avatar_url;
    let user_id_db;
    let sr_setting;
    let user_settings = [];

    if ($tokenStore !== 0) {
        axios
            .get("/user_details", {params: {jwt_token: $tokenStore}})
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
    } else {
        navigate('/');
    }

    function handleSliderInteraction(event, setting) {
        setting.range_start = event.detail.values[0]
        setting.range_end = event.detail.values[1]
    }
</script>

<div class="userbox">
    <div
            alt="Avatar"
            class="rounded-circle avatar"
            crossorigin="anonymous"
            style="background-image: url('{user_avatar_url ? user_avatar_url : ''}')">
    </div>
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
                        <SettingsCheckbox bind:checked={setting.value}/>
                    </div>
                {:else}
                    <div class="rangeslider-container">
                        <RangeSlider id="rangeslider-id" float pushy range formatter={(v, i, p) => {
                            if (v === 10){
                                return '∞'
                            }
                            return v
                        }} pips pipstep={5} all="label"
                                     values={[setting.range_start === -1 ? 0: setting.range_start, setting.range_end === -1 ? 10: setting.range_end]}
                                     step={0.2} min={0} max={10}
                                     on:change={(e) => {handleSliderInteraction(e, setting)}}/>
                    </div>
                {/if}
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
            timeout_secs="4000"
    />
</div>

<style>
    :root {
        --range-slider: var(--theme-inactive-light);
        --range-handle-inactive: var(--theme-alt-color);
        --range-handle: var(--theme-alt-color);
        --range-handle-focus: var(--theme-main-light);
        --range-range: var(--theme-main-color);
        --range-range-inactive: var(--theme-main-color);
        --range-pip-active-text: var(--theme-main-color);
        --range-pip-text: var(--theme-inactive-color);
    }


    .rangeslider-container {
        font-size: small;
        margin-right: 1rem;
    }

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
        grid-template-columns: 10rem auto;
        align-items: center;
    }

    .checkbox {
        display: flex;
        justify-content: right;
        align-items: center;
        margin-right: 1rem;
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
        color: var(--theme-main-color);
        margin: 30px 10px;
    }
</style>
