<template>
  <div class="playlist main-content-gutter">
    <ListUserPlaylistDetails v-bind:playlistID="$route.params.id" />
  </div>
</template>

<script>
import ListUserPlaylistDetails from "../components/ListUserPlaylistDetails.vue";

export default {
  name: "PlaylistView",
  components: {
    ListUserPlaylistDetails,
  },
};
</script>
