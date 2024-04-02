<script setup>
import { user } from "../user.js";
</script>

<template>
  <div class="profile">
    <h1>Welcome, {{ user.displayName }}!</h1>
  </div>
  <p>To get started, view any of the options below:</p>
  <div class="row padding-top-bottom">
    <a class="nav-link col-6 p-2" href="/playlists">
      <div class="card">
        <div class="card-body">Playlists</div>
      </div>
    </a>
    <a class="nav-link col-6 p-2" href="/spotlight">
      <div class="card">
        <div class="card-body">Spotlight</div>
      </div>
    </a>
  </div>
  <p>
    If you need any help beginning or using the application at any time,
    familiarize yourself with the documentation:
  </p>
  <div class="row d-flex justify-content-center padding-top-bottom">
    <a class="nav-link col-6" href="/about">
      <div class="card">
        <div class="card-body">About</div>
      </div>
    </a>
  </div>
</template>

<script>
export default {
  name: "ProfilePage",
};
</script>
