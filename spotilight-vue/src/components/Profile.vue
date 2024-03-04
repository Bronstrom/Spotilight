<template>
  <div class="profile">
    <button
      type="button"
      @click="handleAccountLogout()"
      class="btn btn-primary"
    >
      Logout
    </button>
    <h1 v-if="displayName">Welcome, {{ displayName }}!</h1>
    <p>{{ userProfile }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProfilePage",
  data() {
    return {
      userProfile: "",
      displayName: "",
    };
  },
  methods: {
    retrieveAccountProfile() {
      const path = "/auth/user-profile";
      axios
        .get(path)
        .then((res) => {
          this.userProfile = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    retrieveAccountDisplayName() {
      const path = "/user/display-name";
      axios
        .get(path)
        .then((res) => {
          this.displayName = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    handleAccountLogout() {
      const path = "/auth/logout";
      axios
        .get(path)
        .then((res) => {
          const resposeUrl = res?.data?.url;
          window.open(resposeUrl, "_blank");
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.retrieveAccountProfile();
    this.retrieveAccountDisplayName();
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
