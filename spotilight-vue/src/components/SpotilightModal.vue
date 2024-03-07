<template>
  {{ console.log("Modal to appear") }}
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
        <div class="modal-body">{{ body }}</div>
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
            @click="$emit('action')"
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
  },
};
</script>
