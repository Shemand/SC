<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  components : {  },
  created: function() {
      this.$http.interceptors.response.use(undefined, function (err) {
          return new Promise(function (resolve, reject) {
              if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
                  this.$store.dispatch("logout")
              }
              throw err;
          })
      })
  }
}
</script>

<style lang="scss">
  @import "~materialize-css/dist/css/materialize.min.css";
  body {
    background-color: #eee;
  }
  /* fallback */
    @font-face {
      font-family: 'Material Icons';
      font-style: normal;
      font-weight: 400;
      src: url('./assets/flUhRq6tzZclQEJ-Vdg-IuiaDsNc.woff2') format('woff2');
    }

    .material-icons {
      font-family: 'Material Icons';
      font-weight: normal;
      font-style: normal;
      font-size: 24px;
      line-height: 1;
      letter-spacing: normal;
      text-transform: none;
      display: inline-block;
      white-space: nowrap;
      word-wrap: normal;
      direction: ltr;
      -moz-font-feature-settings: 'liga';
      -moz-osx-font-smoothing: grayscale;
    }

</style>
