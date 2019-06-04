import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard'
import Config from '@/components/Config'
import { PluginRoutes } from '@/plugin'
import buildinfo from '../libs/metadash-buildinfo.js'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: `${buildinfo.relativePath}/`,
  routes: [
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/config',
      name: 'Config',
      component: Config
    }
  ]
  .concat(
    PluginRoutes
  )
  .concat([
    {
      path: '*',
      redirect: '/dashboard'
    }
  ])
})
