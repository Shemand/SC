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
  @import "assets/materializeCustom";
  @import "~materialize-css/sass/materialize";
  @import "assets/general";
  @import "assets/tables";

  $primary-color: $general-color;
  $primary-color-light: $highlight-general-color;
  $primary-color-dark: false;
  $secondary-color: $general-color;
  $success-color: $green-color;
  $error-color: $red-color;

  $link-color: $highlight-general-color;


  body {
    @extend .self-background;
  }
</style>
