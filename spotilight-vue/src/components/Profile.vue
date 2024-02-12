<template>
  <div class="profile">
    <button
      type="button"
      @click="handleAccountLogout()"
      class="btn btn-primary"
    >
      Logout
    </button>
    <h1>Profile</h1>
    <p>{{ userProfile }}</p>
  </div>
</template>

<script>
import axios from "axios";
import cookie from "js-cookie";

function getHeader() {
  return {
    Authorization: `Bearer ${cookie.get("access_token")}`,
    "Content-Type": "application/json",
  };
}

export default {
  name: "ProfilePage",
  data() {
    return {
      userProfile: "",
    };
  },
  methods: {
    retrieveAccountProfile() {
      const profile_endpoint = "https://api.spotify.com/v1/me";
      axios({
        method: "GET",
        url: profile_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.userProfile = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    handleAccountLogout() {
      const path = "http://localhost:5000/account";
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
  created() {
    this.retrieveAccountProfile();
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
