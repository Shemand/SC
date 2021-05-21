<template>
  <div class="modal">
    <div class="computers-info">
      <h1>{{ name }}</h1>
      <div>
        <h3>Puppet: </h3>
        <span>IP: </span><span>{{ puppet.puppet_ip }}</span><br>
        <span>OS: </span><span>{{ puppet.puppet_os }}</span><br>
        <span>Серийный номер мат. платы: </span><span>{{ puppet.board_serial_number }}</span><br>
        <span>Обновление астры: </span><span>{{ puppet.astra_update }}</span><br>
        <span>Environment: </span><span>{{ puppet.environment }}</span><br>
        <span>Домен</span><span>{{ puppet.domain }}</span><br>
        <span>Виртуальная машина: </span><span>{{ (puppet.isVirtual)? "Да" : "Нет" }}</span><br>
        <span>Касперский агент: </span><span>{{ puppet.klnagent_version }}</span><br>
        <span>Касперский защита: </span><span>{{ puppet.kesl_version }}</span><br>
        <span>uptime: </span><span>{{ puppet.uptime_seconds }}</span><br>
        <span>Удален:</span><span>{{ (puppet.isDeleted)? "Да" : "Нет" }}</span><br>
        <span>Последнее изменение: </span><span>{{ puppet.puppet_updated }}</span><br>
        <span>Запись создана: </span><span>{{ puppet.puppet_created }}</span><br>
      </div>
      <div>
        <h3>Active Directory: </h3>
        <span>Последнее появление: </span><span>{{ active_directory.last_visible }}</span><br>
        <span>Активен: </span><span>{{ (active_directory.isActive)? "Да" : "Нет" }}</span><br>
        <span>Компьютер создан: </span><span>{{ active_directory.registred }}</span><br>
        <span>Удален:</span><span>{{ (active_directory.isDeleted)? "Да" : "Нет" }}</span><br>
        <span>Последнее изменение: </span><span>{{ active_directory.puppet_updated }}</span><br>
        <span>Запись создана: </span><span>{{ active_directory.puppet_created }}</span><br>
      </div>
      <div>
        <h3>Dallas Lock: </h3>
        <span>Статус: </span><span>{{ dallas_lock.status }}</span><br>
        <span>Сервер: </span><span>{{ (dallas_lock.server)? "Да" : "Нет" }}</span><br>
        <span>Удален:</span><span>{{ (dallas_lock.isDeleted)? "Да" : "Нет" }}</span><br>
        <span>Последнее изменение: </span><span>{{ dallas_lock.dl_updated }}</span><br>
        <span>Запись создана: </span><span>{{ dallas_lock.dl_created }}</span><br>
      </div>
      <div>
        <h3>Kaspersky: </h3>
        <span>Операционная система: </span><span>{{ kaspersky.kl_os }}</span><br>
        <span>Сервер: </span><span>{{ kaspersky.server }}</span><br>
        <span>IP: </span><span>{{ kaspersky.kl_ip }}</span><br>
        <span>Агент: </span><span>{{ kaspersky.agent_version }}</span><br>
        <span>Защита: </span><span>{{ kaspersky.security_version }}</span><br>
        <span>Удален: </span><span>{{ (kaspersky.isDeleted)? "Да" : "Нет" }}</span><br>
        <span>Последнее изменение: </span><span>{{ kaspersky.kl_updated }}</span><br>
        <span>Запись создана: </span><span>{{ kaspersky.kl_created }}</span><br>
      </div>
    </div>
    <div class="computers-footer">
      <a href="#!" class="modal-close waves-effect waves-red btn-flat">Закрыть</a>
    </div>
  </div>
</template>

<script>
export default {
  props: ['unit', 'name', 'puppet', 'kaspersky', 'active_directory', 'dallas_lock'],
  created : function() {
    setInterval(function() { console.log(this.props)}, 1000)
  },
  // computed: {
  //   puppet: context => context.computer.puppet,
  //   dallas: context => context.computer.dallas_lock,
  //   kaspersky: context => context.computer.kaspersky,
  //   active_directory: context => context.computer.active_directory,
  // },
}
</script>

<style lang="scss" scoped>
nav {
  padding: 0 2rem;
}
</style>