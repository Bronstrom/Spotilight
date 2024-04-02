import { reactive } from "vue";

export const user = reactive({
  displayName: null,
  handleNewDisplayName(name) {
    this.displayName = name;
  },
});
