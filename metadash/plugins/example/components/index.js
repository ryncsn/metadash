import component from './app.vue'

export default {
  path: '/example', // Need to be uniq, and will be used for url routing
  icon: 'extension',
  entry: component,
  title: 'Example Plugin'
}
