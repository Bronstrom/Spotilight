<template>
  <img
    class="playlist card-image"
    v-if="playlistItem.images?.length > 0"
    :src="playlistItem.images[0]?.url"
    :alt="playlistItem.name + ' playlist art'"
  />
  <p v-else class="playlist not-specified">No Playlist Image Provided</p>
  <div class="playlist card-body">
    <h5 class="playlist card-title">{{ playlistItem.name }}</h5>
    <h6 class="playlist card-album">
      Owner: {{ playlistItem.owner?.display_name }}
    </h6>
    <p class="playlist card-album">
      Visibility: {{ playlistItem.public ? "Public" : "Private" }}
    </p>
    <p class="playlist card-album">
      Description: {{ playlistItem.description || "* None *" }}
    </p>
    <p class="playlist card-album">
      Track Count: {{ playlistItem.tracks.total }}
    </p>
    <a class="btn-primary" :href="playlistItem.href">Check it out on Spotify</a>
  </div>
</template>

<script>
export default {
  name: "GridShowPlaylist",
  props: {
    playlistItem: Object,
  },
};
</script>
