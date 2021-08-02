<template xmlns="http://www.w3.org/1999/html">
  <div>
    <ul id="slide-out" class="sidenav self-background">
      <li>
        <div>
          <h1 class="center-align"><img :src="logo_img" alt="SC" class="general-text-color brand-logo"></h1>
        </div>
      </li>
      <li class="self-over-background"><a class="sidenav-close waves-effect text-on-black" href="#!"
                                          data-target="slide-out">BACK</a></li>
      <li>
        <table class="list_of_table">
          <tr v-for="(key, line) of statistics" :key="line_key" class="text-on-black">
            <td class="statistic-td">{{ statistics[line].name }}</td>
            <td class="statistic-td">{{ statistics[line].active_value }}/{{ statistics[line].total_value }}</td>
          </tr>
        </table>
      </li>
      <li class="center-align text-on-black">Скачать</li>
        <ul>
          <li class="center-align"><a class="download-button waves-effect waves-light btn green-color text-on-white" v-on:click.prevent="downloadTableXLSX">XLSX</a></li>
          <li class="center-align"><a class="download-button waves-effect waves-light btn yellow-color text-on-white" v-on:click.prevent="downloadTableXLSX">CSV</a></li>
          <li class="center-align"><a class="download-button waves-effect waves-light btn red-color text-on-white" v-on:click.prevent="downloadTableXLSX">JSON</a></li>
        </ul>
    </ul>

    <div class="fixed-action-btn"><a href="#" data-target="slide-out"
                                     class="sidenav-trigger waves-effect waves-light btn-large btn-floating self-over-background"><i
        class="floating-icon material-icons general-text-color">dehaze</i></a></div>
<!--    <a class="waves-effect waves-light btn right red-color text-on-white" v-on:click.prevent="$emit('openCloseFilters')">Скрыть</a>-->
<!--    <a class="waves-effect waves-light btn right yellow-color text-on-white" v-on:click.prevent="clearFilters">Очистить</a>-->
  </div>
</template>

<script>
import logo_img from "@/assets/sc_logo_2.svg";
export default {
  name: "ComputersTableSideNav",
  props: {
    table: Object,
    updates_count: Number,
  },
  data() {
    return {
      logo_img: logo_img,
      statistics: {
        all_computers: {
          name: "Всего компьютеров",
          active_value: 0,
          total_value: 0,
        },
        in_domain: {
          name: "В домене",
          active_value: 0,
          total_value: 0,
        },
        with_dl: {
          name: "Dallas Lock",
          active_value: 0,
          total_value: 0,
        },
        with_agent: {
          name: "Агент Касперского",
          active_value: 0,
          total_value: 0,
        },
        with_security: {
          name: "Защита Касперского",
          active_value: 0,
          total_value: 0,
        },
        with_puppet: {
          name: "Puppet",
          active_value: 0,
          total_value: 0,
        },
        windows: {
          name: "Windows",
          active_value: 0,
          total_value: 0,
        },
        linux: {
          name: "Linux",
          active_value: 0,
          total_value: 0,
        },
        unknown: {
          name: "Неизвестная ОС",
          active_value: 0,
          total_value: 0,
        }
      },

    }
  },
  methods: {
    clear_statistics_board() {
      for (let prop in this.statistics) {
        this.statistics[prop].active_value = 0
        this.statistics[prop].total_value = 0
      }
    },
    update_statistics_board() {
      this.clear_statistics_board()
      let active_rows = this.table.getRows("active");
      let total_rows = this.table.getRows();
      active_rows.forEach((elem) => {
        let tmpData = elem.getData();

        this.statistics.all_computers.active_value++;

        if (tmpData.active_directory.registred != null) this.statistics.in_domain.active_value++;

        if (tmpData.kaspersky.agent_version != null) this.statistics.with_agent.active_value++;

        if (tmpData.kaspersky.security_version != null) this.statistics.with_security.active_value++;

        if (tmpData.puppet.puppet_os != null) this.statistics.with_puppet.active_value++;

        if (tmpData.dallas_lock.server != null) this.statistics.with_dl.active_value++;

        if(tmpData.os_status === "Windows") this.statistics.windows.active_value++;
        else if(tmpData.os_status === "Linux") this.statistics.linux.active_value++;
        else this.statistics.unknown.active_value++;
      });
      total_rows.forEach((elem) => {
        let tmpData = elem.getData();
        this.statistics.all_computers.total_value++;
        if (tmpData.active_directory.registred != null)
          this.statistics.in_domain.total_value++;
        if (tmpData.kaspersky.agent_version != null)
          this.statistics.with_agent.total_value++;
        if (tmpData.kaspersky.security_version != null)
          this.statistics.with_security.total_value++;
        if (tmpData.puppet.puppet_os != null)
          this.statistics.with_puppet.total_value++;
        if (tmpData.dallas_lock.server != null)
          this.statistics.with_dl.total_value++;
        if(tmpData.os_status === "Windows")
          this.statistics.windows.total_value++;
        else if(tmpData.os_status === "Linux")
          this.statistics.linux.total_value++;
        else
          this.statistics.unknown.total_value++;
      });
    },
    downloadTableXLSX() {
      this.table.download("xlsx", "data.xlsx", {sheetName:"MyData"});
    }
  },
  watch : {
    updates_count(val) {
      setTimeout(this.update_statistics_board, 0)
    }
  },
  mounted() {
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/variables";
.statistic-td {
  padding: 0px 5px;
}

.floating-icon {
  font-size: 2em;
}
.download-block {
  h4 {
    margin: auto;
  }
  a {
    margin: auto;
  }
}
img {
  width: 15rem;
}
</style>