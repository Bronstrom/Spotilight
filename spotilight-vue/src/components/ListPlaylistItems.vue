<template>
  <div>
    <button
      type="button"
      @click="selectionMode = !selectionMode"
      :class="['btn', selectionMode ? 'btn-warning' : 'btn-secondary']"
    >
      Selection Mode
    </button>
  </div>
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
      <a v-if="isTypeTrack()" class="dropdown-item" @click="sortUnsorted"
        >Unsorted (User organized)</a
      >
      <a class="dropdown-item" @click="sortNewestFirst">Newest First</a>
      <a class="dropdown-item" @click="sortOldestFirst">Oldest First</a>
      <a class="dropdown-item" @click="sortAlphAsc">Title Ascending</a>
      <a class="dropdown-item" @click="sortAlphDesc">Title Descending</a>
      <template v-if="isTypePlaylist()">
        <a class="dropdown-item" @click="sortByOwner">Owner</a>
        <a class="dropdown-item" @click="sortByTotalTracks">Total Tracks</a>
      </template>
      <template v-if="isTypeTrack()">
        <a class="dropdown-item" @click="sortByArtist">Lead Artist</a>
      </template>
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
      <template v-if="isTypePlaylist()">
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
      </template>
      <template v-if="isTypeTrack()">
        <a
          class="dropdown-item"
          @click="
            (filterLabel = 'No Local Files Only'), (filterType = 'no-local')
          "
          >No Local Files Only</a
        >
        <a
          class="dropdown-item"
          @click="(filterLabel = 'Local Files Only'), (filterType = 'local')"
          >Local Files Only</a
        >
        <a
          class="dropdown-item"
          @click="
            (filterLabel = 'No Explicits Only'), (filterType = 'no-explicit')
          "
          >No Explicits Only</a
        >
        <a
          class="dropdown-item"
          @click="(filterLabel = 'Explicits Only'), (filterType = 'explicit')"
          >Explicits Only</a
        >
      </template>
    </div>
  </div>
  <div class="toggle grid list">
    <input
      v-on:change="viewType = 'grid'"
      type="radio"
      class="btn-check"
      name="view-options"
      id="grid-selection"
      autocomplete="off"
      checked
    />
    <label class="btn btn-outline-success" for="grid-selection">Grid</label>
    <input
      v-on:change="viewType = 'list'"
      type="radio"
      class="btn-check"
      name="view-options"
      id="list-selection"
      autocomplete="off"
    />
    <label class="btn btn-outline-danger" for="list-selection">List</label>
  </div>
  <div v-if="isTypeTrack() && selectionMode" class="selected-items">
    <button type="button" class="btn btn-primary" @click="selectAllItems">
      Select All Items
    </button>
    <button type="button" class="btn btn-primary" @click="clearSelectedItems">
      Unselect All Items
    </button>
  </div>
  <div
    v-if="isTypePlaylist() && selectedItems?.length > 0"
    class="selected-item-options"
  >
    <button
      class="btn btn-primary delete-selected-item"
      data-bs-toggle="modal"
      data-bs-target="#delete-playlist-item-modal"
    >
      Delete Selected Items
    </button>
    <SpotilightModal
      :title="'Delete ' + playlistItemType + '(s)'"
      id="delete-playlist-item-modal"
      :body="
        'Holy guacamole! You are about to delete  ' +
        selectedItems?.length +
        ' ' +
        playlistItemType +
        '(s). Are you sure you want to do this?'
      "
      :link="
        isTypePlaylist()
          ? 'https://www.spotify.com/us/account/recover-playlists/'
          : null
      "
      :linkInfo="isTypePlaylist() ? 'Playlists can be recovered at: ' : null"
      :linkLabel="isTypePlaylist() ? 'Spotify Recover Playlists' : null"
      :actionLabel="'Delete ' + playlistItemType + '(s)'"
      @action="deleteItems"
    />
    <button
      v-if="selectedItems?.length === 1"
      class="btn btn-primary duplicate-selected-item"
      data-bs-toggle="modal"
      data-bs-target="#duplicate-playlist-item-modal"
    >
      Duplicate Playlist
    </button>
    <SpotilightModal
      :title="'Duplicate ' + playlistItemType"
      id="duplicate-playlist-item-modal"
      :body="
        'Enter a name below for the new ' +
        playlistItemType +
        ' and select Create Playlist.'
      "
      :actionLabel="'Create playlist'"
      :inputLabel="'Playlist name'"
      :inputPlaceholder="'Playlist name'"
      @action="(name) => createPlaylistFromPlaylistID(name)"
    />
    <button
      v-if="selectedItems?.length > 1"
      class="btn btn-primary merge-selected-item"
      data-bs-toggle="modal"
      data-bs-target="#merge-playlist-item-modal"
    >
      Merge Selected Items
    </button>
    <SpotilightModal
      :title="'Merge ' + playlistItemType + 's'"
      id="merge-playlist-item-modal"
      :body="
        'Enter a name for the combination of ' +
        selectedItems?.length +
        ' ' +
        playlistItemType +
        's and select Create Playlist.'
      "
      :actionLabel="'Create playlist'"
      :inputLabel="'Playlist name'"
      :inputPlaceholder="'Playlist name'"
      @action="(name) => mergePlaylists(name)"
    />
  </div>
  <div
    v-if="isTypeTrack() && selectedItems?.length > 0"
    class="selected-item-options"
  >
    <button
      v-if="selectedItems?.length > 0"
      class="btn btn-primary create-playlist-from-selected-items"
      data-bs-toggle="modal"
      data-bs-target="#create-playlist-item-modal"
    >
      Create Playlist from Selected Items
    </button>
    <SpotilightModal
      :title="'Create ' + playlistItemType"
      id="create-playlist-item-modal"
      :body="
        'Enter a name below for the new ' +
        playlistItemType +
        ' containing the ' +
        selectedItems?.length +
        ' and select Create Playlist.'
      "
      :actionLabel="'Create playlist'"
      :inputLabel="'Playlist name'"
      :inputPlaceholder="'Playlist name'"
      @action="(name) => createPlaylistFromSelectedTracks(name)"
    />
  </div>
  <!-- Render grid view -->
  <div
    v-if="viewType === 'grid'"
    class="playlist row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
  >
    <div
      v-for="playlistItem in filterList(sortedPlaylistItems)"
      class="playlist col"
      v-bind:key="getPlaylistItemId(playlistItem)"
      :id="getPlaylistItemId(playlistItem) + '_item'"
      @click="
        !selectionMode
          ? isTypePlaylist() &&
            goToPlaylistPage(getPlaylistItemId(playlistItem))
          : handleSelection(getPlaylistItemId(playlistItem))
      "
    >
      <!--{{ console.log(playlist) }}-->
      <div
        class="playlist card h-100"
        :style="{
          'background-color': selectedItems.includes(
            getPlaylistItemId(playlistItem)
          )
            ? 'orange'
            : 'white',
        }"
      >
        <component :is="playlistItemComponent" :playlistItem="playlistItem" />
      </div>
    </div>
  </div>
  <!-- Render list view -->
  <table v-else class="table table-striped">
    <thead class="thead-dark">
      <tr>
        <th>Image</th>
        <th>Title</th>
        <th v-if="isTypePlaylist()">Owner</th>
        <th v-if="isTypePlaylist()">Visibility</th>
        <th v-if="isTypePlaylist()">Description</th>
        <th v-if="isTypePlaylist()">Track Count</th>
        <th v-if="isTypeTrack()">Added At</th>
        <th v-if="isTypeTrack()">Local</th>
        <th v-if="isTypeTrack()">Explicit</th>
        <th v-if="isTypeTrack()">Album/Single</th>
        <th v-if="isTypeTrack()">Duration</th>
        <th v-if="isTypeTrack()">Artist</th>
        <th>Link</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="playlistItem in filterList(sortedPlaylistItems)"
        v-bind:key="getPlaylistItemId(playlistItem)"
        :id="getPlaylistItemId(playlistItem) + '_item'"
        @click="
          !selectionMode
            ? isTypePlaylist() &&
              goToPlaylistPage(getPlaylistItemId(playlistItem))
            : handleSelection(getPlaylistItemId(playlistItem))
        "
      >
        <component
          :is="playlistItemComponent"
          :playlistItem="playlistItem"
          :color="
            selectedItems.includes(getPlaylistItemId(playlistItem))
              ? 'orange'
              : 'white'
          "
        />
      </tr>
    </tbody>
  </table>
</template>

<script>
import GridShowPlaylist from "../components/GridShowPlaylist.vue";
import GridShowTrack from "../components/GridShowTrack.vue";
import ListShowPlaylist from "../components/ListShowPlaylist.vue";
import ListShowTrack from "../components/ListShowTrack.vue";
import SpotilightModal from "../components/SpotilightModal.vue";
import axios from "axios";

export default {
  name: "ListUsersPlaylists",
  emits: ["deleted"],
  components: {
    GridShowPlaylist,
    GridShowTrack,
    ListShowPlaylist,
    ListShowTrack,
    SpotilightModal,
  },
  props: {
    playlistItemType: String,
    originalPlaylistItems: Object,
    // Single playlist item specific
    itemId: String,
  },
  data() {
    return {
      selectedItems: [],
      selectionMode: false,
      sortLabel: null,
      filterType: "none",
      sortedPlaylistItems: null,
      filtedPlaylistItems: null,
      viewType: "grid",
    };
  },
  watch: {
    $props: {
      handler() {
        if (this.originalPlaylistItems !== null) {
          if (this.isTypeTrack()) {
            this.sortUnsorted();
          } else {
            this.sortNewestFirst();
          }
          this.filterLabel = "No Filter";
        }
      },
      deep: true,
      immediate: true,
    },
    selectionMode: function (val) {
      if (!val) {
        this.resetSelectedItems();
      }
    },
  },
  computed: {
    playlistItemComponent() {
      if (this.isTypePlaylist()) {
        return this.viewType === "grid" ? GridShowPlaylist : ListShowPlaylist;
      } else {
        return this.viewType === "grid" ? GridShowTrack : ListShowTrack;
      }
    },
  },
  methods: {
    isTypePlaylist() {
      return this.playlistItemType === "playlist";
    },
    isTypeTrack() {
      return this.playlistItemType === "track";
    },
    getPlaylistItemId(item) {
      return this.isTypeTrack() ? item.track.id : item.id;
    },
    handleSelection(id) {
      let selection = this.selectedItems;
      // Add item to selection list if it isn't already in there
      if (!selection.includes(id)) {
        this.selectedItems = [...selection, id];
      }
      // Remove item from selection list if it's already within the list
      else {
        const idIndex = selection.indexOf(id);
        selection.splice(idIndex, 1);
        this.selectedItems = selection;
      }
    },
    sortUnsorted() {
      this.sortLabel = "Unsorted";
      this.sortedPlaylistItems = [...this.originalPlaylistItems];
    },
    sortNewestFirst() {
      this.sortLabel = "Newest First";
      if (this.isTypeTrack()) {
        this.sortedPlaylistItems = [...this.originalPlaylistItems].sort(
          (a, b) => b["added_at"].localeCompare(a["added_at"])
        );
      }
      // TODO: This may not really be newest first
      else {
        this.sortedPlaylistItems = [...this.originalPlaylistItems];
      }
    },
    sortOldestFirst() {
      this.sortLabel = "Oldest First";
      if (this.isTypeTrack()) {
        this.sortedPlaylistItems = [...this.originalPlaylistItems].sort(
          (a, b) => a["added_at"].localeCompare(b["added_at"])
        );
      } else {
        this.sortedPlaylistItems = [...this.originalPlaylistItems]
          .slice()
          .reverse();
      }
    },
    sortAlphAsc() {
      this.sortLabel = "Title Ascending";
      this.sortedPlaylistItems = [...this.originalPlaylistItems].sort((a, b) =>
        this.isTypeTrack()
          ? a.track.name.localeCompare(b.track.name)
          : a.name.localeCompare(b.name)
      );
    },
    sortAlphDesc() {
      this.sortLabel = "Title Descending";
      this.sortedPlaylistItems = [...this.originalPlaylistItems].sort((a, b) =>
        this.isTypeTrack()
          ? b.track.name.localeCompare(a.track.name)
          : b.name.localeCompare(a.name)
      );
    },
    sortByOwner() {
      this.sortLabel = "Owner";
      this.sortedPlaylistItems = [...this.originalPlaylistItems].sort((a, b) =>
        a.owner.display_name.localeCompare(b.owner.display_name)
      );
    },
    sortByArtist() {
      this.sortLabel = "Lead Artist";
      this.sortedPlaylistItems = [...this.originalPlaylistItems].sort(function (
        a,
        b
      ) {
        // Sort by artist name appearing alphabetically
        if (a.track.artists[0].name > b.track.artists[0].name) {
          return 1;
        }
        if (a.track.artists[0].name < b.track.artists[0].name) {
          return -1;
        }
        // If there is a tie (same artist name), sort by song title alphabetically
        if (a.track.name > b.track.name) {
          return 1;
        }
        if (a.track.name < b.track.name) {
          return -1;
        }
      });
    },
    // Only relevant to playlists
    sortByTotalTracks() {
      this.sortLabel = "Total Tracks";
      this.sortedPlaylistItems = [...this.originalPlaylistItems].sort(
        (a, b) => b.tracks.total - a.tracks.total
      );
    },
    filterPublicOnly(list) {
      return list.filter((item) => item.public === true);
    },
    filterPrivateOnly(list) {
      return list.filter((item) => item.public === false);
    },
    filterNoLocalOnly(list) {
      return list.filter((item) => item.track["is_local"] === false);
    },
    filterLocalOnly(list) {
      return list.filter((item) => item.track["is_local"] === true);
    },
    filterNoExplicitOnly(list) {
      return list.filter((item) => item.track.explicit === false);
    },
    filterExplicitOnly(list) {
      return list.filter((item) => item.track.explicit === true);
    },
    filterList(list) {
      switch (this.filterType) {
        case "public":
          return this.filterPublicOnly(list);
        case "private":
          return this.filterPrivateOnly(list);
        case "no-local":
          return this.filterNoLocalOnly(list);
        case "local":
          return this.filterLocalOnly(list);
        case "no-explicit":
          return this.filterNoExplicitOnly(list);
        case "explicit":
          return this.filterExplicitOnly(list);
        case "none":
        default:
          return this.sortedPlaylistItems;
      }
    },
    // Only relevant to playlists
    goToPlaylistPage(playlistID) {
      window.location.href = `/playlist/${playlistID}`;
    },
    clearSelectedItems() {
      this.selectedItems = [];
    },
    selectAllItems() {
      this.selectedItems = this.filterList(this.sortedPlaylistItems)?.map(
        (item) => (this.isTypeTrack() ? item.track.id : item.id)
      );
    },
    resetSelectedItems() {
      this.clearSelectedItems();
      this.selectionMode = false;
    },
    deleteSuccess(output) {
      console.log("Delete returned with: ");
      console.log(output);
      this.resetSelectedItems();
      this.$emit("deleted");
    },
    deleteItems() {
      if (this.isTypePlaylist()) {
        const delete_playlists_path = `/playlists/delete`;
        axios({
          method: "delete",
          url: delete_playlists_path,
          data: {
            items: this.selectedItems,
          },
        })
          .then((res) => {
            this.deleteSuccess(res.data);
          })
          .catch((err) => {
            console.error(err);
          });
      } else {
        const delete_tracks_path = `/playlist/${this.itemId}/delete-tracks`;
        axios({
          method: "delete",
          url: delete_tracks_path,
          data: {
            items: this.selectedItems,
          },
        })
          .then((res) => {
            this.deleteSuccess(res.data);
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    // TODO: This function can be placed in a helper function file
    createPlaylistFromUris(trackList, name) {
      const uriList = trackList.map((trackItem) => trackItem.track.uri);
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
          this.resetSelectedItems();
          this.$emit("created");
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // TODO: Refactor mergePlaylist and createPlaylist
    createPlaylistFromPlaylistID(name) {
      const playlistId = this.selectedItems[0];
      let playlist_endpoint = "playlist/" + playlistId;
      axios
        .get(playlist_endpoint)
        .then((res) => {
          const playlist = res.data;
          let trackList = playlist.tracks.items;

          // TODO: Consider instead of grabbing all of these values and determining the next link, use `playlist.tracks.next`
          // for the link. Potentially may need to create a new function to handle axios calls and determine when there is
          // no `next` field.
          let limit = playlist.tracks.limit;
          let offset = playlist.tracks.offset;
          let total = playlist.tracks.total;

          // Aquire all tracks till reaching total track count
          offset = offset + limit;
          if (offset >= total) {
            this.createPlaylistFromUris(trackList, name);
          }
          for (offset; offset < total; offset = offset + limit) {
            playlist_endpoint = `playlist/${playlistId}/${offset}/${limit}`;
            axios
              .get(playlist_endpoint)
              .then((res) => {
                trackList = [...trackList, ...res.data?.items];
                if (offset >= total) {
                  this.createPlaylistFromUris(trackList, name);
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
    // TODO: Refactor mergePlaylist and createPlaylist
    mergePlaylists(name) {
      let trackList = [];
      this.selectedItems.forEach((playlistId, playlistIndex) => {
        playlistId = this.selectedItems[playlistIndex];
        let playlist_endpoint = "playlist/" + playlistId;
        axios
          .get(playlist_endpoint)
          .then((res) => {
            const playlist = res.data;
            trackList = [...trackList, ...playlist.tracks.items];
            // TODO: Consider instead of grabbing all of these values and determining the next link, use `playlist.tracks.next`
            // for the link. Potentially may need to create a new function to handle axios calls and determine when there is
            // no `next` field.
            let limit = playlist.tracks.limit;
            let offset = playlist.tracks.offset;
            let total = playlist.tracks.total;

            // Aquire all tracks till reaching total track count
            offset = offset + limit;
            if (
              offset >= total &&
              playlistIndex === this.selectedItems.length - 1
            ) {
              this.createPlaylistFromUris(trackList, name);
            }
            for (offset; offset < total; offset = offset + limit) {
              playlist_endpoint = `playlist/${playlistId}/${offset}/${limit}`;
              axios
                .get(playlist_endpoint)
                .then((res) => {
                  trackList = [...trackList, ...res.data?.items];
                  if (
                    offset >= total &&
                    playlistIndex === this.selectedItems.length - 1
                  ) {
                    this.createPlaylistFromUris(trackList, name);
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
      });
    },
    createPlaylistFromSelectedTracks(name) {
      const uriList = this.selectedItems.map(
        (trackItem) => "spotify:track:" + trackItem
      );
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
          this.resetSelectedItems();
          this.$emit("created");
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>
