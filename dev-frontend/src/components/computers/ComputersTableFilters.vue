<template>
  <div class="self-over-background filter_block">
    <p>*Выбранные пункты исключают записи из выборки</p>
    <table>
      <tr>
        <td colspan="4" class="general-text-color filter-header">Active Directory</td>
      </tr>
      <tr>
        <td><label for="ad_good"><input class="filter-checkbox" type="checkbox" id="ad_good"><span>В домене</span></label></td>
        <td><label for="ad_error"><input class="filter-checkbox" type="checkbox" id="ad_error"><span>Не в домене</span></label></td>
<!--        <td><label for="ad_new"><input class="filter-checkbox" type="checkbox" id="ad_new"><span>Добавленные в этом году</span></label></td>-->
<!--        <td><label for="ad_old"><input class="filter-checkbox" type="checkbox" id="ad_old"><span>Добавленные в прошлом году</span></label></td>-->
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td colspan="4" class="general-text-color filter-header">Касперский</td>
      </tr>
      <tr>
        <td><label for="kl_good"><input class="filter-checkbox" type="checkbox" id="kl_good"><span>Все правильно</span></label></td>
        <td><label for="kl_warning_agent"><input class="filter-checkbox" type="checkbox" id="kl_warning_agent"><span>Неправильный агент</span></label></td>
        <td><label for="kl_warning_security"><input class="filter-checkbox" type="checkbox" id="kl_warning_security"><span>Неправильная защита</span></label></td>
        <td><label for="kl_error"><input class="filter-checkbox" type="checkbox" id="kl_error"><span>Все неправильно</span></label></td>
      </tr>
      <tr>
        <td colspan="4" class="general-text-color filter-header">Puppet</td>
      </tr>
      <tr>
        <td><label for="pp_good"><input class="filter-checkbox" type="checkbox" id="pp_good"><span>C паппетом</span></label></td>
        <td><label for="pp_error"><input class="filter-checkbox" type="checkbox" id="pp_error"><span>Без паппета</span></label></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td colspan="4" class="general-text-color filter-header">Dallas Lock</td>
      </tr>
      <tr>
        <td><label for="dl_good"><input class="filter-checkbox" type="checkbox" id="dl_good"><span>Установлен</span></label></td>
        <td><label for="dl_warning"><input class="filter-checkbox" type="checkbox" id="dl_warning"><span>С ошибкой</span></label></td>
        <td><label for="dl_error"><input class="filter-checkbox" type="checkbox" id="dl_error"><span>Не установлен</span></label></td>
        <td></td>
      </tr>
      <tr>
        <td colspan="4" class="general-text-color filter-header">Общее</td>
      </tr>
      <tr>
        <td><label for="other_windows"><input class="filter-checkbox" type="checkbox" id="other_windows"><span>Машины на Windows</span></label></td>
        <td><label for="other_linux"><input class="filter-checkbox" type="checkbox" id="other_linux"><span>Машины на Linux</span></label></td>
        <td><label for="other_any_os"><input class="filter-checkbox" type="checkbox" id="other_any_os"><span>Неизвестная ОС</span></label></td>
        <td></td>
      </tr>
      <tr>
        <td colspan="4">
          <a class="waves-effect waves-light btn right green-color text-on-white" v-on:click.prevent="applyFilters">Применить</a>
          <a class="waves-effect waves-light btn right red-color text-on-white" v-on:click.prevent="$emit('openCloseFilters')">Скрыть</a>
          <a class="waves-effect waves-light btn right yellow-color text-on-white" v-on:click.prevent="clearFilters">Очистить</a>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: "ComputersTableFilters",
  methods: /**/{
    applyFilters() {
      let checkboxes = document.getElementsByClassName('filter-checkbox')
      let filtersNames = []
      Array.from(checkboxes).forEach((checkbox) => {
        if(checkbox.checked){
          filtersNames.push(checkbox.id)
        }
      });
      this.$emit('applyFilters', filtersNames);
    },
    clearFilters() {
      let checkboxes = document.getElementsByClassName('filter-checkbox')
      Array.from(checkboxes).forEach((checkbox) => {
        checkbox.checked = false
      });
      this.applyFilters()
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/variables";
.filter_block {
  padding: 5px 5px;
  width: 90%;
  margin: 10px auto;
}

input[type=checkbox]:checked + span {
  color: $general-color;
}

table {
  border-collapse: unset;
  padding: 40px;
}

.filter-header {
  font-weight: bold;
  font-size: 2em;
}
.btn {
  margin-right: 3px;
}
</style>