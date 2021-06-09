<template>
  <div>
      <ul id="slide-out" class="sidenav">
        <li><div class="sc-logo">
            <h1 class="center-align">SC</h1>
        </div></li>
        <li><a class="sidenav-close waves-effect" href="#!" data-target="slide-out">BACK</a></li>
        <li>
            <table class="list_of_table">
                <tr v-for="(line_key, line) of lines" :key="line_key" >
                    <td class="statistic-td">{{ lines[line].name }}</td><td class="statistic-td">{{lines[line].value}}</td>
                </tr>
            </table>
        </li>
      </ul>

      <div class="fixed-action-btn"><a href="#" data-target="slide-out" class="sidenav-trigger waves-effect waves-light btn btn-floating"><i class="large material-icons">blur_on</i></a></div>
  </div>
</template>

<script>
export default {
  name: "ComputersTableSideNav",
  props : {
    lines : Object
  },
}
</script>

<style lang="scss" scoped>
.statistic-td {
  padding: 0px 5px;
}
</style>