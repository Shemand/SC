<template>
  <div>
    <ComputersTableTabs :table="tabulator"></ComputersTableTabs>
    <div id="general_table" class="main_table" ref="computers_table"></div>
    <ComputerModal v-bind="selectedComputer" ref="computer_modal"></ComputerModal>
    <ComputersTableSideNav :updates_count="updates_count" :table="tabulator"></ComputersTableSideNav>
  </div>
</template>

<script>
import ComputerModal from "@/components/computers/ComputersTableModal"
import ComputersTableSideNav from "@/components/computers/ComputersTableSideNav"
import ComputersTableTabs from "@/components/computers/ComputersTableTabs"
import Tabulator from "tabulator-tables"

export default {
  components: {ComputerModal, ComputersTableSideNav, ComputersTableTabs},
  data() {
    return {
      tableData: [],
      tableRef: null,
      tabulator: undefined,
      selectedComputer: {
        puppet: {},
        kaspersky: {},
        active_directory: {},
        dallas_lock: {},
      },
      updates_count: 0
    }
  },
  mounted() {
    let context = this
    this.tabulator = new Tabulator(this.$refs.computers_table, {
      data: this.tableData,
      layout: "fitColumns",
      tooltips: true,
      pagination: "local",
      index: "name",
      paginationSize: 25,
      dataFiltered: function () {
        context.updates_count++;
      },
      initialSort: [
        {column: "name", dir: "asc"},
      ],
      rowFormatter(row) {
        let kl_cell = row.getCell('kl_status')
        let dl_cell = row.getCell('dl_status')
        let pp_cell = row.getCell('pp_status')
        let ad_cell = row.getCell('ad_status')
        let os_cell = row.getCell('os_status')

        // ad status formatting
        if (ad_cell.getValue() === 'Не зарегистрирован')
          ad_cell._cell.element.classList.add('wrong_cell')
        else
          ad_cell._cell.element.classList.add('right_cell')

        // kl status formatting
        if (kl_cell.getValue() === 'Все неправильно')
          kl_cell._cell.element.classList.add('wrong_cell')
        else if (kl_cell.getValue() === 'Неправильный агент')
          kl_cell._cell.element.classList.add('warning_cell')
        else if (kl_cell.getValue() === 'Неправильный защита')
          kl_cell._cell.element.classList.add('warning_cell')
        else
          kl_cell._cell.element.classList.add('right_cell')

        // dl status formatting
        if (dl_cell.getValue() === 'Не зарегистрирован' && os_cell.getValue() !== 'Linux')
          dl_cell._cell.element.classList.add('wrong_cell')
        else
          dl_cell._cell.element.classList.add('right_cell')

        // pp status formatting
        if (pp_cell.getValue() === 'Не зарегистрирован' && os_cell.getValue() !== 'Windows')
          pp_cell._cell.element.classList.add('wrong_cell')
        else
          pp_cell._cell.element.classList.add('right_cell')

        // os status formatting
        if (os_cell.getValue() === 'Неизвестно')
          os_cell._cell.element.classList.add('wrong_cell')
        else
          os_cell._cell.element.classList.add('right_cell')
      },
      reactiveData: true,
      columns: [
        {title: "№", formatter: "rownum", width: 49, sorter: false, editor: false},
        {title: "Имя компьютера", field: "name", sorter: "string", headerFilter: true},
        {
          title: "AD статус",
          field: "ad_status",
          align: "center",
          sorter: "string",
          formatter: "datetime",
          formatterParams: {
            outputFormat: "DD/MM/YY HH:mm",
            timezone: "Europe/Moscow",
            invalidPlaceholder: "Не зарегистрирован",
          }
        },
        {
          title: "KL статус",
          field: "kl_status",
          align: "center",
          sorter: "string",
        },
        {
          title: "DL статус",
          field: "dl_status",
          align: "center",
          sorter: "string",
        },
        {
          title: "PP статус",
          field: "pp_status",
          align: "center",
          sorter: "string",
        },
        {title: "ОС", field: "os_status", align: "center", sorter: "string", formatter: context.formatter_os_status}
      ],
      rowClick: function (e, row) {
        let el = context.$refs.computer_modal.$el
        let instance = M.Modal.getInstance(el)
        let computer_id = row.getData().id
        context.selectedComputer = context.$store.getters.computer(computer_id)
        instance.open()
      }
    })
    this.tableData = []
    this.$store.dispatch('updateComputers').then((status) => {
      if (status === 200) {
        console.log('Data about computers was loaded write!')
        // this.tableData = this.prepareData(this.$store.getters.computers)
        this.tableData = this.$store.getters.computers
        this.tabulator.setData(this.tableData)
      } else {
        console.log('computers gets request have status not equal 200. Check the network in development panel.')
      }
    });
    // this.update_statistics_board()
  },
  beforeDestroy()
  {
    this.tabulator.destroy()
    this.tableData.length = 0
  }
}
</script>

<style lang="scss">
</style>
