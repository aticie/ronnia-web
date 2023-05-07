import { createRouter, createWebHistory } from "vue-router";

import Settings from "../views/Settings.vue";
import Login from "../views/Login.vue";

const Router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/login"
    },
    {
      path: "/login",
      component: Login
    },
    {
      path: "/settings",
      component: Settings
    }
  ]
});

export default Router;
