import { createApp } from 'vue'
import { createPinia } from "pinia";
import App from './App.vue'
import router from "./routes";
import { api, apiErrorMessage, isUnauthorized } from "./api";
import { useUserStore } from "./store";
import { initSentry } from "./sentry";

import './assets/main.css'

const pinia = createPinia();
const app = createApp(App);

app.use(pinia);
const userStore = useUserStore(pinia);
api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (isUnauthorized(error)) {
      userStore.resetSession(apiErrorMessage(error));
      if (router.currentRoute.value.path === "/settings") {
        void router.replace("/login");
      }
    }
    return Promise.reject(error);
  }
);
app.use(router);

// Must run after the router exists so SPA navigations are traced.
initSentry(app, router);

app.mount("#app");
