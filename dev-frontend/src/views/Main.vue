<template>
  <div>
    <Navbar></Navbar>
    <h1>Main</h1>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
export default {
  name: 'Home',
  components: { Navbar },
  async mounted() {
    axios({
      url : '/api/get_computers'
    })
  }
}
</script>
