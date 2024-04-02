import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import "./main.scss";

const globalContext = {
  data() {
    return {
      displayName: null,
    };
  },
};
const app = createApp(App).use(router);
app.mixin(globalContext);
app.mount("#app");
