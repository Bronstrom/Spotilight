const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  // Development proxy is required in Vue in order to communicate properly with Flask
  devServer: {
    proxy: process.env.BACK_END_URL,
  },
});
