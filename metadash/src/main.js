// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueResource from 'vue-resource'
import VuePatternfly from 'vue-patternfly'

import App from '@/App'
import router from '@/router'
import store from '@/store'
import { Plugins } from '@/plugin'

Vue.use(VueResource)
Vue.config.productionTip = false
VuePatternfly.install(Vue)

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
    let vm = this
    Vue.http.interceptors.push((request, next) => {
      next((response) => {
        if (response.status === 401) {
          vm.$store.dispatch('fetchMe')
        }
      })
    })
  }
})
