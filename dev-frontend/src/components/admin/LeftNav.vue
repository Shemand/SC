<template>
  <ul id="admin-sidenav" class="sidenav">
    <li><div>
      <h1 class="center-align"><router-link to="/" class="grey-text text-darken-4 brand-logo">SC</router-link></h1>
    </div></li>
    <li><a class="admin-tab waves-effect" href="MainControl" v-on:click.prevent="changePage"><i class="material-icons">computer</i>Панель управления</a></li>
    <li><div class="divider"></div></li>
    <li><a class="subheader"><i class="material-icons">storage</i>Логи</a></li>
    <li><a class="admin-tab waves-effect" href="UpdateLogs" v-on:click.prevent="changePage">Обновления</a></li>
    <li><a class="admin-tab waves-effect" href="InternalLogs" v-on:click.prevent="changePage">Внутренние ошибки сервера</a></li>
    <li><div class="divider"></div></li>
    <li><a class="subheader"><i class="material-icons">poll</i>Статистика</a></li>
    <li><a class="admin-tab waves-effect" href="ComputersStatistics" v-on:click.prevent="changePage">Общая статистика</a></li>
    <li><a class="admin-tab waves-effect" href="KasperskyStatistics" v-on:click.prevent="changePage">Тут должна быть статистика</a></li>
  </ul>
</template>

<script>
export default {
  name: "LeftNav",
  components : {},
  data() {
    return {
      tabs: undefined,
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
    changePage(event) {
      this.$emit('change-page', event.target.attributes.href.value)
    }
  },
  mounted() {
    console.log(this.currentPage)
    // let tabs = document.getElementsByClassName('admin-tab')
    // tabs = Array.from(tabs)
    // this.tabs = tabs
    // tabs.forEach((tab) => {
    //   tab.addEventListener('click', (event) => {
    //     let target = event.target
    //     this.clearActive()
    //     target.classList.add('active')
    //     this.currentPage = target.attributes.href.value
    //   });
    // });
  }
}
</script>

<style scoped>
.sidenav {
  -webkit-transform: none;
  -moz-transform: none;
  -ms-transform: none;
  -o-transform: none;
}
.brand-logo {
  font-size: 2em;
}
</style>