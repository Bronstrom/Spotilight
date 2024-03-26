<template>
  <NavigationBar
    :userLoggedIn="userLoggedIn"
    :loggedIn="loggedIn"
    :loggedOut="loggedOut"
  />
  <router-view />
</template>

<script>
import NavigationBar from "@/components/NavigationBar.vue";

export default {
  name: "App",
  components: {
    NavigationBar,
  },
  data() {
    return {
      userLoggedIn: false,
    };
  },
  loggedIn() {
    this.userLoggedIn = true;
  },
  loggedOut() {
    this.userLoggedIn = false;
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.main-content-gutter {
  padding-left: 10vw;
  padding-right: 10vw;
}

.space-between {
  display: flex;
  justify-content: space-between;
  width: 100vw;
}
</style>
