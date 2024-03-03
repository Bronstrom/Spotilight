<template>
  <div class="top-tracks m-5">
    <h3>Top Tracks</h3>
    <div class="dropdown time-range">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="top-track-frequency-button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ timeRange }}
      </button>
      <div class="dropdown-menu" aria-labelledby="top-track-frequency-button">
        <a
          class="dropdown-item"
          @click="(timeRange = 'Short Term'), changeTimeRange('short_term')"
          >Short Term (Past 4 Weeks)</a
        >
        <a
          class="dropdown-item"
          @click="(timeRange = 'Medium Term'), changeTimeRange('medium_term')"
          >Medium Term (Past 6 Months)</a
        >
        <a
          class="dropdown-item"
          @click="(timeRange = 'Long Term'), changeTimeRange('long_term')"
          >Long Term (Past Few Years)</a
        >
      </div>
    </div>
    <div class="dropdown limit">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="top-genre-limit-button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        Show Top {{ limit }}
      </button>
      <div class="dropdown-menu" aria-labelledby="top-genre-limit-button">
        <a class="dropdown-item" @click="limit = 3">Show Top 3</a>
        <a class="dropdown-item" @click="limit = 5">Show Top 5</a>
        <a class="dropdown-item" @click="limit = 10">Show Top 10</a>
        <a class="dropdown-item" @click="limit = 25">Show Top 25</a>
      </div>
    </div>
    <div
      class="track row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="track col"
        v-for="track in curTopTracks.slice(0, limit)"
        v-bind:key="track.id"
      >
        <div class="track card h-100">
          <!--{{ console.log(track) }}-->
          <img
            class="track card-image"
            :src="track.album.images[0].url"
            :alt="track.album.name + ' album cover'"
          />
          <div class="track card-body">
            <h5 class="track card-title">{{ track.name }}</h5>
            <h6 class="track card-album">
              {{
                track.album.album_type.toLowerCase() === "single"
                  ? "Single:"
                  : "Album:"
              }}
              {{ track.album.name }}
            </h6>
            <p>
              Artist(s):
              <span
                class="track card-text"
                v-for="(artist, index) in track?.artists"
                :key="artist"
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
const DEFAULT_LIMIT_COUNT = 5;
const MAX_LIMIT_COUNT = 25;

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
      topTracksShort: [],
      topTracksMedium: [],
      topTracksLong: [],
      curTopTracks: [],
      timeRange: "Medium Term",
      limit: DEFAULT_LIMIT_COUNT,
    };
  },
  methods: {
    handleTopTracks() {
      // TODO: Refactor some of this duplication
      const medium_term_track_endpoint = `https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&offset=0&limit=${MAX_LIMIT_COUNT}`;
      axios({
        method: "GET",
        url: medium_term_track_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.topTracksMedium = res.data.items;
          this.curTopTracks = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });
      const short_term_track_endpoint = `https://api.spotify.com/v1/me/top/tracks?time_range=short_term&offset=0&limit=${MAX_LIMIT_COUNT}`;
      axios({
        method: "GET",
        url: short_term_track_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.topTracksShort = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });
      const long_term_track_endpoint = `https://api.spotify.com/v1/me/top/tracks?time_range=long_term&offset=0&limit=${MAX_LIMIT_COUNT}`;
      axios({
        method: "GET",
        url: long_term_track_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.topTracksLong = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    changeTimeRange(range) {
      switch (range) {
        case "short_term":
          this.curTopTracks = this.topTracksShort;
          break;
        case "long_term":
          this.curTopTracks = this.topTracksLong;
          break;
        case "medium_term":
        default:
          this.curTopTracks = this.topTracksMedium;
          break;
      }
    },
  },
  /*
    TODO: Consider handling all api calls in the back-end
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
