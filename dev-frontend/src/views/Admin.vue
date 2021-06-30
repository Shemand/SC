<template>
  <div>
    <LeftNav :currentPage="currentPage" v-on:change-page="changePage" class="container"></LeftNav>
    <keep-alive>
      <component :is="currentPage" class="container"></component>
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

export default {
  components: {LeftNav, MainControl, ComputersStatistics, UpdateLogs, InternalLogs, KasperskyStatistics},
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