import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import sFunctions from '@/store/secondaryFunctions'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        status: '',
        token: localStorage.getItem('token') || '',
        user: {},
        computers: [],
        admin: {
            users: {},
        }
    },
    getters: {
        isLoggedIn: state => !!state.token,
        authStatus: state => state.status,
        computers: state => state.computers,
        computer: state => id => state.computers.filter((comp) => {
            return comp.id == id
        })[0],
    },
    mutations: {
        auth_request(state) {
            state.status = 'loading'
        },
        auth_success(state, token, user) {
            state.status = 'success'
            state.token = token
            state.user = user
        },
        auth_error(state) {
            state.status = 'error'
        },
        logout(state) {
            state.status = ''
            state.token = ''
            localStorage.removeItem('token')
        },
        update_computers(state, computers) {
            state.computers.length = 0
            state.computers = []
            computers.forEach((row) => {
                row.active_directory.registred = window.moment(row.active_directory.registred).format("DD/MM/YY HH:mm")
                row.active_directory.isDeleted = window.moment(row.active_directory.isDeleted).format("DD/MM/YY HH:mm")
                row.active_directory.last_visible = window.moment(row.active_directory.last_visible).format("DD/MM/YY HH:mm")
                row.dallas_lock.isDeleted = window.moment(row.dallas_lock.isDeleted).format("DD/MM/YY HH:mm")
                row.ad_status = sFunctions.buildActiveDirectoryStatus(row)
                row.kl_status = sFunctions.buildKasperskyStatus(row)
                row.dl_status = sFunctions.buildDallasStatus(row)
                row.pp_status = sFunctions.buildPuppetStatus(row)
                row.os_status = sFunctions.buildOSStatus(row)
                state.computers.push(row)
            });
        }
    },
    actions: {
        login({commit}, user) {
            return new Promise((resolve, reject) => {
                commit('auth_request')
                axios({url: '/api/v1/SZO/users/auth', data: user, method: 'POST'})
                    .then(resp => {
                        const token = resp.data.data.Bearer
                        localStorage.setItem('token', token)
                        axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
                        commit('auth_success', token, user)
                        resolve(resp)
                    }).catch(err => {
                    commit('auth_error')
                    localStorage.removeItem('token')
                    reject(err)
                })
            })
        },
        async updateComputers({commit}) {
            let res = await axios({
                url : "/api/v1/SZO/computers?puppet=[]&kaspersky=[]&dallas_lock=[]&active_directory=[]",
                method : 'GET',
                headers: {
                    'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                },
                withCredentials : true
            });
            if (res.status === 200) {
                console.log(res.data)
                commit('update_computers', res.data.data.computers)
                return res.status
            } else {
                console.log('Computers updating status is ' + res.status)
                return res.status
            }
        },
        async updateUsers({commit}) {
            let res = await axios({
                url : "/api/v1/SZO/users",
                method : 'GET',
                headers: {
                    'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                },
                withCredentials : true
            });
            if (res.status === 200) {
                commit('update_computers', res.data.data.computers)
                return res.status
            } else {
                console.log('Computers updating status is ' + res.status)
                return res.status
            }
        }
    },
    modules: {}
})
