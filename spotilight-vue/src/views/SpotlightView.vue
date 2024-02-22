<template>
  <div class="spotlight">
    <TopTracks />
    <TopArtists />
  </div>
</template>

<script>
import TopTracks from "@/components/TopTracks.vue";
import TopArtists from "../components/TopArtists.vue";

export default {
  name: "SpotlightView",
  components: {
    TopTracks,
    TopArtists,
  },
};
</script>
