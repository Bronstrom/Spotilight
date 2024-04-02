<script setup>
import { user } from "../user.js";
</script>

<template>
  <nav
    class="navbar bg-dark navbar-expand-lg border-bottom border-body"
    data-bs-theme="dark"
  >
    <div class="main-content-gutter space-between">
      <div class="navbar-brand">
        <a href="/">
          <img alt="Vue logo" src="@/assets/Spotilight_Logo.png" height="25" />
          Spotilight</a
        >
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="/about">About</a>
          </li>
          <li v-if="user.displayName" class="nav-item">
            <a class="nav-link" href="/playlists">Playlists</a>
          </li>
          <li v-if="user.displayName" class="nav-item">
            <a class="nav-link" href="/showcase">Showcase</a>
          </li>
        </ul>
      </div>
      <div
        class="dropdown"
        @v-show="
          {
            profileIcon;
          }
        "
      >
        <a
          class="dropdown-toggle"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <template v-if="profileIcon !== ''">
            <img
              :src="profileIcon"
              class="rounded-circle"
              height="50"
              alt="User Profile"
              loading="lazy"
            />
          </template>
          <span v-else style="font-size: 2rem">O</span>
        </a>
        <ul class="dropdown-menu">
          <li>
            <a
              v-if="user.displayName"
              class="dropdown-item"
              @click="handleAccountLogout()"
              >Logout</a
            >
            <a v-else class="dropdown-item" @click="handleSpotifyAuthenticate()"
              >Login</a
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  name: "NavigationBar",
  data() {
    return {
      profileIcon: "",
    };
  },
  methods: {
    retrieveAccountProfileIcon() {
      const path = "/user/profile-photo";
      axios
        .get(path)
        .then((res) => {
          this.profileIcon = res.data;
          if (res.data !== "") {
            this.$emit("loggedIn");
          } else {
            this.$emit("loggedOut");
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    retrieveAccountDisplayName() {
      const path = "/user/display-name";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          if (!res.data.url) {
            user.handleNewDisplayName(res?.data);
          } else {
            user.handleNewDisplayName(null);
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    handleAccountLogout() {
      const path = "/auth/logout";
      axios
        .get(path)
        .then((res) => {
          const resposeUrl = res?.data?.url;
          window.open(resposeUrl, "_blank");
        })
        .catch((err) => {
          console.error(err);
        });
    },
    handleSpotifyAuthenticate() {
      const path = "/auth/login";
      axios
        .get(path)
        .then((res) => {
          window.location.href = res?.data?.url;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.retrieveAccountProfileIcon();
    this.retrieveAccountDisplayName();
  },
};
</script>

<style>
.dropdown-toggle {
  color: #ffffff;
  text-decoration: none;
}
</style>
