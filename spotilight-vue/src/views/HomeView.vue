<template>
  <div class="home">
    <img alt="Vue logo" src="@/assets/Spotilight_Logo.png" height="250" />
    <Login welcome_msg="Welcome to Spotilight!" />
  </div>
</template>

<script>
import Login from "@/components/Login.vue";

export default {
  name: "HomeView",
  components: {
    Login,
  },
};
</script>
