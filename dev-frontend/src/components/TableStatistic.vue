<template>
  <div class="statistic-block">
    <ul class="list_of_table">
      <li v-for="(line_key, line) of lines" :key="line_key">{{ lines[line].name }}: {{lines[line].value}}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "TableStatistic",
  props : {
    lines : Object
  },
}
</script>

<style scoped>
.statistic-block {
  position: fixed;
  padding: 20px;
  background-color: #999999;
  z-index: 1000;
}

.list_of_table {
  list-style-type: none;
}
</style>