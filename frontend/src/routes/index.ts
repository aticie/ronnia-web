import { createRouter, createWebHistory } from "vue-router";

import Home from "../views/Home.vue";

const Router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: Home
    }
  ]
});

export default Router;
