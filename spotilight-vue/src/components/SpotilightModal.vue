<template>
  <div
    class="modal fade"
    :id="id"
    tabindex="-1"
    role="dialog"
    aria-labelledby="spotlightModalCenter"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="spotlightModalTitle">{{ title }}</h5>
          <button
            type="button"
            class="close"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div v-if="actionCompletionFlow === 'started'">
          <div class="spinner-border text-primary" role="status"></div>
          <div class="modal-body">
            <p>Processing . . .</p>
            <p>Please wait as the item is created.</p>
          </div>
        </div>
        <div v-else-if="actionCompletionFlow === 'finished'">
          <div class="modal-body">
            <p>Playlist Finished Creating</p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
        <div v-else>
          <div class="modal-body">
            <p>{{ body }}</p>
            <p v-if="link">{{ linkInfo }}</p>
            <a v-if="link" :href="link" target="_blank">{{ linkLabel }}</a>

            <div v-if="inputLabel" class="px-5 pb-3 input-group">
              <label class="sr-only" for="modal-input">{{ inputLabel }}</label>
              <div class="input-group">
                <div class="input-group-prepend">
                  <div class="input-group-text">Name</div>
                </div>
                <input
                  type="text"
                  class="form-control"
                  id="modal-input"
                  :placeholder="inputPlaceholder"
                  :value="inputText"
                  @input="(event) => (inputText = event.target.value)"
                />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              v-if="!actionCompletionFlow"
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="$emit('action', inputText), resetInputText()"
              :disabled="inputLabel && !inputText"
            >
              {{ actionLabel }}
            </button>
            <button
              v-else
              type="button"
              class="btn btn-primary"
              @click="$emit('action', inputText), resetInputText()"
              :disabled="inputLabel && !inputText"
            >
              {{ actionLabel }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SpotilightModal",
  emits: ["action"],
  props: {
    actionCompletionFlow: String,
    id: String,
    title: String,
    body: String,
    actionLabel: String,
    link: String,
    linkInfo: String,
    linkLabel: String,
    inputLabel: String,
    inputPlaceholder: String,
  },
  data() {
    return {
      inputText: "",
    };
  },
  methods: {
    resetInputText() {
      this.inputText = "";
    },
  },
};
</script>

<style>
.modal-backdrop.fade.show {
  z-index: inherit;
}
.modal-header,
.modal-body,
.modal-footer {
  background-color: #777777;
}
.modal-content {
  margin: 2px auto;
  z-index: 2;
}
</style>
