<template>
  <div>
    <br>
    <div ref="users_table"></div>
    <br>
  </div>
</template>

<script>
import moment from 'moment'
import Tabulator from "tabulator-tables";
export default {
  name: "UsersControl",
  data() {
    return {
      users: [],
      tabulator: undefined,
    }
  },
  mounted(){
    this.$http({
      url: "/api/v1/SZO/users/ad",
      method: "GET",
      withCredentials: true
    }).then((res) => {
      if (res.status === 200) {
        let context = this
        this.users = res.data.data.users;
        this.users.forEach((user) => {
          user.registred = this.showDate(user.registred)
          user.last_logon = this.showDate(user.last_logon)
        });
        this.tabulator = new Tabulator(this.$refs.users_table, {
          data: context.users,
          layout: "fitColumns",
          tooltips: true,
          pagination: "local",
          index: "name",
          paginationSize: 25,
          initialSort: [
            {column: "name", dir: "asc"},
          ],
          rowContextMenu: [
            {
              label: "Hide Column",
              action: function (e, column) {
                column.hide();
              }
            },
            {
              separator: true,
            },
            {
              disabled: true,
              label: "Move Column",
              action: function (e, column) {
                column.move("col");
              }
            }
          ],
          columns: [
            {title: "№", formatter: "rownum", width: 49, sorter: false, editor: false},
            {title: "Полное имя", field: "full_name", sorter: "string", headerFilter: true},
            {
              title: "Логин",
              field: "name",
              align: "center",
              sorter: "string",
            },
            {
              title: "Подразделение",
              field: "department",
              align: "center",
              sorter: "string",
            },
            {
              title: "Почта",
              field: "mail",
              align: "center",
              sorter: "string",
            },
            {
              title: "Телефон",
              field: "phone",
              align: "center",
              sorter: "string",
            },
            {
              title: "Создан",
              field: "registred",
              align: "center",
              formatter: "datetime",
              formatterParams: {
                outputFormat: "DD/MM/YY HH:mm",
                timezone: "Europe/Moscow",
                invalidPlaceholder: "-",
              }
            },
            {
              title: "Последний вход",
              field: "last_logon",
              align: "center",
              formatter: "datetime",
              formatterParams: {
                outputFormat: "DD/MM/YY HH:mm",
                timezone: "Europe/Moscow",
                invalidPlaceholder: "-",
              }
            },
          ],
        });
      }
    });
  },
  beforeDestroy()
  {
    this.tabulator.destroy()
    this.users.length = 0
  },
  methods:{
    showDate(timeInMilliseconds) {
      return moment(timeInMilliseconds).format("DD/MM/YY HH:mm")
    }
  }
}
</script>

<style scoped>

</style>