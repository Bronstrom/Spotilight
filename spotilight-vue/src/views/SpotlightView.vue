<template>
  <div class="spotlight" style="max-height: 100vh; overflow: hidden">
    <div class="row">
      <div class="col col-lg-8">
        <div class="row">
          <TopTracks style="background-color: gray" />
        </div>
        <div class="row">
          <TopArtists style="background-color: white" />
        </div>
      </div>
      <div class="col col-lg-4">
        <TopGenres style="background-color: gray" />
      </div>
    </div>
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
