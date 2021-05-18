<template>
  <div>
    <Navbar></Navbar>
    <h1>Main</h1>
    <div class="main_table"><ComputersTable></ComputersTable></div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import ComputersTable from "@/components/ComputersTable";
export default {
  name: 'Home',
  components: { Navbar, ComputersTable },
  async mounted() {

  }
}
</script>

<style lang="scss">
.main_table {
    width: 90%;
    margin: auto;
}
</style>