<script setup>
import { user } from "../user.js";
</script>

<template>
  <div
    class="home align-content-center-v-and-h main-content-gutter"
    style="height: 90vh"
  >
    <img alt="Vue logo" src="@/assets/Spotilight_Logo.png" height="250" />
    <Login v-if="!user.displayName" welcome_msg="Welcome to Spotilight!" />
    <div v-else>
      <Profile />
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
