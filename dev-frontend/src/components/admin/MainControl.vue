<template>
  <div>
    <div class="main_block">
      <span class="header-block">Управление системой</span>
      <table>
        <tr>
          <th colspan="4">Обновить статистику по: </th>
        </tr>
        <tr>
          <td><a class="waves-effect waves-light btn grey-button text-on-white" v-on:click="updatePuppet">Puppet</a></td>
          <td><a class="waves-effect waves-light btn yellow-button text-on-white" v-on:click="updateDallasLock">Dallas Lock</a></td>
          <td><a class="waves-effect waves-light btn green-button text-on-white" v-on:click="updateActiveDirectoryComputers">AD Компьютеры</a></td>
          <td><a class="waves-effect waves-light btn red-button text-on-white" v-on:click="updateKaspersky">Касперский</a></td>
        </tr>
        <tr>
          <td colspan="4"><a class="waves-effect waves-light white-button btn text-on-white" v-on:click="updateAllComputers">Обновить все компьютеры</a></td>
        </tr>
        <tr>
          <td colspan="2"><a class="waves-effect waves-light btn grey-button text-on-white" v-on:click="updateStructure">Структуру</a></td>
          <td colspan="2"><a class="waves-effect waves-light btn green-button text-on-white" v-on:click="updateActiveDirectoryUsers">AD пользователи</a></td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainControl",
  methods: {
    updateAllComputers(){
      this.$http({
        url: "/api/v1/SZO/update/computers",
        method: 'POST',
        withCredentials: true
      }).then((res) => {
        console.log(res);
      });
    },
    updateKaspersky() {
      this.$http({
        url: "/api/v1/SZO/update/kaspersky",
        method: 'POST',
        withCredentials: true
      }).then((res) => {
        console.log(res);
      });
    },
    updateActiveDirectoryComputers() {
      this.$http({
        url: "/api/v1/SZO/update/ad/computers",
        method: 'POST',
        withCredentials: true
      }).then((res) => {
        console.log(res);
      });
    },
    updateActiveDirectoryUsers() {
      this.$http({
        url: "/api/v1/SZO/update/ad/users",
        method: 'POST',
        withCredentials: true
      }).then((res) => {
        console.log(res);
      });
    },
    updateStructure() {
      this.$http({
        url: "/api/v1/SZO/update/reset/structure",
        method: 'POST',
        withCredentials: true
      }).then((res) => {
        console.log(res);
      });
    },
    updatePuppet() {
      this.$http({
        url: "/api/v1/SZO/update/puppet",
        method: 'POST',
        withCredentials: true
      }).then((res) => {
        console.log(res);
      });
    },
    updateDallasLock() {
      this.$http({
        url: "/api/v1/SZO/update/dallas",
        method: 'POST',
        withCredentials: true
      }).then((res) => {
        console.log(res);
      });
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/variables";
.main_block {
  padding: 10px;
}
.btn {
  width: 100%;
}
tr {
  border-bottom: none;
}
td, th {
  padding: 5px 10px;
}
table, td, th {
  border: none;
}
tr {
  border-left: 1px solid $general-color;
}
td {
  color: $text-on-black-color;
}
.header-block{
  font-weight: bold;
  font-size: 2em;
  text-shadow: 1px 10px 10px black;
  color: $general-color;
}
th {
  color: $text-on-black-color;
}
</style>