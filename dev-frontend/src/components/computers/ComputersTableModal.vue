<template>
  <div class="modal computers_table_modal self-background">
    <div class="computers-header row">
      <div class="col s10"><span class="computer_name left-align general-text-color">{{ name }}</span></div>
      <div class="col s2 right-align"><a href="#!" class="modal-close"><i class="closer material-icons red-text-color">close</i></a>
      </div>
    </div>
    <ul class="info-block collapsible self-over-background">
      <li class="self-over-background">
        <div class="collapsible-header general-text-color self-over-background">Puppet</div>
        <div class="collapsible-body text-on-black">
          <table>
            <tr>
              <td class="param_name">IP:</td>
              <td>{{ puppet.puppet_ip }}</td>
            </tr>
            <tr>
              <td class="param_name">OS:</td>
              <td>{{ puppet.puppet_os }}</td>
            </tr>
            <tr>
              <td class="param_name">Серийный номер мат. платы:</td>
              <td>{{ puppet.board_serial_number }}</td>
            </tr>
            <tr>
              <td class="param_name">Обновление астры:</td>
              <td>{{ puppet.astra_update }}</td>
            </tr>
            <tr>
              <td class="param_name">Environment:</td>
              <td>{{ puppet.environment }}</td>
            </tr>
            <tr>
              <td class="param_name">Домен:</td>
              <td>{{ puppet.domain }}</td>
            </tr>
            <tr>
              <td class="param_name">Виртуальная машина:</td>
              <td>{{ (puppet.isVirtual) ? "Да" : "Нет" }}</td>
            </tr>
            <tr>
              <td class="param_name">Касперский агент:</td>
              <td>{{ puppet.klnagent_version }}</td>
            </tr>
            <tr>
              <td class="param_name"></td>
              <td>{{ puppet.kesl_version }}</td>
            </tr>
            <tr>
              <td class="param_name">uptime:</td>
              <td>{{ puppet.uptime_seconds }}</td>
            </tr>
            <tr>
              <td class="param_name">Удален:</td>
              <td>{{ (puppet.isDeleted) ? "Да" : "Нет" }}</td>
            </tr>
            <tr>
              <td class="param_name">Последнее изменение:</td>
              <td>{{ puppet.puppet_updated }}</td>
            </tr>
            <tr>
              <td class="param_name">Запись создана:</td>
              <td>{{ puppet.puppet_created }}</td>
            </tr>
          </table>
        </div>
      </li>
      <li>
        <div class="collapsible-header general-text-color self-over-background">Active Directory</div>
        <div class="collapsible-body text-on-black">
          <table>
            <tr>
              <td class="param_name">Последнее появление:</td>
              <td>{{ active_directory.last_visible }}</td>
            </tr>
            <tr>
              <td class="param_name">Активен:</td>
              <td>{{ (active_directory.isActive) ? "Да" : "Нет" }}</td>
            </tr>
            <tr>
              <td class="param_name">Компьютер создан:</td>
              <td>{{ active_directory.registred }}</td>
            </tr>
            <tr>
              <td class="param_name">Удален:</td>
              <td>{{ (active_directory.isDeleted) ? "Да" : "Нет" }}</td>
            </tr>
            <tr>
              <td class="param_name">Последнее изменение:</td>
              <td>{{ active_directory.puppet_updated }}</td>
            </tr>
            <tr>
              <td class="param_name">Запись создана:</td>
              <td>{{ active_directory.puppet_created }}</td>
            </tr>
          </table>
        </div>
      </li>
      <li>
        <div class="collapsible-header general-text-color self-over-background">Dallas Lock</div>
        <div class="collapsible-body text-on-black">
          <table>
            <tr>
              <td class="param_name">Статус:</td>
              <td>{{ dallas_lock.status }}</td>
            </tr>
            <tr>
              <td class="param_name">Сервер:</td>
              <td>{{ (dallas_lock.server) ? "Да" : "Нет" }}</td>
            </tr>
            <tr>
              <td class="param_name">Удален:</td>
              <td>{{ (dallas_lock.isDeleted) ? "Да" : "Нет" }}</td>
            </tr>
            <tr>
              <td class="param_name">Последнее изменение:</td>
              <td>{{ dallas_lock.dl_updated }}</td>
            </tr>
            <tr>
              <td class="param_name">Запись создана:</td>
              <td>{{ dallas_lock.dl_created }}</td>
            </tr>
          </table>
        </div>
      </li>
      <li>
        <div class="collapsible-header general-text-color self-over-background">Kaspersky</div>
        <div class="collapsible-body text-on-black">
          <table>
            <tr>
              <td class="param_name">Операционная система:</td>
              <td>{{ kaspersky.kl_os }}</td>
            </tr>
            <tr>
              <td class="param_name">Сервер:</td>
              <td>{{ kaspersky.server }}</td>
            </tr>
            <tr>
              <td class="param_name">IP:</td>
              <td>{{ kaspersky.kl_ip }}</td>
            </tr>
            <tr>
              <td class="param_name">Агент:</td>
              <td>{{ kaspersky.agent_version }}</td>
            </tr>
            <tr>
              <td class="param_name">Защита:</td>
              <td>{{ kaspersky.security_version }}</td>
            </tr>
            <tr>
              <td class="param_name">Удален:</td>
              <td>{{ (kaspersky.isDeleted) ? "Да" : "Нет" }}</td>
            </tr>
            <tr>
              <td class="param_name">Последнее изменение:</td>
              <td>{{ kaspersky.kl_updated }}</td>
            </tr>
            <tr>
              <td class="param_name">Запись создана:</td>
              <td>{{ kaspersky.kl_created }}</td>
            </tr>
          </table>
        </div>
      </li>
    </ul>

  </div>
</template>

<script>
export default {
  props: ['unit', 'name', 'puppet', 'kaspersky', 'active_directory', 'dallas_lock'],
}
</script>

<style lang="scss" scoped>
@import "@/assets/variables";

nav {
  padding: 0 2rem;
}

.computers_table_modal {
  padding: 30px;
  box-shadow: 0px 0px 4px #000000;
}

.closer {
  font-size: 3em !important;
}

.computer_name {
  font-size: 3em !important;
  font-weight: bold;
}

.param_name {
  font-weight: bold;
}

.info-block {
  border-top: 1px solid $self-over-background-color !important;
  border-right: 1px solid $self-over-background-color !important;
  border-left: 1px solid $self-over-background-color !important;
  border-bottom: None;
}

.collapsible-header {
  border-bottom: 1px solid $general-color !important;
  font-weight: bold !important;
}

.collapsible-body {
  border-bottom: 1px solid $general-color !important;
}

.closer:hover {
  color: $yellow-color;
}

table {
  border-collapse: collapse;
}

table td {
  border: 1px solid $self-background-color;
}

table tr:first-child td {
  border-top: None;
}

table tr:last-child td {
  border-bottom: None;
}

table tr td:first-child {
  border-left: None;
}

table tr td:last-child {
  border-right: None;
}
</style>