import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user : {},
    computers: [],
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    computer: state => id => state.computers.filter((comp) => {return comp.id == id})[0],
  },
  mutations: {
    auth_request(state){
        state.status = 'loading'
    },
    auth_success(state, token, user){
        state.status = 'success'
        state.token = token
        state.user = user
    },
    auth_error(state){
        state.status = 'error'
    },
    logout(state){
        state.status = ''
        state.token = ''
    },
    update_computers(state, computers) {
        state.computers = computers
        console.log(computers)
//        computers.forEach((computer) => {
//            state.computers.push(computer)
//        });
    }
  },
  actions: {
      login({commit}, user){
          return new Promise((resolve, reject) => {
              commit('auth_request')
              axios({url: '/api/v1/SZO/users/auth', data: user, method: 'POST' })
              .then(resp => {
                  console.log(resp)
                  const token = resp.data.data.jwt_token
                  localStorage.setItem('token', token)
                  axios.defaults.headers.common['Authorization'] = token
                  commit('auth_success', token, user)
                  resolve(resp)
              }).catch(err => {
                  commit('auth_error')
                  localStorage.removeItem('token')
                  reject(err)
              })
          })
      }
  },
  modules: {
  }
})
