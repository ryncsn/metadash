// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import VueResource from 'vue-resource'

// CSS
import 'vuetify/dist/vuetify.min.css'
import 'c3/c3.css'
import 'd3/d3.min.js'
import 'c3/c3.min.js'

// Font
import 'roboto-npm-webfont'

// Components
import App from '@/App'
import store from '@/store'
import router from '@/router'
import { Plugins } from '@/plugin'
import MetadashAPI from '@/libs/metadash-api'

Vue.use(VueResource)
Vue.use(Vuetify)
Vue.use(MetadashAPI)
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
    Vue.http.interceptors.push((request, next) => {
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
