<script setup>
import { user } from "../user.js";
</script>

<template>
  <div class="profile margin-top-bottom row">
    <h1>
      Welcome, <span class="text-primary">{{ user.displayName }}</span
      >!
    </h1>
  </div>
  <div class="margin-top-bottom">
    <p>To get started, view any of the options below:</p>
    <div class="row">
      <a class="nav-link col-6 p-2" href="/playlists">
        <div class="card bg-primary">
          <div class="card-body">Playlists</div>
        </div>
      </a>
      <a class="nav-link col-6 p-2" href="/showcase">
        <div class="card bg-primary">
          <div class="card-body">Showcase</div>
        </div>
      </a>
    </div>
  </div>
  <div class="margin-top-bottom">
    <p>
      If you need help using the application at any time, familiarize yourself
      with the documentation:
    </p>
    <div class="row d-flex justify-content-center">
      <a class="nav-link col-6 p-2" href="/about">
        <div class="card">
          <div class="card-body">About</div>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfilePage",
};
</script>
