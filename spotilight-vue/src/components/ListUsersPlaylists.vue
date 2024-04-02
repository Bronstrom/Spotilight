<template>
  <div class="playlists">
    <ListPlaylistItems
      playlistItemType="playlist"
      playlistItemTitle="List Playlists"
      :originalPlaylistItems="originalPlaylistList"
      :loadedItemList="loadedItemList"
      @deleted="aquireAllPlaylists"
      @created="aquireAllPlaylists"
    />
  </div>
</template>

<script>
import axios from "axios";
import ListPlaylistItems from "../components/ListPlaylistItems.vue";

export default {
  name: "ListUsersPlaylists",
  components: {
    ListPlaylistItems,
  },
  data() {
    return {
      originalPlaylistList: null,
      loadedItemList: false,
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
      let playlists_endpoint = `playlists/${offset}/${limit}`;
      axios
        .get(playlists_endpoint)
        .then((res) => {
          this.originalPlaylistList = res.data?.items;
          total = res.data.total;
          // Aquire all playlists till reaching total playlist count
          offset = offset + limit + 1;
          for (offset; offset < total; offset = offset + limit) {
            playlists_endpoint = `playlists/${offset}/${limit}`;
            axios
              .get(playlists_endpoint)
              .then((res) => {
                this.originalPlaylistList = [
                  ...this.originalPlaylistList,
                  ...res.data?.items,
                ];
                this.loadedItemList = true;
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
  },
  created() {
    this.aquireAllPlaylists();
  },
};
</script>
