<template>
  <NavigationBar />
  <router-view />
</template>

<script>
import NavigationBar from "@/components/NavigationBar.vue";

export default {
  name: "App",
  components: {
    NavigationBar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #eeeeee;
  background-color: #555555;
}

html {
  background-color: #555555;
}

:root {
  color-scheme: dark;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #eeeeee;
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

.align-content-center-v-and-h {
  display: flex;
  align-items: center;
  justify-content: center;
}

.margin-top-bottom {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.text-align-center {
  text-align: center;
}
.text-align-left {
  text-align: left;
}
</style>
