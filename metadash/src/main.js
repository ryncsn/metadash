// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import VueResource from 'vue-resource'
import VuePatternfly from 'vue-patternfly'

import App from './App'
import router from './router'
import Plugins from './libs/metadash-plugins'

Vue.use(VueResource)
Vue.use(Vuex)
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

/* Add Config page */
/* Fallback to default after all plugin entries are added */
/* Or else plugins routing won't work */
router.addRoutes([
  {
    path: '*',
    redirect: '/dashboard'
  }
])

const store = new Vuex.Store({
  state: {
    username: null,
    role: 'anonymous'
  },
  actions: {
    login ({state}, {username, password}) {
      return Vue.http.post('/api/login', {
        username: username,
        password: password
      }).then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    logout ({state}) {
      return Vue.http.get('/api/logout')
        .then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    },
    fetchMe ({state}) {
      return Vue.http.get('/api/me')
        .then(res => res.json())
        .then(data => {
          state.username = data.username
          state.role = data.role
        })
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App :plugins="plugins"/>',
  data: {
    plugins: Plugins
  },
  components: { App },
  created () {
    this.$store.dispatch('fetchMe')
  }
})
