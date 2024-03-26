<template>
  <div class="playlists main-content-gutter">
    <ListUsersPlaylists />
  </div>
</template>

<script>
import ListUsersPlaylists from "@/components/ListUsersPlaylists.vue";

export default {
  name: "PlaylistsView",
  components: {
    ListUsersPlaylists,
  },
};
</script>
