import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/registro",
    name: "registro",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/RegistroView.vue"),
  },
  {
    path: "/recuperar",
    name: "recuperar",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/RecuperarView.vue"),
  },
  {
    path: "/dashboard",
    name: "dashboard",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/DashboardView.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Con el interceptor protegemos las rutas
router.beforeEach((to, from, next) => {
  if (to.path === "/dashboard") {
    if (localStorage.getItem("token")) {
      next();
    } else {
      next("/");
    }
  } else {
    next();
  }
});

export default router;
