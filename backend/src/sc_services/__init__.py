from . import ComputersActiveDirectoryService
from . import ComputersFrameService
from . import ComputersService
from . import DallasLockService
from . import KasperskyService
from . import PuppetService
from . import UnitsService
from . import UsersService

# # Computers Frame
# get_computers_frame = ComputersFrameService.get_computers_frame # Извлекает информацию о компьютерах из базы данных
#
# # Active Directory Service
# get_ad_user = ActiveDirectoryService.get_ad_user # Получить пользователя из базы данных
# get_ad_users = ActiveDirectoryService.get_ad_users # Получить всех пользователей из базы данных
# delete_computer_from_ad = ActiveDirectoryService.delete_computer_from_ad # удалить компьютер из базы данных
# create_computer_ad_record = ActiveDirectoryService.create_computer_ad_record # создать запись о AD компьютере в базе данных
# create_user_ad_record = ActiveDirectoryService.create_user_ad_record # Создать запись о AD пользователей в базе данных
# update_computers_from_ad = ActiveDirectoryService.update_computers_from_ad # Обновить записи о компьютерах в базе данных из AD
# update_users_from_ad = ActiveDirectoryService.update_users_from_ad # Обновить записи о пользователях в базе данных AD
#
# # Computers Service
# get_computer = ComputersService.get_computer # Получить пользователя из базы данных
# get_computers = ComputersService.get_computers # Получить все компьютеры из базы данных
# create_computer = ComputersService.create_computer # Создать компьютер в базе данных
# get_or_create_computer = ComputersService.get_or_create_computer # Получить запись о компьютере в базе данных, если она есть. Иначе создать запись и вернуть созданную запись.
# is_exists_computer = ComputersService.is_exists_computer # Проверить наличие компьютера в базе данных
# inject_row_in_computers_records = ComputersService.inject_row_in_computers_records # Внедрение записей из базы данных в записи из AD.
# change_computer_unit_by_name = ComputersService.change_computer_unit_by_name # Изменение подразделения по имени компьютера
# change_computer_unit = ComputersService.change_computer_unit # Изменение подразделения компьютера по объекту компьютера
# update_computers_unit = ComputersService.update_computers_unit # обновление компьютеров в базе данных по их префиксу.
#
# # Dallas Lock Service
# get_dallas_computers = DallasLockService.get_dallas_computers # получить запись о компьютерах из даллас таблицы
# create_computer_dallas_record = DallasLockService.create_computer_dallas_record # создать компьютер в базе данных по его модели
# update_computers_from_dallas = DallasLockService.update_computers_from_dallas # обновить записи о далласе компьютеров
#
# # Ip Service
# get_ip_all = IpService.get_ip_all # Получить все записи об ip
# get_ip_by_address = IpService.get_ip_by_address # получить запись об ip по его адрессу
# get_ip_by_id = IpService.get_ip_by_id # получить запись об ip по его id
# create_ip = IpService.create_ip # Создать запись об ip
# get_or_create_ip = IpService.get_or_create_ip # получить запись об ip. В случае если ее нет, то создать и вернуть.
#
# # Kaspersky Service
# update_computers_from_kaspersky = KasperskyService.update_computers_from_kaspersky # обновить информацию в базе данных из KSC
#
# # Os Service
# get_os_all = OsService.get_os_all # Получить все записи об операционных системах из базы данных
# get_os_by_name = OsService.get_os_by_name # получить запись об операционной системе по имени ОС
# get_os_by_id = OsService.get_os_by_id # получить запись об операционной системе по id
# create_os = OsService.create_os # создать запись об операционной системе
# get_or_create_os = OsService.get_or_create_os # получить запись об операционной системе по ее имени, если таковой нет, то создаеть и вернуть запись.
#
# # Puppet Service
# get_puppet_computers = PuppetService.get_puppet_computers # получить все записи о компьютерах puppet из базы данных
# create_computer_puppet_record = PuppetService.create_computer_puppet_record # создать запись о компьютере puppet
# update_computers_from_puppet = PuppetService.update_computers_from_puppet # Обновить статистику о компьютерах из puppet в базе данных
#
# # Units Service
# get_default_unit = UnitsService.get_default_unit # Получить подразделение, в которое необходимо записывать когда неизвестно куда отнести объект
# get_units_all = UnitsService.get_units_all # Получить записи о всех подразделениях
# get_unit_by_name = UnitsService.get_unit_by_name # получить запись подразделения по его имени
# get_unit_by_id = UnitsService.get_unit_by_id # получить запись подразделения по его id
# create_unit = UnitsService.create_unit # создать подразделение по его имени
# get_or_create_unit = UnitsService.get_or_create_unit # получить запись об подразделении если таковая имеется иначе создать и вернуть запись.
# change_relation = UnitsService.change_relation # Изменить зависимость между записями о подразделениях по их именам.
# build_structure = UnitsService.build_structure # перестроить структуру по словарю
# get_units_list = UnitsService.get_units_list # получить список всех подразделений
# get_available_units_id = UnitsService.get_available_units_id # получить список айдишников доступных для конкретного подразделения.
#
# # Users Service
# add_user = UsersService.add_user
# get_users = UsersService.get_users
# get_user = UsersService.get_user
# get_or_create_user = UsersService.get_or_create_user
# get_user_by_id = UsersService.get_user_by_id
# tangle_ad = UsersService.tangle_ad
# change_privileges = UsersService.change_privileges
# inject_row_in_users_records = UsersService.inject_row_in_users_records
