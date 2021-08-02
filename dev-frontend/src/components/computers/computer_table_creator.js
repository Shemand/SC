import Tabulator from "tabulator-tables";

function datetimeDownloadAccessor(value) {
    if (window.moment.isMoment(value) && value._isValid) {
        return window.moment(value._d).format("DD-MM-YY HH:mm")
    }
    return ''
}

let columns = [
    {title: "№", formatter: "rownum", width: 49, sorter: false, editor: false},
    {title: "Подразделение", field: "unit", sorter: "string", headerFilter: true},
    {title: "Имя компьютера", field: "name", sorter: "string", headerFilter: true},
    {
        title: "AD статус",
        field: "ad_status",
        hozAlign: "center",
        sorter: "datetime",
        formatter: "datetime",
        formatterParams: {
            outputFormat: "DD/MM/YY HH:mm",
            timezone: "Europe/Moscow",
            invalidPlaceholder: "Не зарегистрирован",
        },
        accessorDownload: datetimeDownloadAccessor,
    },
    {
        title: "KL статус",
        field: "kl_status",
        hozAlign: "center",
        sorter: "string",
    },
    {
        title: "DL статус",
        field: "dl_status",
        hozAlign: "center",
        sorter: "string",
    },
    {
        title: "PP статус",
        field: "pp_status",
        hozAlign: "center",
        sorter: "string",
    },
    {
        title: "ОС",
        field: "os_status",
        hozAlign: "center",
        sorter: "string",
    },
    {
        title: "AD Активен",
        field: "active_directory.isActive",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "AD Удален", field: "active_directory.isDeleted", hozAlign: "center", formatter: "datetime",
        formatterParams: {
            outputFormat: "DD/MM/YY HH:mm",
            timezone: "Europe/Moscow",
            invalidPlaceholder: "Не зарегистрирован",
        }, visible: false, download: true, accessorDownload: datetimeDownloadAccessor,
    },
    {
        title: "AD Последнее появление",
        field: "active_directory.last_visible",
        hozAlign: "center",
        formatter: "datetime",
        formatterParams: {
            outputFormat: "DD/MM/YY HH:mm",
            timezone: "Europe/Moscow",
            invalidPlaceholder: "Не зарегистрирован",
        },
        visible: false,
        download: true,
        accessorDownload: datetimeDownloadAccessor,
    },
    {
        title: "DL Сервер",
        field: "dallas_lock.server",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "DL Удален", field: "dallas_lock.isDeleted", hozAlign: "center", formatter: "datetime",
        formatterParams: {
            outputFormat: "DD/MM/YY HH:mm",
            timezone: "Europe/Moscow",
            invalidPlaceholder: "Не зарегистрирован",
        }, visible: false, download: true, accessorDownload: datetimeDownloadAccessor,
    },
    {
        title: "KL IP",
        field: "kaspersky.kl_ip",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "KL ОС",
        field: "kaspersky.kl_os",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "KL Сервер",
        field: "kaspersky.server",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP Мат.Плата",
        field: "puppet.board_serial_number",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP Апдейт астры",
        field: "puppet.astra_update",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP Окружение",
        field: "puppet.environment",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP KESL",
        field: "puppet.kesl_version",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP klnagent",
        field: "puppet.klnagent_version",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP MAC",
        field: "puppet.mac",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP IP",
        field: "puppet.puppet_ip",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP ОС",
        field: "puppet.puppet_os",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP Serial Number",
        field: "puppet.serial_number",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
    {
        title: "PP Uptime(sec)",
        field: "puppet.uptime_seconds",
        hozAlign: "center",
        sorter: "string",
        visible: false,
        download: true
    },
]

let makeFunctionClickOnRow = function(context) {
    return function (e, row) {
        let el = context.$refs.computer_modal.$el
        let instance = M.Modal.getInstance(el)
        let computer_id = row.getData().id
        context.selectedComputer = context.$store.getters.computer(computer_id)
        instance.open()
    }
}

let formatterOfRows = function (row) {
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
    else if (kl_cell.getValue() === 'Неправильнaя защита')
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
}

let makeFunctionDataFiltered = function (context) {
    return function() { context.updates_count++ };
}

function create_computers_table(context) {
        return new Tabulator(context.$refs.computers_table, {
            data: context.tableData,
            layout: "fitColumns",
            tooltips: true,
            pagination: "local",
            index: "name",
            paginationSize: 25,
            reactiveData: true,
            dataFiltered: makeFunctionDataFiltered(context),
            initialSort: [{column: "name", dir: "asc"}],
            rowFormatter: formatterOfRows,
            columns: columns,
            rowClick: makeFunctionClickOnRow(context)
        });
}

export default create_computers_table