<template>
  <div class="top-genres m-5">
    <h3>Top Genres</h3>
    <div class="chart container" style="height: 60vh; width: 100vw">
      <Doughnut
        v-if="loaded"
        id="top-genres"
        :data="chartDataGenres"
        :options="chartOptionsGenres"
      />
    </div>
    <p>Top Genre:</p>
    <p>
      You've listened to
      <!--{{ userGenreCount.total }} genres in the past
      {{ timeRange }}-->
    </p>
    <div class="chart container" style="height: 60vh; width: 100vw">
      <Doughnut
        v-if="loaded"
        id="top-subgenres"
        :data="chartDataSubgenres"
        :options="chartOptionsSubgenres"
      />
    </div>
    <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="top-genre-frequency-button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ timeRange }}
      </button>
      <div class="dropdown-menu" aria-labelledby="top-genre-frequency-button">
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
    <h4>Specifics</h4>
    <div
      class="genre row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="genre col"
        v-for="(userGenre, userGenreCount) in userGenreCountCurrent"
        v-bind:key="userGenre"
      >
        <div class="genre card h-100">
          {{ console.log(userGenre) }}
          <!--<img
            class="genre card-image"
            :src="userGenre.images[0].url"
            :alt="userGenre + ' album cover'"
          />-->
          <div class="genre card-body">
            <h5 class="genre card-title">
              {{ userGenre + " " + userGenreCount }}
            </h5>
          </div>
        </div>
      </div>
    </div>
    <h4>Catagories</h4>
    <div
      class="genre row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="genre col"
        v-for="(
          spotifyGenre, spotifyGenreCount
        ) in spotifyCategoryGenreCountCurrent"
        v-bind:key="spotifyGenre"
      >
        <div class="genre card h-100">
          {{ console.log(spotifyGenre) }}
          <!--<img
            class="genre card-image"
            :src="spotifyGenre.images[0].url"
            :alt="spotifyGenre + ' album cover'"
          />-->
          <div class="genre card-body">
            <h5 class="genre card-title">
              {{ spotifyGenre + " " + spotifyGenreCount }}
            </h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import cookie from "js-cookie";
//import Chart from "chart.js/auto";
import { Doughnut } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

//const BACK_END_URL = "http://localhost:5000";
const TOP_COUNT = 50;

function getHeader() {
  return {
    Authorization: `Bearer ${cookie.get("access_token")}`,
    "Content-Type": "application/json",
  };
}

export default {
  name: "TopGenres",
  components: { Doughnut },
  data() {
    return {
      userGenreCountShort: [],
      spotifyCategoryGenreCountShort: [],
      userGenreCountMedium: [],
      spotifyCategoryGenreCountMedium: [],
      userGenreCountLong: [],
      spotifyCategoryGenreCountLong: [],
      userGenreCountCurrent: {},
      spotifyCategoryGenreCountCurrent: {},

      timeRange: "Medium Term",

      chartDataGenres: {
        labels: null,
        datasets: null,
        loaded: false,
      },
      chartOptionsGenres: {
        cutoutPercentage: 20,
        rotation: Math.PI,
        animation: {
          animateScale: true,
        },
        responsive: true,
      },
      chartDataSubgenres: {
        labels: null,
        datasets: null,
        loaded: false,
      },
      chartOptionsSubgenres: {
        cutoutPercentage: 20,
        rotation: Math.PI,
        animation: {
          animateScale: true,
        },
        responsive: true,
      },
      /*data: {
          labels: Object.keys(this.spotifyCategoryGenreCountCurrent),
          datasets: [
            {
              label: "Points",
              backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              data: Object.values(this.spotifyCategoryGenreCountCurrent),
            },
          ],
        },
        options: {
          cutoutPercentage: 33,
          rotation: Math.PI,
          animation: {
            animateScale: true,
          },
        },*/
    };
  },
  methods: {
    async getTopGenres() {
      const spotify_genre_seed_endpoint = `https://api.spotify.com/v1/recommendations/available-genre-seeds`;
      await axios({
        method: "GET",
        url: spotify_genre_seed_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.handleUserTopArtistGenres(res.data);
        })
        .catch((err) => {
          console.error(err);
          return null;
        });
    },
    async handleUserTopArtistGenres(spotifyGenreList) {
      const medium_term_artist_endpoint = `https://api.spotify.com/v1/me/top/artists?time_range=medium_term&offset=0&limit=${TOP_COUNT}`;
      await axios({
        method: "GET",
        url: medium_term_artist_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          console.log(res.data);
          const [userGenres, spotifyGenres] = this.compileListOfTopGenres(
            res.data.items,
            spotifyGenreList
          );
          this.userGenreCountMedium = userGenres;
          this.userGenreCountCurrent = userGenres;
          this.spotifyCategoryGenreCountMedium = spotifyGenres;
          this.spotifyCategoryGenreCountCurrent = spotifyGenres;
          this.chartDataGenres = {
            labels: Object.keys(spotifyGenres),
            datasets: [
              {
                data: Object.values(spotifyGenres),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
          this.chartDataSubgenres = {
            labels: Object.keys(userGenres),
            datasets: [
              {
                data: Object.values(userGenres),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
          this.loaded = true;
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
          const [userGenres, spotifyGenres] = this.compileListOfTopGenres(
            res.data.items,
            spotifyGenreList
          );
          this.userGenreCountShort = userGenres;
          this.spotifyCategoryGenreCountShort = spotifyGenres;
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
          console.log(res.data);
          const [userGenres, spotifyGenres] = this.compileListOfTopGenres(
            res.data.items,
            spotifyGenreList
          );
          this.userGenreCountLong = userGenres;
          this.spotifyCategoryGenreCountLong = spotifyGenres;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    compileListOfTopGenres(artistList, spotifyGenreList) {
      // Create genre count hash map
      let userGenreCount = {};
      // Loop through artist object

      artistList?.forEach((artist) => {
        // Loop through genre array and count occurrences of each genre
        artist?.genres?.forEach((genre) => {
          if (userGenreCount[genre] === undefined) {
            userGenreCount[genre] = 1;
          } else {
            userGenreCount[genre]++;
          }
        });
      });

      let spotifyCategoryGenreCount = {};

      // Get the top classification of sub genres provided by artists
      for (const [userGenreKey, userGenreValue] of Object.entries(
        userGenreCount
      )) {
        let foundCategoryGenre = false;
        spotifyGenreList?.genres?.forEach((spotifyGenre, index) => {
          if (this.userGenreMatchSpotifyGenres(userGenreKey, spotifyGenre)) {
            /*console.log(
              "userGenreKey: " +
                userGenreKey +
                ", spotifyGenre: " +
                spotifyGenre
            );*/
            foundCategoryGenre = true;
            if (spotifyCategoryGenreCount[spotifyGenre] === undefined) {
              spotifyCategoryGenreCount[spotifyGenre] = userGenreValue;
            } else {
              spotifyCategoryGenreCount[spotifyGenre] =
                spotifyCategoryGenreCount[spotifyGenre] + userGenreValue;
            }
          } else if (
            !foundCategoryGenre &&
            index === spotifyGenreList.genres.length - 1
          ) {
            //console.log(userGenreKey + " was unclassified");
            if (spotifyCategoryGenreCount["unclassified"] === undefined) {
              spotifyCategoryGenreCount["unclassified"] = userGenreValue;
            } else {
              spotifyCategoryGenreCount["unclassified"] =
                spotifyCategoryGenreCount["unclassified"] + userGenreValue;
            }
          }
        });
      }

      // TODO: Next compare with genre seed recomendations - find at least one match (could be multiple)
      // for these genres - new larger has map (inlude hash counts for current list)
      // ex: indie rock - count 7
      // matches with indie: "indie rock".contains("indie") - now count +7
      // matches with rock: "indie rock".contains("rock") - now count +7
      // If could not find match put this in unknown list for now
      return [userGenreCount, spotifyCategoryGenreCount];
    },
    userGenreMatchSpotifyGenres(userGenre, spotifyGenre) {
      const userGenreAltered = userGenre.toLowerCase().replace("-", " ");
      const spotifyGenreAltered = spotifyGenre.toLowerCase().replace("-", " ");
      return userGenreAltered.includes(spotifyGenreAltered);
    },
    changeTimeRange(range) {
      switch (range) {
        case "short_term":
          this.userGenreCountCurrent = this.userGenreCountCurrentShort;
          this.chartDataGenres = {
            labels: Object.keys(this.spotifyCategoryGenreCountShort),
            datasets: [
              {
                data: Object.values(this.spotifyCategoryGenreCountShort),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
          this.chartDataSubgenres = {
            labels: Object.keys(this.userGenreCountShort),
            datasets: [
              {
                data: Object.values(this.userGenreCountShort),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
          break;
        case "long_term":
          this.chartDataGenres = {
            labels: Object.keys(this.spotifyCategoryGenreCountLong),
            datasets: [
              {
                data: Object.values(this.spotifyCategoryGenreCountLong),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
          this.chartDataSubgenres = {
            labels: Object.keys(this.userGenreCountLong),
            datasets: [
              {
                data: Object.values(this.userGenreCountLong),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
          break;
        case "medium_term":
        default:
          this.chartDataGenres = {
            labels: Object.keys(this.spotifyCategoryGenreCountMedium),
            datasets: [
              {
                data: Object.values(this.spotifyCategoryGenreCountMedium),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
          this.chartDataSubgenres = {
            labels: Object.keys(this.userGenreCountMedium),
            datasets: [
              {
                data: Object.values(this.userGenreCountMedium),
                backgroundColor: ["#f1c40f", "#e67e22", "#16a085"],
              },
            ],
          };
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
    this.getTopGenres();
  },
};
</script>
