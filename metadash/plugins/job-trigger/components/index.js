import component from './app.vue'

export default {
  path: '/job-trigger', // Need to be uniq, and will be used for url routing
  icon: '<i class="fa fa-rocket" aria-hidden="true"></i>', // Or import a webpack resource
  entry: component,
  title: 'Job Trigger'
}
