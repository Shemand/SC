RIGHT_ALL = 'Все правильно';
WRONG_AGENT ='Неправильный агент';
WRONG_SECURITY = 'Неправильная защита';
WRONG_ALL = 'Все неправильно';
win_agent_versions = ["11.0.0.1131", "10.5.1781", "10.4.343", "10.2.434"];
lin_agent_versions = ["11.0.0.29", "10.5.0.42"];
lin_security_versions = ["10.1.1.6421", "10.1.0.6077", "10.1.0.6028"];
win_security_versions = ["11.1.1.126", "11.1.0.15919", "11.0.1.90", "11.0.0.6499", "10.3.3.275", "10.1.2.996",
                         "10.3.0.6294", "11.2.0.2254", "10.2.6.3733", "11.3.0.773", "6.0.4.1611", "10.1.0.867",
                         "10.2.1.23", "2.2.0.605", "10.2.5.3201", "11.4.0.233"];
right_agent_versions = ["11.0.0.29", "11.0.0.1131", "11.0.0.1131"];
right_security_versions = ["10.1.1.6421", "11.1.1.126", "10.1.2.996", "11.0.0.1131"];


function buildKasperskyStatus(row) {
    let kl = row.kaspersky
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
            return RIGHT_ALL
    }
}
function buildActiveDirectoryStatus(row) {
    let ad = row.active_directory
    if (ad.registred) {
        return window.moment(ad.registred)
    } else {
        return "Не зарегистрирован"
    }
}
function buildDallasStatus(row) {
    let dallas = row.dallas_lock
    if (dallas.status) {
        return dallas.status
    } else {
        return "Не зарегистрирован"
    }
}
function buildPuppetStatus(row) {
    let puppet = row.puppet
    if (puppet.puppet_ip) {
        return puppet.puppet_ip
    } else {
        return "Не зарегистрирован"
    }
}
function buildOSStatus(row) {
    let puppet = row.puppet
    let kaspersky = row.kaspersky
    if (puppet.puppet_os) {
        if (String(puppet.puppet_os).toUpperCase().indexOf('WIN') !== -1)
            return 'Windows'
        else
            return 'Linux'
    }
    if (kaspersky.kl_os) {
        if (String(kaspersky.kl_os).toUpperCase().indexOf('WIN') !== -1)
            return 'Windows'
        else
            return 'Linux'
    }
    return 'Неизвестно'
}
module.exports = {
    buildActiveDirectoryStatus,
    buildKasperskyStatus,
    buildDallasStatus,
    buildPuppetStatus,
    buildOSStatus,
}