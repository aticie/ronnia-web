import { createRouter, createWebHistory } from "vue-router";
import { useCookies } from "@vueuse/integrations/useCookies";

const Router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: () => {
        const cookies = useCookies();
        return cookies.get("token") ? "/settings" : "/login"
      }
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
