<template>
  <nav class="blue darken-3">
    <div class="nav-wrapper">
      <router-link to="/" class="brand-logo">Secure Center</router-link>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <router-link
            tag="li"
            to="/"
            exact
            active-class="active"
        ><a href="#">Главная</a></router-link>
        <router-link
            tag="li"
            to="/devices"
            active-class="active"
        ><a href="#">Устройства</a></router-link>
        <router-link
            v-if="isAdmin"
            tag="li"
            to="/admin"
            active-class="active"
        ><a href="#">Панель администратора</a></router-link>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
 data() {
   return {
     'isAdmin' : true
   }
 }
}
</script>

<style lang="scss" scoped>
  nav {
    padding: 0 2rem;
  }
</style>