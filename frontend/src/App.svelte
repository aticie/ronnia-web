
<script>
import { user_local_token } from './store.js';
import Cookies from 'js-cookie'
import axios from 'axios';

user_local_token.useLocalStorage();
let user_token_value;

if (Cookies.get('token')){
    user_local_token.set(Cookies.get('token'));
    Cookies.remove('token');
};

user_local_token.subscribe(value => {
   user_token_value = value;
});

if (user_token_value!=0){
    let user_name;
    axios.get('/user_details', {params: {jwt_token: user_token_value}}).then(res => {
        user_name = res['username'];
    });
}

</script>

<html lang="en">
<body>
<div>
<center>
{#if user_token_value!=0}
  logged in with token: {user_token_value}.
{/if}

{#if user_token_value==0}
<h1>Login using the following links:</h1>
<a href="https://osu.ppy.sh/oauth/authorize?response_type=code&client_id=2408&redirect_uri=http://localhost:8000/identify&scope=identify">osu!</a>
{/if}
</center>
</div>
</body>
</html>

<style>
body, html{
    background: #DB9065
}
div {
    padding: 8px
}

</style>