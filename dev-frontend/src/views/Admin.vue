<template>
  <div class="row">
    <LeftNav :currentPage="currentPage" v-on:change-page="changePage" class="col s2"></LeftNav>
    <keep-alive>
      <component :is="currentPage" class="col s10 offset-s2"></component>
    </keep-alive>
  </div>
</template>

<script>
import MainControl from "@/components/admin/MainControl";
import LeftNav from "@/components/admin/LeftNav";
import ComputersStatistics from "@/components/admin/ComputersStatistics";
import UpdateLogs from "@/components/admin/UpdateLogs";
import InternalLogs from "@/components/admin/InternalLogs";
import KasperskyStatistics from "@/components/admin/KasperskyStatistics";
import UsersControl from "@/components/admin/UsersControl";

export default {
  components: {LeftNav, MainControl, ComputersStatistics, UpdateLogs, InternalLogs, KasperskyStatistics, UsersControl},
  data() {
    return {
      currentPage: 'MainControl',
    }
  },
  methods: {
    changePage(pageName) {
      this.currentPage = pageName
    },
  },
  mounted() {

  }
}
</script>

<style lang="scss" scoped>
.sidenav {
  -webkit-transform: none;
  -moz-transform: none;
  -ms-transform: none;
  -o-transform: none;
}
</style>