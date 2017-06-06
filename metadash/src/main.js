// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VuePatternfly from 'vue-patternfly'
import Plugins from './libs/metadash-plugins'

Vue.config.productionTip = false

VuePatternfly.install(Vue)

let PluginRoutes = []

for (let pluginName in Plugins) {
  let plugin = Plugins[pluginName]
  PluginRoutes.push({
    path: '/' + plugin.path,
    name: plugin.title,
    component: plugin.entry
  })
}

router.addRoutes(PluginRoutes)

/* Fallback to default after all plugin entries are added */
/* Or else plugins routing won't work */
router.addRoutes([
  {
    path: '*',
    redirect: '/dashboard'
  }
])

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App :plugins="plugins"/>',
  data: {
    plugins: Plugins
  },
  components: { App }
})
