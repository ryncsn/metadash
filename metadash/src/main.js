// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VuePatternfly from 'vue-patternfly'
import Plugins from './libs/metadash-plugins'

Vue.config.productionTip = false

VuePatternfly.install(Vue)

console.log(Plugins)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
