<template>
  <div class="showcase main-content-gutter margin-top-bottom">
    <h1 class="text-align-center">Showcase</h1>
    <div class="row">
      <div class="col col-lg-8">
        <div class="row p-3">
          <TopTracks />
        </div>
        <div class="row p-3">
          <TopArtists />
        </div>
      </div>
      <div class="col col-lg-4 p-3">
        <TopGenres />
      </div>
    </div>
  </div>
</template>

<script>
import TopTracks from "@/components/TopTracks.vue";
import TopArtists from "../components/TopArtists.vue";
import TopGenres from "../components/TopGenres.vue";

export default {
  name: "ShowcaseView",
  components: {
    TopTracks,
    TopArtists,
    TopGenres,
  },
};
</script>
