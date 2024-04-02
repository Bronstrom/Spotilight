import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import ShowcaseView from "@/views/ShowcaseView.vue";
import PageNotFound from "@/components/PageNotFound.vue";
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
    path: "/showcase",
    name: "showcase",
    component: ShowcaseView,
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
    path: "/:pathMatch(.*)*",
    name: "PageNotFound",
    component: <PageNotFound />,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
