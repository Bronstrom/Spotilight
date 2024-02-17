<template>
  <div class="top-tracks m-5">
    <h3>Top Tracks</h3>
    <div
      class="track row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="track col"
        v-for="(track, index) in topTracks?.items"
        v-bind:key="track.id - index"
      >
        <div class="track card h-100">
          {{ console.log(track) }}
          <img
            class="track card-image"
            :src="track.album.images[0].url"
            :alt="track.album.name + ' album cover'"
          />
          {{ console.log(track?.album?.artists) }}
          <div class="track card-body">
            <h5 class="track card-title">{{ track.name }}</h5>
            <h6 class="track card-album">
              {{ track.album.album_type === "SINGLE" ? "Single:" : "Album:" }}
              {{ track.album.name }}
            </h6>
            <p>
              Artist(s):
              <span
                class="track card-text"
                v-for="(artist, index) in track?.artists"
                :key="artist - index"
              >
                {{ index === 0 ? "" : ", " }}
                {{ artist.name }} ({{ artist.type }})
              </span>
            </p>
            <a class="btn-primary" :href="track.href"
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
  name: "TopTracks",
  data() {
    return {
      topTracks: "",
    };
  },
  methods: {
    handleTopTracks() {
      const profile_endpoint = `https://api.spotify.com/v1/me/top/tracks?offset=0&limit=${TOP_COUNT}`;
      axios({
        method: "GET",
        url: profile_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.topTracks = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  /*
    handleTopTracks() {
      const path = BACK_END_URL + "/spotlight/toptracks/" + TOP_COUNT;
      axios({
        method: "GET",
        url: path,
        headers: {
          "Access-Control-Allow-Origin": BACK_END_URL + "/*",
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          this.topTracks = res?.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },*/
  created() {
    this.handleTopTracks();
  },
};
</script>
