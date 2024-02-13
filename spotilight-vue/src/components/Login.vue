<template>
  <div class="login">
    <h1>{{ welcome_msg }}</h1>
    <button
      type="button"
      @click="handleSpotifyAuthenticate()"
      class="btn btn-primary"
    >
      Authenticate with Spotify
    </button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  props: {
    welcome_msg: String,
  },
  methods: {
    handleSpotifyAuthenticate() {
      const path = "http://localhost:5000/auth/login";
      axios
        .get(path)
        .then((res) => {
          window.location.href = res?.data?.url;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
