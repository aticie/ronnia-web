<script>
    import {navigate} from "svelte-navigator";
    import SettingsCheckbox from "../components/SettingsCheckbox.svelte";
    import TinyButton from "../components/TinyButton.svelte";
    import SettingsSaveButton from "../components/SettingsSaveButton.svelte";
    import {tokenStore} from "../store.js";
    import RangeSlider from "svelte-range-slider-pips";
    import axios from "axios";

    let cooldown_max = 15
    let button_disabled = false;
    let error_text = "";
    let user_name;
    let user_avatar_url;
    let user_id_db;
    let user_settings = [];
    let user_excludes = []

    let newItem = '';

    function addToList() {
        if (newItem === '') {
            return
        }
        user_excludes = [...user_excludes, newItem];
        newItem = '';
    }

    function removeFromList(index) {
        user_excludes.splice(index, 1)
        user_excludes = user_excludes;
    }

    const onKeyPress = e => {
        if (e.charCode === 13) addToList();
    };

    if ($tokenStore !== 0) {
        axios
            .get("/user_details", {params: {jwt_token: $tokenStore}})
            .then((res) => {
                user_name = res.data["username"];
                user_avatar_url = res.data["avatar_url"];
                user_id_db = res.data["user_id"];
                user_settings = res.data["settings"];
                user_excludes = res.data["excluded_users"];
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
                    <div class="checkbox-container">
                        <SettingsCheckbox bind:checked={setting.value}/>
                    </div>
                {:else if setting.type === "value"}
                    <div class="rangeslider-container">
                        <RangeSlider id="rangeslider-id"
                                     range="min"
                                     formatter={ v => {if (v < 60){
                                            return v + "s"
                                         }
                                         if (v % 60 === 0){
                                             return Math.round(v/60) + "m"
                                         }
                                         return Math.floor(v/60) + "m" + v % 60 + "s"
                                     }}
                                     values={[setting.value]}
                                     step={1} min={0} max={cooldown_max*60}
                                     pips pipstep={12 * cooldown_max} all="label" float
                                     on:change={(e) => {handleSliderInteraction(e, setting)}}/>
                    </div>
                {:else if setting.type === "range"}
                    <div class="rangeslider-container">
                        <RangeSlider id="rangeslider-id" float pushy range formatter={(v, i, p) => {
                            if (v === 10){
                                return '∞'
                            }
                            return v
                        }} pips pipstep={10} all="label"
                                     values={[setting.range_start === -1 ? 0: setting.range_start, setting.range_end === -1 ? 10: setting.range_end]}
                                     step={0.1} min={0} max={10}
                                     on:change={(e) => {handleSliderInteraction(e, setting)}}/>
                    </div>
                {/if}
                <div class="description">
                    {setting.description}
                </div>
            </div>
        {/if}
    {/each}
    <div class="setting">
        <div class="excluded-user-container">
            {#each user_excludes as item, index}
                <div class="excluded-user-item">
                    <span class="user-excluded-item">{item}</span>
                    <span on:click={() => removeFromList(index)}>❌</span>
                </div>
            {/each}
            <div class="excluded-user-input-box">
                <input bind:value={newItem} type="text" maxlength="25"
                       on:keypress={onKeyPress} placeholder="excluded username...">
            </div>
        </div>
        <div class="description">
            Excluded users
        </div>
    </div>
</div>
<div class="errortext">{error_text}</div>
<div class="savebutton">
    <SettingsSaveButton
            bind:disabled={button_disabled}
            settings={user_settings}
            jwt_token={$tokenStore}
            excluded_users={user_excludes}
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
        grid-template-columns: 14rem auto;
        align-items: center;
    }

    .checkbox-container {
        display: flex;
        justify-content: right;
        align-items: center;
        margin-right: 1rem;
    }

    .excluded-user-container {
        display: flex;
        justify-content: right;
        align-items: end;
        margin-right: 1rem;
        flex-direction: column;
    }

    .excluded-user-item {
        flex-direction: row;
        font-size: 1.3rem;
        width: max-content;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
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

    .errortext {
        color: var(--theme-main-color);
        margin: 30px 10px;
    }

    input {
        margin-top: 1rem;
        margin-right: 5px;
        width: 12rem;
        height: 1.5rem;
        font-size: 0.75em;
        font-family: "Roboto", sans-serif;
        border: none;
        border-radius: 5%;
        color: var(--theme-text-color);
        background-color: var(--theme-inactive-light);
        text-align: center;
    }

    input::placeholder {
        color: var(--theme-text-color-placeholder);
    }

    input[type="text"]:focus {
        border: none;
    }
</style>
