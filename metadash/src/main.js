// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import VueResource from 'vue-resource'
import 'vuetify/dist/vuetify.min.css'
import 'roboto-npm-webfont'
import 'c3/c3.css'
import 'd3/build/d3.min.js'
import 'c3/c3.min.js'

import App from '@/App'
import router from '@/router'
import store from '@/store'
import { Plugins } from '@/plugin'

Vue.use(VueResource)
Vue.use(Vuetify)
Vue.config.productionTip = false

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
    Vue.http.interceptors.push(function (request, next) {
      next((response) => {
        // Handle 401 error
        if (response.status === 401) {
          this.$store.dispatch('fetchMe')
        }

        // Regist entity
        return response.json()
          .then(json => {
            if (json.uuid) {
              this.$store.commit('registEntity', json)
            }
          }, () => {})
          .then(() => response)
      })
    })
  }
})
