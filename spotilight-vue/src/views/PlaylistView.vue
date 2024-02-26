<template>
  <div class="playlist">
    <ListPlaylistTracks v-bind:playlistID="$route.params.id" />
  </div>
</template>

<script>
import ListPlaylistTracks from "../components/ListPlaylistTracks.vue";

export default {
  name: "PlaylistView",
  components: {
    ListPlaylistTracks,
  },
};
</script>
