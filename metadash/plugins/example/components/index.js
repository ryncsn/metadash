import component from './app.vue'

export default {
  path: '/example', // Need to be uniq, and will be used for url routing
  icon: '<i class="fa fa-info" aria-hidden="true"></i>', // Or import a webpack resource
  entry: component,
  title: 'Example Plugin'
}
