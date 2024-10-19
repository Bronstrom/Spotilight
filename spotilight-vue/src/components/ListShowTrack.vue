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
    {{ playlistItem["added_at"] }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem["is_local"] }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.track.explicit }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </td>
  <td
    v-if="playlistItem.track.album.album_type.toLowerCase() === 'single'"
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.track.album.name }}
  </td>
  <td
    v-else
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.track.album.name }} (Disc:
    {{ playlistItem.track["disc_number"] }}, Track:
    {{ playlistItem.track["track_number"] }})
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
    {{ playlistItem.track["duration_ms"] }} ms
  </td>
  <td
    :style="{
      'background-color': color,
    }"
  >
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
    <a
      v-if="playlistItem?.track?.external_urls?.spotify"
      :href="playlistItem.track.external_urls.spotify"
      ><button type="button" class="btn btn-secondary">View on Spotify</button>
    </a>
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
