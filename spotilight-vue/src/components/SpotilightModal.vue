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
        <div class="modal-body">
          <p>{{ body }}</p>
          <p v-if="link">{{ linkInfo }}</p>
          <a v-if="link" :href="link" target="_blank">{{ linkLabel }}</a>
        </div>
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
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <!-- TODO: Add @on-click -->
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="$emit('action', inputText), resetInputText()"
            :disabled="inputLabel && !inputText"
          >
            {{ actionLabel }}
          </button>
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

<!-- TODO: Add validation for the field having input -->
