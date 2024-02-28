<template>
  <div class="spotlight">
    <TopTracks />
    <TopArtists />
    <TopGenres />
  </div>
</template>

<script>
import TopTracks from "@/components/TopTracks.vue";
import TopArtists from "../components/TopArtists.vue";
import TopGenres from "../components/TopGenres.vue";

export default {
  name: "SpotlightView",
  components: {
    TopTracks,
    TopArtists,
    TopGenres,
  },
};
</script>
