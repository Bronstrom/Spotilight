<template>
  <div class="playlist">
    <ListPlaylists />
  </div>
</template>

<script>
import ListPlaylists from "@/components/ListPlaylists.vue";

export default {
  name: "PlaylistView",
  components: {
    ListPlaylists,
  },
};
</script>
