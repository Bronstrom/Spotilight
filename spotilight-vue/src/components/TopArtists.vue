<template>
  <div class="top-artists m-5">
    <h3>Top Artists</h3>
    <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="top-artist-frequency-button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ timeRange }}
      </button>
      <div class="dropdown-menu" aria-labelledby="top-artist-frequency-button">
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
    <div
      class="artist row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="artist col"
        v-for="artist in curTopArtists"
        v-bind:key="artist.id"
      >
        <div class="artist card h-100">
          {{ console.log(artist) }}
          <img
            class="artist card-image"
            :src="artist.images[0].url"
            :alt="artist.name + ' album cover'"
          />
          <div class="artist card-body">
            <h5 class="artist card-title">{{ artist.name }}</h5>
            <h6 class="artist card-album">Type: {{ artist.type }}</h6>
            <p>
              Genre(s):
              <span v-if="artist?.genres?.length > 0">
                <span
                  class="artist card-text"
                  v-for="(genre, index) in artist?.genres"
                  :key="genre"
                >
                  {{ index === 0 ? "" : ", " }}
                  {{ genre }}
                </span>
              </span>
              <span v-else class="artist not-specified"
                >No genres specified</span
              >
            </p>
            <p class="artist card-text">
              Follower Count: {{ artist.followers?.total }}
            </p>
            <p class="artist card-text">
              Spotify Popularity Score: {{ artist?.popularity }} / 100
            </p>
            <a class="btn-primary" :href="artist.href"
              >Check them out on Spotify</a
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
  name: "TopArtists",
  data() {
    return {
      topArtistsShort: [],
      topArtistsMedium: [],
      topArtistsLong: [],
      curTopArtists: [],
      timeRange: "Medium Term",
    };
  },
  methods: {
    handleTopArtists() {
      // TODO: Refactor some of this duplication
      const medium_term_artist_endpoint = `https://api.spotify.com/v1/me/top/artists?time_range=medium_term&offset=0&limit=${TOP_COUNT}`;
      axios({
        method: "GET",
        url: medium_term_artist_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.topArtistsMedium = res.data.items;
          this.curTopArtists = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });
      const short_term_artist_endpoint = `https://api.spotify.com/v1/me/top/artists?time_range=short_term&offset=0&limit=${TOP_COUNT}`;
      axios({
        method: "GET",
        url: short_term_artist_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.topArtistsShort = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });
      const long_term_artist_endpoint = `https://api.spotify.com/v1/me/top/artists?time_range=long_term&offset=0&limit=${TOP_COUNT}`;
      axios({
        method: "GET",
        url: long_term_artist_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.topArtistsLong = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    changeTimeRange(range) {
      switch (range) {
        case "short_term":
          this.curTopArtists = this.topArtistsShort;
          break;
        case "long_term":
          this.curTopArtists = this.topArtistsLong;
          break;
        case "medium_term":
        default:
          this.curTopArtists = this.topArtistsMedium;
          break;
      }
    },
  },
  /*
    TODO: Consider handling all api calls in the back-end
    handleTopArtists() {
      const path = BACK_END_URL + "/spotlight/topartists/" + TOP_COUNT;
      axios({
        method: "GET",
        url: path,
        headers: {
          "Access-Control-Allow-Origin": BACK_END_URL + "/*",
          "Content-Type": "application/json",
        },
      })
        .then((res) => {
          this.topArtists = res?.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },*/
  created() {
    this.handleTopArtists();
  },
};
</script>
