<template>
  <div>
    <Navbar></Navbar>
    <ComputersTable></ComputersTable>
  </div>
  <!-- Modal Trigger -->

</template>

<script>
import Navbar from "@/components/Navbar";
import ComputersTable from "@/components/ComputersTable";
export default {
  name: 'Home',
  components: { Navbar, ComputersTable },
  async mounted() {
      var options = {
      }
      var elements = document.querySelectorAll('.modal');
      var instances = M.Modal.init(elements, options);
  }
}
</script>

<style lang="scss">
.main_table {
    width: 90%;
    margin: auto;
}
</style>