import { createRouter, createWebHistory } from "vue-router";

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
