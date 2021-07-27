<template>
  <ul id="admin-sidenav" class="sidenav self-over-background text-on-black">
    <li><div>
      <h1 class="center-align"><router-link to="/" class="brand-logo general-text-color"><img :src="logo_img" alt="SC" class="general-text-color"></router-link></h1>
    </div></li>
    <li><a class="admin-tab waves-effect active" href="MainControl" v-on:click.prevent="changePage"><i class="material-icons text-on-black">computer</i>Панель управления</a></li>
    <li><a class="admin-tab waves-effect" href="UsersControl" v-on:click.prevent="changePage"><i class="material-icons text-on-black">person</i>Пользователи</a></li>
    <li><div class="divider general-color"></div></li>
    <li><a class="subheader text-on-black"><i class="material-icons text-on-black">storage</i>Логи</a></li>
    <li><a class="admin-tab waves-effect" href="UpdateLogs" v-on:click.prevent="changePage">Обновления</a></li>
    <li><a class="admin-tab waves-effect" href="InternalLogs" v-on:click.prevent="changePage">Внутренние ошибки сервера</a></li>
    <li><div class="divider general-color"></div></li>
    <li><a class="subheader text-on-black"><i class="material-icons text-on-black">poll</i>Статистика</a></li>
    <li><a class="admin-tab waves-effect" href="ComputersStatistics" v-on:click.prevent="changePage">Общая статистика</a></li>
    <li><a class="admin-tab waves-effect" href="KasperskyStatistics" v-on:click.prevent="changePage">Тут должна быть статистика</a></li>
  </ul>
</template>

<script>
import logo_img from "@/assets/sc_logo_2.svg";
export default {
  name: "LeftNav",
  components : {},
  data() {
    return {
      tabs: undefined,
      logo_img,
    }
  },
  props : ['currentPage'],
  methods : {
    clearActive() {
      this.tabs.forEach((tab) => {
        if (Array.from(tab.classList).includes('active')){
          tab.classList.remove('active')
        }
      });
    },
    changeActiveTab(tabElement) {
      this.clearActive()
      tabElement.classList.add('active')
    },
    changePage(event) {
      this.changeActiveTab(event.target)
      this.$emit('change-page', event.target.attributes.href.value)
    }
  },
  mounted() {
    let tabs = document.getElementsByClassName('admin-tab')
    this.tabs = Array.from(tabs)
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/general";
.sidenav {
  -webkit-transform: none;
  -moz-transform: none;
  -ms-transform: none;
  -o-transform: none;
}
.active{
  @extend .general-text-color;
  font-weight: bold;
}
.admin-tab {
  @extend .text-on-black;
}
.admin-tab:hover {
  @extend .general-text-color;
}
img {
  width: 15rem;
}
</style>