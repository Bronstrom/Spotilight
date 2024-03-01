<template>
  <!-- TODO: This whole file can be removed once done transitioning over to refactored tracks and playlists -->
  <div class="playlist">
    <button type="button" class="btn btn-primary" @click="goToPlaylistsList">
      Return to Playlists List
    </button>
  </div>
  <div v-if="!playlist.name">
    <h3>Loading Playlist . . .</h3>
  </div>
  <div v-else class="playlist">
    {{ console.log(playlist) }}
    <h3>{{ playlist.name }}</h3>
    <img
      class="playlist card-image"
      v-if="playlist.images?.length > 0"
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
    <div
      class="track row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4 justify-content-center"
    >
      <div v-if="originalTrackList.length < 1" class="track not-specified">
        No tracks in this playlist
      </div>
      <div
        class="track col"
        v-else
        v-for="playlistItem in originalTrackList"
        v-bind:key="playlistItem.id"
      >
        <!--{{ console.log(playlistItem) }}-->
        <div class="track card h-100">
          <img
            class="track card-image"
            v-if="playlistItem.track.album.images?.length > 0"
            :src="playlistItem.track.album.images[0]?.url"
            :alt="playlistItem.track.album.name + ' track art'"
          />
          <p v-else class="track not-specified">No Track Image Provided</p>
          <h5 class="track card-title">{{ playlistItem.track.name }}</h5>
          <h6 class="track card-album">
            Added At: {{ playlistItem["added_at"] }}
            <!--by:
            {{ playlistItem["added_by"] }}-->
          </h6>
          <h6 class="track card-album">
            Local: {{ playlistItem["is_local"] }}
            <!--by:
            {{ playlistItem["added_by"] }}-->
          </h6>
          <h6 class="track card-album">
            Explicit: {{ playlistItem.track.explicit }}
            <!--by:
            {{ playlistItem["added_by"] }}-->
          </h6>
          <h6
            v-if="
              playlistItem.track.album.album_type.toLowerCase() === 'single'
            "
          >
            Single: {{ playlistItem.track.album.name }}
          </h6>
          <h6 v-else class="track card-album">
            Album: {{ playlistItem.track.album.name }} (Disc:
            {{ playlistItem.track["disc_number"] }}, Track:
            {{ playlistItem.track["track_number"] }})
          </h6>
          <p class="track card-album">
            Duration: {{ playlistItem.track["duration_ms"] }} ms
          </p>
          <p>
            Artist(s):
            <span
              class="track card-text"
              v-for="(artist, index) in playlistItem.track?.artists"
              :key="artist"
            >
              {{ index === 0 ? "" : ", " }}
              {{ artist.name }} ({{ artist.type }})
            </span>
          </p>
          <a class="btn-primary" :href="playlistItem.track.href"
            >Check it out on Spotify</a
          >
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
  name: "ListPlaylistTracks",
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
