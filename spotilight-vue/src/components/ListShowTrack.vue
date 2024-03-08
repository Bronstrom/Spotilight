<template>
  {{ console.log(playlistItem) }}
  <td
    :style="{
      'background-color': color,
    }"
  >
    <img
      class="track card-image"
      v-if="playlistItem.track.album.images?.length > 0"
      :src="playlistItem.track.album.images[0]?.url"
      :alt="playlistItem.track.album.name + ' track art'"
      width="50rem"
    />
    <p v-else class="track not-specified">No Track Image Provided</p>
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.track.name }}
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Added At: {{ playlistItem["added_at"] }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Local: {{ playlistItem["is_local"] }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Explicit: {{ playlistItem.track.explicit }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </td>
  <td
    v-if="playlistItem.track.album.album_type.toLowerCase() === 'single'"
    :style="{
      'background-color': color,
    }"
  >
    Single: {{ playlistItem.track.album.name }}
  </td>
  <td
    v-else
    :style="{
      'background-color': color,
    }"
  >
    Album: {{ playlistItem.track.album.name }} (Disc:
    {{ playlistItem.track["disc_number"] }}, Track:
    {{ playlistItem.track["track_number"] }})
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Duration: {{ playlistItem.track["duration_ms"] }} ms
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    Artist(s):
    <span v-for="(artist, index) in playlistItem.track?.artists" :key="artist">
      {{ index === 0 ? "" : ", " }}
      {{ artist.name }} ({{ artist.type }})
    </span>
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    <a class="btn-primary" :href="playlistItem.track.href"
      >Check it out on Spotify</a
    >
  </td>
</template>

<script>
export default {
  name: "ListShowTrack",
  props: {
    playlistItem: Object,
    color: String,
  },
};
</script>
