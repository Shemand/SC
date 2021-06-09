<template>
  <div class="row">
    <div class="col s12">
      <ul class="tabs">
        <li class="tab col s3"><a id="generalTab" class="tableTab" v-on:click.prevent="showGeneral">Главная</a></li>
        <li class="tab col s3"><a id="kasperskyTab" class="tableTab" v-on:click.prevent="showKaspersky">Касперский</a></li>
        <li class="tab col s3"><a id="dallasTab" class="tableTab" v-on:click.prevent="showDallas">Dallas Lock</a></li>
        <li class="tab col s3"><a id="puppetTab" class="tableTab" v-on:click.prevent="showPuppet">Puppet</a></li>
      </ul>
    </div>
  </div>
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

</style>