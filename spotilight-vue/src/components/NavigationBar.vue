<template>
  <nav
    class="navbar bg-dark navbar-expand-lg border-bottom border-body"
    data-bs-theme="dark"
  >
    <div class="container-fluid">
      <img alt="Vue logo" src="@/assets/Spotilight_Logo.png" height="25" />
      <a class="navbar-brand" href="/">Spotilight</a>
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
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/playlists">Playlists</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/spotlight">Spotlight</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/about">About</a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link disabled"
              aria-disabled="true"
              href="/user-profile"
            >
              Profile
            </a>
          </li>
          <li
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
              <img
                :src="profileIcon"
                class="rounded-circle"
                height="50"
                alt="User Profile"
                loading="lazy"
              />
            </a>
            <ul class="dropdown-menu">
              <li>
                <a class="dropdown-item" @click="handleAccountLogout()"
                  >Logout</a
                >
              </li>
            </ul>
          </li>
        </ul>
        <span> </span>
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
  },
  created() {
    this.retrieveAccountProfileIcon();
  },
};
</script>
