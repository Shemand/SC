<template>
  <div>
    <Navbar></Navbar>
    <br>
    <ComputersTable></ComputersTable>
  </div>
  <!-- Modal Trigger -->

</template>

<script>
import Navbar from "@/components/Navbar";
import ComputersTable from "@/components/ComputersTable";

export default {
  name: 'Home',
  components: {Navbar, ComputersTable},
  async mounted() {
    var options = {}
    var elements = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elements, options);
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, options);
    options = {
      edge: 'right'
    }
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, options);
  }
}
</script>

<style lang="scss">
.main_table {
  width: 90%;
  margin: auto;
}
</style>