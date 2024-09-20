<template>
  <div class="align-content-center-v-and-h margin-top-bottom">
    <button
      v-if="addTrackToPlaylistStatus === 'ready'"
      class="btn btn-primary m-2"
      @click="handleSelectAddTrackToPlaylistStatus"
    >
      + Add Track(s)
    </button>
    <div v-else-if="addTrackToPlaylistStatus === 'started'">
      <button
        class="btn btn-secondary m-2"
        @click="handleCloseAddTrackToPlaylistStatus"
      >
        Cancel
      </button>
      <button
        class="btn btn-primary m-2"
        @click="handleSingleTrackToPlaylistStatus"
      >
        Add Individual Track(s)
      </button>
      <button
        class="btn btn-primary m-2"
        @click="handleArtistTracksToPlaylistStatus"
      >
        Add Artist Top Track(s)
      </button>
    </div>
    <!-- addTrackToPlaylistStatus is either 'track' or 'artist'-->
    <div v-else class="col-4 search-track">
      <div
        v-for="selection in selectedMatches"
        class="row search-match"
        :key="selection.id + '_search-match'"
      >
        <p class="col-10">
          {{ selection.name }}
        </p>
        <p class="col-2" @click="updateSelectedMatches(selection)">X</p>
      </div>
      <div class="row">
        <div :class="addTrackToPlaylistStatus !== 'track' ? 'col-9' : 'col-12'">
          <input
            type="text"
            :placeholder="
              addTrackToPlaylistStatus === 'track'
                ? 'Search for track(s)'
                : 'Search for artists(s)'
            "
            :value="searchQuery"
            @input="
              (event) => (
                (searchQuery = event.target.value),
                handleTrackQuerySearch(addTrackToPlaylistStatus)
              )
            "
            style="width: 100%"
          />
        </div>
        <div
          v-if="addTrackToPlaylistStatus !== 'track'"
          class="search-match col-3 counter"
        >
          <div class="row">
            <button
              class="col-4 sm-rounded-button"
              @click="decrementArtistTopTracksCount"
            >
              -
            </button>
            <div class="col-4 align-content-center-v-and-h">
              {{ artistTopTracksCount }}
            </div>
            <button
              class="col-4 sm-rounded-button"
              @click="incrementArtistTopTracksCount"
            >
              +
            </button>
          </div>
        </div>
      </div>
      <div v-if="searchQuery !== '' && !isMaxSelectedMatches()">
        <div v-for="match in searchMatches" :key="match.id + '_search-match'">
          <div
            class="row search-match p-1"
            @click="updateSelectedMatches(match)"
            :style="isItemSelected(match) && 'background-color: orange'"
          >
            {{ console.log(match) }}
            <div class="col-3 search-match icon">
              <template v-if="addTrackToPlaylistStatus === 'track'">
                <img :src="match?.album?.images?.[0]?.url" height="50rem" />
              </template>
              <template v-else>
                <img
                  :src="match?.images?.[0]?.url"
                  class="rounded-circle"
                  height="50rem"
                />
              </template>
            </div>
            <div class="col-9 search-match name text-align-left">
              <p>
                {{ match.name }}
                <i>
                  {{
                    addTrackToPlaylistStatus !== "track"
                      ? ""
                      : "(" + match?.artists?.[0]?.name + ")"
                  }}
                </i>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="isMaxSelectedMatches()">
        {{ console.log(MAX_SELECTED_MATCHES) }}
        {{ console.log(selectedMatches) }}
        <p>
          At maximum ({{ MAX_SELECTED_MATCHES }}) selected
          {{ addTrackToPlaylistStatus }}s
        </p>
      </div>
      <div>
        <button
          class="btn btn-secondary m-2"
          @click="handleCloseAddTrackToPlaylistStatus"
        >
          Cancel
        </button>
        <button
          class="btn btn-primary m-2"
          :disabled="this.selectedMatches.length < 1"
          @click="handleAddTracksToPlaylist"
        >
          {{ determineSubmitButtonText() }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const ARTIST_TOP_TRACKS_COUNT_MAX = 10;
const ARTIST_TOP_TRACKS_COUNT_MIN = 1;

export default {
  name: "SearchToAddTracks",
  props: {
    playlistID: String,
  },
  data() {
    return {
      addTrackToPlaylistStatus: "ready",
      searchQuery: "",
      searchMatches: [],
      selectedMatches: [],
      artistTopTracksCount: 5,
      MAX_SELECTED_MATCHES: 10,
      // TODO: This is just temporary for testing
      testSearchArray: [
        {
          name: "Test Track 1",
          id: "T1",
        },
        {
          name: "Test Track 2",
          id: "T2",
        },
        {
          name: "Test Track 3",
          id: "T3",
        },
      ],
    };
  },
  methods: {
    handleSelectAddTrackToPlaylistStatus() {
      this.addTrackToPlaylistStatus = "started";
    },
    handleSingleTrackToPlaylistStatus() {
      this.addTrackToPlaylistStatus = "track";
    },
    handleArtistTracksToPlaylistStatus() {
      this.addTrackToPlaylistStatus = "artist";
    },
    handleCloseAddTrackToPlaylistStatus() {
      this.addTrackToPlaylistStatus = "ready";
      this.searchQuery = "";
      this.selectedMatches = [];
      this.artistTopTracksCount = 5;
    },
    decrementArtistTopTracksCount() {
      if (this.artistTopTracksCount > ARTIST_TOP_TRACKS_COUNT_MIN) {
        this.artistTopTracksCount -= 1;
      }
    },
    incrementArtistTopTracksCount() {
      if (this.artistTopTracksCount < ARTIST_TOP_TRACKS_COUNT_MAX) {
        this.artistTopTracksCount += 1;
      }
    },
    isItemSelected(match) {
      const curSelectedMatches = this.selectedMatches;

      for (let i = 0; i < curSelectedMatches.length; i++) {
        if (curSelectedMatches[i].id === match.id) {
          return true;
        }
      }
      return false;
    },
    isMaxSelectedMatches() {
      return this.selectedMatches.length >= this.MAX_SELECTED_MATCHES;
    },
    determineSubmitButtonText() {
      let submitButtonText = "Add";
      if (this.addTrackToPlaylistStatus === "track") {
        const pluralString = this.selectedMatches.length > 1 ? "s" : "";
        submitButtonText = submitButtonText + " Track" + pluralString;
      } else {
        const pluralString =
          this.artistTopTracksCount !== 1 || this.selectedMatches.length > 1
            ? "s"
            : "";
        submitButtonText =
          submitButtonText +
          " Top " +
          (this.artistTopTracksCount <= 1 ? "" : this.artistTopTracksCount) +
          " Artist Track" +
          pluralString;
      }
      return submitButtonText;
    },
    tempHandleTrackQuerySearch() {
      let tempSearchMatches = [];

      for (let i = 0; i < this.testSearchArray.length; i++) {
        if (
          this.searchQuery !== "" &&
          this.testSearchArray[i].name.includes(this.searchQuery)
        ) {
          tempSearchMatches = [...tempSearchMatches, this.testSearchArray[i]];
        }
      }

      this.searchMatches = tempSearchMatches;
    },
    updateSearchMatches(searchType, searchData) {
      if (searchType === "track") {
        this.searchMatches = searchData.tracks.items;
      } else if (searchType === "artist") {
        this.searchMatches = searchData.artists.items;
      }
    },
    handleTrackQuerySearch(searchType) {
      // Empty query string check
      if (this.searchQuery === "") {
        this.searchMatches = [];
        return;
      }
      // Replaces special characters with UTF-8 encoding to ensure string is safe
      const encodedSearchQuery = encodeURIComponent(this.searchQuery);

      const path = "/search/" + searchType + "/" + encodedSearchQuery + "/" + 5;
      axios
        .get(path)
        .then((res) => {
          this.updateSearchMatches(searchType, res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    updateSelectedMatches(selectedMatch) {
      // Add a selected match
      if (!this.selectedMatches.includes(selectedMatch)) {
        this.selectedMatches = [...this.selectedMatches, selectedMatch];
      }
      // Remove a selected match
      else {
        let tempSelectedMatches = [];
        const curSelectedMatches = this.selectedMatches;

        for (let i = 0; i < curSelectedMatches.length; i++) {
          if (curSelectedMatches[i] !== selectedMatch) {
            tempSelectedMatches = [
              ...tempSelectedMatches,
              curSelectedMatches[i],
            ];
          }
        }

        this.selectedMatches = tempSelectedMatches;
      }
    },
    handleAddSingleTracksToPlaylist() {
      const uriList = this.selectedMatches.map((track) => track.uri);
      console.log(uriList);

      const post_playlist_path = `/playlist/add-tracks/` + this.playlistID;
      axios({
        method: "post",
        url: post_playlist_path,
        data: {
          items: uriList,
        },
      })
        .then((res) => {
          console.log(res.data);
          this.$emit("added");
        })
        .catch((err) => {
          console.error(err);
        });
    },
    handleAddArtistTracksToPlaylist() {
      let trackList = [];
      const selectedArtistCount = this.selectedMatches.length;
      const topTracksCount = this.artistTopTracksCount;

      this.selectedMatches.forEach((artist) => {
        const artist_top_track_endpoint = `/showcase/${artist.id}/top-tracks`;

        axios
          .get(artist_top_track_endpoint)
          .then((res) => {
            trackList = [...trackList, res.data.tracks];
            // Handle fully populated track list
            console.log(trackList.length);

            // Ensure all artist top track lists have been added to full list
            if (trackList.length === selectedArtistCount) {
              console.log(trackList);
              let uriList = [];
              trackList.forEach((artistTopTrackList) => {
                artistTopTrackList
                  .slice(0, topTracksCount)
                  .map((track) => (uriList = [...uriList, track.uri]));
              });
              console.log(uriList);

              const post_playlist_path =
                "/playlist/add-tracks/" + this.playlistID;
              axios({
                method: "post",
                url: post_playlist_path,
                data: {
                  items: uriList,
                },
              })
                .then((res) => {
                  console.log(res.data);
                  this.$emit("added");
                })
                .catch((err) => {
                  console.error(err);
                });
            }
          })
          .catch((err) => {
            console.error(err);
          });
      });
    },
    handleAddTracksToPlaylist() {
      if (this.addTrackToPlaylistStatus === "track") {
        this.handleAddSingleTracksToPlaylist();
      } else {
        this.handleAddArtistTracksToPlaylist();
      }
      this.handleCloseAddTrackToPlaylistStatus();
    },
  },
};
</script>
