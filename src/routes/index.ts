import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";

const Router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: Home
    },
    {
      path: "/login",
      component: () => import("../views/Login.vue")
    },
    {
      path: "/settings",
      component: () => import("../views/Settings.vue")
    }
  ]
});

export default Router;
