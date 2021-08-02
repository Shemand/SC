<template>
  <div>
    <ComputersTableTabs :table="tabulator" v-on:tabChanged="changeTab"  v-on:openCloseFilters="openCloseFilters"></ComputersTableTabs>
    <ComputersTableFilters v-show="isFiltersShowed" v-on:openCloseFilters="openCloseFilters" v-on:applyFilters="applyFilters"></ComputersTableFilters>
    <div id="general_table" class="main_table" ref="computers_table"></div>
    <ComputerModal v-bind="selectedComputer" ref="computer_modal"></ComputerModal>
    <ComputersTableSideNav :updates_count="updates_count" :table="tabulator"></ComputersTableSideNav>
  </div>
</template>

<script>
import ComputerModal from "@/components/computers/ComputersTableModal"
import ComputersTableSideNav from "@/components/computers/ComputersTableSideNav"
import ComputersTableTabs from "@/components/computers/ComputersTableTabs"
import ComputersTableFilters from "./ComputersTableFilters";
import create_computer_table from "@/components/computers/computer_table_creator.js";
export default {
  components: {ComputerModal, ComputersTableSideNav, ComputersTableTabs, ComputersTableFilters},
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
      updates_count: 0,
      isFiltersShowed: false,
      filters_expressions : {
        ad_good : { field : 'ad_status', type : '=', value : 'Не зарегистрирован'},
        ad_error : { field : 'ad_status', type : '!=', value : 'Не зарегистрирован'},
        kl_good : { field : 'kl_status', type : '!=', value : 'Все правильно'},
        kl_warning_agent : { field : 'kl_status', type : '!=', value : 'Неправильный агент'},
        kl_warning_security : { field : 'kl_status', type : '!=', value : 'Неправильная защита'},
        kl_error : { field : 'kl_status', type : '!=', value : 'Все неправильно'},
        pp_good : { field : 'pp_status', type : '=', value : 'Не зарегистрирован'},
        pp_error : { field : 'pp_status', type : '!=', value : 'Не зарегистрирован'},
        dl_good : { field : 'dl_status', type : '=', value : 'Не зарегистрирован'},
        dl_warning : { field : 'dl_status', type : '!=', value : 'Не зарегистрирован'},
        dl_error : { field : 'dl_status', type : '!=', value : 'Не зарегистрирован'},
        other_windows : { field : 'os_status', type : '!=', value : 'Windows'},
        other_linux : { field : 'os_status', type : '!=', value : 'Linux'},
        other_any_os : { field : 'os_status', type : '!=', value : 'Неизвестно'},
      }
    }
  },
  methods: {
    openCloseFilters() {
      this.isFiltersShowed = !this.isFiltersShowed
    },
    applyFilters(filtersNames) {
      let filters = []
      filtersNames.forEach((filterName) => {
        filters.push(this.filters_expressions[filterName]);
      });
      this.tabulator.setFilter(filters);
    },
    changeTab(tabName) {
      let filters = []
      if (tabName === 'generalTab') {
      } else if (tabName === 'kasperskyTab'){
        filters.push('kl_good')
      } else if (tabName === 'dallasTab'){
        filters.push('dl_good')
        filters.push('other_linux')
      } else if (tabName === 'puppetTab'){
        filters.push('pp_good')
        filters.push('other_windows')
      }
      Array.from(document.getElementsByClassName('filter-checkbox')).forEach((checkbox) => {
        if (filters.includes(checkbox.id)) {
          checkbox.checked = true
        } else {
          checkbox.checked =false
        }
      });
      this.applyFilters(filters)
    },

  },
  mounted() {
    this.tableData = []
    this.tabulator = create_computer_table(this)
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
