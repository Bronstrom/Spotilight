import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import SpotlightView from "@/views/SpotlightView.vue";
import Login from "@/components/Login.vue";
import Profile from "@/components/Profile.vue";
import PlaylistsView from "@/views/PlaylistsView.vue";
import PlaylistView from "@/views/PlaylistView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/playlists",
    name: "playlists",
    component: PlaylistsView,
  },
  {
    path: "/playlist/:id",
    name: "playlist",
    component: PlaylistView,
  },
  {
    path: "/spotlight",
    name: "spotlight",
    component: SpotlightView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/AboutView.vue"),
  },
  {
    path: "/login",
    name: "LoginPage",
    component: Login,
  },
  {
    path: "/user-profile",
    name: "ProfilePage",
    component: Profile,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
