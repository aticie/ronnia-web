import { createRouter, createWebHistory } from "vue-router";
import { useCookies } from "@vueuse/integrations/useCookies";
import axios from "axios";

const Router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/login"
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
