<template>
    <div class="modal" ref="computer_modal">
        <div class="computers-info" v-bind:computer></div>
        <div class="computers-footer">
            <a href="#!" class="modal-close waves-effect waves-red btn-flat">Закрыть</a>
        </div>
    </div>
</template>

<script>
export default {
 props : {
    computer: Object
 }
 data() {
   return {
     'isAdmin' : false
   }
 }
}
</script>

<style lang="scss" scoped>
  nav {
    padding: 0 2rem;
  }
</style>