import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'materialize-css/dist/js/materialize.min'
import Axios from 'axios'
import moment from 'moment'
import 'moment-timezone'

moment.locale('ru')

Vue.config.productionTip = false
window.moment = moment
Vue.prototype.$http = Axios;
const token = localStorage.getItem('token')
if (token) {
    Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + token
};

new Vue({
    store,
    router,
    render: h => h(App)
}).$mount('#app')

