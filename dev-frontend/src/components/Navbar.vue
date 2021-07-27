<template>
  <nav class="self-over-background">
    <div class="nav-wrapper">
      <router-link to="/" class="general-text-color"><span class="brand-text">Secure Center</span></router-link>
      <ul id="nav-mobile" class="right hide-on-med-and-down">
        <router-link
            tag="li"
            to="/"
            exact
            active-class="active"
        ><a href="#">Главная</a></router-link>
<!--        <router-link-->
<!--            tag="li"-->
<!--            to="/devices"-->
<!--            active-class="active"-->
<!--        ><a href="#">Устройства</a></router-link>-->
        <router-link
            v-if="isAdmin"
            tag="li"
            to="/admin"
            active-class="active"
            class="general-text-color"
        ><a href="#">Панель администратора</a></router-link>
        <router-link
            tag="li"
            to="/logout"
            active-class="active"
            class="exit-button"
        ><a href="#">Выйти</a></router-link>
      </ul>
    </div>
  </nav>
</template>

<script>
import logo_img from '@/assets/sc_logo_2.svg'
export default {
 data() {
   return {
     'isAdmin' : true,
     'logo_img': logo_img
   }
 }
}
</script>

<style lang="scss" scoped>
@import "@/assets/variables";
  nav {
    padding: 0 2rem;
  }
  .brand-text {
    padding-left: 2em;
    text-shadow: #000 0px 8px 10px, #000 1px 1px 1px;
    font-family: Courier New;
    font-weight: bold;
    font-size: 2em;
  }
  .exit-button {
    background-color: $red-color;
    transition: background-color 0.5s ease;
    a {
      color: black;
    }
    &:hover {
      background-color: $yellow-color;
    }
  }
</style>