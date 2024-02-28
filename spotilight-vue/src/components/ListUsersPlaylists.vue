<template>
  <div class="top-playlists m-5">
    <h3>List Playlists</h3>
    <div class="sort-playlists m-2">
      <p>Sort</p>
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="sort-playlists-dropdown"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ sortLabel }}
      </button>
      <div class="dropdown-menu" aria-labelledby="sort-playlists-dropdown">
        <a
          class="dropdown-item"
          @click="(sortLabel = 'Newest First'), sortNewestFirst()"
          >Newest First</a
        >
        <a
          class="dropdown-item"
          @click="(sortLabel = 'Oldest First'), sortOldestFirst()"
          >Oldest First</a
        >
        <a
          class="dropdown-item"
          @click="(sortLabel = 'Title Ascending'), sortAlphAsc()"
          >Title Ascending</a
        >
        <a
          class="dropdown-item"
          @click="(sortLabel = 'Title Descending'), sortAlphDesc()"
          >Title Descending</a
        >
        <a class="dropdown-item" @click="(sortLabel = 'Owner'), sortByOwner()"
          >Owner</a
        >
        <a
          class="dropdown-item"
          @click="(sortLabel = 'Total Tracks'), sortBytotalTracks()"
          >Total Tracks</a
        >
      </div>
    </div>
    <div class="filter-playlists m-2">
      <p>Filter</p>
      <button
        class="btn btn-primary dropdown-toggle"
        type="button"
        id="filter-playlists-dropdown"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ filterLabel }}
      </button>
      <div class="dropdown-menu" aria-labelledby="filter-playlists-dropdown">
        <a
          class="dropdown-item"
          @click="(filterLabel = 'No Filter'), (filterType = 'none')"
          >No Filter</a
        >
        <a
          class="dropdown-item"
          @click="
            (filterLabel = 'Public Playlists Only'), (filterType = 'public')
          "
          >Public Playlists Only</a
        >
        <a
          class="dropdown-item"
          @click="
            (filterLabel = 'Private Playlists Only'), (filterType = 'private')
          "
          >Private Playlists Only</a
        >
      </div>
    </div>
    <div
      class="playlist row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div
        class="playlist col"
        v-for="(playlist, index) in filterList(sortedPlaylistList)"
        v-bind:key="'playlist' + index"
        @click="goToPlaylistPage(playlist.id)"
      >
        {{ console.log(playlist) }}
        <div class="playlist card h-100">
          <img
            class="playlist card-image"
            v-if="playlist.images?.length > 0"
            :src="playlist.images[0]?.url"
            :alt="playlist.name + ' playlist art'"
          />
          <p v-else class="playlist not-specified">
            No Playlist Image Provided
          </p>
          <div class="playlist card-body">
            <h5 class="playlist card-title">{{ playlist.name }}</h5>
            <h6 class="playlist card-album">
              Owner: {{ playlist.owner?.display_name }}
            </h6>
            <p class="playlist card-album">
              Visibility: {{ playlist.public ? "Public" : "Private" }}
            </p>
            <p class="playlist card-album">
              Description: {{ playlist.description || "* None *" }}
            </p>
            <p class="playlist card-album">
              Track Count: {{ playlist.tracks.total }}
            </p>
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

function getHeader() {
  return {
    Authorization: `Bearer ${cookie.get("access_token")}`,
    "Content-Type": "application/json",
  };
}

export default {
  name: "ListUsersPlaylists",
  data() {
    return {
      sortLabel: null,
      filterType: "none",
      originalPlaylistsList: null,
      sortedPlaylistList: null,
      filtedPlaylistList: null,
    };
  },
  methods: {
    /* TODO: This method currently gets all of the user's playlists. It would probably be a good idea to limit
          this to some extent. A user can have a ton of playlists, and this could be expensive on the api
          having to chain together so many of these calls. Potentially a "Show more" button could be included
          to limit some more of this to limit the scopem to aquiring something like 250 playlists per call of
          this method (5 Spotify API calls).
     */
    aquireAllPlaylists() {
      let limit = 50;
      let offset = 0;
      let total = 0;
      let playlist_endpoint = `https://api.spotify.com/v1/me/playlists?offset=${offset}&limit=${limit}`;
      axios({
        method: "GET",
        url: playlist_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          this.originalPlaylistsList = res.data?.items;
          total = res.data.total;
          this.sortNewestFirst();

          // Aquire all playlists till reaching total playlist count
          offset = offset + limit;
          for (offset; offset < total; offset = offset + limit) {
            playlist_endpoint = `https://api.spotify.com/v1/me/playlists?offset=${offset}&limit=${limit}`;
            axios({
              method: "GET",
              url: playlist_endpoint,
              headers: getHeader(),
            })
              .then((res) => {
                this.originalPlaylistsList = [
                  ...this.originalPlaylistsList,
                  ...res.data?.items,
                ];
                this.sortLabel = "Newest First";
                this.sortNewestFirst();
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
    sortNewestFirst() {
      // TODO: This may not really be newest first
      this.sortedPlaylistList = [...this.originalPlaylistsList];
    },
    sortOldestFirst() {
      this.sortedPlaylistList = [...this.originalPlaylistsList]
        .slice()
        .reverse();
    },
    sortAlphAsc() {
      this.sortedPlaylistList = [...this.originalPlaylistsList].sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    },
    sortAlphDesc() {
      this.sortedPlaylistList = [...this.originalPlaylistsList].sort((a, b) =>
        b.name.localeCompare(a.name)
      );
    },
    sortByOwner() {
      this.sortedPlaylistList = [...this.originalPlaylistsList].sort((a, b) =>
        a.owner.display_name.localeCompare(b.owner.display_name)
      );
    },
    sortBytotalTracks() {
      this.sortedPlaylistList = [...this.originalPlaylistsList].sort(
        (a, b) => b.tracks.total - a.tracks.total
      );
    },
    filterList(list) {
      if (this.filterType === "none") {
        return this.sortedPlaylistList;
      } else if (this.filterType === "public") {
        return this.filterPublicOnly(list);
      } else if (this.filterType === "private") {
        return this.filterPrivateOnly(list);
      }
    },
    filterPublicOnly(list) {
      return list.filter((item) => item.public === true);
    },
    filterPrivateOnly(list) {
      return list.filter((item) => item.public === false);
    },
    goToPlaylistPage(playlistID) {
      window.location.href = `/playlist/${playlistID}`;
    },
  },
  created() {
    this.aquireAllPlaylists();
    this.filterLabel = "No Filter";
  },
};
</script>
