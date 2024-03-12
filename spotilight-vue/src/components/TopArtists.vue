<template>
  <div class="top-artists m-5">
    <h3>Top Artists</h3>
    <div class="dropdown time-range">
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
    <div class="artist create-playlist-from-list">
      <button
        class="btn btn-primary create-from-list"
        data-bs-toggle="modal"
        data-bs-target="#create-playlist-item-modal-artist"
      >
        + Create Playlist
      </button>
      <SpotilightModal
        title="Create playlist"
        id="create-playlist-item-modal-artist"
        :body="
          'Enter a name below for a playlist with the top five tracks for your top ' +
          limit +
          ' artists and select Create Playlist.'
        "
        :actionLabel="'Create playlist'"
        :inputLabel="'Playlist name'"
        :inputPlaceholder="'Playlist name'"
        @action="(name) => createPlaylist(name, 5)"
      />
    </div>
    <div
      class="artist row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="artist col"
        v-for="artist in limitedTopArtists()"
        v-bind:key="artist.id"
      >
        <div class="artist card h-100">
          <!--{{ console.log(artist) }}-->
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
import SpotilightModal from "../components/SpotilightModal.vue";
import axios from "axios";

const DEFAULT_LIMIT_COUNT = 5;
const MAX_LIMIT_COUNT = 25;

export default {
  name: "TopArtists",
  components: {
    SpotilightModal,
  },
  data() {
    return {
      topArtistsShort: [],
      topArtistsMedium: [],
      topArtistsLong: [],
      curTopArtists: [],
      timeRange: "Medium Term",
      limit: DEFAULT_LIMIT_COUNT,
    };
  },
  methods: {
    limitedTopArtists() {
      return this.curTopArtists?.slice(0, this.limit);
    },
    handleTopArtists() {
      // TODO: Refactor some of this duplication
      const medium_term_artist_endpoint =
        "/spotlight/top-artists/medium_term/0/" + MAX_LIMIT_COUNT;
      axios
        .get(medium_term_artist_endpoint)
        .then((res) => {
          this.topArtistsMedium = res.data.items;
          this.curTopArtists = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });

      const short_term_artist_endpoint =
        "/spotlight/top-artists/short_term/0/" + MAX_LIMIT_COUNT;
      axios
        .get(short_term_artist_endpoint)
        .then((res) => {
          this.topArtistsShort = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });

      const long_term_artist_endpoint =
        "/spotlight/top-artists/long_term/0/" + MAX_LIMIT_COUNT;
      axios
        .get(long_term_artist_endpoint)
        .then((res) => {
          this.topArtistsLong = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });

      /* TOOD: Try simpler axios structure
      const short_term_artist_endpoint = `https://api.spotify.com/v1/me/top/artists?time_range=short_term&offset=0&limit=${TOP_COUNT}`;
      const medium_term_artist_endpoint = `https://api.spotify.com/v1/me/top/artists?time_range=medium_term&offset=0&limit=${TOP_COUNT}`;
      const long_term_artist_endpoint = `https://api.spotify.com/v1/me/top/artists?time_range=long_term&offset=0&limit=${TOP_COUNT}`;

      const [
        shortTermArtistList,
        mediumTermArtistList,
        longTermArtistList,
      ] = await Promise.all([
        axios({
          method: "GET",
          url: short_term_artist_endpoint,
          headers: getHeader(),
        }),
        axios({
          method: "GET",
          url: medium_term_artist_endpoint,
          headers: getHeader(),
        }),
        axios({
          method: "GET",
          url: long_term_artist_endpoint,
          headers: getHeader(),
        }),
      ]);

      this.topArtistsShort = shortTermArtistList.data.item;
      this.topArtistsMedium = mediumTermArtistList.data.item;
      this.topArtistsLong = longTermArtistList.data.item;
      */
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
    createPlaylist(name, trackLimit) {
      let trackList = [];

      this.limitedTopArtists().forEach((artist) => {
        const artist_top_track_endpoint = `/spotlight/${artist.id}/top-tracks`;

        axios
          .get(artist_top_track_endpoint)
          .then((res) => {
            trackList = [...trackList, res.data.tracks];
            // Handle fully populated track list
            console.log(trackList.length);
            // Ensure all artist top track lists have been added to full list
            if (trackList.length === this.limit) {
              console.log(trackList);
              let uriList = [];
              trackList.forEach((artistTopTrackList) => {
                artistTopTrackList
                  .slice(0, trackLimit)
                  .map((track) => (uriList = [...uriList, track.uri]));
              });
              console.log(uriList);
              console.log(name);

              const post_playlist_path = `/playlist/create/${name}`;
              axios({
                method: "post",
                url: post_playlist_path,
                data: {
                  items: uriList,
                },
              })
                .then((res) => {
                  console.log(res.data);
                })
                .catch((err) => {
                  console.error(err);
                });
            }
          })
          .catch((err) => {
            console.error(err);
          });
      });
    },
  },
  created() {
    this.handleTopArtists();
  },
};
</script>
