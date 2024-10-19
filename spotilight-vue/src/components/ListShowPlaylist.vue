<template>
  <td
    :style="{
      'background-color': color,
    }"
  >
    <img
      class="playlist list-image"
      v-if="playlistItem.images?.length > 0"
      :src="playlistItem.images[0]?.url"
      :alt="playlistItem.name + ' playlist art'"
      width="50rem"
    />
    <p v-else class="playlist not-specified">No Playlist Image Provided</p>
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.name }}
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.owner?.display_name }}
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.public ? "Public" : "Private" }}
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Description: {{ playlistItem.description || "* None *" }}
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Track Count: {{ playlistItem.tracks.total }}
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    <a
      v-if="playlistItem?.external_urls?.spotify"
      :href="playlistItem.external_urls.spotify"
      ><button type="button" class="btn btn-secondary">View on Spotify</button>
    </a>
  </td>
</template>

<script>
export default {
  name: "ListShowPlaylist",
  props: {
    playlistItem: Object,
    color: String,
  },
};
</script>
