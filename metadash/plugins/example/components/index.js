import component from './app.vue'
import dashboard from './dashboard.vue'

export default {
  path: '/example', // Need to be uniq, and will be used for url routing
  icon: 'extension',
  dashboard: [
    {
      name: 'example',
      component: dashboard
    }
  ],
  entry: component,
  title: 'Example Plugin'
}
