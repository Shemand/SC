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
</style>
