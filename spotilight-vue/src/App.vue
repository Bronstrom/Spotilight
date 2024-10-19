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

.content-gradient {
  background-image: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.25) 0%,
    rgba(255, 255, 255, 0) 30rem
  );
  background-image: -moz-linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.25) 0%,
    rgba(255, 255, 255, 0) 30rem
  );
  background-image: -webkit-linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.25) 0%,
    rgba(255, 255, 255, 0) 30rem
  );
}

.flex {
  display: flex;
}

.grid {
  display: grid;
}

.cursor-pointer {
  cursor: pointer;
}

.padding-1 {
  padding: 16px;
}
.padding-5 {
  padding: 60px;
}
.padding-left-1 {
  padding-left: 16px;
}
.padding-right-1 {
  padding-right: 16px;
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
.margin-bottom {
  margin-bottom: 2rem;
}

.sm-rounded-button {
  height: 2.5rem;
  width: 2.5rem;
  border-radius: 2rem;
  align-items: center;
  justify-content: center;
  border: none;
  background-color: gray;
}

.text-align-center {
  text-align: center;
}
.text-align-left {
  text-align: left;
}

.items-center {
  align-items: center;
}
</style>
