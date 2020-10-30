<template>
  <div>
    <Navbar v-if="loggined"></Navbar>
    <h1 class="blue-text text-darken-3 valign-wrapper"><b>Страница не найдена.</b></h1>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'
export default {
  name: "Not-found",
  components : { Navbar },
  data() {
    return {
      loggined: true
    }
  }
}
</script>

<style scoped>

</style>