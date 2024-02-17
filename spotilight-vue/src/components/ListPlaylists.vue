<template>
  <div class="top-playlists m-5">
    <h3>List Playlists</h3>
    <div
      class="playlist row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="playlist col"
        v-for="(playlist, index) in playlistsList?.items"
        v-bind:key="playlist.id - index"
      >
        <div class="playlist card h-100">
          {{ console.log(playlist) }}
          <img
            class="playlist card-image"
            :src="playlist.images[0].url"
            :alt="playlist.name + ' playlist art'"
          />
          {{ console.log(playlist?.album?.artists) }}
          <div class="playlist card-body">
            <h5 class="playlist card-title">{{ playlist.name }}</h5>
            <h6 class="playlist card-album">
              Owner: {{ playlist.owner.display_name }}
            </h6>
            <a class="btn-primary" :href="playlist.href"
              >Check it out on Spotify</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import cookie from "js-cookie";

//const BACK_END_URL = "http://localhost:5000";
const TOP_COUNT = 5;

function getHeader() {
  return {
    Authorization: `Bearer ${cookie.get("access_token")}`,
    "Content-Type": "application/json",
  };
}

export default {
  name: "ListPlaylists",
  data() {
    return {
      playlistsList: "",
    };
  },
  methods: {
    aquirePlaylists() {
      const profile_endpoint = `https://api.spotify.com/v1/me/playlists?offset=0&limit=${TOP_COUNT}`;
      axios({
        method: "GET",
        url: profile_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.playlistsList = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.aquirePlaylists();
  },
};
</script>
