import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path : '/',
    name : 'main',
    component : () => import('../views/Main.vue')
  },
  {
    path : '/registration',
    name : 'registration',
    component : () => import('../views/Registration.vue')
  },
  {
    path : '/Authorization',
    name : 'authorization',
    component : () => import('../views/Authorization.vue')
  },
  {
    path : '/Devices',
    name : 'devices',
    component : () => import('../views/Devices.vue')
  },
  {
    path : '/*',
    name : 'notFound',
    component : () => import('../views/Not-found.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
