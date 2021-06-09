<template>
  <div>
    <ComputersTableTabs :table="tabulator"></ComputersTableTabs>
    <div id="general_table" class="main_table" ref="computers_table"></div>
    <ComputerModal v-bind="selectedComputer" ref="computer_modal"></ComputerModal>
    <ComputersTableSideNav :lines="lines"></ComputersTableSideNav>
  </div>
</template>

<script>
import GetRequestsMixin from "@/mixins/GetRequestsMixin.js"
import ComputerModal from "@/components/ComputersTableModal"
import ComputersTableSideNav from "@/components/ComputersTableSideNav"
import ComputersTableTabs from "@/components/ComputersTableTabs"
import Tabulator from "tabulator-tables"

export default {
  components: {ComputerModal, ComputersTableSideNav, ComputersTableTabs},
  mixins: [GetRequestsMixin],
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
      lines: {
        all_computers: {
          name: "Всего компьютеров",
          value: 0
        },
        linux: {
          name: "Linux",
          value: 0
        },
      }
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
      paginationSize: 100,
      initialSort: [
        {column: "name", dir: "asc"},
      ],
      reactiveData: true,
      columns: [
        {title: "№", formatter: "rownum", width: 49, sorter: false, editor: false},
        {title: "Имя компьютера", field: "name", sorter: "string", headerFilter: true},
        {title: "AD статус", field: "ad_status"},
        {title: "KL статус", field: "kl_status"},
        {title: "DL статус", field: "dl_status"},
        {title: "PP статус", field: "pp_status"},
        {title: "ОС", field: "os"}
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
    this.$store.dispatch('updateComputers').then(function (status) {
      if (status === 200) {
        console.log('Data about computers was loaded write!')
        context.tableData = context.prepareData(context.$store.getters.computers)
        context.tabulator.setData(context.tableData)
      } else {
        console.log('computers gets request have status not equal 200. Check the network in development panel.')
      }
    });
  },
  methods: {
    prepareData(computers) {
      let context = this
      let tableArray = []
      computers.forEach(function (computer) {
        tableArray.push({
          id: computer.id,
          name: computer.name,
          ad_status: context.make_ad_status(computer),
          kl_status: context.make_kaspersky_status(computer),
          dl_status: context.make_dallas_status(computer),
          pp_status: context.make_puppet_status(computer),
          os: context.make_os_string(computer),
        })
      });
      return tableArray
    },
    make_kaspersky_status(computer) {
      let kl = computer.kaspersky
      const ALL_RIGHT = 'Отлично'
      const WRONG_AGENT = 'Неправильный агент'
      const WRONG_SECURITY = 'Неправильная защита'
      const WRONG_ALL = 'Все неправильно'
      const win_agent_versions = ["11.0.0.1131", "10.5.1781", "10.4.343", "10.2.434"]
      const lin_agent_versions = ["11.0.0.29", "10.5.0.42"]
      const lin_security_versions = ["10.1.1.6421", "10.1.0.6077", "10.1.0.6028"]
      const win_security_versions = ["11.1.1.126", "11.1.0.15919", "11.0.1.90", "11.0.0.6499", "10.3.3.275", "10.1.2.996", "10.3.0.6294", "11.2.0.2254", "10.2.6.3733", "11.3.0.773", "6.0.4.1611", "10.1.0.867", "10.2.1.23", "2.2.0.605", "10.2.5.3201", "11.4.0.233"]
      const right_agent_versions = ["11.0.0.29", "11.0.0.1131", "11.0.0.1131"]
      const right_security_versions = ["10.1.1.6421", "11.1.1.126", "10.1.2.996", "11.0.0.1131"]
      let kaspersky_status = 0
      if (kl.agent_version && right_agent_versions.includes(kl.agent_version))
        kaspersky_status = kaspersky_status | 1
      kaspersky_status = kaspersky_status << 1
      if (kl.security_version && right_security_versions.includes(kl.security_version))
        kaspersky_status = kaspersky_status | 1
      switch (kaspersky_status) {
        case 0b00:
          return WRONG_ALL
        case 0b01:
          return WRONG_SECURITY
        case 0b10:
          return WRONG_AGENT
        case 0b11:
          return ALL_RIGHT
      }
    },
    make_ad_status(computer) {
      let ad = computer.active_directory
      if (ad.registred)
        return String(ad.registred)
      else
        return "Незарегистрирован"
    },
    make_dallas_status(computer) {
      let dallas = computer.dallas_lock
      if (dallas.status)
        return dallas.status
      else
        return "Незарегистрирован"
    },
    make_puppet_status(computer) {
      let puppet = computer.puppet
      if (puppet.puppet_ip)
        return puppet.puppet_ip
      else
        return "Незарегистрирован"
    },
    make_os_string(computer) {
      let puppet = computer.puppet
      let kaspersky = computer.kaspersky
      if (puppet.puppet_os)
        return puppet.puppet_os
      if (kaspersky.kl_os) {
        return kaspersky.kl_os
      }
      return 'Неизвестно'
    }
  }
}
</script>

<style lang="scss">
@import "~tabulator-tables/dist/css/bootstrap/tabulator_bootstrap";
</style>
