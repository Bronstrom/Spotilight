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
    Owner: {{ playlistItem.owner?.display_name }}
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Visibility: {{ playlistItem.public ? "Public" : "Private" }}
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
    <a class="btn-primary" :href="playlistItem.href">Check it out on Spotify</a>
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
