import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'main',
        component: () => import('../views/Main.vue'),
        meta: {
            requiresAuth: true
        }
    },
    // {
    //   path : '/registration',
    //   name : 'registration',
    //   component : () => import('../views/Registration.vue')
    // },
    {
        path: '/Auth',
        name: 'authorization',
        component: () => import('../views/Authorization.vue')
    },
    {
        path: '/Devices',
        name: 'devices',
        component: () => import('../views/Devices.vue'),
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/admin',
        name: 'admin',
        component: () => import('../views/Admin.vue'),
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '*',
        name: 'notFound',
        component: () => import('../views/Not-found.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (store.getters.isLoggedIn) {
            next()
            return
        }
        next('/auth')
    } else {
        next()
    }
})

export default router
