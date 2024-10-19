<template>
  <img
    class="track card-image"
    v-if="playlistItem.track.album.images?.length > 0"
    :src="playlistItem.track.album.images[0]?.url"
    :alt="playlistItem.track.album.name + ' track art'"
  />
  <p v-else class="track not-specified">No Track Image Provided</p>
  <h5 class="track card-title">{{ playlistItem.track.name }}</h5>
  <h6 class="track card-album">
    Added At: {{ playlistItem["added_at"] }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </h6>
  <h6 class="track card-album">
    Local: {{ playlistItem["is_local"] }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </h6>
  <h6 class="track card-album">
    Explicit: {{ playlistItem.track.explicit }}
    <!--by:
            {{ playlistItem["added_by"] }}-->
  </h6>
  <h6 v-if="playlistItem.track.album.album_type.toLowerCase() === 'single'">
    Single: {{ playlistItem.track.album.name }}
  </h6>
  <h6 v-else class="track card-album">
    Album: {{ playlistItem.track.album.name }} (Disc:
    {{ playlistItem.track["disc_number"] }}, Track:
    {{ playlistItem.track["track_number"] }})
  </h6>
  <p class="track card-album">
    Duration: {{ playlistItem.track["duration_ms"] }} ms
  </p>
  <p>
    Artist(s):
    <span
      class="track card-text"
      v-for="(artist, index) in playlistItem.track?.artists"
      :key="artist"
    >
      {{ index === 0 ? "" : ", " }}
      {{ artist.name }} ({{ artist.type }})
    </span>
  </p>
  <a
    v-if="playlistItem?.track?.external_urls?.spotify"
    :href="playlistItem.track.external_urls.spotify"
    ><button type="button" class="btn btn-secondary">View on Spotify</button>
  </a>
</template>

<script>
export default {
  name: "GridShowTrack",
  props: {
    playlistItem: Object,
  },
};
</script>
