import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard'
import Table from '@/components/Table'
import Config from '@/components/Config'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/table',
      name: 'Table',
      component: Table
    },
    {
      path: '/config',
      name: 'Config',
      component: Config
    }
  ]
})
