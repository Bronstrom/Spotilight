<template>
  <div class="playlists">
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
