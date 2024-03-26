<template>
  <div class="top-genres">
    <div class="dropdown time-range">
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
    <div class="chart container">
      <h3>Top Genres</h3>
      <Doughnut
        v-if="chartloaded"
        id="top-genres"
        :data="chartDataGenres"
        :options="chartOptionsGenres"
      />
      <p>
        {{ genreDebrief(spotifyCategoryGenreCountCurrent, "genre") }}
      </p>
    </div>
    <div class="chart container">
      <h3>Top Sub-Genres:</h3>
      <Doughnut
        v-if="chartloaded"
        id="top-subgenres"
        :data="chartDataSubgenres"
        :options="chartOptionsSubgenres"
      />
      <p>
        {{ genreDebrief(userGenreCountCurrent, "sub-genre") }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
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

const TOP_COUNT = 50;

export default {
  name: "TopGenres",
  components: { Doughnut },
  data() {
    return {
      originalGenresShort: [],
      originalGenresMedium: [],
      originalGenresLong: [],

      userGenreCountShort: [],
      spotifyCategoryGenreCountShort: [],
      userGenreCountMedium: [],
      spotifyCategoryGenreCountMedium: [],
      userGenreCountLong: [],
      spotifyCategoryGenreCountLong: [],
      userGenreCountCurrent: {},
      spotifyCategoryGenreCountCurrent: {},

      timeRange: "Medium Term",
      label: ["Count"],
      backgroundColor: ["#e4cff6", "#ecc5ae", "#c6f1c8"],

      chartDataGenres: {
        labels: null,
        datasets: null,
      },
      chartOptionsGenres: {
        cutoutPercentage: 20,
        rotation: Math.PI,
        animation: {
          animateScale: true,
        },
        // Hide legend
        plugins: {
          legend: {
            display: false,
          },
        },
        responsive: true,
      },
      chartDataSubgenres: {
        labels: null,
        datasets: null,
      },
      chartOptionsSubgenres: {
        cutoutPercentage: 20,
        rotation: Math.PI,
        animation: {
          animateScale: true,
        },
        // Hide legend
        plugins: {
          legend: {
            display: false,
          },
        },
        responsive: true,
      },

      chartloaded: false,
    };
  },
  methods: {
    genreDebrief(currentList, genreType) {
      let period;
      switch (this.timeRange) {
        case "Short Term":
          period = "four weeks";
          break;
        case "Medium Term":
          period = "six months";
          break;
        case "Long Term":
          period = "over a year";
          break;
      }

      return `You've listened to
        ${currentList?.keys?.length} ${genreType}(s) in the
        past ${period}, with ${currentList?.keys?.[0]} at the top.`;
    },
    async getTopGenres() {
      // This genre list is generated from Spotify, plus or minus a few additional
      this.handleUserTopArtistGenres({
        genres: [
          "acoustic",
          "afrobeat",
          "alt-rock",
          "alternative",
          "ambient",
          "anime",
          "black-metal",
          "bluegrass",
          "blues",
          "bossanova",
          "brazil",
          "breakbeat",
          "british",
          "cantopop",
          "chicago-house",
          "children",
          "chill",
          "classical",
          "club",
          "comedy",
          "commercial",
          "country",
          "dance",
          "dancehall",
          "death-metal",
          "deep-house",
          "detroit-techno",
          "disco",
          "drum-and-bass",
          "dub",
          "dubstep",
          "edm",
          "electro",
          "electronic",
          "emo",
          "exercise",
          "flamenco",
          "folk",
          "forro",
          "french",
          "funk",
          "garage",
          "german",
          "gospel",
          "goth",
          "grindcore",
          "groove",
          "grunge",
          "guitar",
          "happy",
          "hard-rock",
          "hardcore",
          "hardstyle",
          "heavy-metal",
          "hip-hop",
          "holidays",
          "honky-tonk",
          "house",
          "idm",
          "indian",
          "indie",
          "indie-pop",
          "industrial",
          "instrumental",
          "iranian",
          "j-dance",
          "j-idol",
          "j-pop",
          "j-rock",
          "jazz",
          "k-pop",
          "kids",
          "latin",
          "latino",
          "lo-fi",
          "malay",
          "mandopop",
          "merengue",
          "metal",
          "metalcore",
          "movies",
          "mpb",
          "new-age",
          "new-release",
          "opera",
          "pagode",
          "party",
          "philippines-opm",
          "piano",
          "pop",
          "pop-film",
          "post-dubstep",
          "post-disco",
          "power-pop",
          "progressive",
          "psych-rock",
          "punk",
          "punk-rock",
          "rap",
          "r-n-b",
          "r&b",
          "rainy-day",
          "reggae",
          "reggaeton",
          "rock",
          "rock-n-roll",
          "rockabilly",
          "romance",
          "sad",
          "salsa",
          "samba",
          "sertanejo",
          "show-tunes",
          "singer-songwriter",
          "ska",
          "sleep",
          "songwriter",
          "soul",
          "soundtrack",
          "spanish",
          "study",
          "summer",
          "swedish",
          "synth-pop",
          "tango",
          "techno",
          "tex-mex",
          "trance",
          "traditional",
          "trip-hop",
          "turkish",
          "vocal",
          "work-out",
          "world",
        ],
      });
      /* TODO: Consider aquiring genre list instead of creating it from sources
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
        });*/
    },
    compileAndSetFinalGenreLists(artistList, genreList) {
      const [userGenres, spotifyGenres] = this.compileListOfTopGenres(
        artistList,
        genreList
      );
      const userCount = this.sortKeyValuePairsByHighestValue(
        Object.keys(userGenres),
        Object.values(userGenres)
      );
      const spotifyCount = this.sortKeyValuePairsByHighestValue(
        Object.keys(spotifyGenres),
        Object.values(spotifyGenres)
      );
      return [userCount, spotifyCount];
    },
    setPieChartData(genres, subgenres) {
      this.chartDataGenres = {
        labels: genres.keys,
        datasets: [
          {
            label: this.label,
            data: genres.values,
            backgroundColor: this.backgroundColor,
          },
        ],
      };
      this.chartDataSubgenres = {
        labels: subgenres.keys,
        datasets: [
          {
            label: this.label,
            data: subgenres.values,
            backgroundColor: this.backgroundColor,
          },
        ],
      };
    },
    async handleUserTopArtistGenres(spotifyGenreList) {
      const medium_term_artist_endpoint = `/spotlight/top-artists/medium_term/0/${TOP_COUNT}`;
      await axios
        .get(medium_term_artist_endpoint)
        .then((res) => {
          //console.log(res.data);
          this.originalGenresMedium = res.data?.items;

          let limit = TOP_COUNT;
          let offset = 0;
          let total = res.data?.total;

          // Aquire all artists till reaching total artist count
          offset = offset + limit;

          // TODO: Create helper function
          if (offset >= total) {
            const [userCountMedium, spotifyCountMedium] =
              this.compileAndSetFinalGenreLists(
                res.data?.items,
                spotifyGenreList
              );
            this.userGenreCountMedium = userCountMedium;
            this.userGenreCountCurrent = userCountMedium;
            this.spotifyCategoryGenreCountMedium = spotifyCountMedium;
            this.spotifyCategoryGenreCountCurrent = spotifyCountMedium;
            this.setPieChartData(spotifyCountMedium, userCountMedium);
            this.chartloaded = true;
          }
          for (offset; offset < total; offset = offset + limit) {
            let artist_endpoint = `/spotlight/top-artists/medium_term/${offset}/${TOP_COUNT}`;
            axios
              .get(artist_endpoint)
              .then((res) => {
                const completeGenreList = [
                  ...this.originalGenresMedium,
                  res.data?.items,
                ];
                this.originalGenresMedium = completeGenreList;

                // TODO: Create helper function
                if (offset >= total) {
                  const [userCountMedium, spotifyCountMedium] =
                    this.compileAndSetFinalGenreLists(
                      completeGenreList,
                      spotifyGenreList
                    );
                  this.userGenreCountMedium = userCountMedium;
                  this.userGenreCountCurrent = userCountMedium;
                  this.spotifyCategoryGenreCountMedium = spotifyCountMedium;
                  this.spotifyCategoryGenreCountCurrent = spotifyCountMedium;
                  this.setPieChartData(spotifyCountMedium, userCountMedium);
                  this.chartloaded = true;
                }
              })
              .catch((err) => {
                console.error(err);
              });
          }
        })
        .catch((err) => {
          console.error(err);
        });
      const short_term_artist_endpoint = `/spotlight/top-artists/short_term/0/${TOP_COUNT}`;
      await axios
        .get(short_term_artist_endpoint)
        .then((res) => {
          this.originalGenresShort = res.data?.items;

          let limit = TOP_COUNT;
          let offset = 0;
          let total = res.data?.total;

          // Aquire all artists till reaching total artist count
          offset = offset + limit;

          // TODO: Create helper function
          if (offset >= total) {
            const [userCountShort, spotifyCountShort] =
              this.compileAndSetFinalGenreLists(
                res.data?.items,
                spotifyGenreList
              );
            this.userGenreCountShort = userCountShort;
            this.spotifyCategoryGenreCountShort = spotifyCountShort;
          }
          for (offset; offset < total; offset = offset + limit) {
            let artist_endpoint = `/spotlight/top-artists/short_term/${offset}/${TOP_COUNT}`;
            axios
              .get(artist_endpoint)
              .then((res) => {
                const completeGenreList = [
                  ...this.originalGenresShort,
                  res.data?.items,
                ];
                this.originalGenresShort = completeGenreList;

                // TODO: Create helper function
                if (offset >= total) {
                  const [userCountShort, spotifyCountShort] =
                    this.compileAndSetFinalGenreLists(
                      completeGenreList,
                      spotifyGenreList
                    );
                  this.userGenreCountShort = userCountShort;
                  this.spotifyCategoryGenreCountShort = spotifyCountShort;
                }
              })
              .catch((err) => {
                console.error(err);
              });
          }
        })
        .catch((err) => {
          console.error(err);
        });
      const long_term_artist_endpoint = `/spotlight/top-artists/long_term/0/${TOP_COUNT}`;
      await axios
        .get(long_term_artist_endpoint)
        .then((res) => {
          this.originalGenresLong = res.data?.items;

          let limit = TOP_COUNT;
          let offset = 0;
          let total = res.data?.total;

          // Aquire all artists till reaching total artist count
          offset = offset + limit;

          // TODO: Create helper function
          if (offset >= total) {
            const [userCountLong, spotifyCountLong] =
              this.compileAndSetFinalGenreLists(
                res.data?.items,
                spotifyGenreList
              );
            this.userGenreCountLong = userCountLong;
            this.spotifyCategoryGenreCountLong = spotifyCountLong;
          }
          for (offset; offset < total; offset = offset + limit) {
            let artist_endpoint = `/spotlight/top-artists/long_term/${offset}/${TOP_COUNT}`;
            axios
              .get(artist_endpoint)
              .then((res) => {
                const completeGenreList = [
                  ...this.originalGenresLong,
                  res.data?.items,
                ];
                this.originalGenresLong = completeGenreList;

                // TODO: Create helper function
                if (offset >= total) {
                  const [userCountLong, spotifyCountLong] =
                    this.compileAndSetFinalGenreLists(
                      completeGenreList,
                      spotifyGenreList
                    );
                  this.userGenreCountLong = userCountLong;
                  this.spotifyCategoryGenreCountLong = spotifyCountLong;
                }
              })
              .catch((err) => {
                console.error(err);
              });
          }
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
      let spotifySubGenreCount = {};

      // Get the top classification of sub genres provided by artists
      for (const [userGenreKey, userGenreValue] of Object.entries(
        userGenreCount
      )) {
        // Set sub-genres - ensure that a top level categorized genre isn't included
        if (!spotifyGenreList?.genres.includes(userGenreKey)) {
          if (spotifySubGenreCount[userGenreKey] === undefined) {
            spotifySubGenreCount[userGenreKey] = userGenreValue;
          } else {
            spotifySubGenreCount[userGenreKey] =
              spotifySubGenreCount[userGenreKey] + userGenreValue;
          }
        }
        let foundCategoryGenre = false;
        spotifyGenreList?.genres?.forEach((spotifyGenre, index) => {
          // Set high level "categorized" genres
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
            // TODO: This unclassified data should probably be used differently or not
            // included in the categorized genre list
            if (spotifyCategoryGenreCount["unclassified"] === undefined) {
              spotifyCategoryGenreCount["unclassified"] = userGenreValue;
            } else {
              spotifyCategoryGenreCount["unclassified"] =
                spotifyCategoryGenreCount["unclassified"] + userGenreValue;
            }
          }
        });
      }

      return [spotifySubGenreCount, spotifyCategoryGenreCount];
    },
    userGenreMatchSpotifyGenres(userGenre, spotifyGenre) {
      const userGenreAltered = userGenre.toLowerCase().replace("-", " ");
      const spotifyGenreAltered = spotifyGenre.toLowerCase().replace("-", " ");
      return userGenreAltered.includes(spotifyGenreAltered);
    },
    sortKeyValuePairsByHighestValue(keys, values) {
      const keyPairDict = keys.map((prevKey, index) => {
        return {
          key: prevKey,
          value: values[index] || 0,
        };
      });

      const sortedDict = keyPairDict.sort((a, b) => {
        return b.value - a.value;
      });

      let sortedKeys = [];
      let sortedValues = [];
      sortedDict.forEach((item) => {
        sortedKeys.push(item.key);
        sortedValues.push(item.value);
      });

      return { keys: sortedKeys, values: sortedValues };
    },
    changeTimeRange(range) {
      const spotifyCountShort = this.spotifyCategoryGenreCountShort;
      const userCountShort = this.userGenreCountShort;
      const spotifyCountLong = this.spotifyCategoryGenreCountLong;
      const userCountLong = this.userGenreCountLong;
      const spotifyCountMedium = this.spotifyCategoryGenreCountMedium;
      const userCountMedium = this.userGenreCountMedium;
      switch (range) {
        case "short_term":
          this.userGenreCountCurrent = userCountShort;
          this.spotifyCategoryGenreCountCurrent = spotifyCountShort;
          this.setPieChartData(spotifyCountShort, userCountShort);
          break;
        case "long_term":
          this.userGenreCountCurrent = userCountLong;
          this.spotifyCategoryGenreCountCurrent = spotifyCountLong;
          this.setPieChartData(spotifyCountLong, userCountLong);
          break;
        case "medium_term":
        default:
          this.userGenreCountCurrent = userCountMedium;
          this.spotifyCategoryGenreCountCurrent = spotifyCountMedium;
          this.setPieChartData(spotifyCountMedium, userCountMedium);
          break;
      }
    },
  },
  created() {
    this.getTopGenres();
  },
};
</script>
