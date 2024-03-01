<template>
  <img
    class="playlist card-image"
    v-if="playlist.images?.length > 0"
    :src="playlist.images[0]?.url"
    :alt="playlist.name + ' playlist art'"
  />
  <p v-else class="playlist not-specified">No Playlist Image Provided</p>
  <div class="playlist card-body">
    <h5 class="playlist card-title">{{ playlist.name }}</h5>
    <h6 class="playlist card-album">
      Owner: {{ playlist.owner?.display_name }}
    </h6>
    <p class="playlist card-album">
      Visibility: {{ playlist.public ? "Public" : "Private" }}
    </p>
    <p class="playlist card-album">
      Description: {{ playlist.description || "* None *" }}
    </p>
    <p class="playlist card-album">Track Count: {{ playlist.tracks.total }}</p>
    <a class="btn-primary" :href="playlist.href">Check it out on Spotify</a>
  </div>
</template>

<script>
export default {
  name: "ListShowPlaylist",
  props: {
    playlist: Object,
  },
};
</script>
