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
  @import "~materialize-css/sass/materialize";
  @import "assets/general";
  @import "assets/tables";

  body {
    @extend .self-background;
  }
</style>
