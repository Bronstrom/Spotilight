<script setup>
import { user } from "../user.js";
</script>

<template>
  <div
    class="home align-content-center-v-and-h main-content-gutter"
    style="height: 90vh"
  >
    <div class="row">
      <div class="col-12 col-md-6">
        <img alt="Vue logo" src="@/assets/Spotilight_Logo.png" height="250" />
      </div>
      <div v-if="!user.displayName" class="col-12 col-md-6">
        <Login welcome_msg="Welcome to Spotilight!" />
      </div>
      <div v-else class="col-12 col-md-6">
        <Profile />
      </div>
    </div>
  </div>
</template>

<script>
import Login from "@/components/Login.vue";
import Profile from "@/components/Profile.vue";

export default {
  name: "HomeView",
  components: {
    Login,
    Profile,
  },
};
</script>
