<template>
  <div class="spotlight">
    <TopTracks />
  </div>
</template>

<script>
import TopTracks from "@/components/TopTracks.vue";

export default {
  name: "SpotlightView",
  components: {
    TopTracks,
  },
};
</script>
