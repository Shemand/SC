<template>
    <ul class="tabs general-color ">
      <li class="tab"><a id="generalTab" class="tableTab text-on-white waves-effect" v-on:click.prevent="showGeneral">Главная</a></li>
      <li class="tab"><a id="kasperskyTab" class="tableTab text-on-white waves-effect" v-on:click.prevent="showKaspersky">Касперский</a></li>
      <li class="tab"><a id="dallasTab" class="tableTab text-on-white waves-effect" v-on:click.prevent="showDallas">Dallas Lock</a></li>
      <li class="tab"><a id="puppetTab" class="tableTab text-on-white waves-effect" v-on:click.prevent="showPuppet">Puppet</a></li>
    </ul>
</template>

<script>
export default {
  name: "ComputersTableTabs",
  props: ['table'],
  data() {
    return {
      activeTab : "generalTab"
    }
  },
  methods: {
    showGeneral() {
      this.activeTab = "generalTab"
    },
    showKaspersky() {
      this.activeTab = "kasperskyTab"
    },
    showDallas() {
      this.activeTab = "dallasTab"
    },
    showPuppet() {
      this.activeTab = "puppetTab"
    },
  },
  mounted() {
    let activeTabElement = document.getElementById(this.activeTab)
    let tabs = document.getElementsByClassName('tableTab')
    activeTabElement.classList.add('active')
    Array.from(tabs).forEach((element) => {
      element.addEventListener('click', (event) => {
        let target = event.target
        Array.from(tabs).forEach((elem) => {
          if (Array.from(elem.classList).includes('active')) {
            elem.classList.remove('active')
          }
        });
        element.classList.add("active")
        this.activeTab = target.id
      });
    });
  }
}
</script>

<style lang="scss" scoped>
.tabs {
  width: 90%;
}
.tab {
  background-color: #00b0ff;
  color: #000000;
  transition: 0.5s ease;
}
.tab:hover{
  background-color: darken(#00b0ff, 15%);

}
.tableTab:hover {
  color: #eceff1 !important;
  font-weight: bold;
}
a.active {
  color: #eceff1 !important;
  font-weight: bold !important;
  background-color: darken(#00b0ff, 15%) !important;
}
</style>