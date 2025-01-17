<template>
  <div class="top-tracks">
    <h3 class="col">Top Tracks</h3>
    <div class="row">
      <div class="col dropdown time-range">
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
      <div class="col dropdown limit">
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
      <div class="col track create-playlist-from-list">
        <button
          class="btn btn-primary create-from-list"
          data-bs-toggle="modal"
          data-bs-target="#create-playlist-item-modal-track"
        >
          + Create Playlist
        </button>
        <SpotilightModal
          title="Create playlist"
          id="create-playlist-item-modal-track"
          :body="
            'Enter a name below for the ' +
            limit +
            ' tracks and select Create Playlist.'
          "
          :actionLabel="'Create playlist'"
          :inputLabel="'Playlist name'"
          :inputPlaceholder="'Playlist name'"
          @action="(name) => createPlaylist(name)"
        />
      </div>
    </div>
    <div
      class="track row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center pt-3"
    >
      <!-- Skeleton items -->
      <template v-if="curTopTracks.length === 0">
        <div
          v-for="index in 5"
          class="track col"
          v-bind:key="index + '_placeholder_item'"
          :id="index + '_placeholder_item'"
        >
          <PlaceholderCard />
        </div>
      </template>
      <div
        v-else
        class="track col"
        v-for="track in limitedTopItems()"
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
                {{ artist.name }}
              </span>
            </p>
            <a
              v-if="track?.external_urls?.spotify"
              :href="track.external_urls.spotify"
              ><button type="button" class="btn btn-secondary">
                View on Spotify
              </button>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SpotilightModal from "../components/SpotilightModal.vue";
import axios from "axios";
import PlaceholderCard from "./PlaceholderCard.vue";

const DEFAULT_LIMIT_COUNT = 5;
const MAX_LIMIT_COUNT = 25;

export default {
  name: "TopTracks",
  components: {
    SpotilightModal,
    PlaceholderCard,
  },
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
      const medium_term_track_endpoint =
        "/showcase/top-tracks/medium_term/" + MAX_LIMIT_COUNT;
      axios
        .get(medium_term_track_endpoint)
        .then((res) => {
          this.topTracksMedium = res.data.items;
          this.curTopTracks = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });

      const short_term_track_endpoint =
        "/showcase/top-tracks/short_term/" + MAX_LIMIT_COUNT;
      axios
        .get(short_term_track_endpoint)
        .then((res) => {
          this.topTracksShort = res.data.items;
        })
        .catch((err) => {
          console.error(err);
        });

      const long_term_track_endpoint =
        "/showcase/top-tracks/long_term/" + MAX_LIMIT_COUNT;
      axios
        .get(long_term_track_endpoint)
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
    limitedTopItems() {
      return this.curTopTracks?.slice(0, this.limit);
    },
    createPlaylist(name) {
      const uriList = this.limitedTopItems().map((track) => track.uri);
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
    },
  },
  created() {
    this.handleTopTracks();
  },
};
</script>
