<script setup>
import { user } from "../user.js";
</script>

<template>
  <div
    class="home align-content-center-v-and-h main-content-gutter content-gradient"
    style="height: 90vh"
  >
    <div class="row flex items-center rounded-light-background padding-5">
      <div class="col-12 col-md-6 padding-1">
        <img alt="Vue logo" src="@/assets/Spotilight_Logo.png" width="65%" />
      </div>
      <div class="col-12 col-md-6 padding-1">
        <div v-if="!user.displayName">
          <Login welcome_msg="Welcome to Spotilight!" />
        </div>
        <div v-else>
          <Profile />
        </div>
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

<style>
.rounded-light-background {
  background-color: rgba(255, 255, 255, 0.25);
  border-radius: 25px;
}
</style>
