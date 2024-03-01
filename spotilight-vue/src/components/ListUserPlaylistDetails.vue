<template>
  <div class="playlist m-5">
    <button type="button" class="btn btn-primary" @click="goToPlaylistsList">
      Return to Playlists List
    </button>
    <div v-if="!playlist.name">
      <h3>Loading Playlist . . .</h3>
    </div>
    <div v-else class="playlist">
      {{ console.log(playlist) }}
      <h3>{{ playlist.name }}</h3>
      <img
        v-if="playlist.images?.length > 0"
        class="playlist card-image"
        :src="playlist.images[0]?.url"
        :alt="playlist.name + ' playlist art'"
      />
      <p v-else class="playlist not-specified">No Playlist Image Provided</p>
      <div class="playlist card-body">
        <p class="playlist card-album">
          Owner: {{ playlist.owner?.display_name }}
        </p>
        <p class="playlist card-album">
          Visibility: {{ playlist.public ? "Public" : "Private" }}
        </p>
        <p class="playlist card-album">
          Follower Count:
          {{
            playlist.public
              ? playlist.followers.total
              : "* Not a public playlist *"
          }}
        </p>
        <p class="playlist card-album">
          Collaboration:
          {{ playlist.collaborative ? "Allowed" : "Not allowed" }}
        </p>
        <p class="playlist card-album">
          Description: {{ playlist.description || "* None *" }}
        </p>
        <p class="playlist card-album">
          Track Count: {{ playlist.tracks.total }}
        </p>
      </div>
    </div>
    <div>
      <p4>Track List</p4>
      <div v-if="originalTrackList.length < 1" class="track not-specified">
        No tracks in this playlist
      </div>
      <div v-else>
        <ListPlaylistItems
          playlistItemType="track"
          :originalPlaylistItems="originalTrackList"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import cookie from "js-cookie";
import ListPlaylistItems from "../components/ListPlaylistItems.vue";

//const BACK_END_URL = "http://localhost:5000";

function getHeader() {
  return {
    Authorization: `Bearer ${cookie.get("access_token")}`,
    "Content-Type": "application/json",
  };
}

export default {
  name: "ListUserPlaylistDetails",
  components: {
    ListPlaylistItems,
  },
  props: {
    playlistID: String,
  },
  data() {
    return {
      originalTrackList: [],
      playlist: [],
    };
  },
  methods: {
    aquirePlaylist() {
      let playlist_endpoint = `https://api.spotify.com/v1/playlists/${this.playlistID}`;
      axios({
        method: "GET",
        url: playlist_endpoint,
        headers: getHeader(),
      })
        .then((res) => {
          const playlist = res.data;
          this.playlist = playlist;
          this.originalTrackList = playlist.tracks.items;

          // TODO: Consider instead of grabbing all of these values and determining the next link, use `playlist.tracks.next`
          // for the link. Potentially may need to create a new function to handle axios calls and determine when there is
          // no `next` field.
          let limit = playlist.tracks.limit;
          let offset = playlist.tracks.offset;
          let total = playlist.tracks.total;

          // Aquire all tracks till reaching total track count
          offset = offset + limit;
          for (offset; offset < total; offset = offset + limit) {
            playlist_endpoint = `https://api.spotify.com/v1/playlists/${this.playlistID}/tracks?offset=${offset}&limit=${limit}`;
            axios({
              method: "GET",
              url: playlist_endpoint,
              headers: getHeader(),
            })
              .then((res) => {
                this.originalTrackList = [
                  ...this.originalTrackList,
                  ...res.data?.items,
                ];
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
    goToPlaylistsList() {
      window.location.href = "/playlists";
    },
  },
  created() {
    this.aquirePlaylist();
  },
};
</script>
